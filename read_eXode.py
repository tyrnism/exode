from errno import errorcode
from beem import exceptions as bexceptions
from beem import Hive
from beem.nodelist import NodeList
from beem.block import Block, Blocks
from beem.blockchain import Blockchain
from beem.account import Account
import json
import os.path
import mysql.connector
from timeit import default_timer as timer
import time
import traceback
import datetime

import discord
from discord.ext import tasks

import exode_const as excst
#############################################################################################

class DataBaseConnector():

	mSQLConnector = mysql.connector.connect()
	
	def db_Connect(self):
		try:
			self.mSQLConnector = mysql.connector.connect(user='exode', password=excst.DB_PASS,
									host='127.0.0.1',
									database=excst.DB_NAME)
									
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("MySQL: Something is wrong with your user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("MySQL: Database does not exist")
			else:
				print("MySQL: ", err)

	def db_Cursor(self):

		try:
			cursor = self.mSQLConnector.cursor()
		except mysql.connector.Error as err:
			self.db_Connect()
			cursor = self.mSQLConnector.cursor()
			
		return cursor
		
	def db_Commit(self):
	
		self.mSQLConnector.commit()
		
##############################################################################################
# Initialise
fDataBase = DataBaseConnector()
fDataBase.db_Connect()

##############################################################################################

def ex_IsPack( mID ):
	(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails( mID )
		
	return is_pack
	
def ex_IsElite( mID ):

	return ( mID[:12] == "exode_card_E" )


def ex_GetAssetDetails( mID ):

	# rank: 
	# 0 -> common
	# 1 -> rare
	# 2 -> epic
	# 3 -> legendary
	
	NO_RARITY = 0
	COMMON_CARD = 0
	RARE_CARD = 1
	EPIC_CARD = 2
	LEGENDARY_CARD = 3
	
	if ( mID == "exode_????_booster" ):
		return (True, "???? booster",							NO_RARITY, 0)
	if ( mID == "exode_alpha_booster" ):
		return (True, "Alpha booster",							NO_RARITY, 0)
	if ( mID == "exode_beta_booster" ):
		return (True, "Beta booster",							NO_RARITY, 0)
		
	if ( mID == "exode_alpha_support_vega" ):
		return (True, "Alpha Escort Pack [Vega]",					NO_RARITY, 0)
	if ( mID == "exode_alpha_support_ionguards" ):
		return (True, "Alpha Escort Pack [Ion Guards]",					NO_RARITY, 0)
	if ( mID == "exode_alpha_support_tom" ):		
		return (True, "Alpha Support Pack [TOM Essentials]",				NO_RARITY, 0)
		
	if ( mID == "exode_alpha_starter_4" ):
		return (True, "Triple Alpha Starter Set",					NO_RARITY, 0)
	if ( mID == "exode_alpha_starter_3" ):
		return (True, "Alpha Starter [Elected Leader]",					NO_RARITY, 0)
	if ( mID == "exode_alpha_starter_2" ):
		return (True, "Alpha Starter [Ark Scientist]",					NO_RARITY, 0)
	if ( mID == "exode_alpha_starter_1" ):
	
		return (True, "Alpha Starter [Navy Lieutenant]",				NO_RARITY, 0)
	if ( mID == "exode_alpha_contract_tom" ):
		return (True, "Alpha Contract [TOM Settler PREMIUM BUDDIES]", 			NO_RARITY, 0)
	if ( mID == "exode_alpha_contract_rekatron" ):
		return (True, "Alpha Contract [WEAPON DROPS BY REKATRON]", 			NO_RARITY, 0)
	if ( mID == "exode_alpha_contract_syndicate" ):
		return (True, "Alpha Contract [SYNDICATE SPONSORSHIP]", 			NO_RARITY, 0)
		
	if ( mID == "exode_beta_contract_achean" ):
		return (True, "Beta Contract [Your Own Achean Gang]",				NO_RARITY, 0)
	if ( mID == "exode_beta_contract_starships_mods" ):
		return (True, "Beta Contract [Vogar Shipyards]",				NO_RARITY, 0)
	if ( mID == "exode_beta_contract_armor_mods" ):
		return (True, "Beta Contract [Esdrovian Armor Docks]",				NO_RARITY, 0)
	if ( mID == "exode_beta_contract_shop_franchise" ):
		return (True, "Beta Contract [Starbase Shop Ownership]",			NO_RARITY, 0)
	if ( mID == "exode_beta_contract_street_franchise" ):
		return (True, "Beta Contract [Street Shop Ownership]",				NO_RARITY, 0)
		
	if ( mID == "exode_alpha_pack_crew_kb119" ):
		return (True, "Alpha Crew Pack [Kilbot-119]",					NO_RARITY, 0)
	if ( mID == "exode_alpha_pack_crew_galvin4" ):
		return (True, "Alpha Crew Pack [Galvin 4]",					NO_RARITY, 0)
		
	if ( mID == "exode_alpha_character_pack_nomad" ):
		return (True, "Alpha Promo Character Pack [Nomad Navigator]", 			NO_RARITY, 0)
	if ( mID == "exode_alpha_character_pack_genetician" ):
		return (True, "Alpha Promo Character Pack [Genetician Scientist]",		NO_RARITY, 0)
	if ( mID == "exode_alpha_character_pack_suntek" ):
		return (True, "Alpha Promo Character Pack [Suntek Survivor]",			NO_RARITY, 0)
	if ( mID == "exode_alpha_character_pack_drachian" ):
		return (True, "Alpha Promo Character Pack [Drachian Colonel]",			NO_RARITY, 0)

	if ( mID == "exode_card_001_originNavy" 			or mID == "exode_card_E001_originNavy" ):
		return (False, "Navy Lieutenant [Origin]", 				EPIC_CARD, 	1)	
	if ( mID == "exode_card_002_shipArcheon" 			or mID == "exode_card_E002_shipArcheon" ):
		return (False, "Military Frigate (\"Archeon Class\")", 		EPIC_CARD,	2)	
	if ( mID == "exode_card_003_officerComms" 			or mID == "exode_card_E003_officerComms" ):
		return (False, "Communications Officer", 				RARE_CARD,	3)
	if ( mID == "exode_card_004_officerWeapons" 			or mID == "exode_card_E004_officerWeapons" ):
		return (False, "Weapons Officer", 					RARE_CARD,	4)		
	if ( mID == "exode_card_005_officerTactical" 			or mID == "exode_card_E005_officerTactical" ):
		return (False, "Tactical Officer", 					RARE_CARD,	5)		
	if ( mID == "exode_card_006_crewPilot" 				or mID == "exode_card_E006_crewPilot" ):
		return (False, "Pilot (Crew)", 					RARE_CARD,	6)		
	if ( mID == "exode_card_007_crewSRT" 				or mID == "exode_card_E007_crewSRT" ):
		return (False, "Signals Specialist (Crew)", 				RARE_CARD,	7)		
	if ( mID == "exode_card_008_crewDefense"			or mID == "exode_card_E008_crewDefense" ):
		return (False, "Defense Specialist (Crew)", 				RARE_CARD,	8)		
	if ( mID == "exode_card_009_crewTrooper" 			or mID == "exode_card_E009_crewTrooper" ):
		return (False, "Trooper (Crew)", 					COMMON_CARD,	9)		
	if ( mID == "exode_card_010_crewEngineer" 			or mID == "exode_card_E010_crewEngineer" ):
		return (False, "Military Engineer (Crew)", 				COMMON_CARD,	10)			
	if ( mID == "exode_card_011_setFMR17" 				or mID == "exode_card_E011_setFMR17" ):
		return (False, "FMR-17 \'Atonis\' (x3)", 				EPIC_CARD,	11)		
	if ( mID == "exode_card_012_setSuitMilitaryC" 			or mID == "exode_card_E012_setSuitMilitaryC" ):
		return (False, "Military Suit Class C (x3)", 				RARE_CARD,	12)		
	if ( mID == "exode_card_013_originArk" 				or mID == "exode_card_E013_originArk" ):
		return (False, "Ark Scientist [Origin]", 				EPIC_CARD,	13)		
	if ( mID == "exode_card_014_shipOrwell1" 			or mID == "exode_card_E014_shipOrwell1" ):
		return (False, "Ark Ship \"Orwell 1\"", 				EPIC_CARD,	14)		
	if ( mID == "exode_card_015_officerResearch" 			or mID == "exode_card_E015_officerResearch" ):
		return (False, "Research Officer", 					RARE_CARD,	15)		
	if ( mID == "exode_card_016_officerExploration" 		or mID == "exode_card_E016_officerExploration" ):
		return (False, "Exploration Officer", 				RARE_CARD,	16)	
	if ( mID == "exode_card_017_officerPreservation" 		or mID == "exode_card_E017_officerPreservation" ):
		return (False, "Preservation Officer", 				RARE_CARD,	17)	
	if ( mID == "exode_card_018_crewSurgeon" 			or mID == "exode_card_E018_crewSurgeon" ):
		return (False, "Space Surgeon", 					RARE_CARD,	18)	
	if ( mID == "exode_card_019_crewXenoAnalyst" 			or mID == "exode_card_E019_crewXenoAnalyst" ):
		return (False, "Xeno Analyst", 					RARE_CARD,	19)	
	if ( mID == "exode_card_020_crewBioScientist" 			or mID == "exode_card_E020_crewBioScientist" ):
		return (False, "Space Bioscientist", 					RARE_CARD,	20)	
	if ( mID == "exode_card_021_crewAnimalHandler" 			or mID == "exode_card_E021_crewAnimalHandler" ):
		return (False, "Animal Handler (Crew)", 				COMMON_CARD,	21)	
	if ( mID == "exode_card_022_crewLifeSearcher" 			or mID == "exode_card_E022_crewLifeSearcher" ):
		return (False, "Life Searcher (Crew)", 				COMMON_CARD,	22)	
	if ( mID == "exode_card_023_crewLabScientist" 			or mID == "exode_card_E023_crewLabScientist" ):
		return (False, "Lab Scientist (Crew)", 				COMMON_CARD,	23)	
	if ( mID == "exode_card_024_setRarePlants" 			or mID == "exode_card_E024_setRarePlants" ):
		return (False, "Rare Plants Collection (x6)", 			EPIC_CARD,	24)	
	if ( mID == "exode_card_025_setSuitResearchC" 			or mID == "exode_card_E025_setSuitResearchC" ):
		return (False, "Research Suits Class C (x3)", 			RARE_CARD,	25)	
	if ( mID == "exode_card_026_originLeader" 			or mID == "exode_card_E026_originLeader" ):
		return (False, "Elected Leader [Origin]", 				EPIC_CARD,	26)	
	if ( mID == "exode_card_027_shipDiplomatic" 			or mID == "exode_card_E027_shipDiplomatic" ):
		return (False, "Diplomatic Corvette \"Amarasia\"", 			EPIC_CARD,	27)	
	if ( mID == "exode_card_028_officerAdministrative" 		or mID == "exode_card_E028_officerAdministrative" ):
		return (False, "Administrative Officer", 				RARE_CARD,	28)	
	if ( mID == "exode_card_029_officerSecurity" 			or mID == "exode_card_E029_officerSecurity" ):
		return (False, "Security Officer", 					RARE_CARD,	29)	
	if ( mID == "exode_card_030_crewPropaganda"			or mID == "exode_card_E030_crewPropaganda" ):
		return (False, "Propaganda Specialist", 				RARE_CARD,	30)	
	if ( mID == "exode_card_031_crewPopulation" 			or mID == "exode_card_E031_crewPopulation" ):
		return (False, "Population Analyst", 					RARE_CARD,	31)	
	if ( mID == "exode_card_032_crewEntertainment" 			or mID == "exode_card_E032_crewEntertainment" ):
		return (False, "Welfare Specialist", 					RARE_CARD,	32)	
	if ( mID == "exode_card_033_crewMaintenance" 			or mID == "exode_card_E033_crewMaintenance" ):
		return (False, "Maintenance Staff (Crew)", 				COMMON_CARD,	33)	
	if ( mID == "exode_card_034_crewPilotCivilian" 			or mID == "exode_card_E034_crewPilotCivilian" ):
		return (False, "Civilian Pilot (Crew)", 				COMMON_CARD,	34)	
	if ( mID == "exode_card_035_crewSecurity" 			or mID == "exode_card_E035_crewSecurity" ):
		return (False, "Security Guard (Crew)", 				COMMON_CARD,	35)	
	if ( mID == "exode_card_036_setLuxury" 				or mID == "exode_card_E036_setLuxury" ):
		return (False, "Diplomatic Gifts", 					RARE_CARD,	36)	
	if ( mID == "exode_card_037_setDatabase" 			or mID == "exode_card_E037_setDatabase" ):
		return (False, "Federal Database", 					EPIC_CARD,	37)	
		
	if ( mID == "exode_card_039_Tom_BeautyCapsule" 			or mID == "exode_card_E039_Tom_BeautyCapsule" ):
		return (False, "BEAUTY Capsule", 					EPIC_CARD,	39)	
		
		
	if ( mID == "exode_card_045_Rekatron_fireworks" 		or mID == "exode_card_E045_Rekatron_fireworks" ):
		return (False, "FIREWORKS",	 					LEGENDARY_CARD,	45)
	if ( mID == "exode_card_046_Rekatron_defensiveAmmo" 		or mID == "exode_card_E046_Rekatron_defensiveAmmo" ):
		return (False, "DEFENSIVE AMMO",	 				COMMON_CARD,	46)
	if ( mID == "exode_card_047_Rekatron_firetalkerPistol" 		or mID == "exode_card_E047_Rekatron_firetalkerPistol" ):
		return (False, "FIRETALKER", 						COMMON_CARD,	47)
	if ( mID == "exode_card_048_Rekatron_karperPistol" 		or mID == "exode_card_E048_Rekatron_karperPistol" ):
		return (False, "KARPER Heavy", 					RARE_CARD,	48)
	if ( mID == "exode_card_049_Rekatron_explanatorRifle" 		or mID == "exode_card_E049_Rekatron_explanatorRifle" ):
		return (False, "EXPLANATOR", 						RARE_CARD,	49)
	if ( mID == "exode_card_050_Rekatron_rsdRifle" 			or mID == "exode_card_E050_Rekatron_rsdRifle" ):
		return (False, "REKATRON SD", 					RARE_CARD,	50)
	if ( mID == "exode_card_051_Rekatron_goodMorningPistol" 	or mID == "exode_card_E051_Rekatron_goodMorningPistol" ):
		return (False, "GOOD MORNING", 					RARE_CARD,	51)
	if ( mID == "exode_card_052_Rekatron_jugdmentDayRifle" 		or mID == "exode_card_E052_Rekatron_jugdmentDayRifle" ):
		return (False, "JUDGEMENT DAY", 					EPIC_CARD,	52)
	if ( mID == "exode_card_053_Rekatron_galacticPeacemaker" 	or mID == "exode_card_E053_Rekatron_galacticPeacemaker" ):
		return (False, "GALACTIC PEACEMAKER", 				EPIC_CARD,	53)
	if ( mID == "exode_card_054_Rekatron_ammoGuided" 		or mID == "exode_card_E054_Rekatron_ammoGuided" ):
		return (False, "AUTOGUIDED AMMO", 					RARE_CARD,	54)
	if ( mID == "exode_card_055_Rekatron_ammoParty" 		or mID == "exode_card_E055_Rekatron_ammoParty" ):
		return (False, "PARTY AMMO", 						EPIC_CARD,	55)
	if ( mID == "exode_card_056_Tom_SmootyAllInOne" 		or mID == "exode_card_E056_Tom_SmootyAllInOne" ):
		return (False, "SMOOTY All-In-One", 					COMMON_CARD,	56)
	if ( mID == "exode_card_057_Tom_FoodieMoodie" 			or mID == "exode_card_E057_Tom_FoodieMoodie" ):
		return (False, "Strategic FOODIE-MOODIE", 				COMMON_CARD,	57)
	if ( mID == "exode_card_058_Tom_FriendlyEyes" 			or mID == "exode_card_E058_Tom_FriendlyEyes" ):
		return (False, "Friendly Eyes XY-6", 					COMMON_CARD,	58)
	if ( mID == "exode_card_059_Tom_BuddyPinger" 			or mID == "exode_card_E059_Tom_BuddyPinger" ):
		return (False, "BUDDY Pinger", 					RARE_CARD,	59)
	if ( mID == "exode_card_060_Tom_VehicleLittleBuddy" 		or mID == "exode_card_E060_Tom_VehicleLittleBuddy" ):
		return (False, "LITTLE Buddy", 					RARE_CARD,	60)
	if ( mID == "exode_card_061_Tom_Custom" 			or mID == "exode_card_E061_Tom_Custom" ):
		return (False, "TOM Custom", 						RARE_CARD,	61)
	if ( mID == "exode_card_062_Tom_WHCConverter" 			or mID == "exode_card_E062_Tom_WHCConverter" ):
		return (False, "WHC Unit", 						RARE_CARD,	62)
	if ( mID == "exode_card_063_Tom_Explorator" 			or mID == "exode_card_E063_Tom_Explorator" ):
		return (False, "TOM Explorator X4", 					EPIC_CARD,	63)
	if ( mID == "exode_card_064_Tom_ShelterHappyFive" 		or mID == "exode_card_E064_Tom_ShelterHappyFive" ):
		return (False, "SHELTER \"Happy Five\"", 				EPIC_CARD,	64)
		
	if ( mID == "exode_card_065_SyndicateGeisha_ThirdSister" 	or mID == "exode_card_E065_SyndicateGeisha_ThirdSister" ):
		return (False, "Syndicate Geisha",	 				EPIC_CARD,	65)
	if ( mID == "exode_card_066_SyndicateEquipment_Chip"	 	or mID == "exode_card_E066_SyndicateEquipment_Chip" ):
		return (False, "Syndicate Chip", 					COMMON_CARD,	66)
	if ( mID == "exode_card_067_SyndicateEquipment_DrugHolidays"	or mID == "exode_card_E067_SyndicateEquipment_DrugHolidays" ):
		return (False, "\'Holidays\'", 					COMMON_CARD,	67)
	if ( mID == "exode_card_068_SyndicateEquipment_DrugNPrime"	or mID == "exode_card_E068_SyndicateEquipment_DrugNPrime" ):
		return (False, "\'N-Prime\'", 					COMMON_CARD,	68)
	if ( mID == "exode_card_069_SyndicateShipBlackLotus" 		or mID == "exode_card_E069_SyndicateShipBlackLotus" ):
		return (False, "\"Black Lotus\"", 					EPIC_CARD,	69)
	if ( mID == "exode_card_070_SyndicateEquipmentAutoBlaster"	or mID == "exode_card_E070_SyndicateEquipmentAutoBlaster" ):
		return (False, "Syndicate Auto Blaster", 				RARE_CARD,	70)	
	if ( mID == "exode_card_071_SyndicateEquipment_NarcoWarfare"	or mID == "exode_card_E071_SyndicateEquipment_NarcoWarfare" ):
		return (False, "Narco-Warfare", 					RARE_CARD,	71)
	if ( mID == "exode_card_072_SyndicateEquipmentSet_Genefactory" 
									or mID == "exode_card_E072_SyndicateEquipmentSet_Genefactory" ):
		return (False, "Nacrotics Genefactory", 				EPIC_CARD,	72)			
	if ( mID == "exode_card_073_SyndicateHacker" 			or mID == "exode_card_E073_SyndicateHacker" ):
		return (False, "Syndicate Hacker", 					RARE_CARD,	73)
	if ( mID == "exode_card_074_SyndicateLeader" 			or mID == "exode_card_E074_SyndicateLeader" ):
		return (False, "Syndicate Squad Leader", 				RARE_CARD,	74)		
	if ( mID == "exode_card_075_SyndicateTransactor" 		or mID == "exode_card_E075_SyndicateTransactor" ):
		return (False, "Programmed Transactor", 				RARE_CARD,	75)	
	if ( mID == "exode_card_076_SyndicateTrooper" 			or mID == "exode_card_E076_SyndicateTrooper" ):
		return (False, "Syndicate Trooper", 					RARE_CARD,	76)
	if ( mID == "exode_card_077_SyndicateAyumi" 			or mID == "exode_card_E077_SyndicateAyumi" ):
		return (False, "Ayumi", 						EPIC_CARD,	77)
	if ( mID == "exode_card_078_SyndicateYakuzaNoble" 		or mID == "exode_card_E078_SyndicateYakuzaNoble" ):
		return (False, "Battle-Trained Socialite", 				EPIC_CARD,	78)
	if ( mID == "exode_card_079_SyndicateYakuzaSniper" 		or mID == "exode_card_E079_SyndicateYakuzaSniper" ):
		return (False, "Camouflaged Sniper", 					EPIC_CARD,	79)
	if ( mID == "exode_card_080_TheKumicho" 			or mID == "exode_card_E080_TheKumicho" ):
		return (False, "The Kumicho", 					LEGENDARY_CARD,	80)
	if ( mID == "exode_card_081_RebelGeneral" 			or mID == "exode_card_E081_RebelGeneral" ):
		return (False, "Rebel General", 					LEGENDARY_CARD,	81)
	if ( mID == "exode_card_082_AlannaVos" 				or mID == "exode_card_E082_AlannaVos" ):
		return (False, "Alanna Vös, Federal Marshal", 			LEGENDARY_CARD,	82)
	if ( mID == "exode_card_083_Sh4rken" 				or mID == "exode_card_E083_Sh4rken" ):
		return (False, "Sh4rken", 						LEGENDARY_CARD,	83)
	if ( mID == "exode_card_084_TheAI" 				or mID == "exode_card_E084_TheAI" ):
		return (False, "Mysterious AI", 					LEGENDARY_CARD, 	84)
	if ( mID == "exode_card_085_Apprentice" 			or mID == "exode_card_E085_Apprentice" ):
		return (False, "Mysterious Robot", 					LEGENDARY_CARD,	85)
	if ( mID == "exode_card_086_Cranium" 				or mID == "exode_card_E086_Cranium" ):
		return (False, "Captain Cranium", 					LEGENDARY_CARD,	86)
	if ( mID == "exode_card_087_Cryptoeater" 			or mID == "exode_card_E087_Cryptoeater" ):
		return (False, "\"Crypto-Eater\"", 					LEGENDARY_CARD,	87)
	if ( mID == "exode_card_088_originRepentantPirate" 		or mID == "exode_card_E088_originRepentantPirate" ):
		return (False, "Repentant Pirate [Origin]", 				LEGENDARY_CARD,	88)
	if ( mID == "exode_card_089_shipColombus" 			or mID == "exode_card_E089_shipColombus" ):
		return (False, "\"The Colombus\" (circa 2113)", 			LEGENDARY_CARD,	89)
	if ( mID == "exode_card_090_shipQuantumSupreme"			or mID == "exode_card_E090_shipQuantumSupreme" ):
		return (False, "\"Quantum\" Class Supreme", 				LEGENDARY_CARD,	90)
	if ( mID == "exode_card_091_vehicleVelvetStorm" 		or mID == "exode_card_E091_vehicleVelvetStorm" ):
		return (False, "\"Velvet Storm\"", 					LEGENDARY_CARD,	91)
	if ( mID == "exode_card_092_vehicleVanguard" 			or mID == "exode_card_E092_vehicleVanguard" ):
		return (False, "\"Vanguard\"", 					LEGENDARY_CARD,	92)
	if ( mID == "exode_card_093_equipmentSuitArena" 		or mID == "exode_card_E093_equipmentSuitArena" ):
		return (False, "Arena Powersuit (signed by Kurban Ko)", 		LEGENDARY_CARD,	93)
		
	if ( mID == "exode_card_101_originSecretAgent" 			or mID == "exode_card_E101_originSecretAgent" ):
		return (False, "Secret Agent [Origin]", 				EPIC_CARD,	101)
	if ( mID == "exode_card_102_originStrandedTrader" 		or mID == "exode_card_E102_originStrandedTrader" ):
		return (False, "Stranded Trader [Origin]", 				EPIC_CARD,	102)
	if ( mID == "exode_card_103_originCruiseShipCaptain" 		or mID == "exode_card_E103_originCruiseShipCaptain" ):
		return (False, "Cruise Ship Captain [Origin]", 			EPIC_CARD,	103)
	if ( mID == "exode_card_104_shipArkLifesavior" 			or mID == "exode_card_E104_shipArkLifesavior" ):
		return (False, "Ark Ship \"Orwell 2\" Lifesavior", 			EPIC_CARD,	104)
	if ( mID == "exode_card_105_shipCargoKormen" 			or mID == "exode_card_E105_shipCargoKormen" ):
		return (False, "\"Kormen\" Class (Cargo)", 				EPIC_CARD,	105)
	if ( mID == "exode_card_106_shipRhino" 				or mID == "exode_card_E106_shipRhino" ):
		return (False, "\"Rhino\" Heavy Attack Frigate", 			EPIC_CARD,	106)
	if ( mID == "exode_card_107_shipCargoTaurus" 			or mID == "exode_card_E107_shipCargoTaurus" ):
		return (False, "\"Taurus\" Class Transport", 				EPIC_CARD,	107)
	if ( mID == "exode_card_108_shipMyrmidon" 			or mID == "exode_card_E108_shipMyrmidon" ):
		return (False, "\"Myrmidon\" Assault Transport", 			EPIC_CARD,	108)
	if ( mID == "exode_card_109_shipAkhen" 				or mID == "exode_card_E109_shipAkhen" ):
		return (False, "\"Akhen\" Cannon", 					EPIC_CARD,	109)
	if ( mID == "exode_card_110_shipCoetus" 			or mID == "exode_card_E110_shipCoetus" ):
		return (False, "\"Coetus\" Class Science Vessel", 			EPIC_CARD,	110)
	if ( mID == "exode_card_111_setGeneticianConsole" 		or mID == "exode_card_E111_setGeneticianConsole" ):
		return (False, "Genetician Console", 					EPIC_CARD,	111)
	if ( mID == "exode_card_112_setMilitaryClassA" 			or mID == "exode_card_E112_setMilitaryClassA" ):
		return (False, "Military Suits Class A (x3)", 			EPIC_CARD,	112)
	if ( mID == "exode_card_113_setEisenSuits" 			or mID == "exode_card_E113_setEisenSuits" ):
		return (False, "Eisen Suits (x3)", 					EPIC_CARD,	113)
	if ( mID == "exode_card_114_vehicleAcheanRacer" 		or mID == "exode_card_E114_vehicleAcheanRacer" ):
		return (False, "Archean Racer", 					EPIC_CARD,	114)
	if ( mID == "exode_card_115_crewSpaceMarshal"			or mID == "exode_card_E115_crewSpaceMarshal" ):
		return (False, "Space Federal Marshal", 				EPIC_CARD,	115)
	if ( mID == "exode_card_116_officerEliza" 			or mID == "exode_card_E116_officerEliza" ):
		return (False, "Eliza", 						EPIC_CARD,	116)
	if ( mID == "exode_card_117_crewOksana" 			or mID == "exode_card_E117_crewOksana" ):
		return (False, "Oksana", 						EPIC_CARD,	117)
	if ( mID == "exode_card_118_officerNorah" 			or mID == "exode_card_E118_officerNorah" ):
		return (False, "Norah", 						EPIC_CARD,	118)
	if ( mID == "exode_card_119_officerShen" 			or mID == "exode_card_E119_officerShen" ):
		return (False, "Shen", 						EPIC_CARD,	119)
	if ( mID == "exode_card_120_officerStug" 			or mID == "exode_card_E120_officerStug" ):
		return (False, "Stug", 						EPIC_CARD,	120)
	if ( mID == "exode_card_121_crewTyron" 				or mID == "exode_card_E121_crewTyron" ):
		return (False, "Tyron", 						EPIC_CARD,	121)
	if ( mID == "exode_card_122_officerAdmiralValro" 		or mID == "exode_card_E122_officerAdmiralValro" ):
		return (False, "Admiral Valro", 					EPIC_CARD,	122)
	if ( mID == "exode_card_123_officerNash" 			or mID == "exode_card_E123_officerNash" ):
		return (False, "Nash, \"The Expert\"", 				EPIC_CARD,	123)
	if ( mID == "exode_card_124_crewSpecialInfiltrationAgent" 	or mID == "exode_card_E124_crewSpecialInfiltrationAgent" ):
		return (False, "Special Infiltration Agent", 				EPIC_CARD,	124)
	if ( mID == "exode_card_125_crewScarletSarah" 			or mID == "exode_card_E125_crewScarletSarah" ):
		return (False, "\'Scarlet Sarah\'", 					EPIC_CARD,	125)
	if ( mID == "exode_card_126_passengerNuclearFamily" 		or mID == "exode_card_E126_passengerNuclearFamily" ):
		return (False, "Nuclear Family", 					EPIC_CARD,	126)
	if ( mID == "exode_card_127_installationOctohome" 		or mID == "exode_card_E127_installationOctohome" ):
		return (False, "Octohome", 						EPIC_CARD,	127)
	if ( mID == "exode_card_128_installationOrbitalShield" 		or mID == "exode_card_E128_installationOrbitalShield" ):
		return (False, "Orbital Shield", 					EPIC_CARD,	128)
	if ( mID == "exode_card_129_installationDreamsphere" 		or mID == "exode_card_E129_installationDreamsphere" ):
		return (False, "Dreamsphere", 					EPIC_CARD,	129)
	if ( mID == "exode_card_130_installationGenerator100"		or mID == "exode_card_E130_installationGenerator100" ):
		return (False, "X-Gen TR100", 					EPIC_CARD,	130)
	if ( mID == "exode_card_131_equipmentFactionCorporate" 		or mID == "exode_card_E131_equipmentFactionCorporate" ):
		return (False, "Corporate License (Level S+)", 			EPIC_CARD,	131)
	if ( mID == "exode_card_132_equipmentSuitRacer" 		or mID == "exode_card_E132_equipmentSuitRacer" ):
		return (False, "Racer Mech-Suit", 					EPIC_CARD,	132)
	if ( mID == "exode_card_133_equipmentSuitSpartan" 		or mID == "exode_card_E133_equipmentSuitSpartan" ):
		return (False, "Spartan Elite Suit", 					EPIC_CARD,	133)
	if ( mID == "exode_card_134_equipmentFactionRebellion" 		or mID == "exode_card_E134_equipmentFactionRebellion" ):
		return (False, "The Rebellion Secrets ||\"They knew\"||", 		EPIC_CARD,	134)
	if ( mID == "exode_card_135_escortSabre" 			or mID == "exode_card_E135_escortSabre" ):
		return (False, "Sabre Regiment", 					EPIC_CARD,	135)
	if ( mID == "exode_card_136_crewFleshCultLeader" 		or mID == "exode_card_E136_crewFleshCultLeader" ):
		return (False, "Flesh Cult Leader", 					EPIC_CARD,	136)
	if ( mID == "exode_card_137_installationDefensiveBunker" 	or mID == "exode_card_E137_installationDefensiveBunker" ):
		return (False, "Defensive Bunker", 					EPIC_CARD,	137)
		
	if ( mID == "exode_card_151_officerDrachianColonel" 		or mID == "exode_card_E151_officerDrachianColonel" ):
		return (False, "Drachian Colonel", 					EPIC_CARD,	151)
	if ( mID == "exode_card_152_crewNomadNavigator" 		or mID == "exode_card_E152_crewNomadNavigator" ):
		return (False, "Nomad Navigator", 					EPIC_CARD,	152)
	if ( mID == "exode_card_153_crewGeneticianScientist" 		or mID == "exode_card_E153_crewGeneticianScientist" ):
		return (False, "Genetician Scientist", 				EPIC_CARD,	153)
	if ( mID == "exode_card_154_crewSuntekSurvivor" 		or mID == "exode_card_E154_crewSuntekSurvivor" ):
		return (False, "Suntek Collector", 					EPIC_CARD,	154)
	if ( mID == "exode_card_155_crewKilbot" 			or mID == "exode_card_E155_crewKilbot" ):
		return (False, "KB-119 \'Kilbot\'", 					EPIC_CARD,	155)
	if ( mID == "exode_card_156_crewGalvin" 			or mID == "exode_card_E156_crewGalvin" ):
		return (False, "Galvin-4, Social Robot", 				EPIC_CARD,	156)
	if ( mID == "exode_card_157_escortVega" 			or mID == "exode_card_E157_escortVega" ):
		return (False, "Vega Elite Squadron", 				EPIC_CARD,	157)
	if ( mID == "exode_card_158_escortIonguards" 			or mID == "exode_card_E158_escortIonguards" ):
		return (False, "Ionguard Defense Fleet", 				EPIC_CARD,	158)
	if ( mID == "exode_card_159_suntekSphere" 			or mID == "exode_card_E159_suntekSphere" ):
		return (False, "Suntek Energy Sphere", 				EPIC_CARD,	159)
		
		
	if ( mID == "exode_card_181_escortLongswords" 			or mID == "exode_card_E181_escortLongswords" ):
		return (False, "Longsword Squadron", 					RARE_CARD,	181)
	if ( mID == "exode_card_182_escortCruiserTaskForce" 		or mID == "exode_card_E182_escortCruiserTaskForce" ):
		return (False, "Cruiser Task Force", 					RARE_CARD,	182)
	if ( mID == "exode_card_183_escortStarsystemGarrison" 		or mID == "exode_card_E183_escortStarsystemGarrison" ):
		return (False, "Starsystem Garrison", 				COMMON_CARD,	183)
	if ( mID == "exode_card_184_shipBaldie" 			or mID == "exode_card_E184_shipBaldie" ):
		return (False, "\'Baldie\' Shuttle", 					COMMON_CARD,	184)
	if ( mID == "exode_card_185_shipClaymoreHyperfighter" 		or mID == "exode_card_E185_shipClaymoreHyperfighter" ):
		return (False, "\"Claymore\" Hyperfighter", 				RARE_CARD,	185)
	if ( mID == "exode_card_186_shipDrachianMantis" 		or mID == "exode_card_E186_shipDrachianMantis" ):
		return (False, "Drachian \"Mantis\"", 				RARE_CARD,	186)
	if ( mID == "exode_card_187_vehicleSalazar" 			or mID == "exode_card_E187_vehicleSalazar" ):
		return (False, "\"Salazar\" Space Cab", 				COMMON_CARD,	187)
	if ( mID == "exode_card_188_vehicleTraveler2" 			or mID == "exode_card_E188_vehicleTraveler2" ):
		return (False, "Traveler-2", 						COMMON_CARD,	188)
	if ( mID == "exode_card_189_vehicleSupplyDropship" 		or mID == "exode_card_E189_vehicleSupplyDropship" ):
		return (False, "Supply Dropship", 					COMMON_CARD,	189)
	if ( mID == "exode_card_190_vehicleExplorationDropship" 	or mID == "exode_card_E190_vehicleExplorationDropship" ):
		return (False, "Exploration Dropship", 				RARE_CARD,	190)
	if ( mID == "exode_card_191_vehicleZandratti" 			or mID == "exode_card_E191_vehicleZandratti" ):
		return (False, "\"Zandratti\"", 					RARE_CARD,	191)
	if ( mID == "exode_card_192_vehicleSecurityDrone" 		or mID == "exode_card_E192_vehicleSecurityDrone" ):
		return (False, "Security Drone", 					RARE_CARD,	192)
	if ( mID == "exode_card_193_vehiclePantherBike" 		or mID == "exode_card_E193_vehiclePantherBike" ):
		return (False, "Pather Bike", 					RARE_CARD,	193)
		
	if ( mID == "exode_card_201_setMedicalBay" 			or mID == "exode_card_E201_setMedicalBay" ):
		return (False, "Medical Bay", 					RARE_CARD,	201)
	if ( mID == "exode_card_202_equipmentRoboticParts" 		or mID == "exode_card_E202_equipmentRoboticParts" ):
		return (False, "Robotic Parts", 					COMMON_CARD,	202)
	if ( mID == "exode_card_203_equipmentEnergyCells" 		or mID == "exode_card_E203_equipmentEnergyCells" ):
		return (False, "Energy Cells", 					COMMON_CARD,	203)
	if ( mID == "exode_card_204_equipmentShipConstructionParts"	or mID == "exode_card_E204_equipmentShipConstructionParts" ):
		return (False, "Ship Construction Parts", 				COMMON_CARD,	204)
	if ( mID == "exode_card_205_equipmentUniversalFixer" 		or mID == "exode_card_E205_equipmentUniversalFixer" ):
		return (False, "\"Universal Fixer\" Suit", 				COMMON_CARD,	205)
	if ( mID == "exode_card_206_equipmentLonestar" 			or mID == "exode_card_E206_equipmentLonestar" ):
		return (False, "\"Lonestar\" Spacesuit", 				COMMON_CARD,	206)
	if ( mID == "exode_card_207_equipmentChipsAndData" 		or mID == "exode_card_E207_equipmentChipsAndData" ):
		return (False, "Chips and Data", 					COMMON_CARD,	207)
	if ( mID == "exode_card_208_equipmentCorporate" 		or mID == "exode_card_E208_equipmentCorporate" ):
		return (False, "Corporate License", 					RARE_CARD,	208)
	if ( mID == "exode_card_209_equipmentEisenSuit" 		or mID == "exode_card_E209_equipmentEisenSuit" ):
		return (False, "Eisen Suit - Artic Edition", 				RARE_CARD,	209)
	if ( mID == "exode_card_210_equipmentDrachianSuit" 		or mID == "exode_card_E210_equipmentDrachianSuit" ):
		return (False, "Drachian Scarab Armor", 				RARE_CARD,	210)
	if ( mID == "exode_card_211_equipmentMilitarySuit" 		or mID == "exode_card_E211_equipmentMilitarySuit" ):
		return (False, "Military Suit Class A", 				RARE_CARD,	211)
	if ( mID == "exode_card_212_equipmentPlanetscan" 		or mID == "exode_card_E212_equipmentPlanetscan" ):
		return (False, "Planetscan VX", 					RARE_CARD,	212)
	if ( mID == "exode_card_213_equipmentRimscan" 			or mID == "exode_card_E213_equipmentRimscan" ):
		return (False, "Rimscan Software", 					RARE_CARD,	213)
	if ( mID == "exode_card_214_equipmentDesigner" 			or mID == "exode_card_E214_equipmentDesigner" ):
		return (False, "Diamondstar Designer", 				RARE_CARD,	214)
	if ( mID == "exode_card_215_equipmentIdentificationMatrix" 	or mID == "exode_card_E215_equipmentIdentificationMatrix" ):
		return (False, "Identification Matrix", 				COMMON_CARD,	215)
		
	if ( mID == "exode_card_221_crewDrachianCommissar" 		or mID == "exode_card_E221_crewDrachianCommissar" ):
		return (False, "Drachian Commissar", 					RARE_CARD,	221)
	if ( mID == "exode_card_222_crewFederalAgent" 			or mID == "exode_card_E222_crewFederalAgent" ):
		return (False, "Federal Agent", 					RARE_CARD,	222)
	if ( mID == "exode_card_223_crewCorporateBodyguard" 		or mID == "exode_card_E223_crewCorporateBodyguard" ):
		return (False, "Corporate Bodyguard", 				RARE_CARD,	223)
	if ( mID == "exode_card_224_crewFederalMarine" 			or mID == "exode_card_E224_crewFederalMarine" ):
		return (False, "Federal Marine", 					RARE_CARD,	224)
	if ( mID == "exode_card_225_crewFederalPolice" 			or mID == "exode_card_E225_crewFederalPolice" ):
		return (False, "Federal Government Police", 				RARE_CARD,	225)
	if ( mID == "exode_card_226_crewDrachianTrooper" 		or mID == "exode_card_E226_crewDrachianTrooper" ):
		return (False, "Drachian Assault Trooper", 				RARE_CARD,	226)
	if ( mID == "exode_card_227_crewCorneredRebelAgent" 		or mID == "exode_card_E227_crewCorneredRebelAgent" ):
		return (False, "Cornered Rebel Agent", 				RARE_CARD,	227)
	if ( mID == "exode_card_228_passengerDangerous" 		or mID == "exode_card_E228_passengerDangerous" ):
		return (False, "Dangerous Passenger", 				RARE_CARD,	228)
	if ( mID == "exode_card_229_passengerUnstable" 			or mID == "exode_card_E229_passengerUnstable" ):
		return (False, "Unstable Genius", 					COMMON_CARD,	229)
	if ( mID == "exode_card_230_crewMaintenanceDroid" 		or mID == "exode_card_E230_crewMaintenanceDroid" ):
		return (False, "Maintenance Droid", 					COMMON_CARD,	230)
	if ( mID == "exode_card_231_passengerScienceStudent" 		or mID == "exode_card_E231_passengerScienceStudent" ):
		return (False, "Science student", 					COMMON_CARD,	231)
	if ( mID == "exode_card_232_passengerSocialite" 		or mID == "exode_card_E232_passengerSocialite" ):
		return (False, "Socialite", 						COMMON_CARD,	232)
	if ( mID == "exode_card_233_passengerTechExpert" 		or mID == "exode_card_E233_passengerTechExpert" ):
		return (False, "Tech Expert", 					COMMON_CARD,	233)
		
	if ( mID == "exode_card_235_crewTriskan" 			or mID == "exode_card_E235_crewTriskan" ):
		return (False, "Triskan Fighter", 					RARE_CARD,	235)
	if ( mID == "exode_card_236_crewFleshCult"			or mID == "exode_card_E236_crewFleshCult" ):
		return (False, "Flesh Cult Recruiter", 				RARE_CARD,	236)
	if ( mID == "exode_card_237_crewFleshCultScientist" 		or mID == "exode_card_E237_crewFleshCultScientist" ):
		return (False, "Magna Cultist", 					RARE_CARD,	237)
		
	if ( mID == "exode_card_241_installationDrillingMachine" 	or mID == "exode_card_E241_installationDrillingMachine" ):
		return (False, "Drilling Machine", 					COMMON_CARD,	241)
	if ( mID == "exode_card_242_installationRadarArray" 		or mID == "exode_card_E242_installationRadarArray" ):
		return (False, "Radar Array", 					COMMON_CARD,	242)
	if ( mID == "exode_card_243_installationGenerator20" 		or mID == "exode_card_E243_installationGenerator20" ):
		return (False, "X-Gen TR20", 						COMMON_CARD,	243)
	if ( mID == "exode_card_244_installationTomStarter" 		or mID == "exode_card_E244_installationTomStarter" ):
		return (False, "TOM STARTER", 					COMMON_CARD,	244)
	if ( mID == "exode_card_245_installationLiveBlock" 		or mID == "exode_card_E245_installationLiveBlock" ):
		return (False, "Life Block", 						COMMON_CARD,	245)
	if ( mID == "exode_card_246_installationBiodomes" 		or mID == "exode_card_E246_installationBiodomes" ):
		return (False, "Biodomes", 						COMMON_CARD,	246)
	if ( mID == "exode_card_247_installationTurret" 		or mID == "exode_card_E247_installationTurret" ):
		return (False, "AA/AT Automatic Turret", 				COMMON_CARD,	247)
	if ( mID == "exode_card_248_layoutProtectionWalls" 		or mID == "exode_card_E248_layoutProtectionWalls" ):
		return (False, "Protection Walls", 					COMMON_CARD,	248)
	if ( mID == "exode_card_249_layoutUnderground" 			or mID == "exode_card_E249_layoutUnderground" ):
		return (False, "Underground Construction", 				COMMON_CARD,	249)
	if ( mID == "exode_card_250_interiorLabEquipment" 		or mID == "exode_card_E250_interiorLabEquipment" ):
		return (False, "Lab Equipment", 					COMMON_CARD,	250)
	if ( mID == "exode_card_251_interiorManagementConsole"	 	or mID == "exode_card_E251_interiorManagementConsole" ):
		return (False, "Management Console", 					COMMON_CARD,	251)
	if ( mID == "exode_card_252_interiorComputerRoom" 		or mID == "exode_card_E252_interiorComputerRoom" ):
		return (False, "Computer Room",					RARE_CARD,	252)
	if ( mID == "exode_card_253_installationMultipurpose" 		or mID == "exode_card_E253_installationMultipurpose" ):
		return (False, "Multipurpose Prefab", 				COMMON_CARD,	253)
	if ( mID == "exode_card_254_installationCommunicationArray"	or mID == "exode_card_E254_installationCommunicationArray" ):
		return (False, "Communication Array", 				RARE_CARD,	254)
	if ( mID == "exode_card_255_interiorCuves" 			or mID == "exode_card_E255_interiorCuves" ):
		return (False, "Chemical Cuves", 					RARE_CARD,	255)
	if ( mID == "exode_card_256_installationPreservationDome"	or mID == "exode_card_E256_installationPreservationDome" ):
		return (False, "Preservation Dome", 					COMMON_CARD,	256)
	if ( mID == "exode_card_257_installationStorage" 		or mID == "exode_card_E257_installationStorage" ):
		return (False, "Storage Building", 					COMMON_CARD,	257)
	if ( mID == "exode_card_258_equipmentTomEssentialsHappyFood"	or mID == "exode_card_E258_equipmentTomEssentialsHappyFood" ):
		return (False, "Soup and Cook", 					EPIC_CARD,	258)
	if ( mID == "exode_card_259_equipmentTomEssentialsHappyAir"	or mID == "exode_card_E259_equipmentTomEssentialsHappyAir" ):
		return (False, "TOM Beauty Air", 					EPIC_CARD,	259)
	if ( mID == "exode_card_260_equipmentTomEssentialsSurvivor"	or mID == "exode_card_E260_equipmentTomEssentialsSurvivor" ):
		return (False, "TOM Survivor CO5", 					EPIC_CARD,	260)
	if ( mID == "exode_card_261_actionImmediateOrder"		or mID == "exode_card_E261_actionImmediateOrder" ):
		return (False, "Emergency Order!", 					COMMON_CARD,	261)
	
	print(mID)
	is_pack = mID[:len("exode_card")] != "exode_card"
	return ( is_pack, mID, -1, 0)

#########################################################################################

def db_TX_GetDetails( tx_id, tx_uid, tx_type, tx_target ):

	cursor = fDataBase.db_Cursor()
	
	query = ("SELECT block, auth FROM exode_tx "
			 "WHERE tx_id = %s and type = %s and uid = %s and player = %s" )	
		
	cursor.execute(query, (tx_id, tx_type, tx_uid, tx_target))
	m_output = cursor.fetchall()
	
	if ( cursor.rowcount != 0 ):	
		tx_exist  = True
		tx_block  = int(m_output[0][0])
		tx_player = tx_target
		tx_auth   = m_output[0][1]
	else:
		tx_exist  = False
		tx_block  = 0
		tx_player = tx_target
		tx_auth   = ""
	
	output = { 'exist': tx_exist, 'block': tx_block, 'player': tx_player, 'auth': tx_auth }
			
	cursor.reset()
	cursor.close()
	
	return output	
	
	
def db_TX_Cancel( tx_id, tx_uid, tx_type, tx_target ):

	cursor = fDataBase.db_Cursor()
	
	query = ("UPDATE exode_tx "
		"SET cancel = %s "
		"WHERE tx_id = %s and type = %s and uid = %s and player = %s") 
				
	cursor.execute(query, (1, tx_id, tx_type, tx_uid, tx_target))
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()
	
def db_TX_Add( tx_id, tx_uid, tx_type, tx_block, tx_player, tx_from, tx_auth ):

	cursor = fDataBase.db_Cursor()
		
	query = ("INSERT INTO exode_tx "
		"(tx_id, type, uid, block, player, player_from, auth) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s)")
		
	cursor.execute(query, (tx_id, tx_type, tx_uid, tx_block, tx_player, tx_from, tx_auth))
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()
	
	
def db_TX_GetLastBlock(mPlayer="exodegame"): 

	cursor = fDataBase.db_Cursor()
	
	query = ("SELECT MAX(block) FROM exode_tx where auth = %s ")
		 
	cursor.execute(query, (mPlayer,) )
	m_out = cursor.fetchall()
	
	if ( m_out[0][0] != None ):
		m_block = int(m_out[0][0])
	else: 
		m_block = 0
		
	cursor.reset()
	cursor.close()
	
	return m_block
	
#########################################################################################

def db_TransferTX_Reset():

	cursor = fDataBase.db_Cursor()
	
	query = ("delete from exode_cards "
		"where minter = 'no_source' ")
		
	cursor.execute(query)
	fDataBase.db_Commit()
	
	cursor.reset()
	
	query = ("UPDATE exode_cards "
		"SET owner = minter, burn = 0, block_update = block ")
		
	cursor.execute(query)
	fDataBase.db_Commit()
	
	cursor.reset()
	
	
	query = ("UPDATE exode_pack "
		"SET nb = buy ")
		
	cursor.execute(query)
	fDataBase.db_Commit()
	
	cursor.reset()
	
	query = ("truncate exode_sales ")
		
	cursor.execute(query)
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()


def db_TransferTX_Add( tx_auth, tx_type, tx_block, tx_id, player_from, player_to, card_id, card_uid, price=0.0 ):

	cursor = fDataBase.db_Cursor()
		
	tx_time = Block(tx_block).time()
	
	query = ("INSERT INTO exode_tx_transfer "
		"(tx_auth, tx_type, tx_block, tx_time, tx_id, player_from, player_to, card_id, card_uid, price) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
		
	cursor.execute(query, (tx_auth, tx_type, tx_block, tx_time, tx_id, player_from, player_to, card_id, card_uid, price))
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()

def db_TransferTX_FixID( card_uid, card_id ):

	cursor = fDataBase.db_Cursor()
	
	query = ("UPDATE exode_tx_transfer "
		"SET card_id = %s WHERE card_uid = %s and card_id = ''")
		
	cursor.execute(query, (card_id, card_uid))
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()
	
	
def db_TransferTX_Get(mBlock=0):

	cursor = fDataBase.db_Cursor()
	
	query = ("SELECT tx_auth, tx_type, tx_block, tx_time, tx_id, player_from, player_to, card_id, card_uid, price FROM exode_tx_transfer where tx_block > %s ORDER BY tx_block")
		
	cursor.execute(query, (mBlock,))
	m_out = cursor.fetchall()
	
	cursor.reset()
	cursor.close()
	
	return m_out

def db_TransferTX_Last():

	cursor = fDataBase.db_Cursor()
	
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
	
#########################################################################################

def db_Player_GetLastBlock(mPlayer): 

	cursor = fDataBase.db_Cursor()
	
	query = ("SELECT last_block FROM exode_player where player = %s ")
		 
	cursor.execute(query, (mPlayer,) )
	m_out = cursor.fetchall()
	
	if ( cursor.rowcount != 0 ):	
		m_block = int(m_out[0][0])
	else:
		m_block = 0
		
	cursor.reset()
	cursor.close()
	
	return m_block
	
def db_Player_SetLastBlock(mPlayer,mBlock): 

	cursor = fDataBase.db_Cursor()
	
	query = ("SELECT last_block FROM exode_player where player = %s ")
		 
	cursor.execute(query, (mPlayer,) )
	m_out = cursor.fetchall()
	
	query = ("UPDATE exode_player "
		"SET last_block = %s "
		"WHERE player = %s") 
	
	cursor.reset()
		 
	cursor.execute(query, (mBlock,mPlayer) )
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()
	
def db_Player_SetLastBlock_all(mBlock):

	cursor = fDataBase.db_Cursor()
	
	query = ("UPDATE exode_player "
		"SET last_block = %s "
		"WHERE last_block < %s") 
			 
	cursor.execute(query, (mBlock,mBlock) )
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()

def db_Player_CompleteList(mFull=False):

	cursor = fDataBase.db_Cursor()
	
	query = ("INSERT INTO exode_player (player) "
		"SELECT exode_pack.player FROM exode_pack "
		"WHERE exode_pack.player not in (select exode_player.player from exode_player) "
		"GROUP BY exode_pack.player ") 
	
	cursor.execute(query)
	fDataBase.db_Commit()
	
	cursor.reset()
	
	query = ("INSERT INTO exode_player (player) "
		"SELECT exode_cards.owner FROM exode_cards "
		"WHERE exode_cards.owner not in (select exode_player.player from exode_player) "
		"GROUP BY exode_cards.owner ") 
	
	cursor.execute(query)
	fDataBase.db_Commit()
	
	if ( mFull ):
	
		cursor.reset()
		
		query = ("INSERT INTO exode_player (player) "
			"SELECT exode_tx_transfer.player_from FROM exode_tx_transfer "
			"WHERE exode_tx_transfer.player_from not in (select exode_player.player from exode_player) "
			"and exode_tx_transfer.player_from != 'exodegame' and exode_tx_transfer.player_from != 'null' and exode_tx_transfer.player_from != 'market' and exode_tx_transfer.player_from != 'burn' and exode_tx_transfer.player_from != '' "
			"GROUP BY exode_tx_transfer.player_from ") 
		
		cursor.execute(query)
		fDataBase.db_Commit()		
	
		cursor.reset()
		
		query = ("INSERT INTO exode_player (player) "
			"SELECT exode_tx_transfer.player_to FROM exode_tx_transfer "
			"WHERE exode_tx_transfer.player_to not in (select exode_player.player from exode_player) "
			"and exode_tx_transfer.player_to != 'exodegame' and exode_tx_transfer.player_to != 'null' and exode_tx_transfer.player_to != 'market' and exode_tx_transfer.player_to != 'burn' and exode_tx_transfer.player_to != '' "
			"GROUP BY exode_tx_transfer.player_to ") 
		
		cursor.execute(query)
		fDataBase.db_Commit()
		
			
	cursor.reset()
	cursor.close()
	

def db_Player_Add(mPlayer):

	cursor = fDataBase.db_Cursor()
	
	query = ("SELECT last_block FROM exode_player where player = %s ")
		 
	cursor.execute(query, (mPlayer,) )
	m_out = cursor.fetchall()

	if ( cursor.rowcount == 0 ):	
		cursor.reset()
		
		query = ("INSERT INTO exode_player "
		"(player) "
		"VALUES (%s)") 
		
		cursor.execute(query, (mPlayer,) )
		fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()
		
	
#########################################################################################

def db_Pack_GetDetails( pack_owner, pack_id ):

	cursor = fDataBase.db_Cursor()
	
	query = ("SELECT nb, opened FROM exode_pack "
			 "WHERE player = %s and type = %s" )	
		
	cursor.execute(query, (pack_owner, pack_id))
	m_output = cursor.fetchall()
	
	if ( cursor.rowcount != 0 ):	
		pack_exist = True
		pack_nb    = int(m_output[0][0])
		pack_open  = int(m_output[0][1])
	else:
		pack_exist = False
		pack_nb    = 0
		pack_open  = 0
	
	output = { 'exist': pack_exist, 'nb': pack_nb, 'open': pack_open }
			
	cursor.reset()
	cursor.close()
	
	return output
	
def db_Pack_New( pack_owner, pack_id, pack_nb, pack_buy, pack_open ):

	cursor = fDataBase.db_Cursor()
		
	query = ("INSERT INTO exode_pack "
		"(player, type, nb, buy, opened) "
		"VALUES (%s, %s, %s, %s, %s)")
		
	cursor.execute(query, (pack_owner, pack_id, pack_nb, pack_buy, pack_open))
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()
	
def db_Pack_Update( pack_owner, pack_id, pack_nb, pack_buy, pack_open ):

	cursor = fDataBase.db_Cursor()
	
	query = ("UPDATE exode_pack "
		"SET nb = nb + %s, buy = buy + %s, opened = opened + %s "
		"WHERE player = %s and type = %s" )	
		
	cursor.execute(query, (pack_nb, pack_buy, pack_open, pack_owner, pack_id))
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()
	
def db_Pack_Apply_TransferAll( pack_prev_owner, pack_new_owner ):

	cursor = fDataBase.db_Cursor()
	
	query = ("SELECT type, nb FROM exode_pack "
			 "WHERE player = %s" )	
		
	cursor.execute(query, (pack_prev_owner, ))
	m_output = cursor.fetchall()
		
	for iRow in range(cursor.rowcount):
	
		pack_id = m_output[iRow][0]
		pack_nb = m_output[iRow][1]
		db_Pack_Apply_Update(pack_new_owner, pack_id, pack_nb, 0)
		
		cursor.reset()
		query = ("UPDATE exode_pack "
			"SET nb = 0 "
			"WHERE player = %s AND type = %s") 					
		cursor.execute(query, (pack_prev_owner, pack_id) )
		fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()
	
def db_Pack_Apply_Transfer( pack_prev_owner, pack_new_owner, pack_id, pack_nb ):
	
	db_Pack_Update( pack_prev_owner, pack_id, -1 * pack_nb, 0, 0 )
	db_Pack_Update( pack_new_owner, pack_id, pack_nb, 0, 0 )	
	
def db_Pack_Apply_Update( pack_owner, pack_id, pack_nb, pack_open ):

	pInfo = db_Pack_GetDetails( pack_owner, pack_id )
	if ( pInfo['exist'] ):
		db_Pack_Update( pack_owner, pack_id, pack_nb, pack_nb, pack_open )
	else:
		db_Pack_New( pack_owner, pack_id, pack_nb, pack_nb, pack_open )
	
#########################################################################################

def db_Card_GetDetails( card_uid ):

	cursor = fDataBase.db_Cursor()
	
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
	
def db_Card_Mint( card_owner, card_id, card_num, card_uid, card_mint, card_elite, card_bound, card_block, card_minter ):
	
	cursor = fDataBase.db_Cursor()
	
	card_burn = 0
	
	query = ("INSERT INTO exode_cards "
		"(type, num, uid, owner, burn, bound, elite, mint_num, block, block_update, minter) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
				
	cursor.execute(query, (card_id, card_num, card_uid, card_owner, card_burn, card_bound, card_elite, card_mint, card_block, card_block, card_minter) )
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()
	
	
def db_Card_Add_Missing( card_owner, card_id, card_uid, card_num, card_elite, card_block ):
	
	cursor = fDataBase.db_Cursor()
		
	query = ("INSERT INTO exode_cards_no_source "
		"(card_owner, card_id, card_uid, card_num, card_elite, card_block) "
		"VALUES (%s, %s, %s, %s, %s, %s)")
				
	cursor.execute(query, (card_owner, card_id, card_uid, card_num, card_elite, card_block) )
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()
	
def db_Card_Mint_Missing():

	cursor = fDataBase.db_Cursor()
		
	query = ("SELECT card_owner, card_id, card_uid, card_num, card_elite, card_block FROM exode_cards_no_source where card_id != '' ")
	
	cursor.execute(query)
	m_output = cursor.fetchall()
	
	
	if ( cursor.rowcount != 0 ):	
		
		tCards = cursor.rowcount
			
		cursor.reset()
		cursor.close()
	
		for iCard in range(tCards):
		
			card_owner  = m_output[iCard][0]
			card_id     = m_output[iCard][1]
			card_uid    = m_output[iCard][2]
			card_num    = m_output[iCard][3]
			card_elite  = m_output[iCard][4]
			card_block  = m_output[iCard][5]
			
			card_mint   = -1
			card_bound  = 0
			card_minter = "no_source"
		
			db_Card_Mint( card_owner, card_id, card_num, card_uid, card_mint, card_elite, card_bound, card_block, card_minter )
	else:
		cursor.reset()
		cursor.close()
		
def db_Card_Mint_Missing_New():

	cursor = fDataBase.db_Cursor()
		
	query = ("SELECT card_owner, card_id, card_uid, card_num, card_elite, card_block FROM exode_cards_no_source where card_id != ''"
		"and card_uid not in (SELECT uid from exode_cards)")
	
	cursor.execute(query)
	m_output = cursor.fetchall()
	
	
	if ( cursor.rowcount != 0 ):	
		
		tCards = cursor.rowcount
			
		cursor.reset()
		cursor.close()
	
		for iCard in range(tCards):
		
			card_owner  = m_output[iCard][0]
			card_id     = m_output[iCard][1]
			card_uid    = m_output[iCard][2]
			card_num    = m_output[iCard][3]
			card_elite  = m_output[iCard][4]
			card_block  = m_output[iCard][5]
			
			card_mint   = -1
			card_bound  = 0
			card_minter = "no_source"
		
			db_Card_Mint( card_owner, card_id, card_num, card_uid, card_mint, card_elite, card_bound, card_block, card_minter )
	else:
		cursor.reset()
		cursor.close()

	
def db_Card_Burn( card_uid, card_block, card_burn, card_burner ):

	cursor = fDataBase.db_Cursor()
	
	query = ("UPDATE exode_cards "
		"SET burn = %s, block_update = %s, owner = %s "
		"WHERE uid = %s") 
		
	cursor.execute(query, (card_burn, card_block, card_burner, card_uid) )
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()

def db_Card_Transfer( card_uid, card_block, card_owner ):

	cursor = fDataBase.db_Cursor()

	card_burn = 1
	
	query = ("UPDATE exode_cards "
		"SET owner = %s, block_update = GREATEST( block_update, %s ) "
		"WHERE uid = %s") 
		
	cursor.execute(query, (card_owner, card_block, card_uid) )
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()
	
def db_Card_LoadMint():

	cursor = fDataBase.db_Cursor()
	
	query = ("SELECT type, COUNT(*) FROM exode_cards "
		 "WHERE mint_num != -1 GROUP BY type ")	
		
	cursor.execute(query)
	m_output = cursor.fetchall()
	
	if ( cursor.rowcount != 0 ):	
		
		tCards = cursor.rowcount
		for iCard in range(tCards):
			excst.MINT_NUM[ m_output[iCard][0] ] = int(m_output[iCard][1])
			
		
	cursor.reset()	
	query = ("SELECT type, COUNT(*) FROM exode_cards "
		 "WHERE minter = 'no_source'  and owner != 'elindos' and owner != 'exolindos' GROUP BY type ")	
		 
	cursor.execute(query)
	m_output = cursor.fetchall()
	if ( cursor.rowcount != 0 ):	
		
		tCards = cursor.rowcount
		for iCard in range(tCards):
			excst.MINT_NUM_NOSOURCE[ m_output[iCard][0] ] = int(m_output[iCard][1])
	
	cursor.reset()
	cursor.close()
	
	
def db_Card_Apply_TransferAll( card_prev_owner, card_owner, card_block ):

	cursor = fDataBase.db_Cursor()

	card_burn = 1
	
	query = ("UPDATE exode_cards "
		"SET owner = %s, block_update = %s "
		"WHERE owner = %s and burn = 0 and bound = 0") 
		
	cursor.execute(query, (card_owner, card_block, card_prev_owner) )
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()

#test
	
	
	
def db_Card_Apply_Mint( card_owner, card_id, card_uid, card_mint, card_elite, card_bound, card_block, tx_id, bypass=False ):
	
	msg = ""
	
	# Will be replaced one day...
	if ( card_owner == "elindos" or card_owner == "exolindos" or card_uid == "none" ):
		card_mint = -1
	else:
	
		if ( card_id in excst.MINT_NUM ):
			excst.MINT_NUM[ card_id ] = excst.MINT_NUM[ card_id ] + 1
		else:
			excst.MINT_NUM[ card_id ] = 1
			
		card_mint = excst.MINT_NUM[ card_id ]
	
	(is_pack, card_name, card_rank, card_num) = ex_GetAssetDetails(card_id)
	
	# Mint here
	db_Card_Mint( card_owner, card_id, card_num, card_uid, card_mint, card_elite, card_bound, card_block, card_owner )
	
	
	if ( (card_mint > 0 and card_mint <= 10) or (int(card_elite) == 1) or (card_rank >= 2) or (card_rank == -1) ):
		if ( int(card_elite) == 1 ):
			msg_elite = "an **Elite "
		else:
			msg_elite = "a **"
				
								
		msg_rarity = "Common"
		if ( card_rank == 1 ):
			msg_rarity = "Rare"
		elif ( card_rank == 2 ):
			msg_rarity = "Epic"
		elif ( card_rank == 3 ):
			msg_rarity = "Legendary"
		elif ( card_rank == -1 ):
			msg_rarity = "???"
		
		msg = ":tada: {player} found {elite}{name}** [*{rarity}*] (**{mint}**/{mint} *uid={uid}*)".format(player=card_owner,rarity=msg_rarity, elite=msg_elite,name=card_name, 
					mint=card_mint, uid=card_uid)
	
	return msg
	
def db_Card_IsTransferable( card_from, card_to, card_id, card_uid, card_block, tx_id, transfer_action, bypass=False ):

	cInfo = db_Card_GetDetails( card_uid )
	
	if ( not cInfo['exist'] ):
		with open('logs/card_error.json', 'a') as f:
			err_msg = { "card": { "id": card_id, "uid": card_uid }, "issue": "no_source", 
					"spotted": { "block": card_block, "tx_id": tx_id, "action": transfer_action, "issue_details": { "player": card_from, "target": card_to } } }
			json.dump( err_msg, f ) 
			f.write("\n")
			
		if ( excst.MINT_IFNOSOURCE and card_id != "" and card_id != "none" ):
			(is_pack, card_name, card_rank, card_num) = ex_GetAssetDetails(card_id)
			card_elite = ex_IsElite(card_id)
			db_Card_Mint( card_from, card_id, card_num, card_uid, -1, card_elite, 0, card_block, "no_source" )	
			db_Card_Add_Missing( card_from, card_id, card_uid, card_num, card_elite, card_block )
			
			if ( card_from != "elindos" and card_from != "exolindos" ):
				if ( card_id in excst.MINT_NUM_NOSOURCE ):
					excst.MINT_NUM_NOSOURCE[card_id] = excst.MINT_NUM_NOSOURCE[card_id] + 1
				else:
					excst.MINT_NUM_NOSOURCE[card_id] = 1
			
			return [ True, -1, True, card_block, card_elite ]
		else:
			db_Card_Add_Missing( card_from, "", card_uid, 0, 0, card_block )
			return [ False, cInfo['mint'], cInfo['exist'], cInfo['block'], cInfo['elite'] ]
		
	if ( cInfo['burn'] == 1 and not bypass ):
		with open('logs/card_error.json', 'a') as f:
			err_msg = { "card": { "id": card_id, "uid": card_uid }, "issue": "already_burnd", 
					"spotted": { "block": card_block, "tx_id": tx_id, "action": transfer_action, "issue_details": { "owner": cInfo['owner'], "player": card_from, "target": card_to } } }
			json.dump( err_msg, f ) 
			f.write("\n")
		return [ False, cInfo['mint'], cInfo['exist'], cInfo['block'], cInfo['elite'] ]
		
	if ( card_from != "market"  and not bypass and cInfo['owner'] != card_from ):
		with open('logs/card_error.json', 'a') as f:
			err_msg = { "card": { "id": card_id, "uid": card_uid }, "issue": "incorrect_owner", 
					"spotted": { "block": card_block, "tx_id": tx_id, "action": transfer_action, "issue_details": { "owner": cInfo['owner'], "player": card_from, "target": card_to } } }
			json.dump( err_msg, f ) 
			f.write("\n")
		return [ False, cInfo['mint'], cInfo['exist'], cInfo['block'], cInfo['elite'] ]
	
	return [ True, cInfo['mint'], cInfo['exist'], cInfo['block'], cInfo['elite'] ]
	
def db_Card_Apply_Burn( card_burner, card_id, card_uid, card_block, tx_id, bypass=False ):
	
	msg = ""	
	cInfo = db_Card_IsTransferable( card_burner, "burn", card_id, card_uid, card_block, tx_id, "burn", bypass )
	#if ( not cInfo[0] ):
	#	return msg
	if ( not cInfo[2] or int(card_block) < int(cInfo[3]) ):
		return msg
		
	db_Card_Burn( card_uid, card_block, 1, card_burner )
	
	card_mint = cInfo[1]
	card_elite = cInfo[4]
	(is_pack, card_name, card_rank, card_num) = ex_GetAssetDetails(card_id)
	if ( (card_mint > 0 and card_mint <= 10) or (int(card_elite) == 1) or (card_rank >= 2) or (card_rank == -1) ):
		if ( card_elite == 1 ):
			msg_elite = "an **Elite "
		else:
			msg_elite = "a **"
				
		msg_rarity = "Common"
		if ( card_rank == 1 ):
			msg_rarity = "Rare"
		elif ( card_rank == 2 ):
			msg_rarity = "Epic"
		elif ( card_rank == 3 ):
			msg_rarity = "Legendary"
		elif ( card_rank == -1 ):
			msg_rarity = "???"
			
		msg = ":fire: {player} burn {elite}{name}** [*{rarity}*] (**{mint}**/{mint} *uid={uid})*".format(player=card_burner,elite=msg_elite,name=card_name, rarity=msg_rarity, mint=card_mint, uid=card_uid)
	
	return msg
	
def db_Card_Apply_Transfer( card_prev_owner, card_new_owner, card_id, card_uid, card_block, tx_id, bypass=False ):

	msg = ""
	
	if ( card_new_owner == 'null' ):
		msg = db_Card_Apply_Burn( card_prev_owner, card_id, card_uid, card_block, tx_id, bypass )
		return msg
	else:
		cInfo = db_Card_IsTransferable( card_prev_owner, card_new_owner, card_id, card_uid, card_block, tx_id, "transfer", bypass )
		#if ( not cInfo[0] ):
		#	return False
		if ( not cInfo[2] or int(card_block) < int(cInfo[3]) ):
			return msg
					
		db_Card_Transfer( card_uid, card_block, card_new_owner )
		
		card_mint = cInfo[1]
		card_elite = cInfo[4]
		(is_pack, card_name, card_rank, card_num) = ex_GetAssetDetails(card_id)
		if ( card_new_owner == "exoderewardspool" ):
			if ( card_elite == 1 ):
				msg_elite = "an **Elite "
			else:
				msg_elite = "a **"
					
			msg_rarity = "Common"
			if ( card_rank == 1 ):
				msg_rarity = "Rare"
			elif ( card_rank == 2 ):
				msg_rarity = "Epic"
			elif ( card_rank == 3 ):
				msg_rarity = "Legendary"
			elif ( card_rank == -1 ):
				msg_rarity = "???"
				
			msg = ":gift: {player} gave {elite}{name}** [*{rarity}*] (**{mint}**/{mint} *uid={uid})* to the EXODE Reward Pool (*@exoderewardspool*)! :tada:".format(player=card_prev_owner,elite=msg_elite,name=card_name, rarity=msg_rarity, mint=card_mint, uid=card_uid)
		
	
	return msg
	
#########################################################################################

def db_Sale_GetDetails( asset_uid, sale_sold, sale_block, sale_seller="" ):

	cursor = fDataBase.db_Cursor()
	
	query = ("SELECT seller, price, sold, cancel FROM exode_sales "
		 "WHERE asset_uid = %s and sold = %s and block < %s ORDER BY block DESC LIMIT 1" )	
	
	cursor.execute(query, (asset_uid,sale_sold,sale_block))
	m_output = cursor.fetchall()
	
	if ( cursor.rowcount != 0 ):	
		sale_exist  = True
		sale_seller = m_output[0][0]
		sale_price  = float(m_output[0][1])
		sale_sold   = int(m_output[0][2])
		sale_cancel = int(m_output[0][3])
	else:
		sale_exist  = False
		sale_seller = ""
		sale_price  = 0.0
		sale_sold   = 0
		sale_cancel = 0
		
	output = { 'exist': sale_exist, 'seller': sale_seller, 'price': sale_price, 'sold': sale_sold, 'cancel': sale_cancel }
			
	cursor.reset()
	cursor.close()
	
	return output
	
def db_Sale_Add( sale_seller, asset_id, asset_uid, sale_tx, sale_price, sale_sold, sale_buyer, sale_block, sale_time ):

	cursor = fDataBase.db_Cursor()
	
	query = ("INSERT INTO exode_sales "
		"(seller, asset_type, asset_uid, price, tx_id, sold, buyer, block, block_update, time_update) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
				
	cursor.execute(query, (sale_seller, asset_id, asset_uid, sale_price, sale_tx, sale_sold, sale_buyer, sale_block, sale_block, sale_time) )
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()
	
def db_Sale_Sold( asset_uid, asset_id, sale_tx, sale_sold, sale_buyer, sale_block, sale_time ):

	cursor = fDataBase.db_Cursor()
	
	query = ("UPDATE exode_sales "
		"SET buyer = %s, sold = %s, asset_type = %s, block_update = %s, time_update = %s "
		"WHERE asset_uid = %s and sold = %s and block < %s and cancel = %s") 
		
	cursor.execute(query, (sale_buyer, sale_sold, asset_id, sale_block, sale_time, asset_uid, 0, sale_block, 0) )
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()
	
def db_Sale_Cancel( asset_uid, sale_seller, sale_block, sale_time ):

	cursor = fDataBase.db_Cursor()
	
	query = ("UPDATE exode_sales "
		"SET cancel = %s, block_update = %s, time_update = %s "
		"WHERE seller = %s and asset_uid = %s and sold = %s and block < %s and block = block_update and cancel = %s")  	
		
	cursor.execute(query, (1, sale_block, sale_time, sale_seller, asset_uid, 0, sale_block, 0) )
	fDataBase.db_Commit()
	
	cursor.reset()
	cursor.close()
	
def db_Sale_Apply_New( sale_seller, asset_id, asset_uid, sale_block, sale_time, sale_tx, sale_price, sale_sold, sale_buyer ):

	# Check asset
	(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails(asset_id)
	if ( not is_pack ):
		cInfo = db_Card_IsTransferable( sale_seller, "market", asset_id, asset_uid, sale_block, sale_tx, "sale" )
		if ( not cInfo[0] ):
			return False
		
	sInfo = db_Sale_GetDetails( asset_uid, 0, sale_block )		
	if ( sInfo['exist'] and sInfo['cancel'] == 0 ):
	
		if ( sale_seller != sInfo['seller'] ):
			with open('logs/sale_error.json', 'a') as f:
				err_msg = { "sale": { "seller": sale_seller, "buyer": sale_buyer, "sold": sale_sold, "card": { "id": asset_id, "uid": asset_uid } }, "issue": "duplicate_sale", "spotted": {"action": "create_sale", "block": sale_block, "tx_id": sale_tx}, "current_seller": sInfo['seller'] } 
				json.dump( err_msg, f ) 
				f.write("\n")
			return False
		elif( sale_seller != "market" ):
			db_Sale_Cancel( asset_uid, sale_seller, sale_block, sale_time )
	
	db_Sale_Add( sale_seller, asset_id, asset_uid, sale_tx, sale_price, sale_sold, sale_buyer, sale_block, sale_time )
		
	return True
	
def db_Sale_Apply_Cancel( sale_seller, asset_id, asset_uid, sale_block, sale_time, sale_tx, transfert_cancel=False ):

	# Check asset
	(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails(asset_id)
	if ( not is_pack and not transfert_cancel ):
		cInfo = db_Card_IsTransferable( sale_seller, "market", asset_id, asset_uid, sale_block, sale_tx, "sale-cancel" )
		if ( not cInfo[0] ):
			return False
		
	sInfo = db_Sale_GetDetails( asset_uid, 0, sale_block )
	
	if ( (not sInfo['exist'] or sInfo['cancel'] == 1) and transfert_cancel ):
		#Skip
		return True
	elif ( not sInfo['exist'] ):
		with open('logs/sale_error.json', 'a') as f:
			err_msg = { "sale": { "seller": sale_seller, "buyer": "", "sold": 0, "card": { "id": asset_id, "uid": asset_uid } }, "issue": "unknown_sale", "spotted": {"action": "cancel_sale", "block": sale_block, "tx_id": sale_tx} } 
			json.dump( err_msg, f ) 
			f.write("\n")
		return False
	elif ( sInfo['cancel'] == 1 ):
		with open('logs/sale_error.json', 'a') as f:
			err_msg = { "sale": { "seller": sale_seller, "buyer": "", "sold": 0, "card": { "id": asset_id, "uid": asset_uid } }, "issue": "already_cancelled", "spotted": {"action": "cancel_sale", "block": sale_block, "tx_id": sale_tx} } 
			json.dump( err_msg, f ) 
			f.write("\n")
		return False
	elif ( sInfo['seller'] != sale_seller ):
		with open('logs/sale_error.json', 'a') as f:
			err_msg = { "sale": { "seller": sale_seller, "buyer": "", "sold": 0, "card": { "id": asset_id, "uid": asset_uid } }, "issue": "incorrect_seller", "spotted": {"action": "cancel_sale", "seller": sInfo['seller'], "block": sale_block, "tx_id": sale_tx} } 
			json.dump( err_msg, f ) 
			f.write("\n")
		return False
	else:
		db_Sale_Cancel( asset_uid, sale_seller, sale_block, sale_time )
		
	return True
	
def db_Sale_Apply_Sold( sale_seller, asset_id, asset_uid, sale_block, sale_time, sale_tx, sale_sold, sale_buyer ):

	# Check asset, created it if needed
	is_pack = ex_IsPack( asset_id )
	if ( not is_pack ):
		cInfo = db_Card_IsTransferable( sale_seller, sale_buyer, asset_id, asset_uid, sale_block, sale_tx, "sale-sold" )
	
	sInfo = db_Sale_GetDetails( asset_uid, 0, sale_block )
	if ( not sInfo['exist'] ):
		with open('logs/sale_error.json', 'a') as f:
			err_msg = { "sale": { "seller": sale_seller, "buyer": sale_buyer, "sold": sale_sold, "card": { "id": asset_id, "uid": asset_uid } }, "issue": "unknown_sale", "spotted": {"action": "complete_sale", "block": sale_block, "tx_id": sale_tx} } 
			json.dump( err_msg, f ) 
			f.write("\n")
		return [ False, "", 0.0 ]
	elif ( sInfo['cancel'] == 1 ):
		with open('logs/sale_error.json', 'a') as f:
			err_msg = { "sale": { "seller": sale_seller, "buyer": "", "sold": 0, "card": { "id": asset_id, "uid": asset_uid } }, "issue": "already_cancelled", "spotted": {"action": "cancel_sale", "block": sale_block, "tx_id": sale_tx} } 
			json.dump( err_msg, f ) 
			f.write("\n")
		return [ False, "", 0.0 ]
	else:
		db_Sale_Sold( asset_uid, asset_id, sale_tx, 1, sale_buyer, sale_block, sale_time)
		
	return [ True, sInfo['seller'], sInfo['price'] ]
	
	
def db_Sale_GetAverageSoldPrice(mID=""): 

	if ( mID == "" ):
		return -1.0

	cursor = fDataBase.db_Cursor()
	
	query = ("SELECT AVG(price) from exode_sales "
		"WHERE asset_type = %s and sold = %s and price != 0.")  
		 
	cursor.execute(query, (mID,1) )
	m_out = cursor.fetchall()
	
	if ( m_out[0][0] != None ):
		m_price = float(m_out[0][0])
	else: 
		m_price = -1.0
		
	cursor.reset()
	cursor.close()
	
	return m_price
	
def db_Sale_GetLastSoldPrice(mID=""): 

	if ( mID == "" ):
		return -1.0

	cursor = fDataBase.db_Cursor()
	
	query = ("SELECT price from exode_sales "
		"WHERE asset_type = %s and sold = %s and price != 0. ORDER BY block_update DESC")  
		 
	cursor.execute(query, (mID,1) )
	m_out = cursor.fetchall()
	
	if (  cursor.rowcount != 0 ):
		m_price = float(m_out[0][0])
	else: 
		m_price = -1.0
		
	cursor.reset()
	cursor.close()
	
	return m_price
			
#########################################################################################

def db_ExodePlayers_List():
	
	#Complete list first
	db_Player_CompleteList(True)
	
	cursor = fDataBase.db_Cursor()
		
	cursor.reset()
	
	query = "SELECT player FROM exode_player "	
	cursor.execute(query)		
	m_output = cursor.fetchall()
	
	m_player_out = []
	if ( cursor.rowcount > 0 ):
		for iPlayer in range(cursor.rowcount):
			m_player_out.append( m_output[iPlayer][0] )
				
	print("Found players in exode_player: ", cursor.rowcount )
		
	cursor.reset()
	cursor.close()

	return m_player_out
	
	

#########################################################################################

def db_Cancel_GetTXs(): 

	cursor = fDataBase.db_Cursor()
	
	query = ("SELECT cancelled_tx_id FROM exode_cancel ")
		 
	cursor.execute(query)
	m_tx = cursor.fetchall()
	
		
	m_tx_out = []
	if ( cursor.rowcount > 0 ):
		for iTx in range(cursor.rowcount):
			if ( m_tx[iTx][0] != "last_block" ):
				m_tx_out.append( m_tx[iTx][0] )
	
	cursor.reset()
	cursor.close()
	
	return m_tx_out
	

def db_Cancel_GetLastBlock(): 

	cursor = fDataBase.db_Cursor()
	
	query = ("SELECT MAX(block) FROM exode_cancel ")
		 
	cursor.execute(query)
	m_out = cursor.fetchall()
	
	if ( m_out[0][0] != None ):
		m_block = m_out[0][0]
	else: 
		m_block = 0
		
	cursor.reset()
	cursor.close()
	
	return m_block
	
def db_Cancel_SetLastBlock( tBlock ): 

	cursor = fDataBase.db_Cursor()
	
	dummy_id = "last_block"
	
	query = ("SELECT cancelled_tx_id, block FROM exode_cancel "
		 "WHERE cancelled_tx_id = %s ")
		 
	cursor.execute(query, (dummy_id, ) )
	m_output = cursor.fetchall()
	
	if ( cursor.rowcount != 0 ):
		query_block = ("UPDATE exode_cancel "
					"SET block = %s "
					"WHERE cancelled_tx_id = %s") 
					
	else:
		
		query_block = ("INSERT INTO exode_cancel "
					"(block, cancelled_tx_id) "
					"VALUES (%s, %s)") 
	
	cursor.reset()
	cursor.execute(query_block, (tBlock, dummy_id) )
	fDataBase.db_Commit()
		
	cursor.reset()	
	cursor.close()
	
def db_Cancel_FillTX( tTxId, tBlock ): 

	cursor = fDataBase.db_Cursor()
	
	query = ("SELECT cancelled_tx_id, block FROM exode_cancel "
		 "WHERE cancelled_tx_id = %s ")
		 
	cursor.execute(query, (tTxId, ) )
	m_output = cursor.fetchall()
	
	if ( cursor.rowcount != 0 ):
		print( "transaction already cancelled: ", tTxId )
	else:
		cursor.reset()
		
		query_add_cancel = ("INSERT INTO exode_cancel "
					"(cancelled_tx_id, block) "
					"VALUES (%s, %s)") 
		      			
		cursor.execute(query_add_cancel, (tTxId, tBlock) )
		fDataBase.db_Commit()
	
	cursor.reset()	
	cursor.close()
	
#########################################################################################
	
def LoadHiveBlockChain():
	print ("HIVE: Loading blockchain")
	nodelist = NodeList()
	nodelist.update_nodes()
	nodes = nodelist.get_hive_nodes()
	bHive = Hive(node=nodes)
	print ( nodes )
	print("Hive loaded?",bHive.is_hive)
	
	return bHive		
		
##############################################################################################
	

class my_eXode_bot(discord.Client):

	######################################################################################
	
	# Parameters:
	fFast            = True
	fDoDiscord       = excst.DO_DISCORD
	
	# Variables
	fFirstBlock       = 0
	
	#
	fLoadExodeGame    = False
	fLoadMintOnly     = False
	
	fLoadPlayerMarket = False
	fReBuildDataBase  = False
	fCancelTransactionList   = []
	
	# Discord Channels
	DISC_CHANNELS_MARKET = []
	DISC_CHANNELS_PING   = []
	DISC_CHANNELS_MINT   = []
	DISC_CHANNELS_GIFT   = []
		
	######################################################################################	

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		# create the background task and run it in the background
		self.read_exode_task.start()
		
	######################################################################################		

	async def on_ready(self):
		print ("DISCORD BOT: on_ready")
		print ("DISCORD BOT: on_ready_end")
				
	######################################################################################
	
	def CheckByPass( self, mBlock ):	
		if ( not self.fReBuildDataBase or mBlock > self.fFirstBlock ):
			return False
		
		return True
		
	######################################################################################
	
	def MakeMessage_List(self, sale_seller, asset_id, asset_nb, asset_uid, asset_mint, asset_elite, sale_price):
		
		msg = ""
				
		(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails(asset_id)
		
		if ( self.fLoadPlayerMarket ):
			mSoldPrice = 0.0
			mLastPrice = 0.0
		else:
			mSoldPrice = db_Sale_GetAverageSoldPrice(asset_id)
			mLastPrice = db_Sale_GetLastSoldPrice(asset_id)
				
		if ( is_pack ):
		
			msg = ":blue_square: {seller} listed {nb} **{name}** on the market for **${price}** (average sold price: **${sold_price:.2f}**, last sold price: **${last_price:.2f}**)".format(seller=sale_seller, 
					nb=asset_nb, name=asset_name, price=sale_price,sold_price=mSoldPrice,last_price=mLastPrice)
		else:
			card_ntot_mint = -1
			if ( asset_id in excst.MINT_NUM ):
				card_ntot_mint = excst.MINT_NUM[ asset_id ]								
					
			card_elite_msg = ""
			if ( asset_elite == 1 ):
				card_elite_msg = "Elite "
					
			msg_rarity = "Common"
			if ( asset_rank == 1 ):
				msg_rarity = "Rare"
			elif ( asset_rank == 2 ):
				msg_rarity = "Epic"
			elif ( asset_rank == 3 ):
				msg_rarity = "Legendary"
			elif ( asset_rank == -1 ):
				msg_rarity = "???"
			
			msg_missing_mint=""
			if ( asset_id in excst.MINT_NUM_NOSOURCE ):
				if ( excst.MINT_NUM_NOSOURCE[asset_id] > 0 ):
					msg_missing_mint = "(+{nb_missing})".format(nb_missing=excst.MINT_NUM_NOSOURCE[asset_id])
			
			print ( "mint", asset_mint, "uid", asset_uid)		
							
			if ( asset_nb == 1 ):
				msg = ":blue_square: {seller} listed 1 **{elite}{name}** [*{rarity}*]  (**{mint}**/{ntot_mint}{missing_mint} *uid={muid})* for **${price}** (avg sold price: **${sold_price:.2f}**, last sold price: **${last_price:.2f}**)".format(seller=sale_seller, 
							name=asset_name, rarity=msg_rarity, mint=asset_mint, missing_mint=msg_missing_mint, elite=card_elite_msg, ntot_mint=card_ntot_mint, muid=asset_uid, price=sale_price,sold_price=mSoldPrice,last_price=mLastPrice)
			else:						
				msg = ":blue_square: {seller} listed {nb} **{elite}{name}** [*{rarity}*] for **${price}** (min. mint is **{mint}**/{ntot_mint}{missing_mint} *uid={muid}*) (avg sold price: **${sold_price:.2f}**, last sold price: **${last_price:.2f}**)".format(seller=sale_seller,
							nb=asset_nb, elite=card_elite_msg, missing_mint=msg_missing_mint, name=asset_name, rarity=msg_rarity, mint=asset_mint, ntot_mint=card_ntot_mint, muid=asset_uid,
							price=sale_price,sold_price=mSoldPrice,last_price=mLastPrice)
		return msg
		
	######################################################################################
	
	def ProcessTransfer( self, tx_auth, tx_type, tx_block, tx_time, tx_id, player_from, player_to, card_id, card_uid, price ):
	
		
		if ( card_id == "" ):
			cInfo = db_Card_GetDetails( card_uid )
			card_id = cInfo['id']
			if ( card_id != "" ):
				print ("Fixing card_id to", card_id )
				card_id_fix = "?" + card_id
				db_TransferTX_FixID( card_uid, card_id_fix )
		else:	
			#Remove flag
			if ( card_id[0] == "?" ):
				card_id = card_id[1:]
		
	
		print ( "Process transfer from", tx_auth, tx_type, int(tx_block), player_from, player_to, card_id, card_uid, price )
		if ( tx_auth == "exodegame" ):
			# Exodegame
			
			if ( tx_type == "exode_extinguish_flames" ):
				#Do nothing for now
				msg = ""				
				#db_Card_Burn( card_uid, tx_block, 0, player_to )
				
			elif ( tx_type == "exode_upgrade_confirmed" ):
				db_Card_Apply_Burn( player_from, card_id, card_uid, tx_block, tx_id, True )	
		
			elif ( tx_type == "exode_transfer" ):
				
				# Cancel sale if any
				db_Sale_Apply_Cancel( player_from, card_id, card_uid, tx_block, tx_time, tx_id,  True )
						
				is_pack = ex_IsPack(card_id)
				if ( is_pack ):
					db_Pack_Apply_Transfer( player_from, player_to, card_id, 1 )
				else:
					msg = db_Card_Apply_Transfer( player_from, player_to, card_id, card_uid, tx_block, tx_id, True )
		
			elif ( tx_type == "exode_market_purchase" ):
				db_Sale_Apply_Sold( player_from, card_id, card_uid, tx_block, tx_time, tx_id, 1, player_to )
				
				is_pack = ex_IsPack(card_id)
				
				if ( is_pack ):
					db_Pack_Apply_Transfer( player_from, player_to, card_id, 1 )							
				else:
					msg = db_Card_Apply_Transfer( player_from, player_to, card_id, card_uid, tx_block, tx_id, True )
		
		else:
			# Players
			if ( tx_type == "exode_market_sell" ):
				db_Sale_Apply_New( player_from, card_id, card_uid, tx_block, tx_time, tx_id, price, 0, "" )
			
			elif ( tx_type == "exode_market_cancel_sell" ):
				db_Sale_Apply_Cancel( player_from, card_id, card_uid, tx_block, tx_time, tx_id )
			elif ( tx_type == "confirm_transfer_packs" ):
				db_Pack_Apply_Transfer( player_from, player_to, card_id, int(price) )	
			elif ( tx_type == "confirm_transfer_account" ):
				db_Pack_Apply_TransferAll( player_from, player_to )
				db_Card_Apply_TransferAll( player_from, player_to, tx_block )
				
	
	def CheckJSON_Transfer( self, tVId, tVJSON, tBlock, tVAuth):
		
		tMSGOut = []
	
		if ( tVId == "exode_extinguish_flames" ):
			
			#print("[DEBUG] New gift card: ", tVJSON)
			tInst   = tVJSON[1]
			mTxId   = tInst['tx_id']
			mPlayer = tInst['recipient']
				
			if ( not self.CheckTransaction(tBlock, tVId, mTxId, "", mPlayer, tVAuth, tVAuth, tInst) ):
				return [ excst.NO_ALERT, tMSGOut ]
					
			#print( 'giftcard', mTxId, tInst['recipient'], tInst['sourceid'], tInst['receivedcardnb'] ) 
					
			l_owner   = tInst['recipient']
			l_card_id = tInst['sourceid']
			l_card_nb = int(tInst['receivedcardnb'])
			
			for iCard in range( l_card_nb ):
				db_TransferTX_Add( tVAuth, tVId, tBlock, mTxId, tVAuth, l_owner, l_card_id, "none", 0.0 )
			
			if ( not self.fLoadMintOnly ):			
				for iCard in range( l_card_nb ):
					lOut = db_Card_Apply_Mint( l_owner, l_card_id, "none", 0, 0, 0, tBlock, mTxId, self.CheckByPass( tBlock ) )					
					if ( lOut != "" ):
						tMSGOut.append(lOut)
							
			return [ excst.ALERT_MINT, tMSGOut ]	
					
		elif ( tVId == "exode_upgrade_confirmed" ):		
			#Burn card	
			#print("[DEBUG] New burn (upgrade): ", tVJSON)
							
			tInst   = tVJSON[1]
			mTxId   = tInst['tx_id']
			mPlayer = tInst['recipient']
				
			if ( not self.CheckTransaction(tBlock, tVId, mTxId, "", mPlayer, tVAuth, tVAuth, tInst) ):
				return [ excst.NO_ALERT, tMSGOut ]
				
			l_card_owner     = tInst['recipient']
			l_card_id        = tInst['globalid']
			l_card_uid       = tInst['cardid']
				
			if ( "burnedid" in tInst ):
				l_card_burn_uids = tInst['burnedid'].split(',')
			else:
				l_card_burn_uids = tInst['burnedids'].split(',')	
								
			#print( 'burn', mTxId, l_card_owner, l_card_uid, l_card_id,  l_card_burn_uids )					
			
			for iCard in range( len(l_card_burn_uids) ):
				db_TransferTX_Add( tVAuth, tVId, tBlock, mTxId, l_card_owner, "burn", l_card_id, l_card_burn_uids[iCard], 0.0 )
				
			if ( not self.fLoadMintOnly ):
				for iCard in range( len(l_card_burn_uids) ):
					lOut = db_Card_Apply_Burn( l_card_owner, l_card_id, l_card_burn_uids[iCard], tBlock, mTxId, self.CheckByPass( tBlock ) )					
					if ( lOut != "" ):
						tMSGOut.append(lOut)	
						
			return [ excst.ALERT_MINT, tMSGOut ]
				
		else:	
			with open('logs/log_unknown.log', 'a') as f:
				f.write("Type: {del_type}, Block: {block}, transaction: {del_txt}\n".format(del_type=tVId,block=tBlock,del_txt=tVJSON) )
				
		return [ excst.NO_ALERT, tMSGOut ]
	
	def CheckJSON_Player( self, tVId, tValue, tBlock, tVAuth ):
				
		tMSGOut = []
			
		if ( tVId == "exode_market_sell" ):
			# Get JSON to add new market sell			
			tVJSON  =  json.loads(tValue['json'])					
			#print("[DEBUG] New sell from : ", tVAuth, tVJSON)
						
			tInst   = tVJSON
			
			if ( "tx_id" in tInst ):
				l_sale_txid    = tInst['tx_id']
			elif ( "txid" in tInst ):
				l_sale_txid    = tInst['txid']
			else:
				return [ excst.NO_ALERT, tMSGOut ]			
							
			if ( not self.CheckTransaction(tBlock, tVId, l_sale_txid, "", tVAuth, tVAuth, tVAuth, tInst, True) ):
				return [ excst.NO_ALERT, tMSGOut ]			
			
			l_asset_seller = tVAuth
			
				
			if ( tInst['priceusd'] != "" ):
				l_sale_price   = float(tInst['priceusd'])
			else:
				l_sale_price   = 0.0
			
			if ( "uniqueids" in tInst ):						
				l_asset_uids = tInst['uniqueids'].split(',')				
			else:			
				l_asset_uids = tInst['uniqueid'].split(',')
			
			l_asset_id = ""	
			if ( "id" in tInst ):	
				l_asset_id = tInst['id']
				
			tMarketType_Pack = False
			if ( "market_type" in tInst ):
				tMarketType_Pack = (tInst['market_type'] == "pack")
					
			tIDUnknown = False
			
			l_asset_ids   = []
			l_asset_elite = []
			l_asset_mint  = []
			
			if ( tMarketType_Pack ):
				if ( l_asset_id == "" ):
					l_asset_id = "exode_????_booster"
					tIDUnknown = True
					
				for iAsset in range(len(l_asset_uids)):
					l_asset_ids.append(l_asset_id)
			else:		
				for iAsset in range(len(l_asset_uids)):
				
					cInfo = db_Card_GetDetails( l_asset_uids[iAsset] )
					# Fix card_id if possible
					if ( cInfo['id'] == "" and l_asset_id != "" ):
						cInfo['id'] = l_asset_id
						cInfo['elite'] = ex_IsElite(l_asset_id)
					
					l_asset_ids.append(cInfo['id'])
					l_asset_elite.append(cInfo['elite'])
					l_asset_mint.append(cInfo['mint'])
					
			print( 'sell', l_sale_txid, l_asset_seller, l_asset_ids, l_asset_uids, l_sale_price, tMarketType_Pack )	
			
			bOK = False
			for iAsset in range(len(l_asset_uids)):
				db_TransferTX_Add( tVAuth, tVId, tBlock, l_sale_txid, l_asset_seller, "market", l_asset_ids[iAsset], l_asset_uids[iAsset], l_sale_price )
			if ( not self.fLoadMintOnly ):
				tTime = Block(tBlock).time()
				for iAsset in range(len(l_asset_uids)):
					bOK = db_Sale_Apply_New( l_asset_seller, l_asset_ids[iAsset], l_asset_uids[iAsset], tBlock, tTime, l_sale_txid, l_sale_price, 0, "" )

			if ( not bOK ):
				return [ excst.NO_ALERT, tMSGOut ]
			
			(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails(l_asset_ids[0]) 
			

			if ( is_pack ):
										
				pack_name = asset_name
				if ( tIDUnknown ):
					pack_name = pack_name + " (?)"
				
				lOut = self.MakeMessage_List(l_asset_seller, l_asset_ids[0], len(l_asset_uids), "", -1, 0, l_sale_price)
				tMSGOut.append(lOut)
							
			else:
									
				card_nb = 0
				prev_id = ""
				
				card_nb    = 0
				prev_id    = ""
				card_elite = 0
				card_mint  = -1
				
				card_mint_low = 0
				card_uid_low  = ""
				
				for iAsset in range(len(l_asset_uids)):
				
					if ( card_nb > 0 and prev_id != l_asset_ids[iAsset] ):
						
						lOut = self.MakeMessage_List(l_asset_seller, prev_id, card_nb, card_uid_low, card_mint_low, card_elite, l_sale_price)
						tMSGOut.append(lOut)
						
						card_nb = 0
						card_mint_low = 0
						card_uid_low  = ""
					
					
					card_nb    = card_nb + 1
					prev_id    = l_asset_ids[iAsset]
					card_elite = l_asset_elite[iAsset]
					card_mint  = l_asset_mint[iAsset]
					card_muid  = l_asset_uids[iAsset]
					
					if ( card_nb == 1 or (card_mint > 0 and (card_mint < card_mint_low or card_mint_low <= 0)) ):
						card_mint_low = card_mint
						card_uid_low = card_muid
				
				if ( card_nb > 0 ):
					lOut = self.MakeMessage_List(l_asset_seller, prev_id, card_nb, card_uid_low, card_mint_low, card_elite, l_sale_price)
					tMSGOut.append(lOut)
			
			return [ excst.ALERT_MARKET, tMSGOut ]
							
						
		elif ( tVId == "exode_market_cancel_sell" ):
			# Get JSON to add new market sell			
			tVJSON  =  json.loads(tValue['json'])					
			#print("[DEBUG] New sell from : ", tVAuth, tVJSON)
						
			tInst   = tVJSON			
				
			l_sale_txid    = tInst['txid']
			l_asset_seller = tVAuth
			l_asset_id     = tInst['id']
			l_sale_price   = 0.0
			
			
			if ( "uniqueid" in tInst ):						
				l_asset_uid = tInst['uniqueid']				
			else:			
				l_asset_uid = tInst['uniqueids']
				print("[DEBUG] New cancel from : ", tVAuth, tVJSON)
				return [ excst.ALERT_KILL, tMSGOut ]	
				
			if ( not self.CheckTransaction(tBlock, tVId, l_sale_txid, l_asset_uid, tVAuth, tVAuth, tVAuth, tInst, True) ):
				return [ excst.NO_ALERT, tMSGOut ]	
				
			
			print( 'cancelsell', l_sale_txid, l_asset_seller, l_asset_id, l_asset_uid )
			
			bOK = False
			db_TransferTX_Add( tVAuth, tVId, tBlock, l_sale_txid, l_asset_seller, l_asset_seller, l_asset_id, l_asset_uid, 0.0 )
			
			if ( not self.fLoadMintOnly ):	
				tTime = Block(tBlock).time()
				bOK = db_Sale_Apply_Cancel( l_asset_seller, l_asset_id, l_asset_uid, tBlock, tTime, l_sale_txid )
				
			if ( not bOK ):
				return [ excst.NO_ALERT, tMSGOut ]
				
			(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails(l_asset_id) 

			if ( is_pack ):
						
				pack_name                               = asset_name
				
				lOut = ":purple_square: {seller} unlisted {nb} **{name}** on the market".format(seller=l_asset_seller, nb=1, name=pack_name)
				tMSGOut.append(lOut)
							
			else:
						
				card_name = asset_name
				card_muid = l_asset_uid
				cInfo = db_Card_GetDetails( card_muid )
				
				card_elite     = cInfo['elite']
				card_mint      = cInfo['mint']	
				card_ntot_mint = excst.MINT_NUM[ l_asset_id ]
										
				msg_missing_mint=""
				if ( l_asset_id in excst.MINT_NUM_NOSOURCE ):
					if ( excst.MINT_NUM_NOSOURCE[l_asset_id] > 0 ):
						msg_missing_mint = "(+{nb_missing})".format(nb_missing=excst.MINT_NUM_NOSOURCE[l_asset_id])	
																						
				card_elite_msg = ""
				if ( card_elite == 1 ):
					card_elite_msg = "Elite "
					
				msg_rarity = "Common"
				if ( asset_rank == 1 ):
					msg_rarity = "Rare"
				elif ( asset_rank == 2 ):
					msg_rarity = "Epic"
				elif ( asset_rank == 3 ):
					msg_rarity = "Legendary"
				elif ( asset_rank == -1 ):
					msg_rarity = "???"
				
				lOut = ":purple_square: {seller} unlisted 1 **{elite}{name}** [*{rarity}*] (**{mint}**/{ntot_mint}{missing_mint} *uid={muid}*)".format(seller=l_asset_seller, 
								name=card_name, rarity=msg_rarity, mint=card_mint, missing_mint=msg_missing_mint, elite=card_elite_msg, ntot_mint=card_ntot_mint, 
								muid=card_muid)
				tMSGOut.append(lOut)
						
			return [ excst.ALERT_MARKET, tMSGOut ]
						
							
		elif ( tVId == "exode_market_transfer" ):
			# Ownership is set by exodegame, ignore
			return [ excst.NO_ALERT, tMSGOut ]
			
		return [ excst.NO_ALERT, tMSGOut ]		
	
	
	def CheckTransaction( self, mBlock, mType, mTxId, mUId, mPlayer, mFrom, mAuth, mTransaction, mCancel=False ):
		if ( mTxId == "" ):
			mTxId = "{player}.{block}".format(player=mPlayer,block=mBlock)

		tInfo = db_TX_GetDetails(mTxId,mUId,mType,mPlayer)
		if ( tInfo['exist'] ):					
			if ( not self.CheckByPass( mBlock ) ):
				with open('logs/transaction_duplicate.json', 'a') as f:
					err_msg = { "transaction": { "type": mType, "block": mBlock, "tx_id": mTxId }, "issue": "duplicate_transaction", 
						"transaction_details": mTransaction }
					json.dump( err_msg, f ) 
					f.write("\n")
			return False
				
		db_TX_Add( mTxId, mUId, mType, mBlock, mPlayer, mFrom, mAuth )
		
		if ( mTxId in self.fCancelTransactionList and not mCancel ):
			print("[WARNING] Cancelled transaction ", mType, mTxId)
			self.fCancelTransactionList.remove(mTxId)
			db_TX_Cancel( mTxId, mUId, mType, mPlayer )
		
			with open('logs/transaction_cancelled.json', 'a') as f:
				err_msg = { "transaction": { "type": mType, "block": mBlock, "tx_id": mTxId }, "issue": "transaction_cancelled", 
					"transaction_details": mTransaction }
				json.dump( err_msg, f ) 
				f.write("\n")
			return False	
					
		return True
		
	
	def ReadJSONTransaction(self,tValue,tBlock):
		
		tMSGOut    = [ ]
		#Get user (player or exodegame) and transaction type
		tVId    = tValue['id']
		tVAuth  = tValue['required_posting_auths'][0]
		
		if ( tVAuth == "exodegame" ):
			# Only eXodegame can send these transactions		
			tVJSON  =  json.loads(tValue['json'])			
										
			if ( tVId == "exode_openpack" or tVId == "exode_dropdelivery" ):
				# Get JSON to add new cards/packs
				#start = timer()
				#print("[DEBUG] New cards (open pack): ", tVJSON)	
							
				tInst   = tVJSON[1]
				mTxId   = tInst['tx_id']
				mPlayer = tInst['recipient']
				
				l_source_uids = [ "none" ]
				if ( "sourceuniqueid" in tInst ):
					l_source_uids = tInst['sourceuniqueid'].split(',')
				
				if ( mTxId == "" and l_source_uids[0] != "none" ):
					mTxId = l_source_uids[0]
				
				if ( not self.CheckTransaction(tBlock, tVId, mTxId, "", mPlayer, tVAuth, tVAuth, tInst) ):
					return [ excst.NO_ALERT, tMSGOut ]
												
				l_owner      = mPlayer
				l_card_ids   = tInst['receivedcardids'].split(',')
				l_card_uids  = tInst['receivedcarduniqueids'].split(',')
								
				if ( "receivedcardiselite" in  tInst ):
					l_card_elite = tInst['receivedcardiselite'].split(',')
				else:
					l_card_elite = [ 0 for i in range(len(l_card_uids))]
				
				l_pack_ids   = tInst['receivedpackids'].split(',')
				
				l_source_id  = tInst['sourceid']
				
				iPack_nb = 0
				
				#print( 'new', mTxId, l_owner, l_pack_ids, l_card_ids, l_card_uids, l_card_elite, l_source_id, l_source_uids )	
				if ( l_source_id == "exode_alpha_booster" ):
					iPack_nb = len(l_card_ids)/5
				elif (	   l_source_id == "exode_alpha_contract_rekatron" 
					or l_source_id == "exode_alpha_contract_syndicate" 
					or l_source_id == "exode_alpha_contract_tom" ):
					#Ignore
					iPack_nb = 0
				elif (     l_source_id == "exode_alpha_starter_4" ):
					iPack_nb = len(l_pack_ids)/3
				elif (	   l_source_id == "exode_alpha_starter_3"
					or l_source_id == "exode_alpha_starter_2"
					or l_source_id == "exode_alpha_starter_1" ):
					iPack_nb = len(l_card_ids)/14					
				elif (     l_source_id == "exode_alpha_pack_crew_galvin4" ):
					iPack_nb = len(l_card_ids)/3
				elif (     l_source_id == "exode_alpha_pack_crew_kb119" ):
					iPack_nb = len(l_card_ids)/2
				elif (	   l_source_id == "exode_alpha_character_pack_nomad"
					or l_source_id == "exode_alpha_character_pack_genetician"
					or l_source_id == "exode_alpha_character_pack_drachian" ):
					iPack_nb = len(l_card_ids)
				elif (	   l_source_id == "exode_alpha_character_pack_suntek" ):
					iPack_nb = len(l_card_ids)/2
				elif (	   l_source_id == "exode_alpha_support_ionguards" 
					or l_source_id == "exode_alpha_support_vega" ):
					iPack_nb = len(l_card_ids)/5
				elif (	   l_source_id == "exode_alpha_support_tom" ):
					iPack_nb = len(l_card_ids)/3	
				elif (	   l_source_id == "exode_card_261_actionImmediateOrder" ):
					#ignore
					iPack_nb = 0					
				else:
					print("[ERROR] New card, unknown pack", l_owner, l_pack_ids, l_card_ids, l_card_uids, l_card_elite, l_source_id, l_source_uids)				
					return [ excst.ALERT_KILL, tMSGOut ]
					
				if ( iPack_nb > 0 ):
					db_Pack_Apply_Update(l_owner, l_source_id, -1*iPack_nb, iPack_nb )
				
				for iPack in range( len(l_pack_ids) ):
					if ( l_pack_ids[iPack] == "" ):
						continue						
					db_Pack_Apply_Update(l_owner, l_pack_ids[iPack], 1, 0 )
					
				for iCard in range( len(l_card_ids) ):
					if ( l_card_ids[iCard] == "" ):
						continue
					lOut = db_Card_Apply_Mint( l_owner, l_card_ids[iCard], l_card_uids[iCard], 0, l_card_elite[iCard], 0, tBlock, mTxId, self.CheckByPass( tBlock )  )
					
					if ( lOut != "" ):
						tMSGOut.append(lOut)
						
				return [ excst.ALERT_MINT, tMSGOut ]
				#end = timer()				
				#print ( "New pack took ", (end-start) )										
			
			elif ( tVId == "exode_contract_dropready" ):
				# contract dropready
				# SKIP!
				return [ excst.NO_ALERT, tMSGOut ]
				
			elif ( 	tVId == "exode_newpacks"	or tVId == "for_community_rewards"
				or 	tVId == "exode_bonuspacks" 	or tVId == "community_gift" 
				or 	tVId == "battlegames_ama" 	or tVId == "community_planetary_challenge" 
				or 	tVId == "contest_rewards"	or tVId == "battlegames_witness"
				or 	tVId == "inventory_transform"	or tVId == "inventory_transform_all" 
				or 	tVId == "evacuationChallenge_2020_11" 
				or	tVId == "for_community_events" or tVId == "art_payment"  ):
				# Details: 
				# Type: inventory_transform_all, Block: 42667828, transaction: 
				# ['inventory_transform_all', 
				#	{'recipient': 'bearbear613', 'typeids': 'exode_alpha_starter_4', 'typenbs': '1', 'base_value': '20', 
				#	'tx_id': '1f4a819c2db0f6627b204fdc0585df5a', 'source': '1c36111462af9608d6483ad1dfe578c1', 'app_tx': '3b45b4392dcf1957ead42082a0628552'}]
				# Type: inventory_transform, Block: 42667866, transaction: 
				# ['inventory_transform', 
				#	{'recipient': 'bearbear613', 'typeids': 'exode_alpha_booster', 'typenbs': '60', 'base_value': '180', 
				#	'tx_id': '9038f94a980f6667f87a7665758c1b2b', 'source': '6adae41cec5db65f0a2bbe08a5c31353', 'app_tx': '3b45b4392dcf1957ead42082a0628552'}]
				# Type: battlegames_witness, Block: 43920851, transaction: 
				# ['battlegames_witness', 
				#	{'recipient': 'agr8buzz', 'typeids': 'exode_alpha_booster', 'typenbs': '6', 'base_value': '18', 
				#	'tx_id': '57c7149e2fb2e9174813138fc54cc99e', 'source': '30e9b871286da19bd704f415c0e89338', 'app_tx': '3b45b4392dcf1957ead42082a0628552'}]
				# Type: battlegames_witness, Block: 43920868, transaction: 
				# ['battlegames_witness', 
				#	{'recipient': 'agr8buzz', 'typeids': 'exode_alpha_starter_4', 'typenbs': '2', 'base_value': '40', 
				#	'tx_id': '6e22cf5bbfcef2f75edb1accb30e8c14', 'source': '3a4b5ed88f9887ed213652aa34bbdd25', 'app_tx': '3b45b4392dcf1957ead42082a0628552'}]
				# Type: for_community_rewards, Block: 45006698, transaction: 
				# ['for_community_rewards', 
				#	{'recipient': 'balticbadger', 'typeids': 'exode_alpha_booster', 'typenbs': '11', 'base_value': '33', 
				#	'tx_id': '07e02f47e7614b82d61c9439eab10f48', 'source': 'f3410ef02954d39feec23eb40ea2328f', 'app_tx': '3b45b4392dcf1957ead42082a0628552'}]
				
				# Get JSON to add new pack
				#print("[DEBUG] New pack: ", tVJSON)
							
				tInst   = tVJSON[1]
				mTxId   = tInst['tx_id']
				mPlayer = tInst['recipient']
				
				if ( not self.CheckTransaction(tBlock, tVId, mTxId, "", mPlayer, tVAuth, tVAuth, tInst) ):
					return [ excst.NO_ALERT, tMSGOut ]
						
				#print( 'pack', mTxId, tInst['recipient'], tInst['typeids'].split(','), tInst['typenbs'].split(',') ) 
				
				l_player  = mPlayer
				l_pack_id = tInst['typeids'].split(',')
				l_pack_nb = tInst['typenbs'].split(',')
				
				for iPack in range( len(l_pack_id) ):
					if ( l_pack_id[iPack] == "" or l_pack_nb[iPack] == "" ):
						continue
							
					db_Pack_Apply_Update(l_player, l_pack_id[iPack], l_pack_nb[iPack], 0 )
					
			elif ( tVId == "exode_reward_medal" ):
				#exode_reward_medal ['exode_reward_medal', {'recipient': 'raudell', 'medal_title': 'Winner of the Ocean World (Planetary Challenge, July 2020)', 'medal_globalid': '', 'medal_nft': '', 'medal_picture': '', 'tx_id': '', 'app_tx': '3b45b4392dcf1957ead42082a0628552'}]
				return [ excst.NO_ALERT, tMSGOut ]
				#TODO
			elif ( tVId == "exode_cancel_test_transaction" ):
				tInst   = tVJSON[1]
				mTxId   = tInst['tx_id']
				
				if ( not self.CheckTransaction(tBlock, tVId, mTxId, "", tVAuth, tVAuth, tVAuth, tInst, True) ):
					return [ excst.NO_ALERT, tMSGOut ]
								
				db_Cancel_FillTX( mTxId, tValue['block'] )	
				
			elif (	   tVId == "for_development_test" 	or tVId == "for_development"
				or tVId == "artist_payment" 		or tVId == "follow" 
				or tVId == "market_test_booster" 	or tVId == "exode_delivery" ):		
				# SKIP
				return [ excst.NO_ALERT, tMSGOut ]
			else:
				#Deal with burn
				return self.CheckJSON_Transfer( tVId, tVJSON, tBlock, tVAuth)
		else:
			return self.CheckJSON_Player( tVId, tValue, tBlock, tVAuth )
				
		return [ excst.NO_ALERT, tMSGOut ]

	######################################################################################

	def ReadTransfert(self,tValue,tBlock):

		tMSGOut = []
		tFrom   = tValue['from']
		tTo     = tValue['to']
		tMemo   = tValue['memo'].split(":")
		tAuth   = "exodegame" # For CheckTransaction mass transfers, in order to avoid missing player transaction later
		
		
		#if (	   tFrom == "elindos"   or tTo == "elindos" 
		#	or tFrom == "exolindos" or tTo == "exolindos"  ):
		#	#Test accounts
		#	return [ 0, tMSGOut ]	
		
		if ( tFrom == "exodegame" ):
			if ( tMemo[0] == "exodegame" ):
			
				tType = tMemo[1]
			
				if ( tType == "exode_transfer" ):
					
					mMemo = tMemo[2].split(" ")
					mFrom = mMemo[-1]
					mUID  = tMemo[4]
					mID   = tMemo[5]
					mTxId = tMemo[8]
					
					
					if ( not self.CheckTransaction(tBlock, tType, mTxId, mUID, tTo, mFrom, tAuth, tMemo) ):
						return [ excst.NO_ALERT, tMSGOut ]	
					
					db_TransferTX_Add( tFrom, tType, tBlock, mTxId, mFrom, tTo, mID, mUID, 0.0 )
					
					if ( not self.fLoadMintOnly ):
						# Cancel sale if any			
						tTime = Block(tBlock).time()
						
						bOK = db_Sale_Apply_Cancel( mFrom, mID, mUID, tBlock, tTime, mTxId, True )
						
						lOut = ""
						(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails( mID )
						if ( is_pack ):
							print('pack-transfer', mTxId, mFrom, tTo, mID, mUID )
							db_Pack_Apply_Transfer( mFrom, tTo, mID, 1 )
							
							if ( tTo == "exoderewardspool" ):
								lOut = ":gift: {giver} gave 1 **{name}** to the EXODE Reward Pool  (*@exoderewardspool*)! :tada:".format(giver=mFrom, name=asset_name)
						else:
							print('card-transfer', mTxId, mFrom, tTo, mID, mUID )						
							lOut = db_Card_Apply_Transfer( mFrom, tTo, mID, mUID, tBlock, mTxId, self.CheckByPass( tBlock ) )
							
						if ( lOut != "" ):
							tMSGOut.append(lOut)					
					return [ excst.ALERT_GIFT, tMSGOut ]
					
				elif ( tType == "exode_market_purchase" ):
					
					mFrom = "market"
					mUID  = tMemo[4]
					mID   = tMemo[5]
					mTxId = tMemo[8]
					
					if ( not self.CheckTransaction(tBlock, tType, mTxId, mUID, tTo, mFrom, tAuth, tMemo) ):
						return [ excst.NO_ALERT, tMSGOut ]	
					
					
					db_TransferTX_Add( tFrom, tType, tBlock, mTxId, mFrom, tTo, mID, mUID, 0.0 )
						
					if ( not self.fLoadMintOnly ):				
						tTime = Block(tBlock).time()
						(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails(mID) 
					
						sInfo = db_Sale_Apply_Sold( mFrom, mID, mUID, tBlock, tTime, mTxId, 1, tTo )

						bOK          = sInfo[0]
						asset_seller = sInfo[1]
						asset_price  = sInfo[2]
											
						if ( not bOK ):
							return [ excst.NO_ALERT, tMSGOut ]	
							
		
						if ( self.fLoadExodeGame ):
							mSoldPrice = 0.0
						else:
							mSoldPrice = db_Sale_GetAverageSoldPrice(mID)
						
						if ( is_pack ):
							print('pack-buy', mTxId, mFrom, tTo, mID, mUID )
							
							pack_name = asset_name
							
							db_Pack_Apply_Transfer( asset_seller, tTo, mID, 1 )
							
							lOut = ":green_square: {buyer} bought 1 **{name}** from {seller} for **${price}** (avg sold price is **${sold_price:.2f}**)".format(buyer=tTo, name=pack_name, seller=asset_seller, price=asset_price, sold_price=mSoldPrice)
							tMSGOut.append(lOut)
							if mSoldPrice > 999.:
								if 'transaction_id' in tValue:
									lOut = f"<@!460463462464618536> <@!232962122043228160> high price sale alert! Link: https://hiveblocks.com/tx/{tValue['transaction_id']}"
								else:
									print(tValue)
									lOut = f"<@!460463462464618536> <@!232962122043228160> high price sale alert!"
								tMSGOut.append(lOut)
						else:
							print('card-buy', mTxId, mFrom, tTo, mID, mUID )
							
							cInfo = db_Card_GetDetails( mUID )
							
							card_elite     = cInfo['elite']
							card_mint      = cInfo['mint']					
							card_name      = asset_name
							card_ntot_mint = excst.MINT_NUM[ mID ]
												
							db_Card_Apply_Transfer( asset_seller, tTo, mID, mUID, tBlock, mTxId, self.CheckByPass( tBlock ) )
													
							msg_missing_mint=""
							if ( mID in excst.MINT_NUM_NOSOURCE ):
								if ( excst.MINT_NUM_NOSOURCE[mID] > 0 ):
									msg_missing_mint = "(+{nb_missing})".format(nb_missing=excst.MINT_NUM_NOSOURCE[mID])	
									
							card_elite_msg = ""
							if ( card_elite == 1 ):
								card_elite_msg = "Elite "
								
							msg_rarity = "Common"
							if ( asset_rank == 1 ):
								msg_rarity = "Rare"
							elif ( asset_rank == 2 ):
								msg_rarity = "Epic"
							elif ( asset_rank == 3 ):
								msg_rarity = "Legendary"
							elif ( asset_rank == -1 ):
								msg_rarity = "???"
												
							lOut = ":green_square: {buyer} bought 1 **{elite}{name}** [*{rarity}*] (**{mint}**/{ntot_mint}{missing_mint}  *uid={muid}*) from {seller} for **${price}** (avg sold price is **${sold_price:.2f}**)".format(buyer=tTo, name=card_name,
										 rarity=msg_rarity, elite=card_elite_msg, mint=card_mint, ntot_mint=card_ntot_mint, missing_mint=msg_missing_mint, muid=mUID, seller=asset_seller, price=asset_price,sold_price=mSoldPrice)
							if ( lOut != "" ):
								tMSGOut.append(lOut)
						
					
					return [ excst.ALERT_MARKET, tMSGOut ]
					
				elif ( tType == "exode_delivery" or tType == "exode_delivery_update" ):	
				
					mTxId = ""
					
					if ( tMemo[2] == "NFT" ):
						mUID = tMemo[3]
					elif ( tMemo[3] == "NFT" ):
						mUID = tMemo[4]
					else: 
						mUID = ""						
					
					if ( not self.CheckTransaction(tBlock, tType, mTxId, mUID, tTo, tFrom, tAuth, tMemo) ):
						return [ excst.NO_ALERT, tMSGOut ]	

					# Stop writing logs for this						
					#with open('logs/transaction_delivery.json', 'a') as f:
					#	err_msg = { "transaction": { "type": tType, "block": tBlock, "tx_id": "" },  
					#		"transaction_details": tMemo[2:] }
					#	json.dump( err_msg, f ) 
					#	f.write("\n")
			
				elif ( tType == "exode_market_rewards" or tType == "exode_market_sale" ):			
					#Add player to list, just in case
					mFrom = "market"
					mUID  = tMemo[4]
					mID   = tMemo[5]
					mTxId = tMemo[8]
					
					if ( not self.CheckTransaction(tBlock, tType, mTxId, mUID, tTo, tFrom, tAuth, tMemo) ):
						return [ excst.NO_ALERT, tMSGOut ]	
						
					db_Player_Add(tTo)
			
				elif ( tType == "exode_market_sale_manual" ):			
					#Add player to list, just in case
					mFrom = "market"
					mUID  = tMemo[2]
					mID   = tMemo[3]
					mTxId = tMemo[0]
					
					if ( not self.CheckTransaction(tBlock, tType, mTxId, mUID, tTo, tFrom, tAuth, tMemo) ):
						return [ excst.NO_ALERT, tMSGOut ]	
						
					db_Player_Add(tTo)
				else:	
					with open('logs/log_unknown_transfert.log', 'a') as f:
						f.write("From: {del_from}, To: {del_to}, Type: {del_type}, Block: {block}, memo: {del_txt}\n".format(del_from=tFrom, del_to=tTo,del_type=tType,block=tBlock,del_txt=tMemo[2:]) )
			
			else:
				with open('logs/log_unknown_transfert.log', 'a') as f:
					f.write("From: {del_from}, To: {del_to}, Type: {del_type}, Block: {block}, memo: {del_txt}\n".format(del_from=tFrom, del_to=tTo,del_type="unknown",block=tBlock,del_txt=tValue['memo']) )
			
		else: 
			tnMemo = tMemo[0].split("|")
			tType = tnMemo[0].strip()
			
			if ( tType == "confirm_transfer_packs" ):
			
				mTo = tnMemo[3].strip()
			
				if ( not self.CheckTransaction(tBlock, tType, tBlock, "", mTo, tFrom, tAuth, tnMemo) ):
					return [ excst.NO_ALERT, tMSGOut ]	
					
				pack_id = tnMemo[1].strip()
				pack_nb = int(tnMemo[2])
				
						
				print( 'mass-transfer-pack', 0, tFrom, mTo, pack_id, pack_nb )		
				
				db_TransferTX_Add( tFrom, tType, tBlock, "", tFrom, mTo, pack_id, "", pack_nb )
				
				if ( not self.fLoadMintOnly ):
					db_Pack_Apply_Transfer( tFrom, mTo, pack_id, pack_nb )
				
			elif ( tType == "confirm_transfer_account" ):
			
				mTo = tnMemo[1].strip()
				
				# fix
				if ( mTo == "birdbeak" ):
					mTo = "birdbeaksd"
					
				if ( not self.CheckTransaction(tBlock, tType, tBlock, "", mTo, tFrom, tAuth, tnMemo) ):
					return [ excst.NO_ALERT, tMSGOut ]	
					
				print( 'mass-transfer-account', 0, tFrom, mTo )
				
				
				db_TransferTX_Add( tFrom, tType, tBlock, "", tFrom, mTo, "", "", 0.0 )
				
				if ( not self.fLoadMintOnly ):
					db_Pack_Apply_TransferAll( tFrom, mTo )
					db_Card_Apply_TransferAll( tFrom, mTo, tBlock )
			else:
				with open('logs/log_unknown_transfert.log', 'a') as f:
					f.write("From: {del_from}, To: {del_to}, Type: {del_type}, Block: {block}, memo: {del_txt}\n".format(del_from=tFrom, del_to=tTo,del_type="unknown",block=tBlock,del_txt=tValue['memo']) )
			

		return [ excst.NO_ALERT, tMSGOut ]
		
	######################################################################################
		
	async def ProcessTransaction(self, tType, tBlock, hTransaction ):
	
		lOut = [ excst.NO_ALERT, [] ]
		
		if ( tType == "transfer" or tType == "transfer_operation" ):
			#transfer transaction
						
			#Get transaction From/To
			tFrom   = hTransaction['from']
			tTo     = hTransaction['to']
							
			if ( tFrom == "exodegame" or tTo == "exodegame" ):
				lOut = self.ReadTransfert(hTransaction, tBlock)
					
		elif ( tType == "custom_json" or tType == "custom_json_operation" ):
			#JSON transaction
						
			#Get transaction value
			tVAuths = hTransaction['required_posting_auths']
			if ( len(tVAuths) <= 0 ):
				return 0
							
			lOut = self.ReadJSONTransaction(hTransaction, tBlock)
			
							
		if ( lOut[0] == excst.ALERT_MINT ):
			if( len(lOut[1]) > 0 ):
				for msg in lOut[1]:
					print ( msg )
								
				await self.disc_send_msg_list( lOut[1], self.DISC_CHANNELS_MINT )
				
		elif ( lOut[0] == excst.ALERT_MARKET ):
			if( len(lOut[1]) > 0 ):
				for msg in lOut[1]:
					print ( msg )	
					
				await self.disc_send_msg_list( lOut[1], self.DISC_CHANNELS_MARKET )
							
							
		elif ( lOut[0] == excst.ALERT_GIFT ):
			if( len(lOut[1]) > 0 ):
				for msg in lOut[1]:
					print ( msg )	
					
				await self.disc_send_msg_list( lOut[1], self.DISC_CHANNELS_GIFT )
							
							
		return int(lOut[0])
				
	######################################################################################							

	async def disc_connect(self):
	
		if ( not self.fDoDiscord ):
			return
			
		DISC_CHANNELS_PING_TMP   = []
		with open('channel/ch_ping.list', 'r') as f:
			for line in f:
				if ( line[0] == "#" or line == "\n" ):
					continue
				
				ch_id = int(line)	
				DISC_CHANNEL = DISC_CLIENT.get_channel(ch_id)					
				DISC_CHANNELS_PING_TMP.append(ch_id)
				
				if ( ch_id not in self.DISC_CHANNELS_PING and DISC_CHANNEL != None ):						
					print ( "DISCORD BOT:eXode bot [PING] connected to {guild_name}".format(guild_name=DISC_CHANNEL.guild.name) )
					await DISC_CHANNEL.send("*eXode BOT [PING] is connected here!*")
					
		DISC_CHANNELS_MINT_TMP   = []			
		with open('channel/ch_mint.list', 'r') as f:
			for line in f:
				if ( line[0] == "#" or line == "\n" ):
					continue
				
				ch_id = int(line)
				DISC_CHANNEL = DISC_CLIENT.get_channel(ch_id)	
				DISC_CHANNELS_MINT_TMP.append(ch_id)
						
				if ( ch_id not in self.DISC_CHANNELS_MINT and DISC_CHANNEL != None ):						
					print ( "DISCORD BOT:eXode bot [EXODE-ALERT] connected to {guild_name}".format(guild_name=DISC_CHANNEL.guild.name) )
					await DISC_CHANNEL.send("*eXode BOT [EXODE-ALERT] is connected here!*")
					
		DISC_CHANNELS_MARKET_TMP   = []			
		with open('channel/ch_market.list', 'r') as f:
			for line in f:
				if ( line[0] == "#" or line == "\n" ):
					continue
				
				ch_id = int(line)
				DISC_CHANNEL = DISC_CLIENT.get_channel(ch_id)	
				DISC_CHANNELS_MARKET_TMP.append(ch_id)
						
				if ( ch_id not in self.DISC_CHANNELS_MARKET and DISC_CHANNEL != None ):				
					print ( "DISCORD BOT:eXode bot [MARKET-ALERT] connected to {guild_name}".format(guild_name=DISC_CHANNEL.guild.name) )
					await DISC_CHANNEL.send("*eXode BOT [MARKET-ALERT] is connected here!*")

		DISC_CHANNELS_GIFT_TMP   = []			
		with open('channel/ch_gift.list', 'r') as f:
			for line in f:
				if ( line[0] == "#" or line == "\n" ):
					continue
				
				ch_id = int(line)
				DISC_CHANNEL = DISC_CLIENT.get_channel(ch_id)	
				DISC_CHANNELS_GIFT_TMP.append(ch_id)
						
				if ( ch_id not in self.DISC_CHANNELS_GIFT and DISC_CHANNEL != None ):	
					print ( "DISCORD BOT:eXode bot [GIFT-ALERT] connected to {guild_name}".format(guild_name=DISC_CHANNEL.guild.name) )
					await DISC_CHANNEL.send("*eXode BOT [GIFT-ALERT] is connected here!*")

		self.DISC_CHANNELS_MARKET = DISC_CHANNELS_MARKET_TMP
		self.DISC_CHANNELS_MINT   = DISC_CHANNELS_MINT_TMP
		self.DISC_CHANNELS_PING   = DISC_CHANNELS_PING_TMP 
		self.DISC_CHANNELS_GIFT   = DISC_CHANNELS_GIFT_TMP
		
	async def disc_send_msg_list(self, msg_list, CHANNEL_LIST):
	
		if ( not self.fDoDiscord ):
			return
	
		for DISCORD_CHANNEL_id in CHANNEL_LIST:
			DISC_CHANNEL = DISC_CLIENT.get_channel(DISCORD_CHANNEL_id)
			
			if ( DISC_CHANNEL == None ): 
				continue
				
			for msg in msg_list:
				await DISC_CHANNEL.send(msg)	
				
	async def disc_send_msg(self, msg, CHANNEL_LIST):
		
		if ( not self.fDoDiscord ):
			return
	
		for DISCORD_CHANNEL_id in CHANNEL_LIST:
			DISC_CHANNEL = DISC_CLIENT.get_channel(DISCORD_CHANNEL_id)
			
			if ( DISC_CHANNEL == None ): 
				continue
				
			await DISC_CHANNEL.send(msg)	
		
	######################################################################################	

	@tasks.loop(seconds=60,count=1) # task runs every 60 seconds
	async def read_exode_task(self):
	
		bRestart = False
	
		try:
			await self.read_exode()			
			bRestart = True
			self.read_exode_task.restart()
					
		except ValueError as err:
		
			print(err)
			if ( str(err) == "Could not receive dynamic_global_properties!" ):
				# Restart
				time.sleep(60)
				LoadHiveBlockChain()
				bRestart = True
				self.read_exode_task.restart()
				
			elif ( str(err) == "stop_order" ):
				print("Shuting down")
				return
				
			else:
				msg = ("%s: Exception occurred:\n" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
				print(msg)
				traceback.print_exc()
				
				msg = ("%s: Exception occurred, request assistance <@!232962122043228160> \n" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
				await self.disc_connect()
				await self.disc_send_msg(msg,self.DISC_CHANNELS_MARKET)
				await self.disc_send_msg(msg,self.DISC_CHANNELS_MINT)
				await self.disc_send_msg(msg,self.DISC_CHANNELS_PING)
		except Exception as exception:
			if ( bRestart ):
				print("Restarting...")
			else:
				msg = ("%s: Exception occurred:\n" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
				print(msg)
				traceback.print_exc()
					
				msg = ("%s: Exception occurred, request assistance <@!232962122043228160> \n" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
				await self.disc_connect()
				await self.disc_send_msg(msg,self.DISC_CHANNELS_MARKET)
				await self.disc_send_msg(msg,self.DISC_CHANNELS_MINT)
				await self.disc_send_msg(msg,self.DISC_CHANNELS_PING)
		
		else:
			if ( bRestart ):
				print("Restarting...")
			else:
				msg = ("%s: Exception occurred:\n" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
				print(msg)
				traceback.print_exc()
				
				msg = ("%s: Exception occurred, request assistance <@!232962122043228160> \n" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
				await self.disc_connect()
				await self.disc_send_msg(msg,self.DISC_CHANNELS_MARKET)
				await self.disc_send_msg(msg,self.DISC_CHANNELS_MINT)
				await self.disc_send_msg(msg,self.DISC_CHANNELS_PING)
			
	@read_exode_task.before_loop
	async def read_exode_preparation(self):
		await self.wait_until_ready() # wait until the bot logs in
		
	######################################################################################	
	async def read_exode(self):
	
		print ( "DISCORD_BOT: read_exode" ) 
		
		bHive = LoadHiveBlockChain()
		if ( bHive.is_hive != True ):
			print("[FATAL] Hive is not loaded")
			quit()
			
		#Get get_current_block
		bBlockC = Blockchain()
		iLastBlock = bBlockC.get_current_block_num()
		iFirstBlock = 0

		if ( os.path.isfile('logs/file_block_fast.json') ):
			with open('logs/file_block_fast.json', 'r') as f:
				self.fFirstBlock = json.load(f) 
	
		iFirstBlock = self.fFirstBlock
		print("read first block as:", iFirstBlock)
		
		if ( iFirstBlock < excst.EXODE_BLOCK_MIN ):
			iFirstBlock = excst.EXODE_BLOCK_MIN
				
		iIterator = 0
		
		self.DISC_CHANNELS      = []
		self.DISC_CHANNELS_PING = []
		self.DISC_CHANNELS_MINT = []		
		
		# Compute card mint numbers:
		db_Card_LoadMint()
		
		MintMissingDone = False
		
		while (self.fFirstBlock + 2000 < iLastBlock and not ( self.fFast or excst.RASPBERRY_PI )):
		
			self.fReBuildDataBase = True
			
			if ( not MintMissingDone ):
				db_TransferTX_Reset()
				db_Card_Mint_Missing()
				MintMissingDone = True
		
			# Load exode history to build the database
			acc = Account("exodegame")
			self.fLoadExodeGame = True
			
			c_last_block_chain = bBlockC.get_current_block_num()
			
			# Load only cancel transaction			
			c_block = int(db_Cancel_GetLastBlock())	
			if ( c_block < excst.EXODE_BLOCK_MIN_CANCEL ):
				c_block = excst.EXODE_BLOCK_MIN_CANCEL
			
			c_block_cur = c_block
			
			for hTransaction in acc.history_reverse(batch_size=1):			
				c_last_block = hTransaction['block']
				break
						
			print("Read cancel transactions from block: ", c_block+1 ," to ",c_last_block)
			if ( (c_block+1) < c_last_block ):
				for hTransaction in acc.history(start=c_block+1, stop=c_last_block, use_block_num=True):
					tType  = hTransaction['type']
					tBlock = hTransaction['block']
					
					if( tType != 'custom_json' ):
						continue
					
					print("Read cancel transactions in block: ", tBlock,"/",c_last_block)
								
					#Get transaction value
					tVAuths = hTransaction['required_posting_auths']
					if ( len(tVAuths) <= 0 ):
						continue
									
					tVId    = hTransaction['id']	
					tVAuth  = hTransaction['required_posting_auths'][0]
						
					if ( tVId == "exode_cancel_test_transaction" ):						
						tVJSON  =  json.loads(hTransaction['json'])					
						tInst   = tVJSON[1]
						mTxId   = tInst['tx_id']
						
						print ( "Add cancellation for ", mTxId, " in block ", tBlock )
						db_Cancel_FillTX( mTxId, tBlock )	
						
					c_block_cur = tBlock
			
			# Set last block seen
			db_Cancel_SetLastBlock(c_block_cur)
			
			# Load list
			self.fCancelTransactionList = db_Cancel_GetTXs()
			
			print ( self.fCancelTransactionList )			
			
			# Temporary test, load everything
			#iFirstBlock = 0
			
			self.fLoadMintOnly = True
			
			# Build the database
			if ( (iFirstBlock+1) < c_last_block ):
				for hTransaction in acc.history(start=iFirstBlock+1, stop=c_last_block, use_block_num=True ):
					#print(hTransaction)
					tType  = hTransaction['type']
					tBlock = hTransaction['block']
					
					if( tType != 'custom_json' and tType != 'transfer' ):
						continue
						
					print("Read transaction in block: ", tBlock,"/",c_last_block)
					
					lOut = await self.ProcessTransaction( tType, tBlock, hTransaction )
					
					if ( lOut == excst.ALERT_KILL ):
						print("Quit...")
						return
											
					with open('logs/file_block_fast.json', 'w') as f:
						json.dump( tBlock, f ) 
					
					iIterator = iIterator + 1
			
			if ( c_last_block_chain > c_last_block ):
				print("Last block registered is: ", c_last_block_chain )
				
				c_last_block_exode = c_last_block_chain
				with open('logs/file_block_fast.json', 'w') as f:
					json.dump( c_last_block_chain, f ) 
			else:
				print("Last block registered is: ", c_last_block )
				c_last_block_exode = c_last_block
			
			c_last_block = c_last_block_exode	
			self.fLoadExodeGame = False
			
			# Load player history to build sell database	
			self.fLoadPlayerMarket = True
			print("Load player list")
			m_players = db_ExodePlayers_List()
			iPlayer   = 0
			for player_name in m_players:
			
				iPlayer = iPlayer + 1
					
				try:
					acc = Account(player_name)
				except bexceptions.AccountDoesNotExistsException:
					print("Account ", player_name, " does not exists!")
					continue
					
									
				c_block_1 = db_TX_GetLastBlock(player_name)
				c_block_2 = db_Player_GetLastBlock(player_name)
				c_block = max(c_block_1,c_block_2)
								
				if ( c_block < excst.EXODE_BLOCK_MIN ):
					c_block = excst.EXODE_BLOCK_MIN
				
				c_player_block_bot = c_last_block+1
				c_player_block_top = c_last_block+1
				
				hTransactionList = []	
				
				print ("Get last transactions from", player_name, "starting from", c_last_block+1, "to", c_block   )
					
				for hTransaction in acc.history_reverse(start=c_last_block+1):			
					tBlock = hTransaction['block']
					tType  = hTransaction['type']
					
					if( tType != 'custom_json' ):
						continue
							
					if ( tBlock < c_block+1 ):
						break
						
					hTransactionList.insert(0, hTransaction)
					c_player_block_bot = tBlock
				
				print("Scan player account: ", player_name, "(", iPlayer, "/", len(m_players),")"," transactions from", c_player_block_bot, "to", c_player_block_top)
				
				c_block_cur = 0
				
				#if ( (c_block+1) < c_last_block ):
					#for hTransaction in acc.history(start=c_block+1, stop=c_last_block, use_block_num=True ):				
				if ( len(hTransactionList) > 0 ):
					for hTransaction in hTransactionList:
					
						#print(hTransaction)
						tType  = hTransaction['type']
						tBlock = hTransaction['block']
						
						
						print("Read ", player_name, "(", iPlayer, "/", len(m_players),")"," transactions in block: ", tBlock,"/",c_last_block+1)
						
						#if( tType != 'custom_json' ):
						#	continue
							
						lOut = await self.ProcessTransaction(tType, tBlock, hTransaction )
						
						if ( lOut == excst.ALERT_KILL ):
							print("Quit...")
							return
						
						iIterator = iIterator + 1
						c_block_cur = tBlock
				
				hTransactionList.clear() 	
				db_Player_SetLastBlock(player_name,c_last_block)			
				
			self.fLoadPlayerMarket = False
							
			print ( "Build loop done" )								
			iLastBlock = bBlockC.get_current_block_num()
		
			if ( os.path.isfile('logs/file_block_fast.json') ):
				with open('logs/file_block_fast.json', 'r') as f:
					self.fFirstBlock = json.load(f) 
		
		#self.fLoadMintOnly    = True
		if ( self.fLoadMintOnly ):
			self.fReBuildDataBase = True
			
			# Rebuild sale/transfer
			print ( "Reset transfer database" )
			db_TransferTX_Reset()	
			print ( "Add known missing mint" )
			db_Card_Mint_Missing()
			print ( "Get last transfer tx block" )	
			c_last_block = db_TransferTX_Last()	
			print ("Load transfer from: ", c_last_block )
			mTransferTX = db_TransferTX_Get(c_last_block)
			for mRow in mTransferTX:
			
				self.ProcessTransfer( tx_auth=mRow[0], tx_type=mRow[1], tx_block=mRow[2], tx_time=mRow[3], tx_id=mRow[4], 
							player_from=mRow[5], player_to=mRow[6], card_id=mRow[7], card_uid=mRow[8], price=mRow[9] )							
						
		else:
			print ( "Add known new missing mint" )
			db_Card_Mint_Missing_New()
		
		# Change flag	
		self.fFast            = False
		self.fReBuildDataBase = False
		self.fLoadMintOnly    = False
		
		# Initialize iterator
		iIterator = 0
		
		# It's running! 
		while True:
		
			# Get first block
			iFirstBlock = 1
			if ( os.path.isfile('logs/file_block_fast.json') ):
				with open('logs/file_block_fast.json', 'r') as f:
					iFirstBlock = json.load(f)+1  
			#print("First block is",iFirstBlock)
			
			if ( iFirstBlock < excst.EXODE_BLOCK_MIN ):
				iFirstBlock = excst.EXODE_BLOCK_MIN
			
			# Get last block
			iLastBlock = bBlockC.get_current_block_num()
			
			#print(iLastBlock, iFirstBlock)
			while iLastBlock <= iFirstBlock:
			
				if ( os.path.isfile('stop.order') ):
					
					# Update player table
					db_Player_CompleteList()
					db_Player_SetLastBlock_all(iBlock-1)
					
					msg = ":zap: Killing order received, going to shutdown... :zap:"
					with open('stop.order', "r") as f:
						msg = msg + "\n Shutdown reason: " + f.read()
							
					os.remove('stop.order')
						
					await self.disc_send_msg(msg, self.DISC_CHANNELS_MARKET)
					await self.disc_send_msg(msg, self.DISC_CHANNELS_MINT)
					await self.disc_send_msg(msg, self.DISC_CHANNELS_PING)
						
					print("shutdown")
					raise ValueError("stop_order")
				
				print("sleeping...")
				time.sleep(3.)
				iLastBlock = bBlockC.get_current_block_num()
				
			block_step = 200
			time.sleep(1.)
			print(f"Loading from {iFirstBlock} to {iFirstBlock+block_step}")
			
			# Loop over blocks
			for fBlock in Blocks(iFirstBlock, count=block_step):
				tBlock = fBlock.block_num
				iBlock = tBlock
										
				# Check if need to reconnect or to ping
				if ( iIterator % 100 == 0 ):					
				
					# Update player table
					db_Player_CompleteList()
					db_Player_SetLastBlock_all(iBlock-1)
					
					if ( os.path.isfile('stop.order') ):
						
						msg = ":zap: Killing order received, going to shutdown... :zap:"
						with open('stop.order', "r") as f:
							msg = msg + "\n Shutdown reason: " + f.read()
							
						os.remove('stop.order')
						
						await self.disc_send_msg(msg, self.DISC_CHANNELS_MARKET)
						await self.disc_send_msg(msg, self.DISC_CHANNELS_MINT)
						await self.disc_send_msg(msg, self.DISC_CHANNELS_PING)
						
						print("shutdown")
						raise ValueError("stop_order")
						
					print("Discord: reconnect")
					# Reconnect
					await self.disc_connect()
						
					print("Discord: ping")
					# Ping
					msg = "[PING] Reading block {block}".format(block=iBlock)
					await self.disc_send_msg(msg, self.DISC_CHANNELS_PING)
					
				# Check if need to reconnect or to ping
				if ( iIterator % 30000 == 0 ):	
									
					msg = "Listing :blue_square:, unlisting :purple_square:, and buy :green_square: alert messages are displayed in this channel.\n**[NOTE]** Mint numbers are estimated from the *currently incomplete* blockchain minting broadcasts. They are not an official information."
					await self.disc_send_msg(msg, self.DISC_CHANNELS_MARKET)
					msg = "**[NOTE]** Mint numbers are estimated from the *currently incomplete* blockchain minting broadcasts. They are not an official information."
					await self.disc_send_msg(msg, self.DISC_CHANNELS_MINT)
					
					iIterator = 0
					
													
				# Increase Iterator
				iIterator = iIterator + 1
				
				print("Read block: ", tBlock)
				
				tTransList = fBlock.json_transactions;	
					
				for tTrans in tTransList:
				
					#print(tTrans)
					tOperationList = tTrans['operations']
				
					for tOperation in tOperationList:
				
						tType = tOperation['type']
				
						if( tType != 'custom_json_operation' and tType != 'transfer_operation' ):
							continue	
						
						#print ( tOperation )
						lOut = await self.ProcessTransaction( tType, tBlock, tOperation['value'] )
						
						if ( lOut == excst.ALERT_KILL ):
							print("Quit...")
							return
			
											
				with open('logs/file_block_fast.json', 'w') as f:
					json.dump( iBlock, f ) 
	
##############################################################################################################################################		
DISC_CLIENT = my_eXode_bot()
DISC_CLIENT.run(excst.BOT_TOKEN_ALERT)
#print ( "Don't restart before Elindos go" )
	


		
