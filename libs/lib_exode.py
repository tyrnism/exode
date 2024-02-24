
def ex_IsPack( mID ):
	(is_pack, asset_name, asset_rank, asset_num) = ex_GetAssetDetails( mID )
	return is_pack
	
def ex_IsElite( mID ):
	return ( mID[:12] == "exode_card_E" )

def ex_IsNameElite( name: str ):
	
	if ( name[:12] == "exode_card_E" ):
		return True
	
	if name.lower()[:5] == "elite":
		return True
	
	return False

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
		return (True, "???? booster",										NO_RARITY, 		0)
	if ( mID == "exode_alpha_booster" ):
		return (True, "Alpha booster",										NO_RARITY, 		0)
	if ( mID == "exode_beta_booster" ):
		return (True, "Beta booster",										NO_RARITY, 		0)
		
	if ( mID == "exode_alpha_support_vega" ):
		return (True, "Alpha Escort Pack [Vega]",							NO_RARITY, 		0)
	if ( mID == "exode_alpha_support_ionguards" ):
		return (True, "Alpha Escort Pack [Ion Guards]",						NO_RARITY, 		0)
	if ( mID == "exode_alpha_support_tom" ):		
		return (True, "Alpha Support Pack [TOM Essentials]",				NO_RARITY, 		0)
		
	if ( mID == "exode_alpha_starter_1" ):
		return (True, "Alpha Starter [Navy Lieutenant]",					NO_RARITY, 		0)
	if ( mID == "exode_alpha_starter_2" ):
		return (True, "Alpha Starter [Ark Scientist]",						NO_RARITY, 		0)
	if ( mID == "exode_alpha_starter_3" ):
		return (True, "Alpha Starter [Elected Leader]",						NO_RARITY, 		0)
	if ( mID == "exode_alpha_starter_4" ):
		return (True, "Triple Alpha Starter Set",							NO_RARITY, 		0)
	
	if ( mID == "exode_beta_starter_1" ):
		return (True, "Beta Starter [Self-Made Savior]",					NO_RARITY, 		0)
	if ( mID == "exode_beta_starter_2" ):
		return (True, "Beta Starter [Utopian Thinker]",						NO_RARITY, 		0)
	if ( mID == "exode_beta_starter_3" ):
		return (True, "Beta Starter [Religious Visionary]",					NO_RARITY, 		0)
	if ( mID == "exode_beta_starter_4" ):
		return (True, "Special Starter [Rebel Agent]",						NO_RARITY, 		0)
	
	if ( mID == "exode_alpha_contract_tom" ):
		return (True, "Alpha Contract [TOM Settler PREMIUM BUDDIES]", 		NO_RARITY, 		0)
	if ( mID == "exode_alpha_contract_rekatron" ):
		return (True, "Alpha Contract [WEAPON DROPS BY REKATRON]", 			NO_RARITY, 		0)
	if ( mID == "exode_alpha_contract_syndicate" ):
		return (True, "Alpha Contract [SYNDICATE SPONSORSHIP]", 			NO_RARITY, 		0)
		
	if ( mID == "exode_beta_contract_achean" ):
		return (True, "Beta Contract [Your Own Achean Gang]",				NO_RARITY, 		0)
	if ( mID == "exode_beta_contract_starships_mods" ):
		return (True, "Beta Contract [Vogar Shipyards]",					NO_RARITY, 		0)
	if ( mID == "exode_beta_contract_armor_mods" ):
		return (True, "Beta Contract [Esdrovian Armor Docks]",				NO_RARITY, 		0)
	if ( mID == "exode_beta_contract_shop_franchise" ):
		return (True, "Beta Contract [Starbase Shop Ownership]",			NO_RARITY, 		0)
	if ( mID == "exode_beta_contract_street_franchise" ):
		return (True, "Beta Contract [Street Shop Ownership]",				NO_RARITY, 		0)
		
	if ( mID == "exode_alpha_pack_crew_kb119" ):
		return (True, "Alpha Crew Pack [Kilbot-119]",						NO_RARITY, 		0)
	if ( mID == "exode_alpha_pack_crew_galvin4" ):
		return (True, "Alpha Crew Pack [Galvin 4]",							NO_RARITY, 		0)
		
	if ( mID == "exode_alpha_character_pack_nomad" ):
		return (True, "Alpha Promo Character Pack [Nomad Navigator]", 		NO_RARITY, 		0)
	if ( mID == "exode_alpha_character_pack_genetician" ):
		return (True, "Alpha Promo Character Pack [Genetician Scientist]",	NO_RARITY, 		0)
	if ( mID == "exode_alpha_character_pack_suntek" ):
		return (True, "Alpha Promo Character Pack [Suntek Survivor]",		NO_RARITY, 		0)
	if ( mID == "exode_alpha_character_pack_drachian" ):
		return (True, "Alpha Promo Character Pack [Drachian Colonel]",		NO_RARITY, 		0)
	
	if ( mID == "exode_pack_currency_200" ):
		return (True, "Credits pack [4400 EXOCREDITS + 1 Unique Epic]",		NO_RARITY, 		0)
	if ( mID == "exode_pack_currency_1000" ):
		return (True, "Credits pack [25.5k EXOCREDITS + 1 Unique Elite Epic]",		NO_RARITY, 		0)

	if ( mID == "exode_card_001_originNavy" 						or mID == "exode_card_E001_originNavy" ):
		return (False, "Navy Lieutenant [Origin]", 							EPIC_CARD, 		1)	
	if ( mID == "exode_card_002_shipArcheon" 						or mID == "exode_card_E002_shipArcheon" ):
		return (False, "Military Frigate (\"Archeon Class\")", 				EPIC_CARD,		2)	
	if ( mID == "exode_card_003_officerComms" 						or mID == "exode_card_E003_officerComms" ):
		return (False, "Communications Officer", 							RARE_CARD,		3)
	if ( mID == "exode_card_004_officerWeapons" 					or mID == "exode_card_E004_officerWeapons" ):
		return (False, "Weapons Officer", 									RARE_CARD,		4)		
	if ( mID == "exode_card_005_officerTactical" 					or mID == "exode_card_E005_officerTactical" ):
		return (False, "Tactical Officer", 									RARE_CARD,		5)		
	if ( mID == "exode_card_006_crewPilot" 							or mID == "exode_card_E006_crewPilot" ):
		return (False, "Pilot (Crew)", 										RARE_CARD,		6)		
	if ( mID == "exode_card_007_crewSRT" 							or mID == "exode_card_E007_crewSRT" ):
		return (False, "Signals Specialist (Crew)", 						RARE_CARD,		7)		
	if ( mID == "exode_card_008_crewDefense"						or mID == "exode_card_E008_crewDefense" ):
		return (False, "Defense Specialist (Crew)", 						RARE_CARD,		8)		
	if ( mID == "exode_card_009_crewTrooper" 						or mID == "exode_card_E009_crewTrooper" ):
		return (False, "Trooper (Crew)", 									COMMON_CARD,	9)		
	if ( mID == "exode_card_010_crewEngineer" 						or mID == "exode_card_E010_crewEngineer" ):
		return (False, "Military Engineer (Crew)", 							COMMON_CARD,	10)			
	if ( mID == "exode_card_011_setFMR17" 							or mID == "exode_card_E011_setFMR17" ):
		return (False, "FMR-17 \'Atonis\' (x3)", 							EPIC_CARD,		11)		
	if ( mID == "exode_card_012_setSuitMilitaryC" 					or mID == "exode_card_E012_setSuitMilitaryC" ):
		return (False, "Military Suit Class C (x3)", 						RARE_CARD,		12)		
	if ( mID == "exode_card_013_originArk" 							or mID == "exode_card_E013_originArk" ):
		return (False, "Ark Scientist [Origin]", 							EPIC_CARD,		13)		
	if ( mID == "exode_card_014_shipOrwell1" 						or mID == "exode_card_E014_shipOrwell1" ):
		return (False, "Ark Ship \"Orwell 1\"", 							EPIC_CARD,		14)		
	if ( mID == "exode_card_015_officerResearch" 					or mID == "exode_card_E015_officerResearch" ):
		return (False, "Research Officer", 									RARE_CARD,		15)		
	if ( mID == "exode_card_016_officerExploration" 				or mID == "exode_card_E016_officerExploration" ):
		return (False, "Exploration Officer", 								RARE_CARD,		16)	
	if ( mID == "exode_card_017_officerPreservation" 				or mID == "exode_card_E017_officerPreservation" ):
		return (False, "Preservation Officer", 								RARE_CARD,		17)	
	if ( mID == "exode_card_018_crewSurgeon" 						or mID == "exode_card_E018_crewSurgeon" ):
		return (False, "Space Surgeon", 									RARE_CARD,		18)	
	if ( mID == "exode_card_019_crewXenoAnalyst" 					or mID == "exode_card_E019_crewXenoAnalyst" ):
		return (False, "Xeno Analyst", 										RARE_CARD,		19)	
	if ( mID == "exode_card_020_crewBioScientist" 					or mID == "exode_card_E020_crewBioScientist" ):
		return (False, "Space Bioscientist", 								RARE_CARD,		20)	
	if ( mID == "exode_card_021_crewAnimalHandler" 					or mID == "exode_card_E021_crewAnimalHandler" ):
		return (False, "Animal Handler (Crew)", 							COMMON_CARD,	21)	
	if ( mID == "exode_card_022_crewLifeSearcher" 					or mID == "exode_card_E022_crewLifeSearcher" ):
		return (False, "Life Searcher (Crew)", 								COMMON_CARD,	22)	
	if ( mID == "exode_card_023_crewLabScientist" 					or mID == "exode_card_E023_crewLabScientist" ):
		return (False, "Lab Scientist (Crew)", 								COMMON_CARD,	23)	
	if ( mID == "exode_card_024_setRarePlants" 						or mID == "exode_card_E024_setRarePlants" ):
		return (False, "Rare Plants Collection (x6)", 						EPIC_CARD,		24)	
	if ( mID == "exode_card_025_setSuitResearchC" 					or mID == "exode_card_E025_setSuitResearchC" ):
		return (False, "Research Suits Class C (x3)", 						RARE_CARD,		25)	
	if ( mID == "exode_card_026_originLeader" 						or mID == "exode_card_E026_originLeader" ):
		return (False, "Elected Leader [Origin]", 							EPIC_CARD,		26)	
	if ( mID == "exode_card_027_shipDiplomatic" 					or mID == "exode_card_E027_shipDiplomatic" ):
		return (False, "Diplomatic Corvette \"Amarasia\"", 					EPIC_CARD,		27)	
	if ( mID == "exode_card_028_officerAdministrative" 				or mID == "exode_card_E028_officerAdministrative" ):
		return (False, "Administrative Officer", 							RARE_CARD,		28)	
	if ( mID == "exode_card_029_officerSecurity" 					or mID == "exode_card_E029_officerSecurity" ):
		return (False, "Security Officer", 									RARE_CARD,		29)	
	if ( mID == "exode_card_030_crewPropaganda"						or mID == "exode_card_E030_crewPropaganda" ):
		return (False, "Propaganda Specialist", 							RARE_CARD,		30)	
	if ( mID == "exode_card_031_crewPopulation" 					or mID == "exode_card_E031_crewPopulation" ):
		return (False, "Population Analyst", 								RARE_CARD,		31)	
	if ( mID == "exode_card_032_crewEntertainment" 					or mID == "exode_card_E032_crewEntertainment" ):
		return (False, "Welfare Specialist", 								RARE_CARD,		32)	
	if ( mID == "exode_card_033_crewMaintenance" 					or mID == "exode_card_E033_crewMaintenance" ):
		return (False, "Maintenance Staff (Crew)", 							COMMON_CARD,	33)	
	if ( mID == "exode_card_034_crewPilotCivilian" 					or mID == "exode_card_E034_crewPilotCivilian" ):
		return (False, "Civilian Pilot (Crew)", 							COMMON_CARD,	34)	
	if ( mID == "exode_card_035_crewSecurity" 						or mID == "exode_card_E035_crewSecurity" ):
		return (False, "Security Guard (Crew)", 							COMMON_CARD,	35)	
	if ( mID == "exode_card_036_setLuxury" 							or mID == "exode_card_E036_setLuxury" ):
		return (False, "Diplomatic Gifts", 									RARE_CARD,		36)	
	if ( mID == "exode_card_037_setDatabase" 						or mID == "exode_card_E037_setDatabase" ):
		return (False, "Federal Database", 									EPIC_CARD,		37)	
		
	if ( mID == "exode_card_039_Tom_BeautyCapsule" 					or mID == "exode_card_E039_Tom_BeautyCapsule" ):
		return (False, "BEAUTY Capsule", 									EPIC_CARD,		39)	
		
		
	if ( mID == "exode_card_045_Rekatron_fireworks" 				or mID == "exode_card_E045_Rekatron_fireworks" ):
		return (False, "FIREWORKS",	 										LEGENDARY_CARD,	45)
	if ( mID == "exode_card_046_Rekatron_defensiveAmmo" 			or mID == "exode_card_E046_Rekatron_defensiveAmmo" ):
		return (False, "DEFENSIVE AMMO",	 								COMMON_CARD,	46)
	if ( mID == "exode_card_047_Rekatron_firetalkerPistol" 			or mID == "exode_card_E047_Rekatron_firetalkerPistol" ):
		return (False, "FIRETALKER", 										COMMON_CARD,	47)
	if ( mID == "exode_card_048_Rekatron_karperPistol" 				or mID == "exode_card_E048_Rekatron_karperPistol" ):
		return (False, "KARPER Heavy", 										RARE_CARD,		48)
	if ( mID == "exode_card_049_Rekatron_explanatorRifle" 			or mID == "exode_card_E049_Rekatron_explanatorRifle" ):
		return (False, "EXPLANATOR", 										RARE_CARD,		49)
	if ( mID == "exode_card_050_Rekatron_rsdRifle" 					or mID == "exode_card_E050_Rekatron_rsdRifle" ):
		return (False, "REKATRON SD", 										RARE_CARD,		50)
	if ( mID == "exode_card_051_Rekatron_goodMorningPistol" 		or mID == "exode_card_E051_Rekatron_goodMorningPistol" ):
		return (False, "GOOD MORNING", 										RARE_CARD,		51)
	if ( mID == "exode_card_052_Rekatron_jugdmentDayRifle" 			or mID == "exode_card_E052_Rekatron_jugdmentDayRifle" ):
		return (False, "JUDGEMENT DAY", 									EPIC_CARD,		52)
	if ( mID == "exode_card_053_Rekatron_galacticPeacemaker"	 	or mID == "exode_card_E053_Rekatron_galacticPeacemaker" ):
		return (False, "GALACTIC PEACEMAKER", 								EPIC_CARD,		53)
	if ( mID == "exode_card_054_Rekatron_ammoGuided" 				or mID == "exode_card_E054_Rekatron_ammoGuided" ):
		return (False, "AUTOGUIDED AMMO", 									RARE_CARD,		54)
	if ( mID == "exode_card_055_Rekatron_ammoParty" 				or mID == "exode_card_E055_Rekatron_ammoParty" ):
		return (False, "PARTY AMMO", 										EPIC_CARD,		55)
	if ( mID == "exode_card_056_Tom_SmootyAllInOne" 				or mID == "exode_card_E056_Tom_SmootyAllInOne" ):
		return (False, "SMOOTY All-In-One", 								COMMON_CARD,	56)
	if ( mID == "exode_card_057_Tom_FoodieMoodie" 					or mID == "exode_card_E057_Tom_FoodieMoodie" ):
		return (False, "Strategic FOODIE-MOODIE", 							COMMON_CARD,	57)
	if ( mID == "exode_card_058_Tom_FriendlyEyes" 					or mID == "exode_card_E058_Tom_FriendlyEyes" ):
		return (False, "Friendly Eyes XY-6", 								COMMON_CARD,	58)
	if ( mID == "exode_card_059_Tom_BuddyPinger" 					or mID == "exode_card_E059_Tom_BuddyPinger" ):
		return (False, "BUDDY Pinger", 										RARE_CARD,		59)
	if ( mID == "exode_card_060_Tom_VehicleLittleBuddy" 			or mID == "exode_card_E060_Tom_VehicleLittleBuddy" ):
		return (False, "LITTLE Buddy", 										RARE_CARD,		60)
	if ( mID == "exode_card_061_Tom_Custom" 						or mID == "exode_card_E061_Tom_Custom" ):
		return (False, "TOM Custom", 										RARE_CARD,		61)
	if ( mID == "exode_card_062_Tom_WHCConverter" 					or mID == "exode_card_E062_Tom_WHCConverter" ):
		return (False, "WHC Unit", 											RARE_CARD,		62)
	if ( mID == "exode_card_063_Tom_Explorator" 					or mID == "exode_card_E063_Tom_Explorator" ):
		return (False, "TOM Explorator X4", 								EPIC_CARD,		63)
	if ( mID == "exode_card_064_Tom_ShelterHappyFive" 				or mID == "exode_card_E064_Tom_ShelterHappyFive" ):
		return (False, "SHELTER \"Happy Five\"", 							EPIC_CARD,		64)
		
	if ( mID == "exode_card_065_SyndicateGeisha_ThirdSister" 		or mID == "exode_card_E065_SyndicateGeisha_ThirdSister" ):
		return (False, "Syndicate Geisha",	 								EPIC_CARD,		65)
	if ( mID == "exode_card_066_SyndicateEquipment_Chip"	 		or mID == "exode_card_E066_SyndicateEquipment_Chip" ):
		return (False, "Syndicate Chip", 									COMMON_CARD,	66)
	if ( mID == "exode_card_067_SyndicateEquipment_DrugHolidays"	or mID == "exode_card_E067_SyndicateEquipment_DrugHolidays" ):
		return (False, "\'Holidays\'", 										COMMON_CARD,	67)
	if ( mID == "exode_card_068_SyndicateEquipment_DrugNPrime"		or mID == "exode_card_E068_SyndicateEquipment_DrugNPrime" ):
		return (False, "\'N-Prime\'", 										COMMON_CARD,	68)
	if ( mID == "exode_card_069_SyndicateShipBlackLotus" 			or mID == "exode_card_E069_SyndicateShipBlackLotus" ):
		return (False, "\"Black Lotus\"", 									EPIC_CARD,		69)
	if ( mID == "exode_card_070_SyndicateEquipmentAutoBlaster"		or mID == "exode_card_E070_SyndicateEquipmentAutoBlaster" ):
		return (False, "Syndicate Auto Blaster", 							RARE_CARD,		70)	
	if ( mID == "exode_card_071_SyndicateEquipment_NarcoWarfare"	or mID == "exode_card_E071_SyndicateEquipment_NarcoWarfare" ):
		return (False, "Narco-Warfare", 									RARE_CARD,		71)
	if ( mID == "exode_card_072_SyndicateEquipmentSet_Genefactory" 	or mID == "exode_card_E072_SyndicateEquipmentSet_Genefactory" ):
		return (False, "Nacrotics Genefactory", 							EPIC_CARD,		72)			
	if ( mID == "exode_card_073_SyndicateHacker" 					or mID == "exode_card_E073_SyndicateHacker" ):
		return (False, "Syndicate Hacker", 									RARE_CARD,		73)
	if ( mID == "exode_card_074_SyndicateLeader" 					or mID == "exode_card_E074_SyndicateLeader" ):
		return (False, "Syndicate Squad Leader", 							RARE_CARD,		74)		
	if ( mID == "exode_card_075_SyndicateTransactor" 				or mID == "exode_card_E075_SyndicateTransactor" ):
		return (False, "Programmed Transactor", 							RARE_CARD,		75)	
	if ( mID == "exode_card_076_SyndicateTrooper" 					or mID == "exode_card_E076_SyndicateTrooper" ):
		return (False, "Syndicate Trooper", 								RARE_CARD,		76)
	if ( mID == "exode_card_077_SyndicateAyumi" 					or mID == "exode_card_E077_SyndicateAyumi" ):
		return (False, "Ayumi", 											EPIC_CARD,		77)
	if ( mID == "exode_card_078_SyndicateYakuzaNoble" 				or mID == "exode_card_E078_SyndicateYakuzaNoble" ):
		return (False, "Battle-Trained Socialite", 							EPIC_CARD,		78)
	if ( mID == "exode_card_079_SyndicateYakuzaSniper" 				or mID == "exode_card_E079_SyndicateYakuzaSniper" ):
		return (False, "Camouflaged Sniper", 								EPIC_CARD,		79)
	if ( mID == "exode_card_080_TheKumicho" 						or mID == "exode_card_E080_TheKumicho" ):
		return (False, "The Kumicho", 										LEGENDARY_CARD,	80)
	if ( mID == "exode_card_081_RebelGeneral" 						or mID == "exode_card_E081_RebelGeneral" ):
		return (False, "Rebel General", 									LEGENDARY_CARD,	81)
	if ( mID == "exode_card_082_AlannaVos" 							or mID == "exode_card_E082_AlannaVos" ):
		return (False, "Alanna Vös, Federal Marshal", 						LEGENDARY_CARD,	82)
	if ( mID == "exode_card_083_Sh4rken" 							or mID == "exode_card_E083_Sh4rken" ):
		return (False, "Sh4rken", 											LEGENDARY_CARD,	83)
	if ( mID == "exode_card_084_TheAI" 								or mID == "exode_card_E084_TheAI" ):
		return (False, "Mysterious AI", 									LEGENDARY_CARD,	84)
	if ( mID == "exode_card_085_Apprentice" 						or mID == "exode_card_E085_Apprentice" ):
		return (False, "Mysterious Robot", 									LEGENDARY_CARD,	85)
	if ( mID == "exode_card_086_Cranium" 							or mID == "exode_card_E086_Cranium" ):
		return (False, "Captain Cranium", 									LEGENDARY_CARD,	86)
	if ( mID == "exode_card_087_Cryptoeater" 						or mID == "exode_card_E087_Cryptoeater" ):
		return (False, "\"Crypto-Eater\"", 									LEGENDARY_CARD,	87)
	if ( mID == "exode_card_088_originRepentantPirate" 				or mID == "exode_card_E088_originRepentantPirate" ):
		return (False, "Repentant Pirate [Origin]", 						LEGENDARY_CARD,	88)
	if ( mID == "exode_card_089_shipColombus" 						or mID == "exode_card_E089_shipColombus" ):
		return (False, "\"The Colombus\" (circa 2113)", 					LEGENDARY_CARD,	89)
	if ( mID == "exode_card_090_shipQuantumSupreme"					or mID == "exode_card_E090_shipQuantumSupreme" ):
		return (False, "\"Quantum\" Class Supreme", 						LEGENDARY_CARD,	90)
	if ( mID == "exode_card_091_vehicleVelvetStorm" 				or mID == "exode_card_E091_vehicleVelvetStorm" ):
		return (False, "\"Velvet Storm\"", 									LEGENDARY_CARD,	91)
	if ( mID == "exode_card_092_vehicleVanguard" 					or mID == "exode_card_E092_vehicleVanguard" ):
		return (False, "\"Vanguard\"", 										LEGENDARY_CARD,	92)
	if ( mID == "exode_card_093_equipmentSuitArena" 				or mID == "exode_card_E093_equipmentSuitArena" ):
		return (False, "Arena Powersuit (signed by Kurban Ko)",				LEGENDARY_CARD,	93)
		
	if ( mID == "exode_card_101_originSecretAgent" 					or mID == "exode_card_E101_originSecretAgent" ):
		return (False, "Secret Agent [Origin]", 							EPIC_CARD,		101)
	if ( mID == "exode_card_102_originStrandedTrader" 				or mID == "exode_card_E102_originStrandedTrader" ):
		return (False, "Stranded Trader [Origin]", 							EPIC_CARD,		102)
	if ( mID == "exode_card_103_originCruiseShipCaptain" 			or mID == "exode_card_E103_originCruiseShipCaptain" ):
		return (False, "Cruise Ship Captain [Origin]", 						EPIC_CARD,		103)
	if ( mID == "exode_card_104_shipArkLifesavior" 					or mID == "exode_card_E104_shipArkLifesavior" ):
		return (False, "Ark Ship \"Orwell 2\" Lifesavior", 					EPIC_CARD,		104)
	if ( mID == "exode_card_105_shipCargoKormen" 					or mID == "exode_card_E105_shipCargoKormen" ):
		return (False, "\"Kormen\" Class (Cargo)", 							EPIC_CARD,		105)
	if ( mID == "exode_card_106_shipRhino" 							or mID == "exode_card_E106_shipRhino" ):
		return (False, "\"Rhino\" Heavy Attack Frigate", 					EPIC_CARD,		106)
	if ( mID == "exode_card_107_shipCargoTaurus" 					or mID == "exode_card_E107_shipCargoTaurus" ):
		return (False, "\"Taurus\" Class Transport", 						EPIC_CARD,		107)
	if ( mID == "exode_card_108_shipMyrmidon" 						or mID == "exode_card_E108_shipMyrmidon" ):
		return (False, "\"Myrmidon\" Assault Transport", 					EPIC_CARD,		108)
	if ( mID == "exode_card_109_shipAkhen" 							or mID == "exode_card_E109_shipAkhen" ):
		return (False, "\"Akhen\" Cannon", 									EPIC_CARD,		109)
	if ( mID == "exode_card_110_shipCoetus" 						or mID == "exode_card_E110_shipCoetus" ):
		return (False, "\"Coetus\" Class Science Vessel", 					EPIC_CARD,		110)
	if ( mID == "exode_card_111_setGeneticianConsole" 				or mID == "exode_card_E111_setGeneticianConsole" ):
		return (False, "Genetician Console", 								EPIC_CARD,		111)
	if ( mID == "exode_card_112_setMilitaryClassA" 					or mID == "exode_card_E112_setMilitaryClassA" ):
		return (False, "Military Suits Class A (x3)", 						EPIC_CARD,		112)
	if ( mID == "exode_card_113_setEisenSuits" 						or mID == "exode_card_E113_setEisenSuits" ):
		return (False, "Eisen Suits (x3)", 									EPIC_CARD,		113)
	if ( mID == "exode_card_114_vehicleAcheanRacer" 				or mID == "exode_card_E114_vehicleAcheanRacer" ):
		return (False, "Archean Racer", 									EPIC_CARD,		114)
	if ( mID == "exode_card_115_crewSpaceMarshal"					or mID == "exode_card_E115_crewSpaceMarshal" ):
		return (False, "Space Federal Marshal", 							EPIC_CARD,		115)
	if ( mID == "exode_card_116_officerEliza" 						or mID == "exode_card_E116_officerEliza" ):
		return (False, "Eliza", 											EPIC_CARD,		116)
	if ( mID == "exode_card_117_crewOksana" 						or mID == "exode_card_E117_crewOksana" ):
		return (False, "Oksana", 											EPIC_CARD,		117)
	if ( mID == "exode_card_118_officerNorah" 						or mID == "exode_card_E118_officerNorah" ):
		return (False, "Norah", 											EPIC_CARD,		118)
	if ( mID == "exode_card_119_officerShen" 						or mID == "exode_card_E119_officerShen" ):
		return (False, "Shen", 												EPIC_CARD,		119)
	if ( mID == "exode_card_120_officerStug" 						or mID == "exode_card_E120_officerStug" ):
		return (False, "Stug", 												EPIC_CARD,		120)
	if ( mID == "exode_card_121_crewTyron" 							or mID == "exode_card_E121_crewTyron" ):
		return (False, "Tyron", 											EPIC_CARD,		121)
	if ( mID == "exode_card_122_officerAdmiralValro" 				or mID == "exode_card_E122_officerAdmiralValro" ):
		return (False, "Admiral Valro", 									EPIC_CARD,		122)
	if ( mID == "exode_card_123_officerNash" 						or mID == "exode_card_E123_officerNash" ):
		return (False, "Nash, \"The Expert\"", 								EPIC_CARD,		123)
	if ( mID == "exode_card_124_crewSpecialInfiltrationAgent" 		or mID == "exode_card_E124_crewSpecialInfiltrationAgent" ):
		return (False, "Special Infiltration Agent", 						EPIC_CARD,		124)
	if ( mID == "exode_card_125_crewScarletSarah" 					or mID == "exode_card_E125_crewScarletSarah" ):
		return (False, "\'Scarlet Sarah\'", 								EPIC_CARD,		125)
	if ( mID == "exode_card_126_passengerNuclearFamily" 			or mID == "exode_card_E126_passengerNuclearFamily" ):
		return (False, "Nuclear Family", 									EPIC_CARD,		126)
	if ( mID == "exode_card_127_installationOctohome" 				or mID == "exode_card_E127_installationOctohome" ):
		return (False, "Octohome", 											EPIC_CARD,		127)
	if ( mID == "exode_card_128_installationOrbitalShield" 			or mID == "exode_card_E128_installationOrbitalShield" ):
		return (False, "Orbital Shield", 									EPIC_CARD,		128)
	if ( mID == "exode_card_129_installationDreamsphere" 			or mID == "exode_card_E129_installationDreamsphere" ):
		return (False, "Dreamsphere", 										EPIC_CARD,		129)
	if ( mID == "exode_card_130_installationGenerator100"			or mID == "exode_card_E130_installationGenerator100" ):
		return (False, "X-Gen TR100", 										EPIC_CARD,		130)
	if ( mID == "exode_card_131_equipmentFactionCorporate" 			or mID == "exode_card_E131_equipmentFactionCorporate" ):
		return (False, "Corporate License (Level S+)", 						EPIC_CARD,		131)
	if ( mID == "exode_card_132_equipmentSuitRacer" 				or mID == "exode_card_E132_equipmentSuitRacer" ):
		return (False, "Racer Mech-Suit", 									EPIC_CARD,		132)
	if ( mID == "exode_card_133_equipmentSuitSpartan" 				or mID == "exode_card_E133_equipmentSuitSpartan" ):
		return (False, "Spartan Elite Suit", 								EPIC_CARD,		133)
	if ( mID == "exode_card_134_equipmentFactionRebellion" 			or mID == "exode_card_E134_equipmentFactionRebellion" ):
		return (False, "The Rebellion Secrets ||\"They knew\"||",			EPIC_CARD,		134)
	if ( mID == "exode_card_135_escortSabre" 						or mID == "exode_card_E135_escortSabre" ):
		return (False, "Sabre Regiment", 									EPIC_CARD,		135)
	if ( mID == "exode_card_136_crewFleshCultLeader" 				or mID == "exode_card_E136_crewFleshCultLeader" ):
		return (False, "Flesh Cult Leader", 								EPIC_CARD,		136)
	if ( mID == "exode_card_137_installationDefensiveBunker" 		or mID == "exode_card_E137_installationDefensiveBunker" ):
		return (False, "Defensive Bunker", 									EPIC_CARD,		137)
		
	if ( mID == "exode_card_151_officerDrachianColonel" 			or mID == "exode_card_E151_officerDrachianColonel" ):
		return (False, "Drachian Colonel", 									EPIC_CARD,		151)
	if ( mID == "exode_card_152_crewNomadNavigator" 				or mID == "exode_card_E152_crewNomadNavigator" ):
		return (False, "Nomad Navigator", 									EPIC_CARD,		152)
	if ( mID == "exode_card_153_crewGeneticianScientist" 			or mID == "exode_card_E153_crewGeneticianScientist" ):
		return (False, "Genetician Scientist", 								EPIC_CARD,		153)
	if ( mID == "exode_card_154_crewSuntekSurvivor" 				or mID == "exode_card_E154_crewSuntekSurvivor" ):
		return (False, "Suntek Collector", 									EPIC_CARD,		154)
	if ( mID == "exode_card_155_crewKilbot" 						or mID == "exode_card_E155_crewKilbot" ):
		return (False, "KB-119 \'Kilbot\'", 								EPIC_CARD,		155)
	if ( mID == "exode_card_156_crewGalvin" 						or mID == "exode_card_E156_crewGalvin" ):
		return (False, "Galvin-4, Social Robot", 							EPIC_CARD,		156)
	if ( mID == "exode_card_157_escortVega" 						or mID == "exode_card_E157_escortVega" ):
		return (False, "Vega Elite Squadron", 								EPIC_CARD,		157)
	if ( mID == "exode_card_158_escortIonguards" 					or mID == "exode_card_E158_escortIonguards" ):
		return (False, "Ionguard Defense Fleet", 							EPIC_CARD,		158)
	if ( mID == "exode_card_159_suntekSphere" 						or mID == "exode_card_E159_suntekSphere" ):
		return (False, "Suntek Energy Sphere", 								EPIC_CARD,		159)
		
		
	if ( mID == "exode_card_181_escortLongswords" 					or mID == "exode_card_E181_escortLongswords" ):
		return (False, "Longsword Squadron", 								RARE_CARD,		181)
	if ( mID == "exode_card_182_escortCruiserTaskForce" 			or mID == "exode_card_E182_escortCruiserTaskForce" ):
		return (False, "Cruiser Task Force", 								RARE_CARD,		182)
	if ( mID == "exode_card_183_escortStarsystemGarrison" 			or mID == "exode_card_E183_escortStarsystemGarrison" ):
		return (False, "Starsystem Garrison", 								COMMON_CARD,	183)
	if ( mID == "exode_card_184_shipBaldie" 						or mID == "exode_card_E184_shipBaldie" ):
		return (False, "\'Baldie\' Shuttle", 								COMMON_CARD,	184)
	if ( mID == "exode_card_185_shipClaymoreHyperfighter" 			or mID == "exode_card_E185_shipClaymoreHyperfighter" ):
		return (False, "\"Claymore\" Hyperfighter", 						RARE_CARD,		185)
	if ( mID == "exode_card_186_shipDrachianMantis" 				or mID == "exode_card_E186_shipDrachianMantis" ):
		return (False, "Drachian \"Mantis\"", 								RARE_CARD,		186)
	if ( mID == "exode_card_187_vehicleSalazar" 					or mID == "exode_card_E187_vehicleSalazar" ):
		return (False, "\"Salazar\" Space Cab", 							COMMON_CARD,	187)
	if ( mID == "exode_card_188_vehicleTraveler2" 					or mID == "exode_card_E188_vehicleTraveler2" ):
		return (False, "Traveler-2", 										COMMON_CARD,	188)
	if ( mID == "exode_card_189_vehicleSupplyDropship" 				or mID == "exode_card_E189_vehicleSupplyDropship" ):
		return (False, "Supply Dropship", 									COMMON_CARD,	189)
	if ( mID == "exode_card_190_vehicleExplorationDropship" 		or mID == "exode_card_E190_vehicleExplorationDropship" ):
		return (False, "Exploration Dropship", 								RARE_CARD,		190)
	if ( mID == "exode_card_191_vehicleZandratti" 					or mID == "exode_card_E191_vehicleZandratti" ):
		return (False, "\"Zandratti\"", 									RARE_CARD,		191)
	if ( mID == "exode_card_192_vehicleSecurityDrone" 				or mID == "exode_card_E192_vehicleSecurityDrone" ):
		return (False, "Security Drone", 									RARE_CARD,		192)
	if ( mID == "exode_card_193_vehiclePantherBike" 				or mID == "exode_card_E193_vehiclePantherBike" ):
		return (False, "Pather Bike", 										RARE_CARD,		193)
		
	if ( mID == "exode_card_201_setMedicalBay" 						or mID == "exode_card_E201_setMedicalBay" ):
		return (False, "Medical Bay", 										RARE_CARD,		201)
	if ( mID == "exode_card_202_equipmentRoboticParts" 				or mID == "exode_card_E202_equipmentRoboticParts" ):
		return (False, "Robotic Parts", 									COMMON_CARD,	202)
	if ( mID == "exode_card_203_equipmentEnergyCells" 				or mID == "exode_card_E203_equipmentEnergyCells" ):
		return (False, "Energy Cells", 										COMMON_CARD,	203)
	if ( mID == "exode_card_204_equipmentShipConstructionParts"		or mID == "exode_card_E204_equipmentShipConstructionParts" ):
		return (False, "Ship Construction Parts", 							COMMON_CARD,	204)
	if ( mID == "exode_card_205_equipmentUniversalFixer" 			or mID == "exode_card_E205_equipmentUniversalFixer" ):
		return (False, "\"Universal Fixer\" Suit", 							COMMON_CARD,	205)
	if ( mID == "exode_card_206_equipmentLonestar" 					or mID == "exode_card_E206_equipmentLonestar" ):
		return (False, "\"Lonestar\" Spacesuit", 							COMMON_CARD,	206)
	if ( mID == "exode_card_207_equipmentChipsAndData" 				or mID == "exode_card_E207_equipmentChipsAndData" ):
		return (False, "Chips and Data", 									COMMON_CARD,	207)
	if ( mID == "exode_card_208_equipmentCorporate" 				or mID == "exode_card_E208_equipmentCorporate" ):
		return (False, "Corporate License", 								RARE_CARD,		208)
	if ( mID == "exode_card_209_equipmentEisenSuit" 				or mID == "exode_card_E209_equipmentEisenSuit" ):
		return (False, "Eisen Suit - Artic Edition", 						RARE_CARD,		209)
	if ( mID == "exode_card_210_equipmentDrachianSuit" 				or mID == "exode_card_E210_equipmentDrachianSuit" ):
		return (False, "Drachian Scarab Armor", 							RARE_CARD,		210)
	if ( mID == "exode_card_211_equipmentMilitarySuit" 				or mID == "exode_card_E211_equipmentMilitarySuit" ):
		return (False, "Military Suit Class A", 							RARE_CARD,		211)
	if ( mID == "exode_card_212_equipmentPlanetscan" 				or mID == "exode_card_E212_equipmentPlanetscan" ):
		return (False, "Planetscan VX", 									RARE_CARD,		212)
	if ( mID == "exode_card_213_equipmentRimscan" 					or mID == "exode_card_E213_equipmentRimscan" ):
		return (False, "Rimscan Software", 									RARE_CARD,		213)
	if ( mID == "exode_card_214_equipmentDesigner" 					or mID == "exode_card_E214_equipmentDesigner" ):
		return (False, "Diamondstar Designer", 								RARE_CARD,		214)
	if ( mID == "exode_card_215_equipmentIdentificationMatrix" 		or mID == "exode_card_E215_equipmentIdentificationMatrix" ):
		return (False, "Identification Matrix", 							COMMON_CARD,	215)
		
	if ( mID == "exode_card_221_crewDrachianCommissar" 				or mID == "exode_card_E221_crewDrachianCommissar" ):
		return (False, "Drachian Commissar", 								RARE_CARD,		221)
	if ( mID == "exode_card_222_crewFederalAgent" 					or mID == "exode_card_E222_crewFederalAgent" ):
		return (False, "Federal Agent", 									RARE_CARD,		222)
	if ( mID == "exode_card_223_crewCorporateBodyguard" 			or mID == "exode_card_E223_crewCorporateBodyguard" ):
		return (False, "Corporate Bodyguard", 								RARE_CARD,		223)
	if ( mID == "exode_card_224_crewFederalMarine" 					or mID == "exode_card_E224_crewFederalMarine" ):
		return (False, "Federal Marine", 									RARE_CARD,		224)
	if ( mID == "exode_card_225_crewFederalPolice" 					or mID == "exode_card_E225_crewFederalPolice" ):
		return (False, "Federal Government Police", 						RARE_CARD,		225)
	if ( mID == "exode_card_226_crewDrachianTrooper" 				or mID == "exode_card_E226_crewDrachianTrooper" ):
		return (False, "Drachian Assault Trooper", 							RARE_CARD,		226)
	if ( mID == "exode_card_227_crewCorneredRebelAgent" 			or mID == "exode_card_E227_crewCorneredRebelAgent" ):
		return (False, "Cornered Rebel Agent", 								RARE_CARD,		227)
	if ( mID == "exode_card_228_passengerDangerous" 				or mID == "exode_card_E228_passengerDangerous" ):
		return (False, "Dangerous Passenger", 								RARE_CARD,		228)
	if ( mID == "exode_card_229_passengerUnstable" 					or mID == "exode_card_E229_passengerUnstable" ):
		return (False, "Unstable Genius", 									COMMON_CARD,	229)
	if ( mID == "exode_card_230_crewMaintenanceDroid" 				or mID == "exode_card_E230_crewMaintenanceDroid" ):
		return (False, "Maintenance Droid", 								COMMON_CARD,	230)
	if ( mID == "exode_card_231_passengerScienceStudent" 			or mID == "exode_card_E231_passengerScienceStudent" ):
		return (False, "Science student", 									COMMON_CARD,	231)
	if ( mID == "exode_card_232_passengerSocialite" 				or mID == "exode_card_E232_passengerSocialite" ):
		return (False, "Socialite", 										COMMON_CARD,	232)
	if ( mID == "exode_card_233_passengerTechExpert" 				or mID == "exode_card_E233_passengerTechExpert" ):
		return (False, "Tech Expert", 										COMMON_CARD,	233)
		
	if ( mID == "exode_card_235_crewTriskan" 						or mID == "exode_card_E235_crewTriskan" ):
		return (False, "Triskan Fighter", 									RARE_CARD,		235)
	if ( mID == "exode_card_236_crewFleshCult"						or mID == "exode_card_E236_crewFleshCult" ):
		return (False, "Flesh Cult Recruiter", 								RARE_CARD,		236)
	if ( mID == "exode_card_237_crewFleshCultScientist" 			or mID == "exode_card_E237_crewFleshCultScientist" ):
		return (False, "Magna Cultist", 									RARE_CARD,		237)
		
	if ( mID == "exode_card_241_installationDrillingMachine" 		or mID == "exode_card_E241_installationDrillingMachine" ):
		return (False, "Drilling Machine", 									COMMON_CARD,	241)
	if ( mID == "exode_card_242_installationRadarArray" 			or mID == "exode_card_E242_installationRadarArray" ):
		return (False, "Radar Array", 										COMMON_CARD,	242)
	if ( mID == "exode_card_243_installationGenerator20" 			or mID == "exode_card_E243_installationGenerator20" ):
		return (False, "X-Gen TR20", 										COMMON_CARD,	243)
	if ( mID == "exode_card_244_installationTomStarter" 			or mID == "exode_card_E244_installationTomStarter" ):
		return (False, "TOM STARTER", 										COMMON_CARD,	244)
	if ( mID == "exode_card_245_installationLiveBlock" 				or mID == "exode_card_E245_installationLiveBlock" ):
		return (False, "Life Block", 										COMMON_CARD,	245)
	if ( mID == "exode_card_246_installationBiodomes" 				or mID == "exode_card_E246_installationBiodomes" ):
		return (False, "Biodomes", 											COMMON_CARD,	246)
	if ( mID == "exode_card_247_installationTurret" 				or mID == "exode_card_E247_installationTurret" ):
		return (False, "AA/AT Automatic Turret", 							COMMON_CARD,	247)
	if ( mID == "exode_card_248_layoutProtectionWalls" 				or mID == "exode_card_E248_layoutProtectionWalls" ):
		return (False, "Protection Walls", 									COMMON_CARD,	248)
	if ( mID == "exode_card_249_layoutUnderground" 					or mID == "exode_card_E249_layoutUnderground" ):
		return (False, "Underground Construction", 							COMMON_CARD,	249)
	if ( mID == "exode_card_250_interiorLabEquipment" 				or mID == "exode_card_E250_interiorLabEquipment" ):
		return (False, "Lab Equipment", 									COMMON_CARD,	250)
	if ( mID == "exode_card_251_interiorManagementConsole"	 		or mID == "exode_card_E251_interiorManagementConsole" ):
		return (False, "Management Console", 								COMMON_CARD,	251)
	if ( mID == "exode_card_252_interiorComputerRoom" 				or mID == "exode_card_E252_interiorComputerRoom" ):
		return (False, "Computer Room",										RARE_CARD,		252)
	if ( mID == "exode_card_253_installationMultipurpose" 			or mID == "exode_card_E253_installationMultipurpose" ):
		return (False, "Multipurpose Prefab", 								COMMON_CARD,	253)
	if ( mID == "exode_card_254_installationCommunicationArray"		or mID == "exode_card_E254_installationCommunicationArray" ):
		return (False, "Communication Array", 								RARE_CARD,		254)
	if ( mID == "exode_card_255_interiorCuves" 						or mID == "exode_card_E255_interiorCuves" ):
		return (False, "Chemical Cuves", 									RARE_CARD,		255)
	if ( mID == "exode_card_256_installationPreservationDome"		or mID == "exode_card_E256_installationPreservationDome" ):
		return (False, "Preservation Dome", 								COMMON_CARD,	256)
	if ( mID == "exode_card_257_installationStorage" 				or mID == "exode_card_E257_installationStorage" ):
		return (False, "Storage Building", 									COMMON_CARD,	257)
	if ( mID == "exode_card_258_equipmentTomEssentialsHappyFood"	or mID == "exode_card_E258_equipmentTomEssentialsHappyFood" ):
		return (False, "Soup and Cook", 									EPIC_CARD,		258)
	if ( mID == "exode_card_259_equipmentTomEssentialsHappyAir"		or mID == "exode_card_E259_equipmentTomEssentialsHappyAir" ):
		return (False, "TOM Beauty Air", 									EPIC_CARD,		259)
	if ( mID == "exode_card_260_equipmentTomEssentialsSurvivor"		or mID == "exode_card_E260_equipmentTomEssentialsSurvivor" ):
		return (False, "TOM Survivor CO5", 									EPIC_CARD,		260)
	if ( mID == "exode_card_261_actionImmediateOrder"				or mID == "exode_card_E261_actionImmediateOrder" ):
		return (False, "Emergency Order!", 									COMMON_CARD,	261)
	
    # Beta
	if ( mID == "exode_card_501_origin_selfmadeSavior"				or mID == "exode_card_E501_origin_selfmadeSavior" ):
		return (False, "Self-Made Savior [Origin]", 						EPIC_CARD,		501)
	if ( mID == "exode_card_502_crew_versatileWorker"				or mID == "exode_card_E502_crew_versatileWorker" ):
		return (False, "Versatile Worker", 		            				COMMON_CARD,	502)
	if ( mID == "exode_card_503_crew_toughWorker"		    		or mID == "exode_card_E503_crew_toughWorker" ):
		return (False, "Tough Worker", 		                				RARE_CARD,		503)
	if ( mID == "exode_card_504_crew_maintenanceWorker"				or mID == "exode_card_E504_crew_maintenanceWorker" ):
		return (False, "Maintenance Worker", 		       					RARE_CARD,		504)
	if ( mID == "exode_card_505_officer_mobLeader"		    		or mID == "exode_card_E505_officer_mobLeader" ):
		return (False, "Mob Leader", 		                				RARE_CARD,		505)
	if ( mID == "exode_card_506_officer_motivatedCivilian"  		or mID == "exode_card_E506_officer_motivatedCivilian" ):
		return (False, "Motivated Civilian", 		        				RARE_CARD,		506)
	if ( mID == "exode_card_507_officer_retiredWarVeteran"  		or mID == "exode_card_E507_officer_retiredWarVeteran" ):
		return (False, "Retired War Veteran", 		        				RARE_CARD,		507)
	if ( mID == "exode_card_508_equipmentSet_foodSupplies"  		or mID == "exode_card_E508_equipmentSet_foodSupplies" ):
		return (False, "Food Supplies (x20)", 		        				RARE_CARD,		508)
	if ( mID == "exode_card_509_starship_daystarTaxiCorvette"  		or mID == "exode_card_E509_starship_daystarTaxiCorvette" ):
		return (False, "Daystar Taxi Corvetter", 		    				EPIC_CARD,		509)
	
	if ( mID == "exode_card_511_origin_religiousVisionary"			or mID == "exode_card_511_origin_religiousVisionary" ):
		return (False, "Religious Visionary [Origin]", 						EPIC_CARD,		511)
	if ( mID == "exode_card_512_crew_inquisitorInitiate"			or mID == "exode_card_512_crew_inquisitorInitiate" ):
		return (False, "Inquisition Initiate", 		        				RARE_CARD, 		512)
	if ( mID == "exode_card_513_crew_religiousClerk"				or mID == "exode_card_513_crew_religiousClerk" ):
		return (False, "Religious Clerk", 		            				COMMON_CARD, 	513)
	if ( mID == "exode_card_514_crew_cultStationSecurity"			or mID == "exode_card_514_crew_cultStationSecurity" ):
		return (False, "Cult Station Security", 		    				RARE_CARD,		514)
	if ( mID == "exode_card_515_crew_cultTechie"		    		or mID == "exode_card_515_crew_cultTechie" ):
		return (False, "Cult Techie", 		                				RARE_CARD,		515)
	if ( mID == "exode_card_516_officer_cultSecurityOfficer" 		or mID == "exode_card_516_officer_cultSecurityOfficer" ):
		return (False, "Cult Security Officer", 		    				RARE_CARD,		516)
	if ( mID == "exode_card_517_passenger_cultFollowers"    		or mID == "exode_card_517_passenger_cultFollowers" ):
		return (False, "Cult Followers", 		            				RARE_CARD,		517)
	if ( mID == "exode_card_518_officer_exiledCultOfficer"  		or mID == "exode_card_518_officer_exiledCultOfficer" ):
		return (False, "Exiled Cult Officer", 		        				RARE_CARD,		518)
	if ( mID == "exode_card_519_starship_fulgurusCruxFrigate"  		or mID == "exode_card_519_starship_fulgurusCruxFrigate" ):
		return (False, "Fulgurus Crux Frigate", 		    				EPIC_CARD,		519)
	
	if ( mID == "exode_card_521_origin_utopianThinker"				or mID == "exode_card_E521_origin_utopianThinker" ):
		return (False, "Utopian Thinker [Origin]", 		    				EPIC_CARD,		521)
	if ( mID == "exode_card_522_crew_colonialSecurity"				or mID == "exode_card_E522_crew_colonialSecurity" ):
		return (False, "Colonial Security", 		        				COMMON_CARD,	522)
	if ( mID == "exode_card_523_crew_labTrainee"		    		or mID == "exode_card_E523_crew_labTrainee" ):
		return (False, "Lab Trainee", 		                				RARE_CARD,		523)
	if ( mID == "exode_card_524_crew_techTrainee"		    		or mID == "exode_card_E524_crew_techTrainee" ):
		return (False, "Tech Trainee", 		                				RARE_CARD,		524)
	if ( mID == "exode_card_525_crew_utopianPilot"		    		or mID == "exode_card_E525_crew_utopianPilot" ):
		return (False, "Test Pilot", 		                				RARE_CARD,		525)
	if ( mID == "exode_card_526_officer_groomedLeader"      		or mID == "exode_card_E526_officer_groomedLeader" ):
		return (False, "Groomed Leader", 		            				RARE_CARD,		526)
	if ( mID == "exode_card_527_officer_mandatedPresident"  		or mID == "exode_card_E527_officer_mandatedPresident" ):
		return (False, "Mandated President", 		        				RARE_CARD,		527)
	if ( mID == "exode_card_528_officer_astrophysicist"     		or mID == "exode_card_E528_officer_astrophysicist" ):
		return (False, "Astrophysicist",									RARE_CARD,		528)
	if ( mID == "exode_card_529_starship_syrvenExploratorAA3" 	 	or mID == "exode_card_E529_starship_syrvenExploratorAA3" ):
		return (False, "Syrven Explorator AA-3",							EPIC_CARD,		529)
	
	if ( mID == "exode_card_531_origin_rebelAgent"  				or mID == "exode_card_E531_origin_rebelAgent" ):
		return (False, "Rebel Agent [Origin]",								EPIC_CARD,		531)
	if ( mID == "exode_card_532_crew_rebelDaringSpyTrainee"  		or mID == "exode_card_E532_crew_rebelDaringSpyTrainee" ):
		return (False, "Daring Spy Trainee",								RARE_CARD,		532)
	if ( mID == "exode_card_533_crew_rebelYoungRecruit"  			or mID == "exode_card_E533_crew_rebelYoungRecruit" ):
		return (False, "Rebel Young Recruit",								RARE_CARD,		533)
	if ( mID == "exode_card_534_crew_rebelFighter" 					or mID == "exode_card_E534_crew_rebelFighter" ):
		return (False, "Rebel Fighter",										RARE_CARD,		534)
	if ( mID == "exode_card_535_officer_rebelGroundOperative"  		or mID == "exode_card_E535_officer_rebelGroundOperative" ):
		return (False, "Ground Operative",									RARE_CARD,		535)
	if ( mID == "exode_card_536_officer_rebelCommsOfficer"  		or mID == "exode_card_E536_officer_rebelCommsOfficer" ):
		return (False, "Rebel Comms Officer",								RARE_CARD,		536)
	if ( mID == "exode_card_537_officer_rebelOperationPlanner"		or mID == "exode_card_E537_officer_rebelOperationPlanner" ):
		return (False, "Rebel Operation Planner",							RARE_CARD,		537)
	if ( mID == "exode_card_538_equipmentSet_intelligenceEquipment"	or mID == "exode_card_E538_equipmentSet_intelligenceEquipment" ):
		return (False, "Intelligent Equipment (x5)",						RARE_CARD,		538)
	if ( mID == "exode_card_539_starship_narazuStealthCorvette"  	or mID == "exode_card_E539_starship_narazuStealthCorvette" ):
		return (False, "Narazu Stealth Corvette",							EPIC_CARD,		539)

	print(mID)
	is_pack = mID[:len("exode_card")] != "exode_card"
	return ( is_pack, mID, -1, 0)

def ex_GetAssetID( mID: str, mElite: bool = False ):
	
	if mID[:10] in ["exode_card", "exode_alph", "exode_beta"]:
		return mID.split(" ")[0]
	
	if ( not mElite ):
	
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
		
		if ( mID == "exode_pack_currency_200"	or mID == "4400 credits pack" ):
			return "exode_pack_currency_200"
		
		if ( mID == "exode_pack_currency_1000"	or mID == "22.5k credits pack" ):
			return "exode_pack_currency_1000"
			
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
			
			
		if ( mID == "exode_card_039_Tom_BeautyCapsule" 		or mID == "39" ):
			return "exode_card_039_Tom_BeautyCapsule"
		if ( mID == "exode_card_045_Rekatron_fireworks" 		or mID == "45" ):
			return "exode_card_045_Rekatron_fireworks"
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
		if ( mID == "exode_card_065_SyndicateGeisha_ThirdSister" 	or mID == "65" ):
			return "exode_card_065_SyndicateGeisha_ThirdSister"
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
		