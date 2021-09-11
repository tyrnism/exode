from beem import exceptions as bexceptions
from beem import Hive
from beem.nodelist import NodeList
from beem.block import Block
from beem.blockchain import Blockchain
from beem.account import Account
import json
import os.path
import mysql.connector
from timeit import default_timer as timer
import time
import traceback
from datetime import datetime
from datetime import timedelta
import ssl

import discord
from discord.ext import tasks
from discord.ext import commands

import random
import matplotlib.dates as pltdates
import matplotlib.pyplot as plt

import exode_const as excst

#############################################################################################

class DataBaseConnector():

	mSQLConnector = mysql.connector.connect()
	mLastConnect  = datetime.now()
	
	def db_Connect(self):    
    
		try:
			self.mSQLConnector = mysql.connector.connect(user='exode', password=excst.DB_PASS,
									host='127.0.0.1',
									database=excst.DB_NAME)
									
			self.mLastConnect = datetime.now()
									
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("MySQL: Something is wrong with your user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("MySQL: Database does not exist")
			else:
				print("MySQL: ", err)

	def db_Cursor(self):
	
		mCurrentTime = datetime.now()
		
		print ( (mCurrentTime - self.mLastConnect).seconds )
		if ( (mCurrentTime - self.mLastConnect).seconds > 10 ):
			self.db_Close()
			self.db_Connect()
			
			
		try:
			cursor = self.mSQLConnector.cursor()
		except mysql.connector.Error as err:
			print ( "reconnect" )
			self.db_Connect()
			cursor = self.mSQLConnector.cursor()
			
		return cursor
		
	def db_Commit(self):
	
		self.mSQLConnector.commit()
		
	def db_Close(self):
	
		try:
			self.mSQLConnector.close()
		except mysql.connector.Error as err:
			print ( "already close" )

#############################################################################################
# Initialise
myDB = DataBaseConnector()
myDB.db_Connect()

##############################################################################################

def ex_IsPack( mID ):
	(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails( mID )
		
	return is_pack
	
def ex_GetAssetDetails( mID ):

	# rank: 
	# 0 -> common
	# 1 -> rare
	# 2 -> epic
	# 3 -> legendary
	
	if ( mID == "exode_alpha_booster" ):
		return (True, "Alpha booster",					0, 0)
		
	if ( mID == "exode_alpha_support_vega" ):
		return (True, "Alpha Escort Pack [Vega]",				0, 0)
	if ( mID == "exode_alpha_support_ionguards" ):
		return (True, "Alpha Escort Pack [Ion Guards]",			0, 0)
	if ( mID == "exode_alpha_support_tom" ):
		return (True, "Alpha Support Pack [TOM Essentials]",			0, 0)
		
		
	if ( mID == "exode_alpha_starter_4" ):
		return (True, "Triple Alpha Starter Set",				0, 0)
	if ( mID == "exode_alpha_starter_3" ):
		return (True, "Alpha Starter [Elected Leader]",			0, 0)
	if ( mID == "exode_alpha_starter_2" ):
		return (True, "Alpha Starter [Ark Scientist]",			0, 0)
	if ( mID == "exode_alpha_starter_1" ):
	
		return (True, "Alpha Starter [Navy Lieutenant]",			0, 0)
	if ( mID == "exode_alpha_contract_tom" ):
		return (True, "Alpha Contract [TOM Settler PREMIUM BUDDIER]", 	0, 0)
	if ( mID == "exode_alpha_contract_rekatron" ):
		return (True, "Alpha Contract [WEAPON DROPS BY REKATRON]", 		0, 0)
	if ( mID == "exode_alpha_contract_syndicate" ):
		return (True, "Alpha Contract [SYNDICATE SPONSORSHIP]", 		0, 0)
		
	if ( mID == "exode_alpha_pack_crew_kb119" ):
		return (True, "Alpha Crew Pack [Kilbot-119]",				0, 0)
	if ( mID == "exode_alpha_pack_crew_galvin4" ):
		return (True, "Alpha Crew Pack [Galvin 4]",				0, 0)
		
	if ( mID == "exode_alpha_character_pack_nomad" ):
		return (True, "Alpha Promo Character Pack [Nomad Navigator]", 	0, 0)
	if ( mID == "exode_alpha_character_pack_genetician" ):
		return (True, "Alpha Promo Character Pack [Genetician Scientist]",	0, 0)
	if ( mID == "exode_alpha_character_pack_suntek" ):
		return (True, "Alpha Promo Character Pack [Suntek Survivor]",	0, 0)
	if ( mID == "exode_alpha_character_pack_drachian" ):
		return (True, "Alpha Promo Character Pack [Drachian Colonel]",	0, 0)
		
	if ( mID == "exode_card_001_originNavy" 			or mID == "exode_card_E001_originNavy" ):
		return (False, "Navy Lieutenant [Origin]", 				2, 	1)	
	if ( mID == "exode_card_002_shipArcheon" 			or mID == "exode_card_E002_shipArcheon" ):
		return (False, "Military Frigate (\"Archeon Class\")", 		2,	2)	
	if ( mID == "exode_card_003_officerComms" 			or mID == "exode_card_E003_officerComms" ):
		return (False, "Communications Officer", 				1,	3)
	if ( mID == "exode_card_004_officerWeapons" 			or mID == "exode_card_E004_officerWeapons" ):
		return (False, "Weapons Officer", 					1,	4)		
	if ( mID == "exode_card_005_officerTactical" 			or mID == "exode_card_E005_officerTactical" ):
		return (False, "Tactical Officer", 					1,	5)		
	if ( mID == "exode_card_006_crewPilot" 			or mID == "exode_card_E006_crewPilot" ):
		return (False, "Pilot (Crew)", 					1,	6)		
	if ( mID == "exode_card_007_crewSRT" 				or mID == "exode_card_E007_crewSRT" ):
		return (False, "Signals Specialist (Crew)", 				1,	7)		
	if ( mID == "exode_card_008_crewDefense"			or mID == "exode_card_E008_crewDefense" ):
		return (False, "Defense Specialist (Crew)", 				1,	8)		
	if ( mID == "exode_card_009_crewTrooper" 			or mID == "exode_card_E009_crewTrooper" ):
		return (False, "Trooper (Crew)", 					0,	9)		
	if ( mID == "exode_card_010_crewEngineer" 			or mID == "exode_card_E010_crewEngineer" ):
		return (False, "Military Engineer (Crew)", 				0,	10)			
	if ( mID == "exode_card_011_setFMR17" 			or mID == "exode_card_E011_setFMR17" ):
		return (False, "FMR-17 \'Atonis\' (x3)", 				2,	11)		
	if ( mID == "exode_card_012_setSuitMilitaryC" 		or mID == "exode_card_E012_setSuitMilitaryC" ):
		return (False, "Military Suit Class C (x3)", 				1,	12)		
	if ( mID == "exode_card_013_originArk" 			or mID == "exode_card_E013_originArk" ):
		return (False, "Ark Scientist [Origin]", 				2,	13)		
	if ( mID == "exode_card_014_shipOrwell1" 			or mID == "exode_card_E014_shipOrwell1" ):
		return (False, "Ark Ship \"Orwell 1\"", 				2,	14)		
	if ( mID == "exode_card_015_officerResearch" 			or mID == "exode_card_E015_officerResearch" ):
		return (False, "Research Officer", 					1,	15)		
	if ( mID == "exode_card_016_officerExploration" 		or mID == "exode_card_E016_officerExploration" ):
		return (False, "Exploration Officer", 				1,	16)	
	if ( mID == "exode_card_017_officerPreservation" 		or mID == "exode_card_E017_officerPreservation" ):
		return (False, "Preservation Officer", 				1,	17)	
	if ( mID == "exode_card_018_crewSurgeon" 			or mID == "exode_card_E018_crewSurgeon" ):
		return (False, "Space Surgeon", 					1,	18)	
	if ( mID == "exode_card_019_crewXenoAnalyst" 			or mID == "exode_card_E019_crewXenoAnalyst" ):
		return (False, "Xeno Analyst", 					1,	19)	
	if ( mID == "exode_card_020_crewBioScientist" 		or mID == "exode_card_E020_crewBioScientist" ):
		return (False, "Space Bioscientist", 					1,	20)	
	if ( mID == "exode_card_021_crewAnimalHandler" 		or mID == "exode_card_E021_crewAnimalHandler" ):
		return (False, "Animal Handler (Crew)", 				0,	21)	
	if ( mID == "exode_card_022_crewLifeSearcher" 		or mID == "exode_card_E022_crewLifeSearcher" ):
		return (False, "Life Searcher (Crew)", 				0,	22)	
	if ( mID == "exode_card_023_crewLabScientist" 		or mID == "exode_card_E023_crewLabScientist" ):
		return (False, "Lab Scientist (Crew)", 				0,	23)	
	if ( mID == "exode_card_024_setRarePlants" 			or mID == "exode_card_E024_setRarePlants" ):
		return (False, "Rare Plants Collection (x6)", 			2,	24)	
	if ( mID == "exode_card_025_setSuitResearchC" 		or mID == "exode_card_E025_setSuitResearchC" ):
		return (False, "Research Suits Class C (x3)", 			1,	25)	
	if ( mID == "exode_card_026_originLeader" 			or mID == "exode_card_E026_originLeader" ):
		return (False, "Elected Leader [Origin]", 				2,	26)	
	if ( mID == "exode_card_027_shipDiplomatic" 			or mID == "exode_card_E027_shipDiplomatic" ):
		return (False, "Diplomatic Corvette \"Amarasia\"", 			2,	27)	
	if ( mID == "exode_card_028_officerAdministrative" 		or mID == "exode_card_E028_officerAdministrative" ):
		return (False, "Administrative Officer", 				1,	28)	
	if ( mID == "exode_card_029_officerSecurity" 			or mID == "exode_card_E029_officerSecurity" ):
		return (False, "Security Officer", 					1,	29)	
	if ( mID == "exode_card_030_crewPropaganda"			or mID == "exode_card_E030_crewPropaganda" ):
		return (False, "Propaganda Specialist", 				1,	30)	
	if ( mID == "exode_card_031_crewPopulation" 			or mID == "exode_card_E031_crewPopulation" ):
		return (False, "Population Analyst", 					1,	31)	
	if ( mID == "exode_card_032_crewEntertainment" 		or mID == "exode_card_E032_crewEntertainment" ):
		return (False, "Welfare Specialist", 					1,	32)	
	if ( mID == "exode_card_033_crewMaintenance" 			or mID == "exode_card_E033_crewMaintenance" ):
		return (False, "Maintenance Staff (Crew)", 				0,	33)	
	if ( mID == "exode_card_034_crewPilotCivilian" 		or mID == "exode_card_E034_crewPilotCivilian" ):
		return (False, "Civilian Pilot (Crew)", 				0,	34)	
	if ( mID == "exode_card_035_crewSecurity" 			or mID == "exode_card_E035_crewSecurity" ):
		return (False, "Security Guard (Crew)", 				0,	35)	
	if ( mID == "exode_card_036_setLuxury" 			or mID == "exode_card_E036_setLuxury" ):
		return (False, "Diplomatic Gifts", 					2,	36)	
	if ( mID == "exode_card_037_setDatabase" 			or mID == "exode_card_E037_setDatabase" ):
		return (False, "Federal Database", 					2,	37)	
		
		
	if ( mID == "exode_card_046_Rekatron_defensiveAmmo" 		or mID == "exode_card_E046_Rekatron_defensiveAmmo" ):
		return (False, "DEFENSIVE AMMO",	 				0,	46)
	if ( mID == "exode_card_047_Rekatron_firetalkerPistol" 	or mID == "exode_card_E047_Rekatron_firetalkerPistol" ):
		return (False, "FIRETALKER", 						0,	47)
	if ( mID == "exode_card_048_Rekatron_karperPistol" 		or mID == "exode_card_E048_Rekatron_karperPistol" ):
		return (False, "KARPER Heavy", 					1,	48)
	if ( mID == "exode_card_049_Rekatron_explanatorRifle" 	or mID == "exode_card_E049_Rekatron_explanatorRifle" ):
		return (False, "EXPLANATOR", 						1,	49)
	if ( mID == "exode_card_050_Rekatron_rsdRifle" 		or mID == "exode_card_E050_Rekatron_rsdRifle" ):
		return (False, "REKATRON SD", 					1,	50)
	if ( mID == "exode_card_051_Rekatron_goodMorningPistol" 	or mID == "exode_card_E051_Rekatron_goodMorningPistol" ):
		return (False, "GOOD MORNING", 					1,	51)
	if ( mID == "exode_card_052_Rekatron_jugdmentDayRifle" 	or mID == "exode_card_E052_Rekatron_jugdmentDayRifle" ):
		return (False, "JUDGEMENT DAY", 					2,	52)
	if ( mID == "exode_card_053_Rekatron_galacticPeacemaker" 	or mID == "exode_card_E053_Rekatron_galacticPeacemaker" ):
		return (False, "GALACTIC PEACEMAKER", 				2,	53)
	if ( mID == "exode_card_054_Rekatron_ammoGuided" 		or mID == "exode_card_E054_Rekatron_ammoGuided" ):
		return (False, "AUTOGUIDED AMMO", 					1,	54)
	if ( mID == "exode_card_055_Rekatron_ammoParty" 		or mID == "exode_card_E055_Rekatron_ammoParty" ):
		return (False, "PARTY AMMO", 						2,	55)
	if ( mID == "exode_card_056_Tom_SmootyAllInOne" 		or mID == "exode_card_E056_Tom_SmootyAllInOne" ):
		return (False, "SMOOTY All-In-One Ammo", 				0,	56)
	if ( mID == "exode_card_057_Tom_FoodieMoodie" 		or mID == "exode_card_E057_Tom_FoodieMoodie" ):
		return (False, "Strategic FOODIE-MOODIE", 				0,	57)
	if ( mID == "exode_card_058_Tom_FriendlyEyes" 		or mID == "exode_card_E058_Tom_FriendlyEyes" ):
		return (False, "Friendly Eyes XY-6", 					0,	58)
	if ( mID == "exode_card_059_Tom_BuddyPinger" 			or mID == "exode_card_E059_Tom_BuddyPinger" ):
		return (False, "BUDDY Pinger", 					1,	59)
	if ( mID == "exode_card_060_Tom_VehicleLittleBuddy" 		or mID == "exode_card_E060_Tom_VehicleLittleBuddy" ):
		return (False, "LITTLE Buddy", 					1,	60)
	if ( mID == "exode_card_061_Tom_Custom" 			or mID == "exode_card_E061_Tom_Custom" ):
		return (False, "TOM Custom", 						1,	61)
	if ( mID == "exode_card_062_Tom_WHCConverter" 		or mID == "exode_card_E062_Tom_WHCConverter" ):
		return (False, "WHC Unit", 						1,	62)
	if ( mID == "exode_card_063_Tom_Explorator" 			or mID == "exode_card_E063_Tom_Explorator" ):
		return (False, "TOM Explorator X4", 					2,	63)
	if ( mID == "exode_card_064_Tom_ShelterHappyFive" 		or mID == "exode_card_E064_Tom_ShelterHappyFive" ):
		return (False, "SHELTER \"Happy Five\"", 				2,	64)
		
	if ( mID == "exode_card_066_SyndicateEquipment_Chip" 	or mID == "exode_card_E066_SyndicateEquipment_Chip" ):
		return (False, "Syndicate Chip", 					0,	66)
	if ( mID == "exode_card_067_SyndicateEquipment_DrugHolidays"	or mID == "exode_card_E067_SyndicateEquipment_DrugHolidays" ):
		return (False, "\'Holidays\'", 					0,	67)
	if ( mID == "exode_card_068_SyndicateEquipment_DrugNPrime"	or mID == "exode_card_E068_SyndicateEquipment_DrugNPrime" ):
		return (False, "\'N-Prime\'", 					0,	68)
	if ( mID == "exode_card_069_SyndicateShipBlackLotus" 	or mID == "exode_card_E069_SyndicateShipBlackLotus" ):
		return (False, "\"Black Lotus\"", 					2,	69)
	if ( mID == "exode_card_070_SyndicateEquipmentAutoBlaster"	or mID == "exode_card_E070_SyndicateEquipmentAutoBlaster" ):
		return (False, "Syndicate Auto Blaster", 				1,	70)	
	if ( mID == "exode_card_071_SyndicateEquipment_NarcoWarfare"	or mID == "exode_card_E071_SyndicateEquipment_NarcoWarfare" ):
		return (False, "Narco-Warfare", 					1,	71)
	if ( mID == "exode_card_072_SyndicateEquipmentSet_Genefactory" 
									or mID == "exode_card_E072_SyndicateEquipmentSet_Genefactory" ):
		return (False, "Nacrotics Genefactory", 				2,	72)			
	if ( mID == "exode_card_073_SyndicateHacker" 			or mID == "exode_card_E073_SyndicateHacker" ):
		return (False, "Syndicate Hacker", 					1,	73)
	if ( mID == "exode_card_074_SyndicateLeader" 			or mID == "exode_card_E074_SyndicateLeader" ):
		return (False, "Syndicate Squad Leader", 				1,	74)		
	if ( mID == "exode_card_075_SyndicateTransactor" 		or mID == "exode_card_E075_SyndicateTransactor" ):
		return (False, "Programmed Transactor", 				1,	75)	
	if ( mID == "exode_card_076_SyndicateTrooper" 		or mID == "exode_card_E076_SyndicateTrooper" ):
		return (False, "Syndicate Trooper", 					1,	76)
	if ( mID == "exode_card_077_SyndicateAyumi" 			or mID == "exode_card_E077_SyndicateAyumi" ):
		return (False, "Ayumi", 						2,	77)
	if ( mID == "exode_card_078_SyndicateYakuzaNoble" 		or mID == "exode_card_E078_SyndicateYakuzaNoble" ):
		return (False, "Battle-Trained Socialite", 				2,	78)
	if ( mID == "exode_card_079_SyndicateYakuzaSniper" 		or mID == "exode_card_E079_SyndicateYakuzaSniper" ):
		return (False, "Camouflaged Sniper", 					2,	79)
	if ( mID == "exode_card_080_TheKumicho" 			or mID == "exode_card_E080_TheKumicho" ):
		return (False, "The Kumicho", 					3,	80)
	if ( mID == "exode_card_081_RebelGeneral" 			or mID == "exode_card_E081_RebelGeneral" ):
		return (False, "Rebel General", 					3,	81)
	if ( mID == "exode_card_082_AlannaVos" 			or mID == "exode_card_E082_AlannaVos" ):
		return (False, "Alanna Vös, Federal Marshal", 			3,	82)
	if ( mID == "exode_card_083_Sh4rken" 				or mID == "exode_card_E083_Sh4rken" ):
		return (False, "Sh4rken", 						3,	83)
	if ( mID == "exode_card_084_TheAI" 				or mID == "exode_card_E084_TheAI" ):
		return (False, "Mysterious AI", 					3, 	84)
	if ( mID == "exode_card_085_Apprentice" 			or mID == "exode_card_E085_Apprentice" ):
		return (False, "Mysterious Robot", 					3,	85)
	if ( mID == "exode_card_086_Cranium" 				or mID == "exode_card_E086_Cranium" ):
		return (False, "Captain Cranium", 					3,	86)
	if ( mID == "exode_card_087_Cryptoeater" 			or mID == "exode_card_E087_Cryptoeater" ):
		return (False, "\"Crypto-Eater\"", 					3,	87)
	if ( mID == "exode_card_088_originRepentantPirate" 		or mID == "exode_card_E088_originRepentantPirate" ):
		return (False, "Repentant Pirate [Origin]", 				3,	88)
	if ( mID == "exode_card_089_shipColombus" 			or mID == "exode_card_E089_shipColombus" ):
		return (False, "\"The Colombus\" (circa 2113)", 			3,	89)
	if ( mID == "exode_card_090_shipQuantumSupreme"		or mID == "exode_card_E090_shipQuantumSupreme" ):
		return (False, "\"Quantum\" Class Supreme", 				3,	90)
	if ( mID == "exode_card_091_vehicleVelvetStorm" 		or mID == "exode_card_E091_vehicleVelvetStorm" ):
		return (False, "\"Velvet Storm\"", 					3,	91)
	if ( mID == "exode_card_092_vehicleVanguard" 			or mID == "exode_card_E092_vehicleVanguard" ):
		return (False, "\"Vanguard\"", 					3,	92)
	if ( mID == "exode_card_093_equipmentSuitArena" 		or mID == "exode_card_E093_equipmentSuitArena" ):
		return (False, "Arena Powersuit (signed by Kurban Ko)", 		3,	93)
		
	if ( mID == "exode_card_101_originSecretAgent" 		or mID == "exode_card_E101_originSecretAgent" ):
		return (False, "Secret Agent [Origin]", 				2,	101)
	if ( mID == "exode_card_102_originStrandedTrader" 		or mID == "exode_card_E102_originStrandedTrader" ):
		return (False, "Stranded Trader [Origin]", 				2,	102)
	if ( mID == "exode_card_103_originCruiseShipCaptain" 	or mID == "exode_card_E103_originCruiseShipCaptain" ):
		return (False, "Cruise Ship Captain [Origin]", 			2,	103)
	if ( mID == "exode_card_104_shipArkLifesavior" 		or mID == "exode_card_E104_shipArkLifesavior" ):
		return (False, "Ark Ship \"Orwell 2\" Lifesavior", 			2,	104)
	if ( mID == "exode_card_105_shipCargoKormen" 			or mID == "exode_card_E105_shipCargoKormen" ):
		return (False, "\"Kormen\" Class (Cargo)", 				2,	105)
	if ( mID == "exode_card_106_shipRhino" 			or mID == "exode_card_E106_shipRhino" ):
		return (False, "\"Rhino\" Heavy Attack Frigate", 			2,	106)
	if ( mID == "exode_card_107_shipCargoTaurus" 			or mID == "exode_card_E107_shipCargoTaurus" ):
		return (False, "\"Taurus\" Class Transport", 				2,	107)
	if ( mID == "exode_card_108_shipMyrmidon" 			or mID == "exode_card_E108_shipMyrmidon" ):
		return (False, "\"Myrmidon\" Assault Transport", 			2,	108)
	if ( mID == "exode_card_109_shipAkhen" 			or mID == "exode_card_E109_shipAkhen" ):
		return (False, "\"Akhen\" Cannon", 					2,	109)
	if ( mID == "exode_card_110_shipCoetus" 			or mID == "exode_card_E110_shipCoetus" ):
		return (False, "\"Coetus\" Class Science Vessel", 			2,	110)
	if ( mID == "exode_card_111_setGeneticianConsole" 		or mID == "exode_card_E111_setGeneticianConsole" ):
		return (False, "Genetician Console", 					2,	111)
	if ( mID == "exode_card_112_setMilitaryClassA" 		or mID == "exode_card_E112_setMilitaryClassA" ):
		return (False, "Military Suits Class A (x3)", 			2,	112)
	if ( mID == "exode_card_113_setEisenSuits" 			or mID == "exode_card_E113_setEisenSuits" ):
		return (False, "Eisen Suits (x3)", 					2,	113)
	if ( mID == "exode_card_114_vehicleAcheanRacer" 		or mID == "exode_card_E114_vehicleAcheanRacer" ):
		return (False, "Archean Racer", 					2,	114)
	if ( mID == "exode_card_115_crewSpaceMarshal"			or mID == "exode_card_E115_crewSpaceMarshal" ):
		return (False, "Space Federal Marshal", 				2,	115)
	if ( mID == "exode_card_116_officerEliza" 			or mID == "exode_card_E116_officerEliza" ):
		return (False, "Eliza", 						2,	116)
	if ( mID == "exode_card_117_crewOksana" 			or mID == "exode_card_E117_crewOksana" ):
		return (False, "Oksana", 						2,	117)
	if ( mID == "exode_card_118_officerNorah" 			or mID == "exode_card_E118_officerNorah" ):
		return (False, "Norah", 						2,	118)
	if ( mID == "exode_card_119_officerShen" 			or mID == "exode_card_E119_officerShen" ):
		return (False, "Shen", 						2,	119)
	if ( mID == "exode_card_120_officerStug" 			or mID == "exode_card_E120_officerStug" ):
		return (False, "Stug", 						2,	120)
	if ( mID == "exode_card_121_crewTyron" 			or mID == "exode_card_E121_crewTyron" ):
		return (False, "Tyron", 						2,	121)
	if ( mID == "exode_card_122_officerAdmiralValro" 		or mID == "exode_card_E122_officerAdmiralValro" ):
		return (False, "Admiral Valro", 					2,	122)
	if ( mID == "exode_card_123_officerNash" 			or mID == "exode_card_E123_officerNash" ):
		return (False, "Nash, \"The Expert\"", 				2,	123)
	if ( mID == "exode_card_124_crewSpecialInfiltrationAgent" 	or mID == "exode_card_E124_crewSpecialInfiltrationAgent" ):
		return (False, "Special Infiltration Agent", 				2,	124)
	if ( mID == "exode_card_125_crewScarletSarah" 		or mID == "exode_card_E125_crewScarletSarah" ):
		return (False, "\'Scarlet Sarah\'", 					2,	125)
	if ( mID == "exode_card_126_passengerNuclearFamily" 		or mID == "exode_card_E126_passengerNuclearFamily" ):
		return (False, "Nuclear Family", 					2,	126)
	if ( mID == "exode_card_127_installationOctohome" 		or mID == "exode_card_E127_installationOctohome" ):
		return (False, "Octohome", 						2,	127)
	if ( mID == "exode_card_128_installationOrbitalShield" 	or mID == "exode_card_E128_installationOrbitalShield" ):
		return (False, "Orbital Shield", 					2,	128)
	if ( mID == "exode_card_129_installationDreamsphere" 	or mID == "exode_card_E129_installationDreamsphere" ):
		return (False, "Dreamsphere", 					2,	129)
	if ( mID == "exode_card_130_installationGenerator100"	or mID == "exode_card_E130_installationGenerator100" ):
		return (False, "X-Gen TR100", 					2,	130)
	if ( mID == "exode_card_131_equipmentFactionCorporate" 	or mID == "exode_card_E131_equipmentFactionCorporate" ):
		return (False, "Corporate License (Level S+)", 			2,	131)
	if ( mID == "exode_card_132_equipmentSuitRacer" 		or mID == "exode_card_E132_equipmentSuitRacer" ):
		return (False, "Racer Mech-Suit", 					2,	132)
	if ( mID == "exode_card_133_equipmentSuitSpartan" 		or mID == "exode_card_E133_equipmentSuitSpartan" ):
		return (False, "Spartan Elite Suit", 					2,	133)
	if ( mID == "exode_card_134_equipmentFactionRebellion" 	or mID == "exode_card_E134_equipmentFactionRebellion" ):
		return (False, "The Rebellion Secrets ||\"They knew\"||", 		2,	134)
	if ( mID == "exode_card_135_escortSabre" 			or mID == "exode_card_E135_escortSabre" ):
		return (False, "Sabre Regiment", 					2,	135)
	if ( mID == "exode_card_136_crewFleshCultLeader" 		or mID == "exode_card_E136_crewFleshCultLeader" ):
		return (False, "Flesh Cult Leader", 					2,	136)
	if ( mID == "exode_card_137_installationDefensiveBunker" 	or mID == "exode_card_E137_installationDefensiveBunker" ):
		return (False, "Defensive Bunker", 					2,	137)
		
	if ( mID == "exode_card_151_officerDrachianColonel" 		or mID == "exode_card_E151_officerDrachianColonel" ):
		return (False, "Drachian Colonel", 					2,	151)
	if ( mID == "exode_card_152_crewNomadNavigator" 		or mID == "exode_card_E152_crewNomadNavigator" ):
		return (False, "Nomad Navigator", 					2,	152)
	if ( mID == "exode_card_153_crewGeneticianScientist" 	or mID == "exode_card_E153_crewGeneticianScientist" ):
		return (False, "Genetician Scientist", 				2,	153)
	if ( mID == "exode_card_154_crewSuntekSurvivor" 		or mID == "exode_card_E154_crewSuntekSurvivor" ):
		return (False, "Suntek Collector", 					2,	154)
	if ( mID == "exode_card_155_crewKilbot" 			or mID == "exode_card_E155_crewKilbot" ):
		return (False, "KB-119 \'Kilbot\'", 					2,	155)
	if ( mID == "exode_card_156_crewGalvin" 			or mID == "exode_card_E156_crewGalvin" ):
		return (False, "Galvin-4, Social Robot", 				2,	156)
	if ( mID == "exode_card_157_escortVega" 			or mID == "exode_card_E157_escortVega" ):
		return (False, "Vega Elite Squadron", 				2,	157)
	if ( mID == "exode_card_158_escortIonguards" 			or mID == "exode_card_E158_escortIonguards" ):
		return (False, "Ionguard Defense Fleet", 				2,	158)
	if ( mID == "exode_card_159_suntekSphere" 			or mID == "exode_card_E159_suntekSphere" ):
		return (False, "Suntek Energy Sphere", 				2,	159)
		
		
	if ( mID == "exode_card_181_escortLongswords" 		or mID == "exode_card_E181_escortLongswords" ):
		return (False, "Longsword Squadron", 					1,	181)
	if ( mID == "exode_card_182_escortCruiserTaskForce" 		or mID == "exode_card_E182_escortCruiserTaskForce" ):
		return (False, "Cruiser Task Force", 					1,	182)
	if ( mID == "exode_card_183_escortStarsystemGarrison" 	or mID == "exode_card_E183_escortStarsystemGarrison" ):
		return (False, "Starsystem Garrison", 				0,	183)
	if ( mID == "exode_card_184_shipBaldie" 			or mID == "exode_card_E184_shipBaldie" ):
		return (False, "\'Baldie\' Shuttle", 					0,	184)
	if ( mID == "exode_card_185_shipClaymoreHyperfighter" 	or mID == "exode_card_E185_shipClaymoreHyperfighter" ):
		return (False, "\"Claymore\" Hyperfighter", 				1,	185)
	if ( mID == "exode_card_186_shipDrachianMantis" 		or mID == "exode_card_E186_shipDrachianMantis" ):
		return (False, "Drachian \"Mantis\"", 				1,	186)
	if ( mID == "exode_card_187_vehicleSalazar" 			or mID == "exode_card_E187_vehicleSalazar" ):
		return (False, "\"Salazar\" Space Cab", 				0,	187)
	if ( mID == "exode_card_188_vehicleTraveler2" 		or mID == "exode_card_E188_vehicleTraveler2" ):
		return (False, "Traveler-2", 						0,	188)
	if ( mID == "exode_card_189_vehicleSupplyDropship" 		or mID == "exode_card_E189_vehicleSupplyDropship" ):
		return (False, "Supply Dropship", 					0,	189)
	if ( mID == "exode_card_190_vehicleExplorationDropship" 	or mID == "exode_card_E190_vehicleExplorationDropship" ):
		return (False, "Exploration Dropship", 				1,	190)
	if ( mID == "exode_card_191_vehicleZandratti" 		or mID == "exode_card_E191_vehicleZandratti" ):
		return (False, "\"Zandratti\"", 					1,	191)
	if ( mID == "exode_card_192_vehicleSecurityDrone" 		or mID == "exode_card_E192_vehicleSecurityDrone" ):
		return (False, "Security Drone", 					1,	192)
	if ( mID == "exode_card_193_vehiclePantherBike" 		or mID == "exode_card_E193_vehiclePantherBike" ):
		return (False, "Pather Bike", 					1,	193)
		
	if ( mID == "exode_card_201_setMedicalBay" 			or mID == "exode_card_E201_setMedicalBay" ):
		return (False, "Medical Bay", 					1,	201)
	if ( mID == "exode_card_202_equipmentRoboticParts" 		or mID == "exode_card_E202_equipmentRoboticParts" ):
		return (False, "Robotic Parts", 					0,	202)
	if ( mID == "exode_card_203_equipmentEnergyCells" 		or mID == "exode_card_E203_equipmentEnergyCells" ):
		return (False, "Energy Cells", 					0,	203)
	if ( mID == "exode_card_204_equipmentShipConstructionParts"	or mID == "exode_card_E204_equipmentShipConstructionParts" ):
		return (False, "Ship Construction Parts", 				0,	204)
	if ( mID == "exode_card_205_equipmentUniversalFixer" 	or mID == "exode_card_E205_equipmentUniversalFixer" ):
		return (False, "\"Universal Fixer\" Suit", 				0,	205)
	if ( mID == "exode_card_206_equipmentLonestar" 		or mID == "exode_card_E206_equipmentLonestar" ):
		return (False, "\"Lonestar\" Spacesuit", 				0,	206)
	if ( mID == "exode_card_207_equipmentChipsAndData" 		or mID == "exode_card_E207_equipmentChipsAndData" ):
		return (False, "Chips and Data", 					0,	207)
	if ( mID == "exode_card_208_equipmentCorporate" 		or mID == "exode_card_E208_equipmentCorporate" ):
		return (False, "Corporate License", 					1,	208)
	if ( mID == "exode_card_209_equipmentEisenSuit" 		or mID == "exode_card_E209_equipmentEisenSuit" ):
		return (False, "Eisen Suit - Artic Edition", 				1,	209)
	if ( mID == "exode_card_210_equipmentDrachianSuit" 		or mID == "exode_card_E210_equipmentDrachianSuit" ):
		return (False, "Drachian Scarab Armor", 				1,	210)
	if ( mID == "exode_card_211_equipmentMilitarySuit" 		or mID == "exode_card_E211_equipmentMilitarySuit" ):
		return (False, "Military Suit Class A", 				1,	211)
	if ( mID == "exode_card_212_equipmentPlanetscan" 		or mID == "exode_card_E212_equipmentPlanetscan" ):
		return (False, "Planetscan VX", 					1,	212)
	if ( mID == "exode_card_213_equipmentRimscan" 		or mID == "exode_card_E213_equipmentRimscan" ):
		return (False, "Rimscan Software", 					1,	213)
	if ( mID == "exode_card_214_equipmentDesigner" 		or mID == "exode_card_E214_equipmentDesigner" ):
		return (False, "Diamondstar Designer", 				1,	214)
	if ( mID == "exode_card_215_equipmentIdentificationMatrix" 	or mID == "exode_card_E215_equipmentIdentificationMatrix" ):
		return (False, "Identification Matrix", 				0,	215)
		
	if ( mID == "exode_card_221_crewDrachianCommissar" 		or mID == "exode_card_E221_crewDrachianCommissar" ):
		return (False, "Drachian Commissar", 					1,	221)
	if ( mID == "exode_card_222_crewFederalAgent" 		or mID == "exode_card_E222_crewFederalAgent" ):
		return (False, "Federal Agent", 					1,	222)
	if ( mID == "exode_card_223_crewCorporateBodyguard" 		or mID == "exode_card_E223_crewCorporateBodyguard" ):
		return (False, "Corporate Bodyguard", 				1,	223)
	if ( mID == "exode_card_224_crewFederalMarine" 		or mID == "exode_card_E224_crewFederalMarine" ):
		return (False, "Federal Marine", 					1,	224)
	if ( mID == "exode_card_225_crewFederalPolice" 		or mID == "exode_card_E225_crewFederalPolice" ):
		return (False, "Federal Government Police", 				1,	225)
	if ( mID == "exode_card_226_crewDrachianTrooper" 		or mID == "exode_card_E226_crewDrachianTrooper" ):
		return (False, "Drachian Assault Trooper", 				1,	226)
	if ( mID == "exode_card_227_crewCorneredRebelAgent" 		or mID == "exode_card_E227_crewCorneredRebelAgent" ):
		return (False, "Cornered Rebel Agent", 				1,	227)
	if ( mID == "exode_card_228_passengerDangerous" 		or mID == "exode_card_E228_passengerDangerous" ):
		return (False, "Dangerous Passenger", 				1,	228)
	if ( mID == "exode_card_229_passengerUnstable" 		or mID == "exode_card_E229_passengerUnstable" ):
		return (False, "Unstable Genius", 					0,	229)
	if ( mID == "exode_card_230_crewMaintenanceDroid" 		or mID == "exode_card_E230_crewMaintenanceDroid" ):
		return (False, "Maintenance Droid", 					0,	230)
	if ( mID == "exode_card_231_passengerScienceStudent" 	or mID == "exode_card_E231_passengerScienceStudent" ):
		return (False, "Science student", 					0,	231)
	if ( mID == "exode_card_232_passengerSocialite" 		or mID == "exode_card_E232_passengerSocialite" ):
		return (False, "Socialite", 						0,	232)
	if ( mID == "exode_card_233_passengerTechExpert" 		or mID == "exode_card_E233_passengerTechExpert" ):
		return (False, "Tech Expert", 					0,	233)
		
	if ( mID == "exode_card_235_crewTriskan" 			or mID == "exode_card_E235_crewTriskan" ):
		return (False, "Triskan Fighter", 					1,	235)
	if ( mID == "exode_card_236_crewFleshCult"			or mID == "exode_card_E236_crewFleshCult" ):
		return (False, "Flesh Cult Recruiter", 				1,	236)
	if ( mID == "exode_card_237_crewFleshCultScientist" 		or mID == "exode_card_E237_crewFleshCultScientist" ):
		return (False, "Magna Cultist", 					1,	237)
		
	if ( mID == "exode_card_241_installationDrillingMachine" 	or mID == "exode_card_E241_installationDrillingMachine" ):
		return (False, "Drilling Machine", 					0,	241)
	if ( mID == "exode_card_242_installationRadarArray" 		or mID == "exode_card_E242_installationRadarArray" ):
		return (False, "Radar Array", 					0,	242)
	if ( mID == "exode_card_243_installationGenerator20" 	or mID == "exode_card_E243_installationGenerator20" ):
		return (False, "X-Gen TR20", 						0,	243)
	if ( mID == "exode_card_244_installationTomStarter" 		or mID == "exode_card_E244_installationTomStarter" ):
		return (False, "TOM STARTER", 					0,	244)
	if ( mID == "exode_card_245_installationLiveBlock" 		or mID == "exode_card_E245_installationLiveBlock" ):
		return (False, "Life Block", 						0,	245)
	if ( mID == "exode_card_246_installationBiodomes" 		or mID == "exode_card_E246_installationBiodomes" ):
		return (False, "Biodomes", 						0,	246)
	if ( mID == "exode_card_247_installationTurret" 		or mID == "exode_card_E247_installationTurret" ):
		return (False, "AA/AT Automatic Turret", 				0,	247)
	if ( mID == "exode_card_248_layoutProtectionWalls" 		or mID == "exode_card_E248_layoutProtectionWalls" ):
		return (False, "Protection Walls", 					0,	248)
	if ( mID == "exode_card_249_layoutUnderground" 		or mID == "exode_card_E249_layoutUnderground" ):
		return (False, "Underground Construction", 				0,	249)
	if ( mID == "exode_card_250_interiorLabEquipment" 		or mID == "exode_card_E250_interiorLabEquipment" ):
		return (False, "Lab Equipment", 					0,	250)
	if ( mID == "exode_card_251_interiorManagementConsole" 	or mID == "exode_card_E251_interiorManagementConsole" ):
		return (False, "Management Console", 					0,	251)
	if ( mID == "exode_card_252_interiorComputerRoom" 		or mID == "exode_card_E252_interiorComputerRoom" ):
		return (False, "Computer Room",					1,	252)
	if ( mID == "exode_card_253_installationMultipurpose" 	or mID == "exode_card_E253_installationMultipurpose" ):
		return (False, "Multipurpose Prefab", 				0,	253)
	if ( mID == "exode_card_254_installationCommunicationArray"	or mID == "exode_card_E254_installationCommunicationArray" ):
		return (False, "Communication Array", 				1,	254)
	if ( mID == "exode_card_255_interiorCuves" 			or mID == "exode_card_E255_interiorCuves" ):
		return (False, "Chemical Cuves", 					1,	255)
	if ( mID == "exode_card_256_installationPreservationDome"	or mID == "exode_card_E256_installationPreservationDome" ):
		return (False, "Preservation Dome", 					0,	256)
	if ( mID == "exode_card_257_installationStorage" 		or mID == "exode_card_E257_installationStorage" ):
		return (False, "Storage Building", 					0,	257)
	if ( mID == "exode_card_258_equipmentTomEssentialsHappyFood"	or mID == "exode_card_E258_equipmentTomEssentialsHappyFood" ):
		return (False, "Soup and Cook", 					2,	258)
	if ( mID == "exode_card_259_equipmentTomEssentialsHappyAir"	or mID == "exode_card_E259_equipmentTomEssentialsHappyAir" ):
		return (False, "TOM Beauty Air", 					2,	259)
	if ( mID == "exode_card_260_equipmentTomEssentialsSurvivor"	or mID == "exode_card_E260_equipmentTomEssentialsSurvivor" ):
		return (False, "TOM Survivor CO5", 					2,	260)
	if ( mID == "exode_card_261_actionImmediateOrder"		or mID == "exode_card_E261_actionImmediateOrder" ):
		return (False, "Emergency Order!", 					0,	261)
	
		
	return (False, mID, -1, 0)
	
	
def ex_GetAssetID( mID, mElite ):

	# rank: 
	# 0 -> common
	# 1 -> rare
	# 2 -> epic
	# 3 -> legendary
	
	if ( mElite == 0 ):
	
		if ( mID == "exode_alpha_booster"			or mID == "alpha booster"		or mID == "booster" ):
			return "exode_alpha_booster"
			
		if ( mID == "exode_alpha_support_vega"		or mID == "vega pack" ):
			return "exode_alpha_support_vega"
		if ( mID == "exode_alpha_support_ionguards"		or mID == "ion guards pack" ):
			return "exode_alpha_support_ionguards"
		if ( mID == "exode_alpha_support_tom"			or mID == "tom essentials"		or mID == "tom pack" ):
			return "exode_alpha_support_tom"
			
			
		if ( mID == "exode_alpha_starter_4"			or mID == "triple alpha starter" ):
			return "exode_alpha_starter_4"
		if ( mID == "exode_alpha_starter_3"			or mID == "civilian starter"		or mID == "civilian alpha starter" ):
			return "exode_alpha_starter_3"
		if ( mID == "exode_alpha_starter_2"			or mID == "scientist starter"		or mID == "scientific starter"		or mID == "scientific alpha starter"		or mID == "scientist alpha starter" ):
			return "exode_alpha_starter_2"
		if ( mID == "exode_alpha_starter_1"			or mID == "military starter"		or mID == "military alpha starter" ):	
			return "exode_alpha_starter_1"
			
		if ( mID == "exode_alpha_contract_tom"		or mID == "tom alpha contract"	or mID == "tom contract" ):
			return "exode_alpha_contract_tom"
		if ( mID == "exode_alpha_contract_rekatron"		or mID == "rekatron alpha contract"	or mID == "rekatron contract" ):
			return "exode_alpha_contract_rekatron"
		if ( mID == "exode_alpha_contract_syndicate"		or mID == "syndicate alpha contract"	or mID == "syndicate contract" ):
			return "exode_alpha_contract_syndicate"
			
		if ( mID == "exode_alpha_pack_crew_kb119"		or mID == "kilbot-119 pack"		or mID == "kb-119 pack" ):
			return "exode_alpha_pack_crew_kb119"
		if ( mID == "exode_alpha_pack_crew_galvin4"		or mID == "galvin 4 pack"		or mID == "galvin pack" ):
			return "exode_alpha_pack_crew_galvin4"
			
		if ( mID == "exode_alpha_character_pack_nomad"	or mID == "nomad pack"			or mID == "nomad promo pack" ):
			return "exode_alpha_character_pack_nomad"
		if ( mID == "exode_alpha_character_pack_genetician"	or mID == "genetician pack"		or mID == "genetician promo pack" ):
			return "exode_alpha_character_pack_genetician"
		if ( mID == "exode_alpha_character_pack_suntek"	or mID == "suntek pack"		or mID == "suntek promo pack" ):
			return "exode_alpha_character_pack_suntek"
		if ( mID == "exode_alpha_character_pack_drachian"	or mID == "drachian pack"		or mID == "drachian promo pack" ):
			return "exode_alpha_character_pack_drachian"
			
		if ( mID == "exode_card_001_originNavy"		or mID == "navy lieutenant"		or mID == "military origin"		or mID == "1" ): 	
			return "exode_card_001_originNavy"		
		if ( mID == "exode_card_002_shipArcheon"		or mID == "archeon ship"		or mID == "military ship"		or mID == "2" ): 	
			return "exode_card_002_shipArcheon"
		if ( mID == "exode_card_003_officerComms"		or mID == "communications officer"						or mID == "3" ): 	
			return "exode_card_003_officerComms"
		if ( mID == "exode_card_004_officerWeapons" 		or mID == "weapons officer"							or mID == "4" ): 
			return "exode_card_004_officerWeapons"	
		if ( mID == "exode_card_005_officerTactical" 		or mID == "tactical officer"							or mID == "5" ): 
			return "exode_card_005_officerTactical"	
		if ( mID == "exode_card_006_crewPilot" 		or mID == "pilot"			or mID == "military pilot"		or mID == "6" ): 
			return "exode_card_006_crewPilot"	
		if ( mID == "exode_card_007_crewSRT" 			or mID == "signals specialist"						or mID == "7" ): 
			return "exode_card_007_crewSRT"	
		if ( mID == "exode_card_008_crewDefense"		or mID == "defense specialist"						or mID == "8" ): 
			return "exode_card_008_crewDefense"	
		if ( mID == "exode_card_009_crewTrooper" 		or mID == "trooper"								or mID == "9" ): 
			return "exode_card_009_crewTrooper"	
		if ( mID == "exode_card_010_crewEngineer" 		or mID == "military engineer "						or mID == "10" ): 
			return "exode_card_010_crewEngineer"	
		if ( mID == "exode_card_011_setFMR17" 		or mID == "fmr-17 x3"			or mID == "atonis x3"			or mID == "11" ): 
			return "exode_card_011_setFMR17"	
		if ( mID == "exode_card_012_setSuitMilitaryC" 	or mID == "military suit class c x3"						or mID == "12" ): 
			return "exode_card_012_setSuitMilitaryC"	
		if ( mID == "exode_card_013_originArk" 		or mID == "ark scientist"		or mID == "scientific origin"		or mID == "13" ): 
			return "exode_card_013_originArk"	
		if ( mID == "exode_card_014_shipOrwell1" 		or mID == "ark ship"			or mID == "orwell1"			or mID == "scientific ship"	or mID == "14" ): 
			return "exode_card_014_shipOrwell1"	
		if ( mID == "exode_card_015_officerResearch" 		or mID == "research officer"		or mID == "15" ): 
			return "exode_card_015_officerResearch"	
		if ( mID == "exode_card_016_officerExploration" 	or mID == "exploration officer"	or mID == "16" ): 
			return "exode_card_016_officerExploration"	
		if ( mID == "exode_card_017_officerPreservation" 	or mID == "preservation officer"	or mID == "17" ): 
			return "exode_card_017_officerPreservation"	
		if ( mID == "exode_card_018_crewSurgeon" 		or mID == "space surgeon"		or mID == "18" ): 
			return "exode_card_018_crewSurgeon"	
		if ( mID == "exode_card_019_crewXenoAnalyst" 		or mID == "xeno analyst"		or mID == "19" ): 
			return "exode_card_019_crewXenoAnalyst"	
		if ( mID == "exode_card_020_crewBioScientist" 	or mID == "bio scientist"		or mID == "20" ): 
			return "exode_card_020_crewBioScientist"	
		if ( mID == "exode_card_021_crewAnimalHandler" 	or mID == "animal handler"		or mID == "21" ): 
			return "exode_card_021_crewAnimalHandler"	
		if ( mID == "exode_card_022_crewLifeSearcher" 	or mID == "life searcher"		or mID == "22" ): 
			return "exode_card_022_crewLifeSearcher"	
		if ( mID == "exode_card_023_crewLabScientist" 	or mID == "lab scientist"		or mID == "23" ): 
			return "exode_card_023_crewLabScientist"	
		if ( mID == "exode_card_024_setRarePlants" 		or mID == "rare plants"		or mID == "24" ): 
			return "exode_card_024_setRarePlants"	
		if ( mID == "exode_card_025_setSuitResearchC" 	or mID == "research suits class c x3"	or mID == "25" ): 
			return "exode_card_025_setSuitResearchC"	
		if ( mID == "exode_card_026_originLeader" 		or mID == "elected leader" 		or mID == "civilian origin"	or mID == "26" ): 
			return "exode_card_026_originLeader"	
		if ( mID == "exode_card_027_shipDiplomatic" 		or mID == "diplomatic corvette" 	or mID == "amarasia" or mID == "civilian ship"	or mID == "27" ): 
			return "exode_card_027_shipDiplomatic"	
		if ( mID == "exode_card_028_officerAdministrative"	or mID == "administrative officer"	or mID == "28" ): 
			return "exode_card_028_officerAdministrative"	
		if ( mID == "exode_card_029_officerSecurity" 		or mID == "security officer"		or mID == "29" ): 
			return "exode_card_029_officerSecurity"	
		if ( mID == "exode_card_030_crewPropaganda"		or mID == "propaganda specialist"	or mID == "30" ): 
			return "exode_card_030_crewPropaganda"	
		if ( mID == "exode_card_031_crewPopulation" 		or mID == "population analyst"	or mID == "31" ): 
			return "exode_card_031_crewPopulation"	
		if ( mID == "exode_card_032_crewEntertainment" 	or mID == "welfare specialist"	or mID == "32" ): 
			return "exode_card_032_crewEntertainment"	
		if ( mID == "exode_card_033_crewMaintenance" 		or mID == "maintenance staff"		or mID == "33" ): 
			return "exode_card_033_crewMaintenance"	
		if ( mID == "exode_card_034_crewPilotCivilian" 	or mID == "civilian pilot"		or mID == "34" ): 
			return "exode_card_034_crewPilotCivilian"	
		if ( mID == "exode_card_035_crewSecurity" 		or mID == "security guard"		or mID == "35" ): 
			return "exode_card_035_crewSecurity"	
		if ( mID == "exode_card_036_setLuxury" 		or mID == "diplomatic gifts"		or mID == "36" ): 
			return "exode_card_036_setLuxury"	
		if ( mID == "exode_card_037_setDatabase" 		or mID == "federal database"		or mID == "37" ): 
			return "exode_card_037_setDatabase"	
			
			
		if ( mID == "exode_card_046_Rekatron_defensiveAmmo"		or mID == "46" ): 
			return "exode_card_046_Rekatron_defensiveAmmo"
		if ( mID == "exode_card_047_Rekatron_firetalkerPistol" 	or mID == "47" ): 
			return "exode_card_047_Rekatron_firetalkerPistol"
		if ( mID == "exode_card_048_Rekatron_karperPistol" 		or mID == "48" ): 
			return "exode_card_048_Rekatron_karperPistol"
		if ( mID == "exode_card_049_Rekatron_explanatorRifle" 	or mID == "49" ): 
			return "exode_card_049_Rekatron_explanatorRifle"
		if ( mID == "exode_card_050_Rekatron_rsdRifle" 		or mID == "50" ): 
			return "exode_card_050_Rekatron_rsdRifle"
		if ( mID == "exode_card_051_Rekatron_goodMorningPistol" 	or mID == "51" ): 
			return "exode_card_051_Rekatron_goodMorningPistol"
		if ( mID == "exode_card_052_Rekatron_jugdmentDayRifle" 	or mID == "52" ): 
			return "exode_card_052_Rekatron_jugdmentDayRifle"
		if ( mID == "exode_card_053_Rekatron_galacticPeacemaker" 	or mID == "53" ): 
			return "exode_card_053_Rekatron_galacticPeacemaker"
		if ( mID == "exode_card_054_Rekatron_ammoGuided" 		or mID == "54" ): 
			return "exode_card_054_Rekatron_ammoGuided"
		if ( mID == "exode_card_055_Rekatron_ammoParty" 		or mID == "55" ): 
			return "exode_card_055_Rekatron_ammoParty"
		if ( mID == "exode_card_056_Tom_SmootyAllInOne" 		or mID == "56" ): 
			return "exode_card_056_Tom_SmootyAllInOne"
		if ( mID == "exode_card_057_Tom_FoodieMoodie" 		or mID == "57" ): 
			return "exode_card_057_Tom_FoodieMoodie"
		if ( mID == "exode_card_058_Tom_FriendlyEyes" 		or mID == "58" ): 
			return "exode_card_058_Tom_FriendlyEyes"
		if ( mID == "exode_card_059_Tom_BuddyPinger" 			or mID == "59" ): 
			return "exode_card_059_Tom_BuddyPinger"
		if ( mID == "exode_card_060_Tom_VehicleLittleBuddy" 		or mID == "60" ): 
			return "exode_card_060_Tom_VehicleLittleBuddy"
		if ( mID == "exode_card_061_Tom_Custom" 			or mID == "61" ): 
			return "exode_card_061_Tom_Custom"
		if ( mID == "exode_card_062_Tom_WHCConverter" 		or mID == "62" ): 
			return "exode_card_062_Tom_WHCConverter"
		if ( mID == "exode_card_063_Tom_Explorator" 			or mID == "63" ): 
			return "exode_card_063_Tom_Explorator"
		if ( mID == "exode_card_064_Tom_ShelterHappyFive" 		or mID == "64" ): 
			return "exode_card_064_Tom_ShelterHappyFive"
			
		if ( mID == "exode_card_066_SyndicateEquipment_Chip" 	or mID == "66" ): 
			return "exode_card_066_SyndicateEquipment_Chip"
		if ( mID == "exode_card_067_SyndicateEquipment_DrugHolidays"	or mID == "67" ): 
			return "exode_card_067_SyndicateEquipment_DrugHolidays"
		if ( mID == "exode_card_068_SyndicateEquipment_DrugNPrime"	or mID == "68" ): 
			return "exode_card_068_SyndicateEquipment_DrugNPrime"
		if ( mID == "exode_card_069_SyndicateShipBlackLotus" 	or mID == "69" ): 
			return "exode_card_069_SyndicateShipBlackLotus"
		if ( mID == "exode_card_070_SyndicateEquipmentAutoBlaster"	or mID == "70" ): 
			return "exode_card_070_SyndicateEquipmentAutoBlaster"
		if ( mID == "exode_card_071_SyndicateEquipment_NarcoWarfare"	or mID == "71" ): 
			return "exode_card_071_SyndicateEquipment_NarcoWarfare"
		if ( mID == "exode_card_072_SyndicateEquipmentSet_Genefactory" or mID == "72" ): 
			return "exode_card_072_SyndicateEquipmentSet_Genefactory"
		if ( mID == "exode_card_073_SyndicateHacker" 			or mID == "73" ): 
			return "exode_card_073_SyndicateHacker"
		if ( mID == "exode_card_074_SyndicateLeader" 			or mID == "74" ): 
			return "exode_card_074_SyndicateLeader"
		if ( mID == "exode_card_075_SyndicateTransactor" 		or mID == "75" ): 
			return "exode_card_075_SyndicateTransactor"
		if ( mID == "exode_card_076_SyndicateTrooper" 		or mID == "76" ): 
			return "exode_card_076_SyndicateTrooper"
		if ( mID == "exode_card_077_SyndicateAyumi" 			or mID == "77" ): 
			return "exode_card_077_SyndicateAyumi"
		if ( mID == "exode_card_078_SyndicateYakuzaNoble" 		or mID == "78" ): 
			return "exode_card_078_SyndicateYakuzaNoble"
		if ( mID == "exode_card_079_SyndicateYakuzaSniper" 		or mID == "79" ): 
			return "exode_card_079_SyndicateYakuzaSniper"
		if ( mID == "exode_card_080_TheKumicho" 			or mID == "80" ): 
			return "exode_card_080_TheKumicho"
		if ( mID == "exode_card_081_RebelGeneral" 			or mID == "81" ): 
			return "exode_card_081_RebelGeneral"
		if ( mID == "exode_card_082_AlannaVos" 			or mID == "82" ): 
			return "exode_card_082_AlannaVos"
		if ( mID == "exode_card_083_Sh4rken" 				or mID == "83" ): 
			return "exode_card_083_Sh4rken"
		if ( mID == "exode_card_084_TheAI" 				or mID == "84" ): 
			return "exode_card_084_TheAI"
		if ( mID == "exode_card_085_Apprentice" 			or mID == "85" ): 
			return "exode_card_085_Apprentice"
		if ( mID == "exode_card_086_Cranium" 				or mID == "86" ): 
			return "exode_card_086_Cranium"
		if ( mID == "exode_card_087_Cryptoeater" 			or mID == "87" ): 
			return "exode_card_087_Cryptoeater"
		if ( mID == "exode_card_088_originRepentantPirate" 		or mID == "88" ): 
			return "exode_card_088_originRepentantPirate"
		if ( mID == "exode_card_089_shipColombus" 			or mID == "89" ): 
			return "exode_card_089_shipColombus"
		if ( mID == "exode_card_090_shipQuantumSupreme"		or mID == "90" ): 
			return "exode_card_090_shipQuantumSupreme"
		if ( mID == "exode_card_091_vehicleVelvetStorm" 		or mID == "91" ): 
			return "exode_card_091_vehicleVelvetStorm"
		if ( mID == "exode_card_092_vehicleVanguard" 			or mID == "92" ): 
			return "exode_card_092_vehicleVanguard"
		if ( mID == "exode_card_093_equipmentSuitArena" 		or mID == "93" ): 
			return "exode_card_093_equipmentSuitArena"
			
		if ( mID == "exode_card_101_originSecretAgent" 		or mID == "101" ): 
			return "exode_card_101_originSecretAgent"
		if ( mID == "exode_card_102_originStrandedTrader" 		or mID == "102" ): 
			return "exode_card_102_originStrandedTrader"
		if ( mID == "exode_card_103_originCruiseShipCaptain" 	or mID == "103" ): 
			return "exode_card_103_originCruiseShipCaptain"
		if ( mID == "exode_card_104_shipArkLifesavior" 		or mID == "104" ): 
			return "exode_card_104_shipArkLifesavior"
		if ( mID == "exode_card_105_shipCargoKormen" 			or mID == "105" ): 
			return "exode_card_105_shipCargoKormen"
		if ( mID == "exode_card_106_shipRhino" 			or mID == "106" ): 
			return "exode_card_106_shipRhino"
		if ( mID == "exode_card_107_shipCargoTaurus" 			or mID == "107" ): 
			return "exode_card_107_shipCargoTaurus"
		if ( mID == "exode_card_108_shipMyrmidon" 			or mID == "108" ): 
			return "exode_card_108_shipMyrmidon"
		if ( mID == "exode_card_109_shipAkhen" 			or mID == "109" ): 
			return "exode_card_109_shipAkhen"
		if ( mID == "exode_card_110_shipCoetus" 			or mID == "110" ): 
			return "exode_card_110_shipCoetus"
		if ( mID == "exode_card_111_setGeneticianConsole" 		or mID == "111" ): 
			return "exode_card_111_setGeneticianConsole"
		if ( mID == "exode_card_112_setMilitaryClassA" 		or mID == "112" ): 
			return "exode_card_112_setMilitaryClassA"
		if ( mID == "exode_card_113_setEisenSuits" 			or mID == "113" ): 
			return "exode_card_113_setEisenSuits"
		if ( mID == "exode_card_114_vehicleAcheanRacer" 		or mID == "114" ): 
			return "exode_card_114_vehicleAcheanRacer"
		if ( mID == "exode_card_115_crewSpaceMarshal"			or mID == "115" ): 
			return "exode_card_115_crewSpaceMarshal"
		if ( mID == "exode_card_116_officerEliza" 			or mID == "116" ): 
			return "exode_card_116_officerEliza"
		if ( mID == "exode_card_117_crewOksana" 			or mID == "117" ): 
			return "exode_card_117_crewOksana"
		if ( mID == "exode_card_118_officerNorah" 			or mID == "118" ): 
			return "exode_card_118_officerNorah"
		if ( mID == "exode_card_119_officerShen" 			or mID == "119" ): 
			return "exode_card_119_officerShen"
		if ( mID == "exode_card_120_officerStug" 			or mID == "120" ): 
			return "exode_card_120_officerStug"
		if ( mID == "exode_card_121_crewTyron" 			or mID == "121" ): 
			return "exode_card_121_crewTyron"
		if ( mID == "exode_card_122_officerAdmiralValro" 		or mID == "122" ): 
			return "exode_card_122_officerAdmiralValro"
		if ( mID == "exode_card_123_officerNash" 			or mID == "123" ): 
			return "exode_card_123_officerNash"
		if ( mID == "exode_card_124_crewSpecialInfiltrationAgent" 	or mID == "124" ): 
			return "exode_card_124_crewSpecialInfiltrationAgent"
		if ( mID == "exode_card_125_crewScarletSarah" 		or mID == "125" ): 
			return "exode_card_125_crewScarletSarah"
		if ( mID == "exode_card_126_passengerNuclearFamily" 		or mID == "126" ): 
			return "exode_card_126_passengerNuclearFamily"
		if ( mID == "exode_card_127_installationOctohome" 		or mID == "127" ): 
			return "exode_card_127_installationOctohome"
		if ( mID == "exode_card_128_installationOrbitalShield" 	or mID == "128" ): 
			return "exode_card_128_installationOrbitalShield"
		if ( mID == "exode_card_129_installationDreamsphere" 	or mID == "129" ): 
			return "exode_card_129_installationDreamsphere"
		if ( mID == "exode_card_130_installationGenerator100"	or mID == "130" ): 
			return "exode_card_130_installationGenerator100"
		if ( mID == "exode_card_131_equipmentFactionCorporate" 	or mID == "131" ): 
			return "exode_card_131_equipmentFactionCorporate"
		if ( mID == "exode_card_132_equipmentSuitRacer" 		or mID == "132" ): 
			return "exode_card_132_equipmentSuitRacer"
		if ( mID == "exode_card_133_equipmentSuitSpartan" 		or mID == "133" ): 
			return "exode_card_133_equipmentSuitSpartan"
		if ( mID == "exode_card_134_equipmentFactionRebellion" 	or mID == "134" ): 
			return "exode_card_134_equipmentFactionRebellion"
		if ( mID == "exode_card_135_escortSabre" 			or mID == "135" ): 
			return "exode_card_135_escortSabre"
		if ( mID == "exode_card_136_crewFleshCultLeader" 		or mID == "136" ): 
			return "exode_card_136_crewFleshCultLeader"
		if ( mID == "exode_card_137_installationDefensiveBunker" 	or mID == "137" ): 
			return "exode_card_137_installationDefensiveBunker"
			
		if ( mID == "exode_card_151_officerDrachianColonel" 		or mID == "151" ): 
			return "exode_card_151_officerDrachianColonel"
		if ( mID == "exode_card_152_crewNomadNavigator" 		or mID == "152" ): 
			return "exode_card_152_crewNomadNavigator"
		if ( mID == "exode_card_153_crewGeneticianScientist" 	or mID == "153" ): 
			return "exode_card_153_crewGeneticianScientist"
		if ( mID == "exode_card_154_crewSuntekSurvivor" 		or mID == "154" ): 
			return "exode_card_154_crewSuntekSurvivor"
		if ( mID == "exode_card_155_crewKilbot" 			or mID == "155" ): 
			return "exode_card_155_crewKilbot"
		if ( mID == "exode_card_156_crewGalvin" 			or mID == "156" ): 
			return "exode_card_156_crewGalvin"
		if ( mID == "exode_card_157_escortVega" 			or mID == "157" ): 
			return "exode_card_157_escortVega"
		if ( mID == "exode_card_158_escortIonguards" 			or mID == "158" ): 
			return "exode_card_158_escortIonguards"
		if ( mID == "exode_card_159_suntekSphere" 			or mID == "159" ): 
			return "exode_card_159_suntekSphere"
			
			
		if ( mID == "exode_card_181_escortLongswords" 		or mID == "181" ): 
			return "exode_card_181_escortLongswords"
		if ( mID == "exode_card_182_escortCruiserTaskForce" 		or mID == "182" ): 
			return "exode_card_182_escortCruiserTaskForce"
		if ( mID == "exode_card_183_escortStarsystemGarrison" 	or mID == "183" ): 
			return "exode_card_183_escortStarsystemGarrison"
		if ( mID == "exode_card_184_shipBaldie" 			or mID == "184" ): 
			return "exode_card_184_shipBaldie"
		if ( mID == "exode_card_185_shipClaymoreHyperfighter" 	or mID == "185" ): 
			return "exode_card_185_shipClaymoreHyperfighter"
		if ( mID == "exode_card_186_shipDrachianMantis" 		or mID == "186" ): 
			return "exode_card_186_shipDrachianMantis"
		if ( mID == "exode_card_187_vehicleSalazar" 			or mID == "187" ): 
			return "exode_card_187_vehicleSalazar"
		if ( mID == "exode_card_188_vehicleTraveler2" 		or mID == "188" ): 
			return "exode_card_188_vehicleTraveler2"
		if ( mID == "exode_card_189_vehicleSupplyDropship" 		or mID == "189" ): 
			return "exode_card_189_vehicleSupplyDropship"
		if ( mID == "exode_card_190_vehicleExplorationDropship" 	or mID == "190" ): 
			return "exode_card_190_vehicleExplorationDropship"
		if ( mID == "exode_card_191_vehicleZandratti" 		or mID == "191" ): 
			return "exode_card_191_vehicleZandratti"
		if ( mID == "exode_card_192_vehicleSecurityDrone" 		or mID == "192" ): 
			return "exode_card_192_vehicleSecurityDrone"
		if ( mID == "exode_card_193_vehiclePantherBike" 		or mID == "193" ): 
			return "exode_card_193_vehiclePantherBike"
			
		if ( mID == "exode_card_201_setMedicalBay" 			or mID == "201" ): 
			return "exode_card_201_setMedicalBay"
		if ( mID == "exode_card_202_equipmentRoboticParts" 		or mID == "202" ): 
			return "exode_card_202_equipmentRoboticParts"
		if ( mID == "exode_card_203_equipmentEnergyCells" 		or mID == "203" ): 
			return "exode_card_203_equipmentEnergyCells"
		if ( mID == "exode_card_204_equipmentShipConstructionParts"	or mID == "204" ): 
			return "exode_card_204_equipmentShipConstructionParts"
		if ( mID == "exode_card_205_equipmentUniversalFixer" 	or mID == "205" ): 
			return "exode_card_205_equipmentUniversalFixer"
		if ( mID == "exode_card_206_equipmentLonestar" 		or mID == "206" ): 
			return "exode_card_206_equipmentLonestar"
		if ( mID == "exode_card_207_equipmentChipsAndData" 		or mID == "207" ): 
			return "exode_card_207_equipmentChipsAndData"
		if ( mID == "exode_card_208_equipmentCorporate" 		or mID == "208" ): 
			return "exode_card_208_equipmentCorporate"
		if ( mID == "exode_card_209_equipmentEisenSuit" 		or mID == "209" ): 
			return "exode_card_209_equipmentEisenSuit"
		if ( mID == "exode_card_210_equipmentDrachianSuit" 		or mID == "210" ): 
			return "exode_card_210_equipmentDrachianSuit"
		if ( mID == "exode_card_211_equipmentMilitarySuit" 		or mID == "211" ): 
			return "exode_card_211_equipmentMilitarySuit"
		if ( mID == "exode_card_212_equipmentPlanetscan" 		or mID == "212" ): 
			return "exode_card_212_equipmentPlanetscan"
		if ( mID == "exode_card_213_equipmentRimscan" 		or mID == "213" ): 
			return "exode_card_213_equipmentRimscan"
		if ( mID == "exode_card_214_equipmentDesigner" 		or mID == "214" ): 
			return "exode_card_214_equipmentDesigner"
		if ( mID == "exode_card_215_equipmentIdentificationMatrix" 	or mID == "215" ): 
			return "exode_card_215_equipmentIdentificationMatrix"
			
		if ( mID == "exode_card_221_crewDrachianCommissar" 		or mID == "221" ): 
			return "exode_card_221_crewDrachianCommissar"
		if ( mID == "exode_card_222_crewFederalAgent" 		or mID == "222" ): 
			return "exode_card_222_crewFederalAgent"
		if ( mID == "exode_card_223_crewCorporateBodyguard" 		or mID == "223" ): 
			return "exode_card_223_crewCorporateBodyguard"
		if ( mID == "exode_card_224_crewFederalMarine" 		or mID == "224" ): 
			return "exode_card_224_crewFederalMarine"
		if ( mID == "exode_card_225_crewFederalPolice" 		or mID == "225" ): 
			return "exode_card_225_crewFederalPolice"
		if ( mID == "exode_card_226_crewDrachianTrooper" 		or mID == "226" ): 
			return "exode_card_226_crewDrachianTrooper"
		if ( mID == "exode_card_227_crewCorneredRebelAgent" 		or mID == "227" ): 
			return "exode_card_227_crewCorneredRebelAgent"
		if ( mID == "exode_card_228_passengerDangerous" 		or mID == "228" ): 
			return "exode_card_228_passengerDangerous"
		if ( mID == "exode_card_229_passengerUnstable" 		or mID == "229" ): 
			return "exode_card_229_passengerUnstable"
		if ( mID == "exode_card_230_crewMaintenanceDroid" 		or mID == "230" ): 
			return "exode_card_230_crewMaintenanceDroid"
		if ( mID == "exode_card_231_passengerScienceStudent" 	or mID == "231" ): 
			return "exode_card_231_passengerScienceStudent"
		if ( mID == "exode_card_232_passengerSocialite" 		or mID == "232" ): 
			return "exode_card_232_passengerSocialite"
		if ( mID == "exode_card_233_passengerTechExpert" 		or mID == "233" ): 
			return "exode_card_233_passengerTechExpert"
			
		if ( mID == "exode_card_235_crewTriskan" 			or mID == "235" ): 
			return "exode_card_235_crewTriskan"
		if ( mID == "exode_card_236_crewFleshCult"			or mID == "236" ): 
			return "exode_card_236_crewFleshCult"
		if ( mID == "exode_card_237_crewFleshCultScientist" 		or mID == "237" ): 
			return "exode_card_237_crewFleshCultScientist"
			
		if ( mID == "exode_card_241_installationDrillingMachine" 	or mID == "drill"			or mID == "drilling machine"			or mID == "241" ): 
			return "exode_card_241_installationDrillingMachine"
		if ( mID == "exode_card_242_installationRadarArray" 		or mID == "242" ): 
			return "exode_card_242_installationRadarArray"
		if ( mID == "exode_card_243_installationGenerator20" 	or mID == "243" ): 
			return "exode_card_243_installationGenerator20"
		if ( mID == "exode_card_244_installationTomStarter" 		or mID == "244" ): 
			return "exode_card_244_installationTomStarter"
		if ( mID == "exode_card_245_installationLiveBlock" 		or mID == "245" ): 
			return "exode_card_245_installationLiveBlock"
		if ( mID == "exode_card_246_installationBiodomes" 		or mID == "246" ): 
			return "exode_card_246_installationBiodomes"
		if ( mID == "exode_card_247_installationTurret" 		or mID == "247" ): 
			return "exode_card_247_installationTurret"
		if ( mID == "exode_card_248_layoutProtectionWalls" 		or mID == "248" ): 
			return "exode_card_248_layoutProtectionWalls"
		if ( mID == "exode_card_249_layoutUnderground" 		or mID == "249" ): 
			return "exode_card_249_layoutUnderground"
		if ( mID == "exode_card_250_interiorLabEquipment" 		or mID == "250" ): 
			return "exode_card_250_interiorLabEquipment"
		if ( mID == "exode_card_251_interiorManagementConsole" 	or mID == "251" ): 
			return "exode_card_251_interiorManagementConsole"
		if ( mID == "exode_card_252_interiorComputerRoom" 		or mID == "252" ): 
			return "exode_card_252_interiorComputerRoom"
		if ( mID == "exode_card_253_installationMultipurpose" 	or mID == "253" ): 
			return "exode_card_253_installationMultipurpose"
		if ( mID == "exode_card_254_installationCommunicationArray"	or mID == "254" ): 
			return "exode_card_254_installationCommunicationArray"
		if ( mID == "exode_card_255_interiorCuves" 			or mID == "255" ): 
			return "exode_card_255_interiorCuves"
		if ( mID == "exode_card_256_installationPreservationDome"	or mID == "256" ): 
			return "exode_card_256_installationPreservationDome"
		if ( mID == "exode_card_257_installationStorage" 		or mID == "257" ): 
			return "exode_card_257_installationStorage"
		if ( mID == "exode_card_258_equipmentTomEssentialsHappyFood"	or mID == "258" ): 
			return "exode_card_258_equipmentTomEssentialsHappyFood"
		if ( mID == "exode_card_259_equipmentTomEssentialsHappyAir"	or mID == "259" ): 
			return "exode_card_259_equipmentTomEssentialsHappyAir"
		if ( mID == "exode_card_260_equipmentTomEssentialsSurvivor"	or mID == "260" ): 
			return "exode_card_260_equipmentTomEssentialsSurvivor"
		if ( mID == "exode_card_261_actionImmediateOrder"		or mID == "261" ): 
			return "exode_card_261_actionImmediateOrder"
		
			
		return ""
	else:
	
		if ( mID == "exode_card_E001_originNavy"		or mID == "navy lieutenant"		or mID == "military origin"		or mID == "1" ): 	
			return "exode_card_E001_originNavy"		
		if ( mID == "exode_card_E002_shipArcheon"		or mID == "archeon ship"		or mID == "military ship"		or mID == "2" ): 	
			return "exode_card_E002_shipArcheon"
		if ( mID == "exode_card_E003_officerComms"		or mID == "communications officer"						or mID == "3" ): 	
			return "exode_card_E003_officerComms"
		if ( mID == "exode_card_E004_officerWeapons" 		or mID == "weapons officer"							or mID == "4" ): 
			return "exode_card_E004_officerWeapons"	
		if ( mID == "exode_card_E005_officerTactical" 		or mID == "tactical officer"							or mID == "5" ): 
			return "exode_card_E005_officerTactical"	
		if ( mID == "exode_card_E006_crewPilot" 		or mID == "pilot"			or mID == "military pilot"		or mID == "6" ): 
			return "exode_card_E006_crewPilot"	
		if ( mID == "exode_card_E007_crewSRT" 			or mID == "signals specialist"						or mID == "7" ): 
			return "exode_card_E007_crewSRT"	
		if ( mID == "exode_card_E008_crewDefense"		or mID == "defense specialist"						or mID == "8" ): 
			return "exode_card_E008_crewDefense"	
		if ( mID == "exode_card_E009_crewTrooper" 		or mID == "trooper"								or mID == "9" ): 
			return "exode_card_E009_crewTrooper"	
		if ( mID == "exode_card_E010_crewEngineer" 		or mID == "military engineer "						or mID == "10" ): 
			return "exode_card_E010_crewEngineer"	
		if ( mID == "exode_card_E011_setFMR17" 		or mID == "fmr-17 x3"			or mID == "atonis x3"			or mID == "11" ): 
			return "exode_card_E011_setFMR17"	
		if ( mID == "exode_card_E012_setSuitMilitaryC" 	or mID == "military suit class c x3"						or mID == "12" ): 
			return "exode_card_E012_setSuitMilitaryC"	
		if ( mID == "exode_card_E013_originArk" 		or mID == "ark scientist"		or mID == "scientific origin"		or mID == "13" ): 
			return "exode_card_E013_originArk"	
		if ( mID == "exode_card_E014_shipOrwell1" 		or mID == "ark ship"			or mID == "orwell1"			or mID == "scientific ship"	or mID == "14" ): 
			return "exode_card_E014_shipOrwell1"	
		if ( mID == "exode_card_E015_officerResearch" 		or mID == "research officer"		or mID == "15" ): 
			return "exode_card_E015_officerResearch"	
		if ( mID == "exode_card_E016_officerExploration" 	or mID == "exploration officer"	or mID == "16" ): 
			return "exode_card_E016_officerExploration"	
		if ( mID == "exode_card_E017_officerPreservation" 	or mID == "preservation officer"	or mID == "17" ): 
			return "exode_card_E017_officerPreservation"	
		if ( mID == "exode_card_E018_crewSurgeon" 		or mID == "space surgeon"		or mID == "18" ): 
			return "exode_card_E018_crewSurgeon"	
		if ( mID == "exode_card_E019_crewXenoAnalyst" 		or mID == "xeno analyst"		or mID == "19" ): 
			return "exode_card_E019_crewXenoAnalyst"	
		if ( mID == "exode_card_E020_crewBioScientist" 	or mID == "bio scientist"		or mID == "20" ): 
			return "exode_card_E020_crewBioScientist"	
		if ( mID == "exode_card_E021_crewAnimalHandler" 	or mID == "animal handler"		or mID == "21" ): 
			return "exode_card_E021_crewAnimalHandler"	
		if ( mID == "exode_card_E022_crewLifeSearcher" 	or mID == "life searcher"		or mID == "22" ): 
			return "exode_card_E022_crewLifeSearcher"	
		if ( mID == "exode_card_E023_crewLabScientist" 	or mID == "lab scientist"		or mID == "23" ): 
			return "exode_card_E023_crewLabScientist"	
		if ( mID == "exode_card_E024_setRarePlants" 		or mID == "rare plants"		or mID == "24" ): 
			return "exode_card_E024_setRarePlants"	
		if ( mID == "exode_card_E025_setSuitResearchC" 	or mID == "research suits class c x3"	or mID == "25" ): 
			return "exode_card_E025_setSuitResearchC"	
		if ( mID == "exode_card_E026_originLeader" 		or mID == "elected leader" 		or mID == "civilian origin"	or mID == "26" ): 
			return "exode_card_E026_originLeader"	
		if ( mID == "exode_card_E027_shipDiplomatic" 		or mID == "diplomatic corvette" 	or mID == "amarasia" or mID == "civilian ship"	or mID == "27" ): 
			return "exode_card_E027_shipDiplomatic"	
		if ( mID == "exode_card_E028_officerAdministrative"	or mID == "administrative officer"	or mID == "28" ): 
			return "exode_card_E028_officerAdministrative"	
		if ( mID == "exode_card_E029_officerSecurity" 		or mID == "security officer"		or mID == "29" ): 
			return "exode_card_E029_officerSecurity"	
		if ( mID == "exode_card_E030_crewPropaganda"		or mID == "propaganda specialist"	or mID == "30" ): 
			return "exode_card_E030_crewPropaganda"	
		if ( mID == "exode_card_E031_crewPopulation" 		or mID == "population analyst"	or mID == "31" ): 
			return "exode_card_E031_crewPopulation"	
		if ( mID == "exode_card_E032_crewEntertainment" 	or mID == "welfare specialist"	or mID == "32" ): 
			return "exode_card_E032_crewEntertainment"	
		if ( mID == "exode_card_E033_crewMaintenance" 		or mID == "maintenance staff"		or mID == "33" ): 
			return "exode_card_E033_crewMaintenance"	
		if ( mID == "exode_card_E034_crewPilotCivilian" 	or mID == "civilian pilot"		or mID == "34" ): 
			return "exode_card_E034_crewPilotCivilian"	
		if ( mID == "exode_card_E035_crewSecurity" 		or mID == "security guard"		or mID == "35" ): 
			return "exode_card_E035_crewSecurity"	
		if ( mID == "exode_card_E036_setLuxury" 		or mID == "diplomatic gifts"		or mID == "36" ): 
			return "exode_card_E036_setLuxury"	
		if ( mID == "exode_card_E037_setDatabase" 		or mID == "federal database"		or mID == "37" ): 
			return "exode_card_E037_setDatabase"	
			
			
		if ( mID == "exode_card_E046_Rekatron_defensiveAmmo"		or mID == "46" ): 
			return "exode_card_E046_Rekatron_defensiveAmmo"
		if ( mID == "exode_card_E047_Rekatron_firetalkerPistol" 	or mID == "47" ): 
			return "exode_card_E047_Rekatron_firetalkerPistol"
		if ( mID == "exode_card_E048_Rekatron_karperPistol" 		or mID == "48" ): 
			return "exode_card_E048_Rekatron_karperPistol"
		if ( mID == "exode_card_E049_Rekatron_explanatorRifle" 	or mID == "49" ): 
			return "exode_card_E049_Rekatron_explanatorRifle"
		if ( mID == "exode_card_E050_Rekatron_rsdRifle" 		or mID == "50" ): 
			return "exode_card_E050_Rekatron_rsdRifle"
		if ( mID == "exode_card_E051_Rekatron_goodMorningPistol" 	or mID == "51" ): 
			return "exode_card_E051_Rekatron_goodMorningPistol"
		if ( mID == "exode_card_E052_Rekatron_jugdmentDayRifle" 	or mID == "52" ): 
			return "exode_card_E052_Rekatron_jugdmentDayRifle"
		if ( mID == "exode_card_E053_Rekatron_galacticPeacemaker" 	or mID == "53" ): 
			return "exode_card_E053_Rekatron_galacticPeacemaker"
		if ( mID == "exode_card_E054_Rekatron_ammoGuided" 		or mID == "54" ): 
			return "exode_card_E054_Rekatron_ammoGuided"
		if ( mID == "exode_card_E055_Rekatron_ammoParty" 		or mID == "55" ): 
			return "exode_card_E055_Rekatron_ammoParty"
		if ( mID == "exode_card_E056_Tom_SmootyAllInOne" 		or mID == "56" ): 
			return "exode_card_E056_Tom_SmootyAllInOne"
		if ( mID == "exode_card_E057_Tom_FoodieMoodie" 		or mID == "57" ): 
			return "exode_card_E057_Tom_FoodieMoodie"
		if ( mID == "exode_card_E058_Tom_FriendlyEyes" 		or mID == "58" ): 
			return "exode_card_E058_Tom_FriendlyEyes"
		if ( mID == "exode_card_E059_Tom_BuddyPinger" 			or mID == "59" ): 
			return "exode_card_E059_Tom_BuddyPinger"
		if ( mID == "exode_card_E060_Tom_VehicleLittleBuddy" 		or mID == "60" ): 
			return "exode_card_E060_Tom_VehicleLittleBuddy"
		if ( mID == "exode_card_E061_Tom_Custom" 			or mID == "61" ): 
			return "exode_card_E061_Tom_Custom"
		if ( mID == "exode_card_E062_Tom_WHCConverter" 		or mID == "62" ): 
			return "exode_card_E062_Tom_WHCConverter"
		if ( mID == "exode_card_E063_Tom_Explorator" 			or mID == "63" ): 
			return "exode_card_E063_Tom_Explorator"
		if ( mID == "exode_card_E064_Tom_ShelterHappyFive" 		or mID == "64" ): 
			return "exode_card_E064_Tom_ShelterHappyFive"
			
		if ( mID == "exode_card_E066_SyndicateEquipment_Chip" 	or mID == "66" ): 
			return "exode_card_E066_SyndicateEquipment_Chip"
		if ( mID == "exode_card_E067_SyndicateEquipment_DrugHolidays"	or mID == "67" ): 
			return "exode_card_E067_SyndicateEquipment_DrugHolidays"
		if ( mID == "exode_card_E068_SyndicateEquipment_DrugNPrime"	or mID == "68" ): 
			return "exode_card_E068_SyndicateEquipment_DrugNPrime"
		if ( mID == "exode_card_E069_SyndicateShipBlackLotus" 	or mID == "69" ): 
			return "exode_card_E069_SyndicateShipBlackLotus"
		if ( mID == "exode_card_E070_SyndicateEquipmentAutoBlaster"	or mID == "70" ): 
			return "exode_card_E070_SyndicateEquipmentAutoBlaster"
		if ( mID == "exode_card_E071_SyndicateEquipment_NarcoWarfare"	or mID == "71" ): 
			return "exode_card_E071_SyndicateEquipment_NarcoWarfare"
		if ( mID == "exode_card_E072_SyndicateEquipmentSet_Genefactory" or mID == "72" ): 
			return "exode_card_E072_SyndicateEquipmentSet_Genefactory"
		if ( mID == "exode_card_E073_SyndicateHacker" 			or mID == "73" ): 
			return "exode_card_E073_SyndicateHacker"
		if ( mID == "exode_card_E074_SyndicateLeader" 			or mID == "74" ): 
			return "exode_card_E074_SyndicateLeader"
		if ( mID == "exode_card_E075_SyndicateTransactor" 		or mID == "75" ): 
			return "exode_card_E075_SyndicateTransactor"
		if ( mID == "exode_card_E076_SyndicateTrooper" 		or mID == "76" ): 
			return "exode_card_E076_SyndicateTrooper"
		if ( mID == "exode_card_E077_SyndicateAyumi" 			or mID == "77" ): 
			return "exode_card_E077_SyndicateAyumi"
		if ( mID == "exode_card_E078_SyndicateYakuzaNoble" 		or mID == "78" ): 
			return "exode_card_E078_SyndicateYakuzaNoble"
		if ( mID == "exode_card_E079_SyndicateYakuzaSniper" 		or mID == "79" ): 
			return "exode_card_E079_SyndicateYakuzaSniper"
		if ( mID == "exode_card_E080_TheKumicho" 			or mID == "80" ): 
			return "exode_card_E080_TheKumicho"
		if ( mID == "exode_card_E081_RebelGeneral" 			or mID == "81" ): 
			return "exode_card_E081_RebelGeneral"
		if ( mID == "exode_card_E082_AlannaVos" 			or mID == "82" ): 
			return "exode_card_E082_AlannaVos"
		if ( mID == "exode_card_E083_Sh4rken" 				or mID == "83" ): 
			return "exode_card_E083_Sh4rken"
		if ( mID == "exode_card_E084_TheAI" 				or mID == "84" ): 
			return "exode_card_E084_TheAI"
		if ( mID == "exode_card_E085_Apprentice" 			or mID == "85" ): 
			return "exode_card_E085_Apprentice"
		if ( mID == "exode_card_E086_Cranium" 				or mID == "86" ): 
			return "exode_card_E086_Cranium"
		if ( mID == "exode_card_E087_Cryptoeater" 			or mID == "87" ): 
			return "exode_card_E087_Cryptoeater"
		if ( mID == "exode_card_E088_originRepentantPirate" 		or mID == "88" ): 
			return "exode_card_E088_originRepentantPirate"
		if ( mID == "exode_card_E089_shipColombus" 			or mID == "89" ): 
			return "exode_card_E089_shipColombus"
		if ( mID == "exode_card_E090_shipQuantumSupreme"		or mID == "90" ): 
			return "exode_card_E090_shipQuantumSupreme"
		if ( mID == "exode_card_E091_vehicleVelvetStorm" 		or mID == "91" ): 
			return "exode_card_E091_vehicleVelvetStorm"
		if ( mID == "exode_card_E092_vehicleVanguard" 			or mID == "92" ): 
			return "exode_card_E092_vehicleVanguard"
		if ( mID == "exode_card_E093_equipmentSuitArena" 		or mID == "93" ): 
			return "exode_card_E093_equipmentSuitArena"
			
		if ( mID == "exode_card_E101_originSecretAgent" 		or mID == "101" ): 
			return "exode_card_E101_originSecretAgent"
		if ( mID == "exode_card_E102_originStrandedTrader" 		or mID == "102" ): 
			return "exode_card_E102_originStrandedTrader"
		if ( mID == "exode_card_E103_originCruiseShipCaptain" 	or mID == "103" ): 
			return "exode_card_E103_originCruiseShipCaptain"
		if ( mID == "exode_card_E104_shipArkLifesavior" 		or mID == "104" ): 
			return "exode_card_E104_shipArkLifesavior"
		if ( mID == "exode_card_E105_shipCargoKormen" 			or mID == "105" ): 
			return "exode_card_E105_shipCargoKormen"
		if ( mID == "exode_card_E106_shipRhino" 			or mID == "106" ): 
			return "exode_card_E106_shipRhino"
		if ( mID == "exode_card_E107_shipCargoTaurus" 			or mID == "107" ): 
			return "exode_card_E107_shipCargoTaurus"
		if ( mID == "exode_card_E108_shipMyrmidon" 			or mID == "108" ): 
			return "exode_card_E108_shipMyrmidon"
		if ( mID == "exode_card_E109_shipAkhen" 			or mID == "109" ): 
			return "exode_card_E109_shipAkhen"
		if ( mID == "exode_card_E110_shipCoetus" 			or mID == "110" ): 
			return "exode_card_E110_shipCoetus"
		if ( mID == "exode_card_E111_setGeneticianConsole" 		or mID == "111" ): 
			return "exode_card_E111_setGeneticianConsole"
		if ( mID == "exode_card_E112_setMilitaryClassA" 		or mID == "112" ): 
			return "exode_card_E112_setMilitaryClassA"
		if ( mID == "exode_card_E113_setEisenSuits" 			or mID == "113" ): 
			return "exode_card_E113_setEisenSuits"
		if ( mID == "exode_card_E114_vehicleAcheanRacer" 		or mID == "114" ): 
			return "exode_card_E114_vehicleAcheanRacer"
		if ( mID == "exode_card_E115_crewSpaceMarshal"			or mID == "115" ): 
			return "exode_card_E115_crewSpaceMarshal"
		if ( mID == "exode_card_E116_officerEliza" 			or mID == "116" ): 
			return "exode_card_E116_officerEliza"
		if ( mID == "exode_card_E117_crewOksana" 			or mID == "117" ): 
			return "exode_card_E117_crewOksana"
		if ( mID == "exode_card_E118_officerNorah" 			or mID == "118" ): 
			return "exode_card_E118_officerNorah"
		if ( mID == "exode_card_E119_officerShen" 			or mID == "119" ): 
			return "exode_card_E119_officerShen"
		if ( mID == "exode_card_E120_officerStug" 			or mID == "120" ): 
			return "exode_card_E120_officerStug"
		if ( mID == "exode_card_E121_crewTyron" 			or mID == "121" ): 
			return "exode_card_E121_crewTyron"
		if ( mID == "exode_card_E122_officerAdmiralValro" 		or mID == "122" ): 
			return "exode_card_E122_officerAdmiralValro"
		if ( mID == "exode_card_E123_officerNash" 			or mID == "123" ): 
			return "exode_card_E123_officerNash"
		if ( mID == "exode_card_E124_crewSpecialInfiltrationAgent" 	or mID == "124" ): 
			return "exode_card_E124_crewSpecialInfiltrationAgent"
		if ( mID == "exode_card_E125_crewScarletSarah" 		or mID == "125" ): 
			return "exode_card_E125_crewScarletSarah"
		if ( mID == "exode_card_E126_passengerNuclearFamily" 		or mID == "126" ): 
			return "exode_card_E126_passengerNuclearFamily"
		if ( mID == "exode_card_E127_installationOctohome" 		or mID == "127" ): 
			return "exode_card_E127_installationOctohome"
		if ( mID == "exode_card_E128_installationOrbitalShield" 	or mID == "128" ): 
			return "exode_card_E128_installationOrbitalShield"
		if ( mID == "exode_card_E129_installationDreamsphere" 	or mID == "129" ): 
			return "exode_card_E129_installationDreamsphere"
		if ( mID == "exode_card_E130_installationGenerator100"	or mID == "130" ): 
			return "exode_card_E130_installationGenerator100"
		if ( mID == "exode_card_E131_equipmentFactionCorporate" 	or mID == "131" ): 
			return "exode_card_E131_equipmentFactionCorporate"
		if ( mID == "exode_card_E132_equipmentSuitRacer" 		or mID == "132" ): 
			return "exode_card_E132_equipmentSuitRacer"
		if ( mID == "exode_card_E133_equipmentSuitSpartan" 		or mID == "133" ): 
			return "exode_card_E133_equipmentSuitSpartan"
		if ( mID == "exode_card_E134_equipmentFactionRebellion" 	or mID == "134" ): 
			return "exode_card_E134_equipmentFactionRebellion"
		if ( mID == "exode_card_E135_escortSabre" 			or mID == "135" ): 
			return "exode_card_E135_escortSabre"
		if ( mID == "exode_card_E136_crewFleshCultLeader" 		or mID == "136" ): 
			return "exode_card_E136_crewFleshCultLeader"
		if ( mID == "exode_card_E137_installationDefensiveBunker" 	or mID == "137" ): 
			return "exode_card_E137_installationDefensiveBunker"
			
		if ( mID == "exode_card_E151_officerDrachianColonel" 		or mID == "151" ): 
			return "exode_card_E151_officerDrachianColonel"
		if ( mID == "exode_card_E152_crewNomadNavigator" 		or mID == "152" ): 
			return "exode_card_E152_crewNomadNavigator"
		if ( mID == "exode_card_E153_crewGeneticianScientist" 	or mID == "153" ): 
			return "exode_card_E153_crewGeneticianScientist"
		if ( mID == "exode_card_E154_crewSuntekSurvivor" 		or mID == "154" ): 
			return "exode_card_E154_crewSuntekSurvivor"
		if ( mID == "exode_card_E155_crewKilbot" 			or mID == "155" ): 
			return "exode_card_E155_crewKilbot"
		if ( mID == "exode_card_E156_crewGalvin" 			or mID == "156" ): 
			return "exode_card_E156_crewGalvin"
		if ( mID == "exode_card_E157_escortVega" 			or mID == "157" ): 
			return "exode_card_E157_escortVega"
		if ( mID == "exode_card_E158_escortIonguards" 			or mID == "158" ): 
			return "exode_card_E158_escortIonguards"
		if ( mID == "exode_card_E159_suntekSphere" 			or mID == "159" ): 
			return "exode_card_E159_suntekSphere"
			
			
		if ( mID == "exode_card_E181_escortLongswords" 		or mID == "181" ): 
			return "exode_card_E181_escortLongswords"
		if ( mID == "exode_card_E182_escortCruiserTaskForce" 		or mID == "182" ): 
			return "exode_card_E182_escortCruiserTaskForce"
		if ( mID == "exode_card_E183_escortStarsystemGarrison" 	or mID == "183" ): 
			return "exode_card_E183_escortStarsystemGarrison"
		if ( mID == "exode_card_E184_shipBaldie" 			or mID == "184" ): 
			return "exode_card_E184_shipBaldie"
		if ( mID == "exode_card_E185_shipClaymoreHyperfighter" 	or mID == "185" ): 
			return "exode_card_E185_shipClaymoreHyperfighter"
		if ( mID == "exode_card_E186_shipDrachianMantis" 		or mID == "186" ): 
			return "exode_card_E186_shipDrachianMantis"
		if ( mID == "exode_card_E187_vehicleSalazar" 			or mID == "187" ): 
			return "exode_card_E187_vehicleSalazar"
		if ( mID == "exode_card_E188_vehicleTraveler2" 		or mID == "188" ): 
			return "exode_card_E188_vehicleTraveler2"
		if ( mID == "exode_card_E189_vehicleSupplyDropship" 		or mID == "189" ): 
			return "exode_card_E189_vehicleSupplyDropship"
		if ( mID == "exode_card_E190_vehicleExplorationDropship" 	or mID == "190" ): 
			return "exode_card_E190_vehicleExplorationDropship"
		if ( mID == "exode_card_E191_vehicleZandratti" 		or mID == "191" ): 
			return "exode_card_E191_vehicleZandratti"
		if ( mID == "exode_card_E192_vehicleSecurityDrone" 		or mID == "192" ): 
			return "exode_card_E192_vehicleSecurityDrone"
		if ( mID == "exode_card_E193_vehiclePantherBike" 		or mID == "193" ): 
			return "exode_card_E193_vehiclePantherBike"
			
		if ( mID == "exode_card_E201_setMedicalBay" 			or mID == "201" ): 
			return "exode_card_E201_setMedicalBay"
		if ( mID == "exode_card_E202_equipmentRoboticParts" 		or mID == "202" ): 
			return "exode_card_E202_equipmentRoboticParts"
		if ( mID == "exode_card_E203_equipmentEnergyCells" 		or mID == "203" ): 
			return "exode_card_E203_equipmentEnergyCells"
		if ( mID == "exode_card_E204_equipmentShipConstructionParts"	or mID == "204" ): 
			return "exode_card_E204_equipmentShipConstructionParts"
		if ( mID == "exode_card_E205_equipmentUniversalFixer" 	or mID == "205" ): 
			return "exode_card_E205_equipmentUniversalFixer"
		if ( mID == "exode_card_E206_equipmentLonestar" 		or mID == "206" ): 
			return "exode_card_E206_equipmentLonestar"
		if ( mID == "exode_card_E207_equipmentChipsAndData" 		or mID == "207" ): 
			return "exode_card_E207_equipmentChipsAndData"
		if ( mID == "exode_card_E208_equipmentCorporate" 		or mID == "208" ): 
			return "exode_card_E208_equipmentCorporate"
		if ( mID == "exode_card_E209_equipmentEisenSuit" 		or mID == "209" ): 
			return "exode_card_E209_equipmentEisenSuit"
		if ( mID == "exode_card_E210_equipmentDrachianSuit" 		or mID == "210" ): 
			return "exode_card_E210_equipmentDrachianSuit"
		if ( mID == "exode_card_E211_equipmentMilitarySuit" 		or mID == "211" ): 
			return "exode_card_E211_equipmentMilitarySuit"
		if ( mID == "exode_card_E212_equipmentPlanetscan" 		or mID == "212" ): 
			return "exode_card_E212_equipmentPlanetscan"
		if ( mID == "exode_card_E213_equipmentRimscan" 		or mID == "213" ): 
			return "exode_card_E213_equipmentRimscan"
		if ( mID == "exode_card_E214_equipmentDesigner" 		or mID == "214" ): 
			return "exode_card_E214_equipmentDesigner"
		if ( mID == "exode_card_E215_equipmentIdentificationMatrix" 	or mID == "215" ): 
			return "exode_card_E215_equipmentIdentificationMatrix"
			
		if ( mID == "exode_card_E221_crewDrachianCommissar" 		or mID == "221" ): 
			return "exode_card_E221_crewDrachianCommissar"
		if ( mID == "exode_card_E222_crewFederalAgent" 		or mID == "222" ): 
			return "exode_card_E222_crewFederalAgent"
		if ( mID == "exode_card_E223_crewCorporateBodyguard" 		or mID == "223" ): 
			return "exode_card_E223_crewCorporateBodyguard"
		if ( mID == "exode_card_E224_crewFederalMarine" 		or mID == "224" ): 
			return "exode_card_E224_crewFederalMarine"
		if ( mID == "exode_card_E225_crewFederalPolice" 		or mID == "225" ): 
			return "exode_card_E225_crewFederalPolice"
		if ( mID == "exode_card_E226_crewDrachianTrooper" 		or mID == "226" ): 
			return "exode_card_E226_crewDrachianTrooper"
		if ( mID == "exode_card_E227_crewCorneredRebelAgent" 		or mID == "227" ): 
			return "exode_card_E227_crewCorneredRebelAgent"
		if ( mID == "exode_card_E228_passengerDangerous" 		or mID == "228" ): 
			return "exode_card_E228_passengerDangerous"
		if ( mID == "exode_card_E229_passengerUnstable" 		or mID == "229" ): 
			return "exode_card_E229_passengerUnstable"
		if ( mID == "exode_card_E230_crewMaintenanceDroid" 		or mID == "230" ): 
			return "exode_card_E230_crewMaintenanceDroid"
		if ( mID == "exode_card_E231_passengerScienceStudent" 	or mID == "231" ): 
			return "exode_card_E231_passengerScienceStudent"
		if ( mID == "exode_card_E232_passengerSocialite" 		or mID == "232" ): 
			return "exode_card_E232_passengerSocialite"
		if ( mID == "exode_card_E233_passengerTechExpert" 		or mID == "233" ): 
			return "exode_card_E233_passengerTechExpert"
			
		if ( mID == "exode_card_E235_crewTriskan" 			or mID == "235" ): 
			return "exode_card_E235_crewTriskan"
		if ( mID == "exode_card_E236_crewFleshCult"			or mID == "236" ): 
			return "exode_card_E236_crewFleshCult"
		if ( mID == "exode_card_E237_crewFleshCultScientist" 		or mID == "237" ): 
			return "exode_card_E237_crewFleshCultScientist"
			
		if ( mID == "exode_card_E241_installationDrillingMachine" 	or mID == "drill"			or mID == "drilling machine"			or mID == "241" ): 
			return "exode_card_E241_installationDrillingMachine"
		if ( mID == "exode_card_E242_installationRadarArray" 		or mID == "242" ): 
			return "exode_card_E242_installationRadarArray"
		if ( mID == "exode_card_E243_installationGenerator20" 	or mID == "243" ): 
			return "exode_card_E243_installationGenerator20"
		if ( mID == "exode_card_E244_installationTomStarter" 		or mID == "244" ): 
			return "exode_card_E244_installationTomStarter"
		if ( mID == "exode_card_E245_installationLiveBlock" 		or mID == "245" ): 
			return "exode_card_E245_installationLiveBlock"
		if ( mID == "exode_card_E246_installationBiodomes" 		or mID == "246" ): 
			return "exode_card_E246_installationBiodomes"
		if ( mID == "exode_card_E247_installationTurret" 		or mID == "247" ): 
			return "exode_card_E247_installationTurret"
		if ( mID == "exode_card_E248_layoutProtectionWalls" 		or mID == "248" ): 
			return "exode_card_E248_layoutProtectionWalls"
		if ( mID == "exode_card_E249_layoutUnderground" 		or mID == "249" ): 
			return "exode_card_E249_layoutUnderground"
		if ( mID == "exode_card_E250_interiorLabEquipment" 		or mID == "250" ): 
			return "exode_card_E250_interiorLabEquipment"
		if ( mID == "exode_card_E251_interiorManagementConsole" 	or mID == "251" ): 
			return "exode_card_E251_interiorManagementConsole"
		if ( mID == "exode_card_E252_interiorComputerRoom" 		or mID == "252" ): 
			return "exode_card_E252_interiorComputerRoom"
		if ( mID == "exode_card_E253_installationMultipurpose" 	or mID == "253" ): 
			return "exode_card_E253_installationMultipurpose"
		if ( mID == "exode_card_E254_installationCommunicationArray"	or mID == "254" ): 
			return "exode_card_E254_installationCommunicationArray"
		if ( mID == "exode_card_E255_interiorCuves" 			or mID == "255" ): 
			return "exode_card_E255_interiorCuves"
		if ( mID == "exode_card_E256_installationPreservationDome"	or mID == "256" ): 
			return "exode_card_E256_installationPreservationDome"
		if ( mID == "exode_card_E257_installationStorage" 		or mID == "257" ): 
			return "exode_card_E257_installationStorage"
		if ( mID == "exode_card_E258_equipmentTomEssentialsHappyFood"	or mID == "258" ): 
			return "exode_card_E258_equipmentTomEssentialsHappyFood"
		if ( mID == "exode_card_E259_equipmentTomEssentialsHappyAir"	or mID == "259" ): 
			return "exode_card_E259_equipmentTomEssentialsHappyAir"
		if ( mID == "exode_card_E260_equipmentTomEssentialsSurvivor"	or mID == "260" ): 
			return "exode_card_E260_equipmentTomEssentialsSurvivor"
		if ( mID == "exode_card_E261_actionImmediateOrder"		or mID == "261" ): 
			return "exode_card_E261_actionImmediateOrder"
		return ""
		
def db_Pack_GetDetails( pack_id ):

	cursor = myDB.db_Cursor()
	
	query = ("SELECT SUM(opened), SUM(nb) FROM exode_pack "
			 "WHERE type = %s and player != %s and player != %s" )	
		
	cursor.execute(query, (pack_id,"elindos","exolindos"))
	m_output = cursor.fetchall()
	
	
	tOpened = 0
	tExist  = 0
	
	if ( m_output[0][0] != None ):
			
		tOpened = int(m_output[0][0])
		tExist  = int(m_output[0][1])
	
	output = { 'nb': tExist, 'open': tOpened }
			
	cursor.reset()
	cursor.close()
	
	return output
		
def db_Pack_GetOwners( mID, mVar, mMax ):

	cursor = myDB.db_Cursor()
	
	if ( mVar == "nb" ):	
		query = ("SELECT player, nb, opened FROM exode_pack "
			 "WHERE type = %s and nb > 0 and player != %s ORDER BY nb DESC LIMIT %s" )	
	else:
		query = ("SELECT player, nb, opened FROM exode_pack "
			 "WHERE type = %s and opened > 0 and player != %s ORDER BY opened DESC LIMIT %s" )	
		
	cursor.execute(query, (mID,"elindos",mMax))
	m_output = cursor.fetchall()
	
	tPack_owners = []
	tPack_nbs    = []
	tPack_open   = []
	tPacks = 0
		
	if ( cursor.rowcount != 0 ):	
	
		tPacks = int(cursor.rowcount)
		for iRow in range( tPacks ):
		
			tPack_owners.append( m_output[iRow][0] )
			tPack_nbs.append( m_output[iRow][1] - m_output[iRow][2] )
			tPack_open.append( m_output[iRow][2] )
			
	cursor.reset()
	
	
	if ( mVar == "nb" ):	
		query = ("SELECT player FROM exode_pack "
			 "WHERE type = %s and nb > 0 and player != %s" )	
	else:
		query = ("SELECT player FROM exode_pack "
			 "WHERE type = %s and opened > 0 and player != %s" )	
	
		
	cursor.execute(query, (mID,"elindos"))
	m_output = cursor.fetchall()
	
	tPacks_n = cursor.rowcount
		
	cursor.reset()	 
	cursor.close()
	
	return (tPacks, tPack_owners, tPack_nbs, tPack_open, tPacks_n)
	
def db_Card_GetDetails( card_uid ):

	cursor = myDB.db_Cursor()
	
	query = ("SELECT owner, type, mint_num, elite, burn, block_update FROM exode_cards "
			 "WHERE uid = %s" )	
		
	cursor.execute(query, (card_uid, ))
	m_output = cursor.fetchall()
	
	if ( cursor.rowcount != 0 ):	
		card_exist = True
		card_owner = m_output[0][0]
		card_id    = m_output[0][1]
		card_mint  = int(m_output[0][2])
		card_elite = int(m_output[0][3])
		card_burn  = int(m_output[0][4])
		card_block = int(m_output[0][5])
	else:
		card_exist = False
		card_owner = ""
		card_id    = ""
		card_mint  = -1
		card_elite = 0	
		card_burn  = 0
		card_block = 0
	
	output = { 'exist': card_exist, 'owner': card_owner, 'id': card_id, 'mint': card_mint, 'elite': card_elite, 'burn': card_burn, 'block': card_block }
			
	cursor.reset()
	cursor.close()
	
	return output
	
def db_Card_GetNMintTot( card_id, card_elite ):

	cursor = myDB.db_Cursor()
	
	query = ("SELECT COUNT(*) FROM exode_cards "
		 "WHERE type = %s AND elite = %s AND mint_num != -1")	
		
	cursor.execute(query, (card_id, card_elite))
	m_output = cursor.fetchall()
	
	card_ntot_mint  = int(m_output[0][0])
	
	cursor.reset()
	cursor.close()
	
	return card_ntot_mint
	
#########################################################################################

def db_Sale_GetInfo(mID=""): 

	if ( mID == "" ):
		return (-1.0, -1.0, 0, [], [])
		
	cursor = myDB.db_Cursor()
	
	query = ("SELECT price, block_update, time_update from exode_sales "
		"WHERE asset_type = %s and sold = %s and price != 0. ORDER BY block_update")  
	 
	cursor.execute(query, (mID,1) )
	m_out = cursor.fetchall()
	
	tSale_times  = []
	tSale_prices = []
	tSale_lastB  = 0
	tSale_lastP  = -1.0
	tSale_avgP   = -1.0
	tSales       = 0
	
	if ( cursor.rowcount != 0 ):
	
		tSale_avgP = 0.0
		tSales = int(cursor.rowcount)
		for iRow in range( tSales ):
			
			tPrice = float(m_out[iRow][0])
			tBlock  = int(m_out[iRow][1])
			tTime  = m_out[iRow][2]
		
			tSale_prices.append( tPrice )
			tSale_times.append( tTime )
			
			if ( tBlock > tSale_lastB ):
				tSale_lastB = tBlock
				tSale_lastP = tPrice
			
			tSale_avgP = tSale_avgP + tPrice / float(tSales)
			
	
		
		
	cursor.reset()
	cursor.close()
	
	return (tSale_avgP, tSale_lastP, tSales, tSale_times, tSale_prices)

def db_Card_Owners(mID, mMax):

	cursor = myDB.db_Cursor()
	
	query = ("SELECT owner, COUNT(*) as co_cards FROM exode_cards "
			 "WHERE type = %s and burn = 0 and mint_num > 0 GROUP BY owner ORDER BY co_cards DESC LIMIT %s" )	
		
	cursor.execute(query, (mID,mMax))
	m_output = cursor.fetchall()
	
	tCard_owners = []
	tCard_nbs    = []
	tCards = 0
	
	if ( cursor.rowcount != 0 ):	
	
		tCards = int(cursor.rowcount)
		for iRow in range( tCards ):
		
			tCard_owners.append( m_output[iRow][0] )
			tCard_nbs.append( m_output[iRow][1] )
			
	cursor.reset()
	
	
	query = ("SELECT owner FROM exode_cards "
			 "WHERE type = %s and burn = 0 and mint_num > 0 GROUP BY owner" )	
		
	cursor.execute(query, (mID,))
	m_output = cursor.fetchall()
	
	tOwners = cursor.rowcount
		
	cursor.reset()	 
	cursor.close()
	
	return (tCards, tCard_owners, tCard_nbs, tOwners)
	
def db_Card_Owners_Mint(mID, mMax):
		
	cursor = myDB.db_Cursor()		
	
	query = ("SELECT owner, mint_num as co_cards FROM exode_cards "
			 "WHERE type = %s and burn = 0 and mint_num > 0 ORDER BY mint_num LIMIT %s" )	
		
	cursor.execute(query, (mID,mMax))
	m_output = cursor.fetchall()
	
	tCard_owners = []
	tCard_mints  = []
	tCards = 0
	
	if ( cursor.rowcount != 0 ):	
	
		tCards = int(cursor.rowcount)
		for iRow in range( tCards ):
		
			tCard_owners.append( m_output[iRow][0] )
			tCard_mints.append( m_output[iRow][1] )
	
	
	query = ("SELECT owner FROM exode_cards "
			 "WHERE type = %s and burn = 0 and mint_num > 0 ORDER BY mint_num" )	
		
	cursor.execute(query, (mID,))
	m_output = cursor.fetchall()
	
	tCards_all = cursor.rowcount
			
		
	cursor.reset()	 
	cursor.close()
	
	return (tCards, tCard_owners, tCard_mints, tCards_all)

	
def db_TransferTX_Last():

	cursor = myDB.db_Cursor()	
	
	query = ("SELECT MAX(block_update) FROM exode_sales")
		
	cursor.execute(query)
	m_out = cursor.fetchall()
		
	if ( m_out[0][0] != None ):
		m_out_sale = int(m_out[0][0])
	else: 
		m_out_sale = 0
		
	cursor.reset()
	
	query = ("SELECT MAX(block_update) FROM exode_cards WHERE block != block_update")
		
	cursor.execute(query)
	m_out = cursor.fetchall()
		
	if ( m_out[0][0] != None ):
		m_out_card = int(m_out[0][0])
	else: 
		m_out_card = 0
		
	cursor.close()
	
	return max(m_out_sale,m_out_card)
	
def db_TransferTX_LastTX():

	cursor = myDB.db_Cursor()	
	
	query = ("SELECT MAX(block) FROM exode_tx")
		
	cursor.execute(query)
	m_out = cursor.fetchall()
		
	if ( m_out[0][0] != None ):
		m_out_block = int(m_out[0][0])
	else: 
		m_out_block = 0
		
	cursor.reset()		
	cursor.close()
	
	return m_out_block
	
def db_TransferTX_Remain(mBlock):

	cursor = myDB.db_Cursor()	
	
	query = ("SELECT tx_block FROM exode_tx_transfer WHERE tx_block > %s")
		
	cursor.execute(query,(mBlock,))
	cursor.fetchall()
	
	m_out = cursor.rowcount
		
	cursor.reset()		
	cursor.close()
	
	return m_out

def ArgToID(iArg, arg):

	tID = ""
	tElite = 0	
	iArgN = len(arg)
	
	if ( iArg >= iArgN ):
		return (tID, tElite)
	
	if ( arg[iArg].lower() == "elite" or arg[iArg].lower() == "e" ):
		iArg = iArg + 1
		tElite = 1
		
	if ( iArg >= iArgN ):
		return (tID, tElite)
		
	if ( arg[iArg][0:12] == "exode_card_E" ):
		tElite = 1
		
	sName = arg[iArg]
	iArg = iArg + 1
	
	if ( iArg < iArgN ):
		for i in range(iArg,iArgN):
			sName = sName + " " + arg[i] 
			
	tID = ex_GetAssetID( sName, tElite )
	
	return (tID, tElite)

##############################################################################################
	
DISC_BOT = commands.Bot(command_prefix="$")	

##############################################################################################

@DISC_BOT.event
async def on_ready():
	print('Discord bot ready')
    
	for discord_guild in DISC_BOT.guilds:
		DISC_CHANNEL = discord.utils.get(discord_guild.channels, name=excst.CHANNEL_ANALYSE_NAME)
		if ( DISC_CHANNEL != None ):
			print ( "DISCORD BOT:eXode bot [MARKET-ANALYSER] connected to {guild_name}".format(guild_name=discord_guild.name) )
			await DISC_CHANNEL.send("*eXode BOT [MARKET-ANALYSER] is connected here!*")    
    
@DISC_BOT.event
async def on_message(message):
	if message.channel.name == excst.CHANNEL_ANALYSE_NAME:
		await DISC_BOT.process_commands(message)
##############################################################################################

@DISC_BOT.command(
#	help="Display the average sold price and the last sold price of the requested asset.\n Usage: $sales [elite] <asset id or asset name or card num>",
#	brief="Display the average and last sold prices"
	help="Disabled",
	brief="Disable"
)
async def sales(ctx, *arg):

	print ("sales", arg)
	
	(tID, tElite) = ArgToID(0, arg)	
	if ( tID == "" ):
		return

	(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails( tID )
	(tSale_avgP, tSale_lastP, tSales, tSale_times, tSale_prices) = db_Sale_GetInfo( tID )
	
	msg_elite = ""
	if ( tElite == 1 ):
		msg_elite = "Elite "
	
	msg = " **{elite}{name}** ({asset_id}) was sold {nSales} times for an average price of **${price_avg}**, the last was sold at **${price_last}** ".format(elite=msg_elite,name=asset_name,nSales=tSales,price_avg=tSale_avgP,price_last=tSale_lastP,asset_id=tID)
	

	await ctx.channel.send(msg)
	
	
@DISC_BOT.command(
#	help="Display a graph showing the last sales of the requested asset. \n Usage: $graphsales [all/year/month/week] [elite] <asset id or asset name or card num>",
#	brief="Display a graph showing the last sales"
	help="Disabled",
	brief="Disable"
)
async def graphsales(ctx, *arg):

	print ("graphsales", arg)
	if ( len(arg) == 0 ):
		return

	iArg = 0
	sTime = "all"
	tTimeCut = ""
	
	tElite = 0	
	if ( arg[iArg].lower() == "all" ):
		iArg = iArg + 1
		tTimeCut = ""		
	elif ( arg[iArg].lower() == "year" or arg[iArg].lower() == "month" or arg[iArg].lower() == "week" ):
		sTime = arg[iArg].lower()
		iArg = iArg + 1
		
		iDay = 0
		
		if ( sTime == "year" ):
			iDay = 365
		if ( sTime == "month" ):
			iDay = 30
		if ( sTime == "week" ):
			iDay = 7			
		
		ts = datetime.now()
		td = timedelta(days=iDay)
		
		
		tTimeFirst = ts - td
		tTimeLast  = ts
		
		tTimeCut = (ts - td).isoformat()
		
		
		
		
	
	(tID, tElite) = ArgToID(iArg, arg)	
	if ( tID == "" ):
		return
		
	(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails( tID )
	(tSale_avgP, tSale_lastP, tSales, tSale_times, tSale_prices) = db_Sale_GetInfo( tID )
	
	msg_elite = ""
	if ( tElite == 1 ):
		msg_elite = "Elite "
	
	print("mysql completed")	
	
	tMaxPrice = 0.
	
	for iSale in range(len(tSale_prices)):
		if ( tSale_prices[iSale] > tMaxPrice ):
			tMaxPrice = tSale_prices[iSale]
			
	print ("max price: ", tMaxPrice)
		
	tSale_dates = pltdates.date2num(tSale_times)
	
	fig, ax = plt.subplots()
		
	plt.plot_date(tSale_dates, tSale_prices, color='green', linestyle='dashed', linewidth = 3,
			marker='o', markerfacecolor='blue', markersize=12)
	plt.xlabel('Time')
	plt.ylabel('Price')
	plt.title("{asset_id} sales: {period}".format(asset_id=tID, period=sTime))
	plt.gcf().autofmt_xdate()
	plt.grid(True)
	plt.ylim(bottom=0.0, top=tMaxPrice*1.1)
	
	if ( tTimeCut != "" ):
		ax.set_xlim([tTimeFirst, tTimeLast])

	#plt.show()
	nRnd = random.randint(0,1000000)
	plt.savefig("./plot_{asset_id}_{rnd}.png".format(asset_id=tID,rnd=nRnd))
	plt.clf()
		

	
	if ( sTime != "all" ):
		msg = " **{elite}{name}** ({asset_id}) sales during last {period} period were: ".format(elite=msg_elite,name=asset_name,period=sTime,asset_id=tID)
	else:
		msg = " **{elite}{name}** ({asset_id}) sales since the beginning of eXode were: ".format(elite=msg_elite,name=asset_name,period=sTime,asset_id=tID)

	await ctx.channel.send(msg,file=discord.File("./plot_{asset_id}_{rnd}.png".format(asset_id=tID,rnd=nRnd)))
	
	os.remove("./plot_{asset_id}_{rnd}.png".format(asset_id=tID,rnd=nRnd))


@DISC_BOT.command(
#	help="Display up to 10 players owning the requested card. \n Usage: $owners [elite] <card id or number>",
#	brief="Display a list of 10 players owning the card."
	help="Disabled",
	brief="Disable"
)
async def owners(ctx, *arg):

	print ("owners", arg)
	iArgN = len(arg)
	if ( iArgN == 0 ):
		return

	iArg = 0
	sTime = "all"
	
	tElite = 0	
	
	(tID, tElite) = ArgToID(0, arg)	
	if ( tID == "" ):
		return
	(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails( tID )
		
	if ( is_pack ):
		return
		
	mMax = 10
	(tCards, tCard_Owner, tCard_Num, tOwners) = db_Card_Owners( tID, mMax )
		
	msg_elite = ""
	if ( tElite == 1 ):
		msg_elite = "Elite "
	
	
	msg = " **{elite}{name}** ({asset_id}) owners are: \n".format(elite=msg_elite,name=asset_name,asset_id=tID)
	if ( tCards > 0 ):
		for i in range(tCards):
			msg = msg + " - **{owner}** who owns {card_count} cards \n".format(owner=tCard_Owner[i],card_count=tCard_Num[i])
		if ( tOwners > mMax ):
			msg = msg + " ... and {own_num} others".format(own_num=(tOwners-mMax))
	
	

	await ctx.channel.send(msg)


@DISC_BOT.command(
	help="Display up who owns mint up to 10 for the requested card. \n Usage: $owners_topmint [elite] <card id or number>",
	brief="Display the list of owners for the top 10 mints."
)
async def owners_topmint(ctx, *arg):

	print ("owners_topmint", arg)
	iArgN = len(arg)
	if ( iArgN == 0 ):
		return

	iArg = 0
	
	tElite = 0	
	
	(tID, tElite) = ArgToID(0, arg)	
	if ( tID == "" ):
		return
	(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails( tID )
		
	if ( is_pack ):
		return
		
	mMax = 10
	(tCards, tCard_Owner, tCard_Mint, tOwners) = db_Card_Owners_Mint( tID, mMax )
		
	msg_elite = ""
	if ( tElite == 1 ):
		msg_elite = "Elite "
	
	
	msg = " **{elite}{name}** ({asset_id}) owners are: \n".format(elite=msg_elite,name=asset_name,asset_id=tID)
	if ( tCards > 0 ):
		for i in range(tCards):
			msg = msg + " - #**{mint_num}** is owned by **{owner}** \n".format(owner=tCard_Owner[i],mint_num=tCard_Mint[i])
		if ( tOwners > mMax ):
			msg = msg + " ... and **{card_num}** others".format(card_num=(tOwners-mMax))
	
	

	await ctx.channel.send(msg)


@DISC_BOT.command(
	help="Display info about a specific card. \n Usage: $card_details <card uid>",
	brief="Display info about a specific card."
)
async def card_details(ctx, *arg):

	print ("card_details", arg)
	iArgN = len(arg)
	if ( iArgN != 1 ):
		return

	tUID = arg[0]
	
	cInfo = db_Card_GetDetails( tUID )
	
	if ( not cInfo['exist' ] ):
		msg = "Unknown uid"
	else:
		tMintTot = db_Card_GetNMintTot( cInfo['id'], cInfo['elite'] )		
		(is_pack, card_name, card_rank, card_num) = ex_GetAssetDetails(cInfo['id'])
		
		card_rank_name = "Common"
		if ( card_rank == 1 ):
			card_rank_name = "Rare"
		if ( card_rank == 2 ):
			card_rank_name = "Epic"
		if ( card_rank == 3 ):
			card_rank_name = "Legendary"
		
		msg_elite = "a **"
		if ( cInfo['elite'] == 1 ):
			msg_elite = "an **Elite "
			
		msg = "*{uid}* is a {elite}{name}** [*{rank}*], owned by **{player}** with mint **{mint}**/{mint_tot}".format(uid=tUID, elite=msg_elite, player=cInfo['owner'],name=card_name, rank=card_rank_name, mint=cInfo['mint'], mint_tot=tMintTot)

	await ctx.channel.send(msg)



@DISC_BOT.command(
	help="Display info about a pack. \n Usage: $pack_details <pack id or name>",
	brief="Display info about a pack."
)
async def pack_details(ctx, *arg):

	print ("pack_details", arg)
	iArgN = len(arg)
	if ( iArgN == 0 ):
		return


	(tID, tElite) = ArgToID(0, arg)	
	if ( tID == "" ):
		return
	(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails( tID )
		
	if ( not is_pack ):
		return
	
	cInfo = db_Pack_GetDetails( tID )
		
	msg = "**{name}** ({asset_id}) was distributed **{num}** times and opened **{num_o}** times, **{num_l}** are left\n".format(name=asset_name,asset_id=tID, num=(cInfo['nb']+cInfo['open']), num_o=cInfo['open'], num_l=cInfo['nb'])
	msg = msg + "**[Note]** distributed pack number is incorrect"
	await ctx.channel.send(msg)


@DISC_BOT.command(
#	help="Display list of owners for a pack. \n Usage: $pack_owners <pack id or name>",
#	brief="Display list of owners for a pack."
	help="Disabled",
	brief="Disable"
)
async def pack_owners(ctx, *arg):

	print ("pack_details", arg)
	iArgN = len(arg)
	if ( iArgN == 0 ):
		return


	(tID, tElite) = ArgToID(0, arg)	
	if ( tID == "" ):
		return
	(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails( tID )
		
	if ( not is_pack ):
		return
	
	mMax = 10
	(tPacks, tPack_owners, tPack_nbs, tPack_open, tPacks_n) = db_Pack_GetOwners( tID, "nb", mMax )
		
	msg = "**{name}** ({asset_id}) owners are: \n".format(name=asset_name,asset_id=tID)
	if ( tPacks > 0 ):
		for i in range(tPacks):
			msg = msg + " - **{owner}** owns {pack_n} packs and opened {pack_no} packs\n".format(owner=tPack_owners[i],pack_n=tPack_nbs[i],pack_no=tPack_open[i])
		if ( tPacks_n > mMax ):
			msg = msg + " ... and **{pack_num}** others\n".format(pack_num=(tPacks_n-mMax))
		msg = msg + "**[Note]** distributed pack number is incorrect"
	else:
		msg = "**{name}** ({asset_id}) was never distributed \n".format(name=asset_name,asset_id=tID)
		msg = msg + "**[Note]** distributed pack number is incorrect"
		
	await ctx.channel.send(msg)
	
@DISC_BOT.command(
	help="Display list of openers for a pack. \n Usage: $pack_open <pack id or name>",
	brief="Display list of openers for a pack."
)
async def pack_open(ctx, *arg):

	print ("pack_open", arg)
	iArgN = len(arg)
	if ( iArgN == 0 ):
		return


	(tID, tElite) = ArgToID(0, arg)	
	if ( tID == "" ):
		return
	(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails( tID )
		
	if ( not is_pack ):
		return
	
	mMax = 10
	(tPacks, tPack_owners, tPack_nbs, tPack_open, tPacks_n) = db_Pack_GetOwners( tID, "opened", mMax )
		
	
	
	msg = "**{name}** ({asset_id}) top 'openers' are: \n".format(name=asset_name,asset_id=tID)
	if ( tPacks > 0 ):
		for i in range(tPacks):
			msg = msg + " - **{owner}** opened {pack_no} packs\n".format(owner=tPack_owners[i],pack_no=tPack_open[i])
		if ( tPacks_n > mMax ):
			msg = msg + " ... and **{pack_num}** others\n".format(pack_num=(tPacks_n-mMax))
		msg = msg + "**[Note]** distributed pack number is incorrect"
	else:
		msg = "**{name}** ({asset_id}) was never opened \n".format(name=asset_name,asset_id=tID)
		msg = msg + "**[Note]** distributed pack number is incorrect"
		
	await ctx.channel.send(msg)
	
	
@DISC_BOT.command(
	help="Display the status of the database. \n Usage: $database_status",
	brief="Display the status of the database."
)
async def database_status(ctx):

	print ("database_status")
	m_last_block = 0
	m_last_tx_block = 0
	m_remains = 0
	
	m_last_block = db_TransferTX_Last()
	m_last_tx_block = db_TransferTX_LastTX()
	m_remains = db_TransferTX_Remain(m_last_block)
	
	print ( m_last_block, m_last_tx_block, m_remains )
	
	msg = "The sale and ownership database is build up to block **{block_last}** / **{block_real}**, still **{tx_rem}** transactions to process".format(block_last=m_last_block, block_real=m_last_tx_block, tx_rem=m_remains)		
	await ctx.channel.send(msg)



##############################################################################################

DISC_BOT.run(excst.BOT_TOKEN_ANALYSER)
		
