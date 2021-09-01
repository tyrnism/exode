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

import discord
from dotenv import load_dotenv
from discord.ext import tasks

import exode_const as excst


load_dotenv()
BOT_TOKEN = os.getenv('EXODE_DISCORD_TOKEN')
DB_PASS = os.getenv('EXODE_DB_PASS')


#bot variables

#############################################################################################

try:
	mSQLConnector = mysql.connector.connect(user='exode', password=DB_PASS,
							host='127.0.0.1',
							database='exode_db')
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("MySQL: Something is wrong with your user name or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("MySQL: Database does not exist")
	else:
		print("MySQL: ", err)

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

#########################################################################################

def db_TX_GetDetails( tx_id, tx_uid, tx_type, tx_target ):

	cursor = mSQLConnector.cursor()
	
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

	cursor = mSQLConnector.cursor()
	
	query = ("UPDATE exode_tx "
		"SET cancel = %s "
		"WHERE tx_id = %s and type = %s and uid = %s and player = %s") 
				
	cursor.execute(query, (1, tx_id, tx_type, tx_uid, tx_target))
	mSQLConnector.commit()
	
	cursor.reset()
	cursor.close()
	
def db_TX_Add( tx_id, tx_uid, tx_type, tx_block, tx_player, tx_from, tx_auth ):

	cursor = mSQLConnector.cursor()
	
	pack_open = 0
	
	query = ("INSERT INTO exode_tx "
		"(tx_id, type, uid, block, player, player_from, auth) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s)")
		
	cursor.execute(query, (tx_id, tx_type, tx_uid, tx_block, tx_player, tx_from, tx_auth))
	mSQLConnector.commit()
	
	cursor.reset()
	cursor.close()
	
	
def db_TX_GetLastBlock(mPlayer="exodegame"): 

	cursor = mSQLConnector.cursor()
	
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

def db_Player_GetLastBlock(mPlayer): 

	cursor = mSQLConnector.cursor()
	
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

	cursor = mSQLConnector.cursor()
	
	query = ("SELECT last_block FROM exode_player where player = %s ")
		 
	cursor.execute(query, (mPlayer,) )
	m_out = cursor.fetchall()
	
	query = ("UPDATE exode_player "
		"SET last_block = %s "
		"WHERE player = %s") 
	
	cursor.reset()
		 
	cursor.execute(query, (mBlock,mPlayer) )
	mSQLConnector.commit()
	
	cursor.reset()
	cursor.close()
	
def db_Player_SetLastBlock_all(mBlock):

	cursor = mSQLConnector.cursor()
	
	query = ("UPDATE exode_player "
		"SET last_block = %s "
		"WHERE last_block < %s") 
			 
	cursor.execute(query, (mBlock,mBlock) )
	mSQLConnector.commit()
	
	cursor.reset()
	cursor.close()

def db_Player_CompleteList():

	cursor = mSQLConnector.cursor()
	
	query = ("INSERT INTO exode_player (player) "
		"SELECT exode_pack.player FROM exode_pack "
		"WHERE exode_pack.player not in (select exode_player.player from exode_player) "
		"GROUP BY exode_pack.player ") 
	
	cursor.execute(query)
	mSQLConnector.commit()
	
	cursor.reset()
	
	query = ("INSERT INTO exode_player (player) "
		"SELECT exode_cards.owner FROM exode_cards "
		"WHERE exode_cards.owner not in (select exode_player.player from exode_player) "
		"GROUP BY exode_cards.owner ") 
	
	cursor.execute(query)
	mSQLConnector.commit()
	
	cursor.reset()
	cursor.close()
	
#########################################################################################

def db_Pack_GetDetails( pack_owner, pack_id ):

	cursor = mSQLConnector.cursor()
	
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
	
def db_Pack_New( pack_owner, pack_id, pack_nb, pack_open ):

	cursor = mSQLConnector.cursor()
		
	query = ("INSERT INTO exode_pack "
		"(player, type, nb, opened) "
		"VALUES (%s, %s, %s, %s)")
		
	cursor.execute(query, (pack_owner, pack_id, pack_nb, pack_open))
	mSQLConnector.commit()
	
	cursor.reset()
	cursor.close()
	
def db_Pack_Update( pack_owner, pack_id, pack_nb, pack_open ):

	cursor = mSQLConnector.cursor()
	
	query = ("UPDATE exode_pack "
		"SET nb = nb + %s, opened = opened + %s "
		"WHERE player = %s and type = %s" )	
		
	cursor.execute(query, (pack_nb, pack_open, pack_owner, pack_id))
	mSQLConnector.commit()
	
	cursor.reset()
	cursor.close()
	
def db_Pack_Apply_TransferAll( pack_prev_owner, pack_new_owner ):

	cursor = mSQLConnector.cursor()
	
	query = ("SELECT type, nb FROM exode_pack "
			 "WHERE player = %s" )	
		
	cursor.execute(query, (pack_prev_owner, ))
	m_output = cursor.fetchall()
		
	for iRow in range(cursor.rowcount):
		cursor.reset()
		query = ("UPDATE exode_pack "
			"SET nb = nb + %s "
			"WHERE player = %s AND type = %s") 					
		cursor.execute(query, (m_output[iRow][1], pack_new_owner, m_output[iRow][0]) )
		mSQLConnector.commit()
	
	cursor.reset()
	cursor.close()
	
def db_Pack_Apply_Transfer( pack_prev_owner, pack_new_owner, pack_id, pack_nb ):
	
	db_Pack_Update( pack_prev_owner, pack_id, -1 * pack_nb, 0 )
	db_Pack_Update( pack_new_owner, pack_id, pack_nb, 0 )	
	
def db_Pack_Apply_Update( pack_owner, pack_id, pack_nb, pack_open ):

	pInfo = db_Pack_GetDetails( pack_owner, pack_id )
	if ( pInfo['exist'] ):
		db_Pack_Update( pack_owner, pack_id, pack_nb, pack_open )
	else:
		db_Pack_New( pack_owner, pack_id, pack_nb, pack_open )
	
#########################################################################################

def db_Card_GetDetails( card_uid ):

	cursor = mSQLConnector.cursor()
	
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
			
	cursor = mSQLConnector.cursor()
	
	query = ("SELECT COUNT(*) FROM exode_cards "
		 "WHERE type = %s AND elite = %s AND mint_num != -1")	
		
	cursor.execute(query, (card_id, card_elite))
	m_output = cursor.fetchall()
	
	card_ntot_mint  = int(m_output[0][0])
	
	cursor.reset()
	cursor.close()
	
	return card_ntot_mint
	
def db_Card_Mint( card_owner, card_id, card_num, card_uid, card_mint, card_elite, card_bound, card_block ):

	cursor = mSQLConnector.cursor()
	
	card_burn = 0
	
	query = ("INSERT INTO exode_cards "
		"(type, num, uid, owner, burn, bound, elite, mint_num, block, block_update, minter) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
				
	cursor.execute(query, (card_id, card_num, card_uid, card_owner, card_burn, card_bound, card_elite, card_mint, card_block, card_block, card_owner) )
	mSQLConnector.commit()
	
	cursor.reset()
	cursor.close()
	
def db_Card_Burn( card_uid, card_block, card_burn, card_burner ):

	cursor = mSQLConnector.cursor()
	
	query = ("UPDATE exode_cards "
		"SET burn = %s, block_update = %s, owner = %s "
		"WHERE uid = %s") 
		
	cursor.execute(query, (card_burn, card_block, card_burner, card_uid) )
	mSQLConnector.commit()
	
	cursor.reset()
	cursor.close()

def db_Card_Transfer( card_uid, card_block, card_owner ):

	cursor = mSQLConnector.cursor()

	card_burn = 1
	
	query = ("UPDATE exode_cards "
		"SET owner = %s, block_update = GREATEST( block_update, %s ) "
		"WHERE uid = %s") 
		
	cursor.execute(query, (card_owner, card_block, card_uid) )
	mSQLConnector.commit()
	
	cursor.reset()
	cursor.close()
	
def db_Card_Apply_TransferAll( card_prev_owner, card_owner, card_block ):

	cursor = mSQLConnector.cursor()

	card_burn = 1
	
	query = ("UPDATE exode_cards "
		"SET owner = %s, block_update = %s "
		"WHERE owner = %s and burn = 0 and bound = 0") 
		
	cursor.execute(query, (card_owner, card_block, card_prev_owner) )
	mSQLConnector.commit()
	
	cursor.reset()
	cursor.close()
	
	
	
def db_Card_Apply_Mint( card_owner, card_id, card_uid, card_mint, card_elite, card_bound, card_block, tx_id, bypass=False ):
	
	msg = ""
	
	cInfo = db_Card_GetDetails( card_uid )
	if ( cInfo['exist'] and card_uid != "none" ):
		if ( not bypass and tx_id != "" ):
			with open('logs/card_error.json', 'a') as f:
				err_msg = { "card": { "id": card_id, "uid": card_uid }, "issue": "card_duplicate", 
						"spotted": { "block": card_block, "tx_id": tx_id, "action": "mint", "issue_details": { "minter": card_owner } } }
				json.dump( err_msg, f ) 
				f.write("\n")
		return msg	
	
	# Will be replaced one day...
	if ( card_owner == "elindos" or card_owner == "exolindos" or card_uid == "none" ):
		card_mint = -1
	else:
		card_mint = db_Card_GetNMintTot( card_id, card_elite ) + 1
	
	(is_pack, card_name, card_rank, card_num) = ex_GetAssetDetails(card_id)
	
	db_Card_Mint( card_owner, card_id, card_num, card_uid, card_mint, card_elite, card_bound, card_block )
	
	
	if ( (card_mint > 0 and card_mint <= 10) or (card_rank == 2 and int(card_elite) == 1) or card_rank == 3 ):
		if ( int(card_elite) == 1 ):
			msg_elite = "an **Elite "
		else:
			msg_elite = "a **"
				
		
		msg = ":tada: {player} found {elite}{name}** (**{mint}**/{mint} *uid={uid}*)".format(player=card_owner,elite=msg_elite,name=card_name, mint=card_mint, uid=card_uid)
	
	return msg
	
def db_Card_IsTransferable( card_from, card_to, card_id, card_uid, card_block, tx_id, transfer_action, bypass=False ):

	cInfo = db_Card_GetDetails( card_uid )
	
	if ( not cInfo['exist'] ):
		with open('logs/card_error.json', 'a') as f:
			err_msg = { "card": { "id": card_id, "uid": card_uid }, "issue": "no_source", 
					"spotted": { "block": card_block, "tx_id": tx_id, "action": transfer_action, "issue_details": { "player": card_from, "target": card_to } } }
			json.dump( err_msg, f ) 
			f.write("\n")
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
	if ( not cInfo[2] or card_block < cInfo[3] ):
		return msg
		
	db_Card_Burn( card_uid, card_block, 1, card_burner )
	
	card_mint = cInfo[1]
	card_elite = cInfo[4]
	(is_pack, card_name, card_rank, card_num) = ex_GetAssetDetails(card_id)
	if ( (card_mint > 0 and card_mint <= 10) or (card_rank == 2 and card_elite == 1) or card_rank == 3 ):
		if ( card_elite == 1 ):
			msg_elite = "an **Elite "
		else:
			msg_elite = "a **"
				
		msg = ":fire: {player} burn {elite}{name}** (**{mint}**/{mint} *uid={uid})*".format(player=card_burner,elite=msg_elite,name=card_name, mint=card_mint, uid=card_uid)
	
	return msg
	
def db_Card_Apply_Transfer( card_prev_owner, card_new_owner, card_id, card_uid, card_block, tx_id, bypass=False ):

	cInfo = db_Card_IsTransferable( card_prev_owner, card_new_owner, card_id, card_uid, card_block, tx_id, "transfer", bypass )
	#if ( not cInfo[0] ):
	#	return False
	if ( not cInfo[2] or card_block < cInfo[3] ):
		return False
	
	db_Card_Transfer( card_uid, card_block, card_new_owner )
	
	return True
	
#########################################################################################

def db_Sale_GetDetails( asset_uid, sale_sold, sale_block, sale_seller="", sale_fix=0 ):

	cursor = mSQLConnector.cursor()
	
	if ( sale_fix == 1 ):
	
		query = ("SELECT seller, price, sold FROM exode_sales "
			 "WHERE seller = %s and asset_uid = %s and sold = %s and block > %s and block = block_update ORDER BY block_update LIMIT 1" )	
			 
		cursor.execute(query, (sale_seller, asset_uid,sale_sold,sale_block))
		m_output = cursor.fetchall()
	elif ( sale_fix == 2 ):
	
		query = ("SELECT seller, price, sold FROM exode_sales "
			 "WHERE seller = %s and asset_uid = %s and sold = %s and block < %s and block_update > %s ORDER BY block_update LIMIT 1" )
			 
		cursor.execute(query, (sale_seller, asset_uid,sale_sold,sale_block, sale_block))
		m_output = cursor.fetchall()
	else:
	
		query = ("SELECT seller, price, sold FROM exode_sales "
			 "WHERE asset_uid = %s and sold = %s and block < %s" )	
	
		cursor.execute(query, (asset_uid,sale_sold,sale_block))
		m_output = cursor.fetchall()
	
	if ( cursor.rowcount != 0 ):	
		sale_exist  = True
		sale_seller = m_output[0][0]
		sale_price  = float(m_output[0][1])
		sale_sold   = int(m_output[0][2])
	else:
		sale_exist  = False
		sale_seller = ""
		sale_price  = 0.0
		sale_sold   = 0
		
	output = { 'exist': sale_exist, 'seller': sale_seller, 'price': sale_price, 'sold': sale_sold }
			
	cursor.reset()
	cursor.close()
	
	return output
	
def db_Sale_Add( sale_seller, asset_id, asset_uid, sale_tx, sale_price, sale_sold, sale_buyer, sale_block ):

	cursor = mSQLConnector.cursor()
	
	query = ("INSERT INTO exode_sales "
		"(seller, asset_type, asset_uid, price, tx_id, sold, buyer, block, block_update) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
				
	cursor.execute(query, (sale_seller, asset_id, asset_uid, sale_price, sale_tx, sale_sold, sale_buyer, sale_block, sale_block) )
	mSQLConnector.commit()
	
	cursor.reset()
	cursor.close()
	
def db_Sale_Sold( asset_uid, sale_tx, sale_sold, sale_buyer, sale_block ):

	cursor = mSQLConnector.cursor()
	
	query = ("UPDATE exode_sales "
		"SET buyer = %s, sold = %s, block_update = %s "
		"WHERE asset_uid = %s and sold = %s and block < %s") 
		
	cursor.execute(query, (sale_buyer, sale_sold, sale_block, asset_uid, 0, sale_block) )
	mSQLConnector.commit()
	
	cursor.reset()
	cursor.close()
	
def db_Sale_Fix( asset_uid, sale_tx, sale_seller, sale_price, sale_block ):

	cursor = mSQLConnector.cursor()
	
	query = ("SELECT id from exode_sales "
		"WHERE seller = %s and asset_uid = %s and sold = %s and block > %s and block = block_update ORDER BY block_update LIMIT 1 ")  
	
	cursor.execute(query, ("market",  asset_uid, 1, sale_block) )
	m_output = cursor.fetchall()
		
	if ( cursor.rowcount != 0 ):	
			
		cursor.reset()
		query = ("UPDATE exode_sales "
			"SET price = %s, seller = %s, block = %s "
			"WHERE id = %s")  
	else:
		print( " Mysql error, sale to fix not found " )
	
		
	cursor.execute(query, (sale_price, sale_seller, sale_block, m_output[0][0]) )
	mSQLConnector.commit()
	
	cursor.reset()
	cursor.close()
	
def db_Sale_Cancel( asset_uid, sale_seller, sale_block, sale_fix=False ):

	cursor = mSQLConnector.cursor()
	
	query = ("delete from  exode_sales "
		"WHERE seller = %s and asset_uid = %s and sold = %s and block < %s and block = block_update")  	
		
	cursor.execute(query, (sale_seller, asset_uid, 0, sale_block) )
	mSQLConnector.commit()
	
	if ( sale_fix ):
	
		cursor.reset()
		
		query = ("SELECT id from exode_sales "
			"WHERE seller = %s and asset_uid = %s and sold = %s and block < %s and block_update > %s ORDER BY block_update LIMIT 1 ")  
	
		cursor.execute(query, (sale_seller,  asset_uid, 1, sale_block, sale_block) )
		m_output = cursor.fetchall()
		
		if ( cursor.rowcount != 0 ):	
			
			cursor.reset()
				
			query = ("UPDATE exode_sales "
				"SET price = %s, seller = %s, block = block_update "
				"WHERE id = %s ")  
			
			cursor.execute(query, (0.0, "market",  m_output[0][0]) )
			mSQLConnector.commit()
		else:
			print( " Mysql error, sale to cancel not found " )
		
	
	cursor.reset()
	cursor.close()
	
def db_Sale_Apply_New( sale_seller, asset_id, asset_uid, sale_block, sale_tx, sale_price, sale_sold, sale_buyer, sale_update, bypass = False ):

	# Check asset
	(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails(asset_id)
	if ( not is_pack ):
		cInfo = db_Card_IsTransferable( sale_seller, "market", asset_id, asset_uid, sale_block, sale_tx, "sale", sale_update )
		if ( not cInfo[0] and not bypass ):
			return False
	
	if ( sale_update ):
		sInfo = db_Sale_GetDetails( asset_uid, 1, sale_block, "market", 1 )
		
		if ( sInfo['exist'] ):
			db_Sale_Fix( asset_uid, sale_tx, sale_seller, sale_price, sale_block )
			return True
			
		sInfo = db_Sale_GetDetails( asset_uid, 1, sale_block, sale_seller, 2 )
		
		if ( sInfo['exist'] ):
			# cancel previous... 
			db_Sale_Cancel( asset_uid, sale_seller, sale_block, True )
			
		sInfo = db_Sale_GetDetails( asset_uid, 1, sale_block, "market", 1 )
		
		if ( sInfo['exist'] ):
			db_Sale_Fix( asset_uid, sale_tx, sale_seller, sale_price, sale_block )
			return True
	
	sInfo = db_Sale_GetDetails( asset_uid, 0, sale_block )
		
	if ( sInfo['exist'] and sale_seller != sInfo['seller'] ):
		with open('logs/sale_error.json', 'a') as f:
			err_msg = { "sale": { "seller": sale_seller, "buyer": sale_buyer, "sold": sale_sold, "card": { "id": asset_id, "uid": asset_uid } }, "issue": "duplicate_sale", "spotted": {"action": "create_sale", "block": sale_block, "tx_id": sale_tx}, "current_seller": sInfo['seller'] } 
			json.dump( err_msg, f ) 
			f.write("\n")
		return False
	elif ( sInfo['exist'] and sale_seller != "market" ):
		db_Sale_Cancel( asset_uid, sale_seller, sale_block )
	
	db_Sale_Add( sale_seller, asset_id, asset_uid, sale_tx, sale_price, sale_sold, sale_buyer, sale_block )
		
	return True
	
def db_Sale_Apply_Cancel( sale_seller, asset_id, asset_uid, sale_block, sale_tx, sale_update, transfert_cancel=False ):

	# Check asset
	(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails(asset_id)
	if ( not is_pack and not sale_update and not transfert_cancel ):
		cInfo = db_Card_IsTransferable( sale_seller, "market", asset_id, asset_uid, sale_block, sale_tx, "sale-cancel" )
		if ( not cInfo[0] ):
			return False
	
	if ( sale_update ):
		sInfo = db_Sale_GetDetails( asset_uid, 1, sale_block, sale_seller, 2 )
		
		if ( sInfo['exist'] ):
			db_Sale_Cancel( asset_uid, sale_seller, sale_block, True )
			return True
	
	sInfo = db_Sale_GetDetails( asset_uid, 0, sale_block )
	
	if ( not sInfo['exist'] and transfert_cancel ):
		#Skip
		return True
	elif ( not sInfo['exist'] ):
		with open('logs/sale_error.json', 'a') as f:
			err_msg = { "sale": { "seller": sale_seller, "buyer": "", "sold": 0, "card": { "id": asset_id, "uid": asset_uid } }, "issue": "unknown_sale", "spotted": {"action": "cancel_sale", "block": sale_block, "tx_id": sale_tx} } 
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
		db_Sale_Cancel( asset_uid, sale_seller, sale_block )
		
	return True
	
def db_Sale_Apply_Sold( sale_seller, asset_id, asset_uid, sale_block, sale_tx, sale_sold, sale_buyer ):

	# Check asset
	(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails(asset_id)
	if ( not is_pack ):
		cInfo = db_Card_IsTransferable( sale_seller, sale_buyer, asset_id, asset_uid, sale_block, sale_tx, "sale-sold" )
		#if ( not cInfo[0] ):
		#	return [ False, "", 0.0 ]
	
	sInfo = db_Sale_GetDetails( asset_uid, 0, sale_block )
	if ( not sInfo['exist'] ):
		with open('logs/sale_error.json', 'a') as f:
			err_msg = { "sale": { "seller": sale_seller, "buyer": sale_buyer, "sold": sale_sold, "card": { "id": asset_id, "uid": asset_uid } }, "issue": "unknown_sale", "spotted": {"action": "complete_sale", "block": sale_block, "tx_id": sale_tx} } 
			json.dump( err_msg, f ) 
			f.write("\n")
		return [ False, "", 0.0 ]
	else:
		db_Sale_Sold( asset_uid, sale_tx, 1, sale_buyer, sale_block)
		
	return [ True, sInfo['seller'], sInfo['price'] ]
	
	
def db_Sale_GetAverageSoldPrice(mID=""): 

	if ( mID == "" ):
		return -1.0
	cursor = mSQLConnector.cursor()
	
	query = ("SELECT AVG(price) from exode_sales "
		"WHERE asset_type = %s and sold = %s")  
		 
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
	cursor = mSQLConnector.cursor()
	
	query = ("SELECT price from exode_sales "
		"WHERE asset_type = %s and sold = %s ORDER BY block_update DESC")  
		 
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
	db_Player_CompleteList()
	
	cursor = mSQLConnector.cursor()	
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

	cursor = mSQLConnector.cursor()
	
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

	cursor = mSQLConnector.cursor()
	
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
	cursor = mSQLConnector.cursor()
	
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
	mSQLConnector.commit()
		
	cursor.reset()	
	cursor.close()
	
def db_Cancel_FillTX( tTxId, tBlock ): 
	cursor = mSQLConnector.cursor()
	
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
		mSQLConnector.commit()
	
	cursor.reset()	
	cursor.close()
	
#########################################################################################
	
def LoadHiveBlockChain():
	print ("HIVE: Loading blockchain")
	nodelist = NodeList()
	nodelist.update_nodes()
	nodes = nodelist.get_hive_nodes()
	bHive = Hive(node=nodes)
	print("Hive loaded?",bHive.is_hive)
	
	return bHive		
		
##############################################################################################


class my_eXode_bot(discord.Client):

	######################################################################################
	
	# Parameters:
	fFast            = False
	fDoDiscord       = False
	
	# Variables
	fFirstBlock       = 0
	fLastTransaction  = "0000"
	fLoadExodeGame    = False
	fLoadPlayerMarket = False
	fReBuildDataBase  = False
	fCancelTransactionList   = []
	
	# Discord Channels
	DISC_CHANNELS_MARKET = []
	DISC_CHANNELS_PING   = []
	DISC_CHANNELS_MINT   = []
	
	DISC_CHANNEL_MARKET_NAME = "exode-market"
	DISC_CHANNEL_MINT_NAME   = "exode-alert"
	DISC_CHANNEL_PING_NAME   = "exode-bot-ping"
		
	
	######################################################################################	

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		# create the background task and run it in the background
		self.read_exode.start()
		
	######################################################################################		

	async def on_ready(self):
		print ("DISCORD BOT: on_ready")
		print ("DISCORD BOT: on_ready_end")
				
	######################################################################################
	
	def CheckByPass( self, mBlock ):	
		if ( not self.fReBuildDataBase or mBlock > self.fFirstBlock ):
			return False
		
		return True
	
	def CheckTransaction( self, mBlock, mType, mTxId, mUId, mPlayer, mFrom, mAuth, mTransaction, mCancel=False ):
		if ( mTxId == "" ):
			mTxId = mBlock

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
				l_source_uids = [ "none" ]
				if ( "sourceuniqueid" in tInst ):
					l_source_uids = tInst['sourceuniqueid'].split(',')
				
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
					iPack_nb = len(l_pack_ids)/14					
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
				
			elif ( 	tVId == "exode_newpacks" 
				or 	tVId == "exode_bonuspacks" 	or tVId == "community_gift" 
				or 	tVId == "battlegames_ama" 	or tVId == "community_planetary_challenge" 
				or 	tVId == "contest_rewards"	or tVId == "battlegames_witness"
				or 	tVId == "inventory_transform"	or tVId == "inventory_transform_all" 
				or 	tVId == "for_community_rewards" ):
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
				
				l_player  = tInst['recipient']
				l_pack_id = tInst['typeids'].split(',')
				l_pack_nb = tInst['typenbs'].split(',')
				
				for iPack in range( len(l_pack_id) ):
					if ( l_pack_id[iPack] == "" or l_pack_nb[iPack] == "" ):
						continue
							
					db_Pack_Apply_Update(l_player, l_pack_id[iPack], l_pack_nb[iPack], 0 )
					
			elif ( tVId == "exode_extinguish_flames" ):
			
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
					lOut = db_Card_Apply_Burn( l_card_owner, l_card_id, l_card_burn_uids[iCard], tBlock, mTxId, self.CheckByPass( tBlock ) )					
					if ( lOut != "" ):
						tMSGOut.append(lOut)	
						
				return [ excst.ALERT_MINT, tMSGOut ]
					
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
				with open('logs/log_unknown.log', 'a') as f:
					f.write("Type: {del_type}, Block: {block}, transaction: {del_txt}\n".format(del_type=tVId,block=tBlock,del_txt=tVJSON) )
							
		elif ( tVId == "exode_market_sell" ):
			# Get JSON to add new market sell			
			tVJSON  =  json.loads(tValue['json'])					
			#print("[DEBUG] New sell from : ", tVAuth, tVJSON)
						
			tInst   = tVJSON
			
			if ( "tx_id" in tInst ):
				self.fLastTransaction = tInst['tx_id']
				l_sale_txid    = tInst['tx_id']
			elif ( "txid" in tInst ):
				self.fLastTransaction = tInst['txid']
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
			
			if ( "uniqueid" in tInst ):						
				l_asset_uids = tInst['uniqueid'].split(',')				
			else:			
				l_asset_uids = tInst['uniqueids'].split(',')
				
			if ( "id" in tInst ):	
				l_asset_id     = tInst['id']
			else:
				cInfo = db_Card_GetDetails( l_asset_uids[0] )
				l_asset_id     = cInfo['id']
		
			print( 'sell', l_sale_txid, l_asset_seller, l_asset_id, l_asset_uids, l_sale_price )	
			
			for iAsset in range(len(l_asset_uids)):
				bOK = db_Sale_Apply_New( l_asset_seller, l_asset_id, l_asset_uids[iAsset], tBlock, l_sale_txid, l_sale_price, 0, "", self.fLoadPlayerMarket )

			if ( not bOK ):
				return [ excst.NO_ALERT, tMSGOut ]
			
			(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails(l_asset_id) 
			mSoldPrice = db_Sale_GetAverageSoldPrice(l_asset_id)
			mLastPrice = db_Sale_GetLastSoldPrice(l_asset_id)

			if ( is_pack ):
						
				pack_name                               = asset_name
				
				lOut = ":blue_square: {seller} listed {nb} **{name}** on the market for **${price}** (average sold price: **${sold_price:.2f}**, last sold price: **${last_price:.2f}**)".format(seller=l_asset_seller, nb=len(l_asset_uids), name=pack_name, price=l_sale_price,sold_price=mSoldPrice,last_price=mLastPrice)
				tMSGOut.append(lOut)
							
			else:
						
				card_name  = asset_name
				card_elite = 0
				card_mint = -1
				card_muid = -1
				card_id   = 0
				for iAsset in range(len(l_asset_uids)):
								
					cInfo = db_Card_GetDetails( l_asset_uids[iAsset] )
					
					is_elite   = cInfo['elite']
					n_mint     = cInfo['mint']
					card_id    = cInfo['id']
						
					if ( n_mint < card_mint or card_mint == -1 ):
						card_muid = l_asset_uids[iAsset]
						card_mint = n_mint
					if ( is_elite == 1 ):
						card_elite = is_elite
						
				card_ntot_mint = db_Card_GetNMintTot( l_asset_id, card_elite )
				(is_pack, card_name, card_rank, asset_num) = ex_GetAssetDetails(card_id)
																					
				card_elite_msg = ""
				if ( card_elite == 1 ):
					card_elite_msg = "Elite "
				
				if ( len(l_asset_uids) == 1 ):
					lOut = ":blue_square: {seller} listed 1 **{elite}{name}** (**{mint}**/{ntot_mint} *uid={muid})* for **${price}** (avg sold price: **${sold_price:.2f}**, last sold price: **${last_price:.2f}**)".format(seller=l_asset_seller, 
								name=card_name, mint=card_mint, elite=card_elite_msg, ntot_mint=card_ntot_mint, muid=card_muid, price=l_sale_price,sold_price=mSoldPrice,last_price=mLastPrice)
				else:						
					lOut = ":blue_square: {seller} listed {nb} **{elite}{name}** for **${price}** (min. mint is **{mint}**/{ntot_mint} *uid={muid}*) (avg sold price: **${sold_price:.2f}**, last sold price: **${last_price:.2f}**)".format(seller=l_asset_seller,
								nb=len(l_asset_uids), elite=card_elite_msg, name=card_name, mint=card_mint, ntot_mint=card_ntot_mint, muid=card_muid,
								price=l_sale_price,sold_price=mSoldPrice,last_price=mLastPrice)
				tMSGOut.append(lOut)
			
			return [ excst.ALERT_MARKET, tMSGOut ]
							
						
		elif ( tVId == "exode_market_cancel_sell" ):
			# Get JSON to add new market sell			
			tVJSON  =  json.loads(tValue['json'])					
			#print("[DEBUG] New sell from : ", tVAuth, tVJSON)
						
			tInst   = tVJSON			
			self.fLastTransaction = tInst['txid']
				
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
			bOK = db_Sale_Apply_Cancel( l_asset_seller, l_asset_id, l_asset_uid, tBlock, l_sale_txid, self.fLoadPlayerMarket )
				
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
				
				card_elite = cInfo['elite']
				card_mint  = cInfo['mint']	
				card_ntot_mint = db_Card_GetNMintTot( l_asset_id, card_elite )
																											
				card_elite_msg = ""
				if ( card_elite == 1 ):
					card_elite_msg = "Elite "
				
				lOut = ":purple_square: {seller} unlisted 1 **{elite}{name}** (**{mint}**/{ntot_mint} *uid={muid}*)".format(seller=l_asset_seller, 
								name=card_name, mint=card_mint, elite=card_elite_msg, ntot_mint=card_ntot_mint, muid=card_muid)
				tMSGOut.append(lOut)
						
			return [ excst.ALERT_MARKET, tMSGOut ]
						
							
		elif ( tVId == "exode_market_transfer" ):
			# Ownership is set by exodegame, ignore
			return [ excst.NO_ALERT, tMSGOut ]	
				
		return [ excst.NO_ALERT, tMSGOut ]

	######################################################################################

	def ReadTransfert(self,tValue,tBlock):

		tMSGOut = []
		tFrom   = tValue['from']
		tTo     = tValue['to']
		tMemo   = tValue['memo'].split(":")
		
		#if (	   tFrom == "elindos"   or tTo == "elindos" 
		#	or tFrom == "exolindos" or tTo == "exolindos"  ):
		#	#Test accounts
		#	return [ 0, tMSGOut ]	
		
		if ( tFrom == "exodegame" ):
			if ( tMemo[0] == "exodegame" ):
			
				if ( tMemo[1] == "exode_transfer" ):
					
					mMemo = tMemo[2].split(" ")
					mFrom = mMemo[-1]
					mUID  = tMemo[4]
					mID   = tMemo[5]
					mTxId = tMemo[8]
					
					
					if ( not self.CheckTransaction(tBlock, tMemo[1], mTxId, mUID, tTo, mFrom, tFrom, tMemo) ):
						return [ excst.NO_ALERT, tMSGOut ]	
					
					# Cancel sale if any
					bOK = db_Sale_Apply_Cancel( mFrom, mID, mUID, tBlock, mTxId, False, True )
					
					if ( ex_IsPack(mID) ):
						print('pack-transfer', mTxId, mFrom, tTo, mID, mUID )
						db_Pack_Apply_Transfer( mFrom, tTo, mID, 1 )
							
					else:
						print('card-transfer', mTxId, mFrom, tTo, mID, mUID )						
						db_Card_Apply_Transfer( mFrom, tTo, mID, mUID, tBlock, mTxId, self.CheckByPass( tBlock ) )
					
				elif ( tMemo[1] == "exode_market_purchase" ):
					
					mFrom = "market"
					mUID  = tMemo[4]
					mID   = tMemo[5]
					mTxId = tMemo[8]
					
					if ( not self.CheckTransaction(tBlock, tMemo[1], mTxId, mUID, tTo, mFrom, tFrom, tMemo) ):
						return [ excst.NO_ALERT, tMSGOut ]	
		
					if ( self.fLoadExodeGame ):
						bOK = db_Sale_Apply_New( "market", mID, mUID, tBlock, mTxId, 0.0, 1, tTo, self.CheckByPass( tBlock ), True )
						
						asset_seller = "market"
						asset_price  = 0.0
					else:
						sInfo = db_Sale_Apply_Sold( "market", mID, mUID, tBlock, mTxId, 1, tTo )

						bOK          = sInfo[0]
						asset_seller = sInfo[1]
						asset_price  = sInfo[2]
										
					if ( not bOK ):
						return [ excst.NO_ALERT, tMSGOut ]	
						
					(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails(mID) 
					mSoldPrice = db_Sale_GetAverageSoldPrice(mID)
					
					if ( is_pack ):
						print('pack-buy', mTxId, mFrom, tTo, mID, mUID )
						
						pack_name = asset_name
						
						db_Pack_Apply_Transfer( asset_seller, tTo, mID, 1 )
						
						lOut = ":green_square: {buyer} bought 1 **{name}** from {seller} for **${price}** (avg sold price is **${sold_price:.2f}**)".format(buyer=tTo, name=pack_name, seller=asset_seller, price=asset_price, sold_price=mSoldPrice)
						tMSGOut.append(lOut)
							
					else:
						print('card-buy', mTxId, mFrom, tTo, mID, mUID )
						
						cInfo = db_Card_GetDetails( mUID )
						
						card_elite = cInfo['elite']
						card_mint  = cInfo['mint']					
						card_name = asset_name
						card_ntot_mint = db_Card_GetNMintTot( mID, card_elite )
											
						db_Card_Apply_Transfer( asset_seller, tTo, mID, mUID, tBlock, mTxId, self.CheckByPass( tBlock ) )
												
						card_elite_msg = ""
						if ( card_elite == 1 ):
							card_elite_msg = "Elite "
											
						lOut = ":green_square: {buyer} bought 1 **{elite}{name}** (**{mint}**/{ntot_mint}  *uid={muid}*) from {seller} for **${price}** (avg sold price is **${sold_price:.2f}**)".format(buyer=tTo, name=card_name,
									 elite=card_elite_msg, mint=card_mint, ntot_mint=card_ntot_mint, muid=mUID, seller=asset_seller, price=asset_price,sold_price=mSoldPrice)
						if ( lOut != "" ):
							tMSGOut.append(lOut)
						
					
					return [ excst.ALERT_MARKET, tMSGOut ]
					
				elif ( tMemo[1] == "exode_delivery" or tMemo[1] == "exode_delivery_update" ):	
				
					mTxId = ""
					
					if ( tMemo[2] == "NFT" ):
						mUID = tMemo[3]
					elif ( tMemo[3] == "NFT" ):
						mUID = tMemo[4]
					else: 
						mUID = ""						
					
					if ( not self.CheckTransaction(tBlock, tMemo[1], mTxId, mUID, tTo, tFrom, tFrom, tMemo) ):
						return [ excst.NO_ALERT, tMSGOut ]	
						
					with open('logs/transaction_delivery.json', 'a') as f:
						err_msg = { "transaction": { "type": tMemo[1], "block": tBlock, "tx_id": "" },  
							"transaction_details": tMemo[2:] }
						json.dump( err_msg, f ) 
						f.write("\n")
			
				elif ( tMemo[1] == "exode_market_rewards" or tMemo[1] == "exode_market_sale" or tMemo[1] == "exode_market_sale_manual" ):			
					#SKIP!
					return [ excst.NO_ALERT, tMSGOut ]
			
				else:	
					with open('logs/log_unknown_transfert.log', 'a') as f:
						f.write("From: {del_from}, To: {del_to}, Type: {del_type}, Block: {block}, memo: {del_txt}\n".format(del_from=tFrom, del_to=tTo,del_type=tMemo[1],block=tBlock,del_txt=tMemo[2:]) )
			
			else:
				with open('logs/log_unknown_transfert.log', 'a') as f:
					f.write("From: {del_from}, To: {del_to}, Type: {del_type}, Block: {block}, memo: {del_txt}\n".format(del_from=tFrom, del_to=tTo,del_type="unknown",block=tBlock,del_txt=tValue['memo']) )
			
		else: 
			tnMemo = tMemo[0].split("|")
			
			if ( tnMemo[0] == "confirm_transfer_packs" ):
			
				mTo = tnMemo[3]
			
				if ( not self.CheckTransaction(tBlock, tnMemo[0], tBlock, "", mTo, tFrom, tFrom, tnMemo) ):
					return [ excst.NO_ALERT, tMSGOut ]	
						
				print( 'mass-transfer-pack', 0, tFrom, tnMemo[3], tnMemo[1], tnMemo[2] )		
				
				db_Pack_Apply_Transfer( tFrom, mTo, tnMemo[1], tnMemo[2] )
				
			elif ( tnMemo[0] == "confirm_transfer_account" ):
			
				mTo = tnMemo[1]
				
				# fix
				if ( mTo == "birdbeak" ):
					mTo = "birdbeaksd"
					
				if ( not self.CheckTransaction(tBlock, tnMemo[0], tBlock, "", mTo, tFrom, tFrom, tnMemo) ):
					return [ excst.NO_ALERT, tMSGOut ]	
					
				print( 'mass-transfer-account', 0, tFrom, mTo )
				
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
							
							
		return int(lOut[0])
				
	######################################################################################							

	async def disc_connect(self):
	
		if ( not self.fDoDiscord ):
			return
		
		DISC_CHANNELS_MARKET_TMP = []
		DISC_CHANNELS_MINT_TMP   = []
		DISC_CHANNELS_PING_TMP   = []
				
		for discord_guild in self.guilds:
			DISC_CHANNEL = discord.utils.get(discord_guild.channels, name=self.DISC_CHANNEL_MARKET_NAME)
			if ( DISC_CHANNEL != None ):
				DISC_CHANNELS_MARKET_TMP.append(DISC_CHANNEL.id)
						
				if ( DISC_CHANNEL.id not in self.DISC_CHANNELS_MARKET):					
					print ( "DISCORD BOT:eXode bot [MARKET-ALERT] connected to {guild_name}".format(guild_name=discord_guild.name) )
					await DISC_CHANNEL.send("*eXode BOT [MARKET-ALERT] is connected here!*")
							
			DISC_CHANNEL = discord.utils.get(discord_guild.channels, name=self.DISC_CHANNEL_MINT_NAME)
			if ( DISC_CHANNEL != None ):
				DISC_CHANNELS_MINT_TMP.append(DISC_CHANNEL.id)
						
				if ( DISC_CHANNEL.id not in self.DISC_CHANNELS_MINT):					
					print ( "DISCORD BOT:eXode bot [EXODE-ALERT] connected to {guild_name}".format(guild_name=discord_guild.name) )
					await DISC_CHANNEL.send("*eXode BOT [EXODE-ALERT] is connected here!*")
					
						
			DISC_CHANNEL = discord.utils.get(discord_guild.channels, name=self.DISC_CHANNEL_PING_NAME)
			if ( DISC_CHANNEL != None ):
				DISC_CHANNELS_PING_TMP.append(DISC_CHANNEL.id)
						
				if ( DISC_CHANNEL.id not in self.DISC_CHANNELS_PING):					
					print ( "DISCORD BOT:eXode bot [PING] connected to {guild_name}".format(guild_name=discord_guild.name) )
					await DISC_CHANNEL.send("*eXode BOT [PING] is connected here!*")

		self.DISC_CHANNELS_MARKET = DISC_CHANNELS_MARKET_TMP
		self.DISC_CHANNELS_MINT   = DISC_CHANNELS_MINT_TMP
		self.DISC_CHANNELS_PING   = DISC_CHANNELS_PING_TMP 
		
	async def disc_send_msg_list(self, msg_list, CHANNEL_LIST):
	
		if ( not self.fDoDiscord ):
			return
	
		for DISCORD_CHANNEL_id in CHANNEL_LIST:
			DISC_CHANNEL = DISC_CLIENT.get_channel(DISCORD_CHANNEL_id)
			for msg in msg_list:
				await DISC_CHANNEL.send(msg)	
				
	async def disc_send_msg(self, msg, CHANNEL_LIST):
		
		if ( not self.fDoDiscord ):
			return
	
		for DISCORD_CHANNEL_id in CHANNEL_LIST:
			DISC_CHANNEL = DISC_CLIENT.get_channel(DISCORD_CHANNEL_id)
			await DISC_CHANNEL.send(msg)	
		
	######################################################################################	

	@tasks.loop(seconds=60,count=1) # task runs every 60 seconds
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
		
		iMinimumBlock        = 42233330
		iMinimumBlock_cancel = 45975275 # Minimum block for cancellation broadcast
		if ( iFirstBlock < iMinimumBlock ):
			iFirstBlock = iMinimumBlock
				
		iIterator = 0
		
		self.DISC_CHANNELS      = []
		self.DISC_CHANNELS_PING = []
		self.DISC_CHANNELS_MINT = []
		
		
		while self.fFirstBlock + 2000 < iLastBlock or self.fFast:
		
			self.fReBuildDataBase = True
			self.fFast = False
		
			# Load exode history to build the database
			acc = Account("exodegame")
			self.fLoadExodeGame = True
			
			c_last_block_chain = bBlockC.get_current_block_num()
			
			# Load only cancel transaction			
			c_block = int(db_Cancel_GetLastBlock())	
			if ( c_block < iMinimumBlock_cancel ):
				c_block = iMinimumBlock_cancel
			
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
						db_FillCancellation_TX( mTxId, tBlock )	
						
					c_block_cur = tBlock
			
			# Set last block seen
			db_Cancel_SetLastBlock(c_block_cur)
			
			# Load list
			self.fCancelTransactionList = db_Cancel_GetTXs()
			
			print ( self.fCancelTransactionList )			
			
			# Temporary test, load everything
			#iFirstBlock = 0
			
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
				
			self.fLoadExodeGame = False
			
			# Load player history to build sell database	
			self.fLoadPlayerMarket = True
			print("Load player list")
			m_players = db_ExodePlayers_List()
			iPlayer   = 0
			for player_name in m_players:
			
				
				try:
					acc = Account(player_name)
				except bexceptions.AccountDoesNotExistsException:
					print("Account ", player_name, " does not exists!")
					continue
					
									
				c_block_1 = db_TX_GetLastBlock(player_name)
				c_block_2 = db_Player_GetLastBlock(player_name)
				c_block = max(c_block_1,c_block_2)
								
				if ( c_block < iMinimumBlock ):
					c_block = iMinimumBlock
				
				hTransactionList = []	
					
				for hTransaction in acc.history_reverse(start=c_last_block_exode+1,batch_size=1):			
					tBlock = hTransaction['block']
					
					if ( tBlock < c_block+1 ):
						break
						
					hTransactionList.insert(0, hTransaction)
					
				
				print("Scan player account: ", player_name, "(", iPlayer, "/", len(m_players),")"," transactions")
				iPlayer = iPlayer + 1
				
				c_block_cur = 0
				
				#if ( (c_block+1) < c_last_block ):
					#for hTransaction in acc.history(start=c_block+1, stop=c_last_block, use_block_num=True ):				
				if ( len(c_last_transaction) > 0 ):
					for hTransaction in hTransactionList:
					
						#print(hTransaction)
						tType  = hTransaction['type']
						tBlock = hTransaction['block']
						
						
						print("Read ", player_name, "(", iPlayer, "/", len(m_players),")"," transactions in block: ", tBlock,"/",c_last_block)
						
						if( tType != 'custom_json' ):
							continue
							
						lOut = await self.ProcessTransaction(tType, tBlock, hTransaction )
						
						if ( lOut == excst.ALERT_KILL ):
							print("Quit...")
							return
						
						iIterator = iIterator + 1
						c_block_cur = tBlock
				
				hTransactionList.clear() 	
				db_Player_SetLastBlock(player_name,c_last_block)
			self.fLoadPlayerMarket = False
				
			iLastBlock = bBlockC.get_current_block_num()

			if ( os.path.isfile('logs/file_block_fast.json') ):
				with open('logs/file_block_fast.json', 'r') as f:
					self.fFirstBlock = json.load(f) 
		
		# Change flag	
		self.fReBuildDataBase = False
		self.fDoDiscord       = True
		
		# Initialize iterator
		iIterator = 0
		
		# It's running! 
		while True:
		
			# Get first block
			iFirstBlock = 0
			if ( os.path.isfile('logs/file_block_fast.json') ):
				with open('logs/file_block_fast.json', 'r') as f:
					iFirstBlock = json.load(f) 
			
			if ( iFirstBlock < iMinimumBlock ):
				iFirstBlock = iMinimumBlock
			
			# Get last block
			iLastBlock = bBlockC.get_current_block_num()
			
			while iLastBlock < iFirstBlock+1:
				print("sleeping...")
				time.sleep(3.)
				iLastBlock = bBlockC.get_current_block_num()
			
			# Loop over blocks
			for iBlock in range(iFirstBlock+1,iLastBlock):
										
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
						return
						
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
					
				print("Read block: ", iBlock+1)
				tTransList = Block(iBlock+1).json_transactions;
					
				for tTrans in tTransList:
				
					#print(tTrans)
					tOperationList = tTrans['operations']
				
					for tOperation in tOperationList:
				
						tType = tOperation['type']
				
						if( tType != 'custom_json_operation' and tType != 'transfer_operation' ):
							continue	
						
						#print ( tOperation )
						lOut = await self.ProcessTransaction( tType, iBlock+1, tOperation['value'] )
						
						if ( lOut == excst.ALERT_KILL ):
							print("Quit...")
							return
			
											
				with open('logs/file_block_fast.json', 'w') as f:
					json.dump( iBlock, f ) 

			
	@read_exode.before_loop
	async def read_exode_preparation(self):
		await self.wait_until_ready() # wait until the bot logs in
	
##############################################################################################################################################		

DISC_CLIENT = my_eXode_bot()

DISC_CLIENT.run(BOT_TOKEN)


		
