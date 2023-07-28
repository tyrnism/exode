
import cst_exode, lib_exode, lib_database
from lib_mysql import lib_mysql
import json, os, time

from beem import exceptions as bexceptions
from beem import Hive
from beem.nodelist import NodeList
from beem.block import Block, Blocks
from beem.blockchain import Blockchain
from beem.account import Account

from nextcord.ext import commands

class lib_monitoring:
	def __init__(self, client: commands.Bot ) -> None:
		######################################################################################
		# Initialise
		self.client			  = client
		self.fFast            = True
		self.fDoDiscord       = cst_exode.DO_DISCORD
			
		# Variables
		self.fFirstBlock       = 0
		self.fIterator         = 0
		self.fStart            = True
			
		#
		self.fLoadExodeGame    = False
		self.fLoadPlayerMarket = False
		self.fLoadMintOnly     = False
			
		self.fReBuildDataBase  = False
		self.fRebuildSaleDatabase = False

		self.MINT_NUM = {}
		self.MINT_NUM_NOSOURCE = {}

		self.fCancelTransactionList   = []
			
		# Discord Channels
		self.DISC_CHANNELS_MARKET = []
		self.DISC_CHANNELS_PING   = []
		self.DISC_CHANNELS_MINT   = []
		self.DISC_CHANNELS_GIFT   = []

		# Hive
		self.Hive = None
		
		if ( os.path.isfile('database_rebuild.flag') ):
			print("Flag to rebuild database is active")
			self.fReBuildDataBase = True

		if ( os.path.isfile('database_sale_rebuild.flag') ):
			print("Flag to rebuild sale database is active")
			self.fRebuildSaleDatabase = True

		######################################################################################

	def LoadHiveBlockChain(self):
		print ("HIVE: Loading blockchain")
		nodelist = NodeList()
		nodelist.update_nodes()
		nodes = nodelist.get_hive_nodes()
		bHive = Hive(node=nodes)
		print ( nodes )
		print("Hive loaded?",bHive.is_hive)
		self.Hive = bHive

	def CheckByPass(self, mBlock ):	
		if ( not self.fReBuildDataBase or mBlock > self.fFirstBlock ):
			return False
		return True
	
	def GetCardMintId(self, card_owner: str, card_id: str, card_uid: str) -> int:
		if ( card_owner == "elindos" or card_owner == "exolindos" or card_uid == "none" ):
			return -1
		
		try:
			self.MINT_NUM[ card_id ] += 1
		except:
			self.MINT_NUM[ card_id ] = 1

		return self.MINT_NUM[ card_id ]
			
	def MakeMessage_List(self, sale_seller, asset_id, asset_nb, asset_uid, asset_mint, asset_elite, sale_price, mysql: lib_mysql):
			
		msg = ""
					
		(is_pack, asset_name, asset_rank, asset_num) = lib_exode.ex_GetAssetDetails(asset_id)
			
		if ( self.fLoadPlayerMarket ):
			mSoldPrice = 0.0
			mLastPrice = 0.0
		else:
			mSoldPrice = lib_database.db_Sale_GetAverageSoldPrice(mID=asset_id, mysql=mysql)
			mLastPrice = lib_database.db_Sale_GetLastSoldPrice(mID=asset_id, mysql=mysql)
					
		if ( is_pack ):
			
			msg = ":blue_square: {seller} listed {nb} **{name}** on the market for **${price}** (average sold price: **${sold_price:.2f}**, last sold price: **${last_price:.2f}**)".format(seller=sale_seller, 
					nb=asset_nb, name=asset_name, price=sale_price,sold_price=mSoldPrice,last_price=mLastPrice)
		else:
			try:
				card_ntot_mint = self.MINT_NUM[ asset_id ]	
			except:
				self.MINT_NUM[ asset_id ] = 0		
				card_ntot_mint = -1	
			try:
				card_ntot_mint_no_source = self.MINT_NUM_NOSOURCE[ asset_id ]	
			except:
				self.MINT_NUM_NOSOURCE[ asset_id ] = 0	
				card_ntot_mint_no_source = 0

			card_elite_msg = ""
			if ( asset_elite == 1 ):
				card_elite_msg = "<:exoelite:716334248524775485> Elite "
						
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
			if ( card_ntot_mint_no_source > 0 ):
				msg_missing_mint = f"(+{card_ntot_mint_no_source})"

			print ( "mint", asset_mint, "uid", asset_uid)		
								
			if ( asset_nb == 1 ):
				msg = ":blue_square: {seller} listed 1 **{elite}{name}** [*{rarity}*]  (**{mint}**/{ntot_mint}{missing_mint} *uid={muid})* for **${price}** (avg sold price: **${sold_price:.2f}**, last sold price: **${last_price:.2f}**)".format(seller=sale_seller, 
						name=asset_name, rarity=msg_rarity, mint=asset_mint, missing_mint=msg_missing_mint, elite=card_elite_msg, ntot_mint=card_ntot_mint, muid=asset_uid, price=sale_price,sold_price=mSoldPrice,last_price=mLastPrice)
			else:						
				msg = ":blue_square: {seller} listed {nb} **{elite}{name}** [*{rarity}*] for **${price}** (min. mint is **{mint}**/{ntot_mint}{missing_mint} *uid={muid}*) (avg sold price: **${sold_price:.2f}**, last sold price: **${last_price:.2f}**)".format(seller=sale_seller,
						nb=asset_nb, elite=card_elite_msg, missing_mint=msg_missing_mint, name=asset_name, rarity=msg_rarity, mint=asset_mint, ntot_mint=card_ntot_mint, muid=asset_uid,
						price=sale_price,sold_price=mSoldPrice,last_price=mLastPrice)
		return msg


	def ProcessTransfer( self, tx_auth, tx_type, tx_block, tx_time, tx_id, player_from, player_to, card_id, card_uid, price, mysql: lib_mysql ):
	
		if ( card_id == "" ):
			cInfo = lib_database.db_Card_GetDetails( card_uid=card_uid, mysql=mysql )
			card_id = cInfo['id']
			if ( card_id != "" ):
				print ("Fixing card_id to", card_id )
				card_id_fix = "?" + card_id
				lib_database.db_TransferTX_FixID( card_uid=card_uid, card_id=card_id_fix, mysql=mysql )
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
				self.db_Card_Apply_Burn( card_burner=player_from, card_id=card_id, card_uid=card_uid, card_block=tx_block, tx_id=tx_id, bypass=True, mysql=mysql )	
		
			elif ( tx_type == "exode_transfer" ):
				
				# Cancel sale if any
				self.db_Sale_Apply_Cancel( sale_seller=player_from, asset_id=card_id, asset_uid=card_uid, sale_block=tx_block, sale_time=tx_time, sale_tx=tx_id, transfert_cancel=True, mysql=mysql )
						
				is_pack = lib_exode.ex_IsPack(card_id)
				if ( is_pack ):
					lib_database.db_Pack_Apply_Transfer( pack_prev_owner=player_from, pack_new_owner=player_to, pack_id=card_id, pack_nb=1, mysql=mysql )
				else:
					msg = self.db_Card_Apply_Transfer( card_prev_owner=player_from, card_new_owner=player_to, card_id=card_id, card_uid=card_uid, card_block=tx_block, tx_id=tx_id, bypass=True, mysql=mysql )
		
			elif ( tx_type == "exode_market_purchase" ):
				self.db_Sale_Apply_Sold( sale_seller=player_from, asset_id=card_id, asset_uid=card_uid, sale_block=tx_block, sale_time=tx_time, sale_tx=tx_id, sale_sold=1, sale_buyer=player_to, mysql=mysql )
				
				is_pack = lib_exode.ex_IsPack(card_id)
				
				if ( is_pack ):
					lib_database.db_Pack_Apply_Transfer( pack_prev_owner=player_from, pack_new_owner=player_to, pack_id=card_id, pack_nb=1, mysql=mysql )							
				else:
					msg = self.db_Card_Apply_Transfer( card_prev_owner=player_from, card_new_owner=player_to, card_id=card_id, card_uid=card_uid, card_block=tx_block, tx_id=tx_id, bypass=True, mysql=mysql )
		
		else:
			# Players
			if ( tx_type == "exode_market_sell" ):
				self.db_Sale_Apply_New( sale_seller=player_from, asset_id=card_id, asset_uid=card_uid, sale_block=tx_block, sale_time=tx_time, sale_tx=tx_id, sale_price=price, sale_sold=0, sale_buyer="", mysql=mysql )
			
			elif ( tx_type == "exode_market_cancel_sell" ):
				self.db_Sale_Apply_Cancel( sale_seller=player_from, asset_id=card_id, asset_uid=card_uid, sale_block=tx_block, sale_time=tx_time, sale_tx=tx_id, mysql=mysql )
			elif ( tx_type == "confirm_transfer_packs" ):
				lib_database.db_Pack_Apply_Transfer( pack_prev_owner=player_from, pack_new_owner=player_to, pack_id=card_id, pack_nb=int(price), mysql=mysql )	
			elif ( tx_type == "confirm_transfer_account" ):
				lib_database.db_Pack_Apply_TransferAll( pack_prev_owner=player_from, pack_new_owner=player_to, mysql=mysql )
				lib_database.db_Card_Apply_TransferAll( card_prev_owner=player_from, card_owner=player_to, card_block=tx_block, mysql=mysql )
				
	def CheckJSON_Transfer( self, tVId, tVJSON, tBlock, tVAuth, mysql: lib_mysql):
		
		tMSGOut = []
	
		if ( tVId == "exode_extinguish_flames" ):
			
			#print("[DEBUG] New gift card: ", tVJSON)
			tInst   = tVJSON[1]
			mTxId   = tInst['tx_id']
			mPlayer = tInst['recipient']
				
			if ( not self.CheckTransaction(mBlock=tBlock, mType=tVId, mTxId=mTxId, mUId="", mPlayer=mPlayer, mFrom=tVAuth, mAuth=tVAuth, mTransaction=tInst, mysql=mysql) ):
				return [ cst_exode.NO_ALERT, tMSGOut ]
					
			#print( 'giftcard', mTxId, tInst['recipient'], tInst['sourceid'], tInst['receivedcardnb'] ) 
					
			l_owner   = tInst['recipient']
			l_card_id = tInst['sourceid']
			l_card_nb = int(tInst['receivedcardnb'])
			
			for iCard in range( l_card_nb ):
				lib_database.db_TransferTX_Add( tx_auth=tVAuth, tx_type=tVId, tx_block=tBlock, tx_id=mTxId, player_from=tVAuth, player_to=l_owner, card_id=l_card_id, card_uid="none", price=0.0, mysql=mysql )
			
			if ( not self.fLoadMintOnly ):			
				for iCard in range( l_card_nb ):
					card_mint = self.GetCardMintId(card_owner=l_owner, card_id=l_card_id, card_uid="none")
					lOut = lib_database.db_Card_Apply_Mint( card_owner=l_owner, card_id=l_card_id, card_uid="none", card_mint=card_mint, card_elite=0, card_bound=0, card_block=tBlock, tx_id=mTxId, bypass=self.CheckByPass( tBlock ), mysql=mysql )					
					if ( lOut != "" and tBlock >= cst_exode.NO_MINT_ALERT_BELOW_BLOCK):
						tMSGOut.append(lOut)
							
			return [ cst_exode.ALERT_MINT, tMSGOut ]	
					
		elif ( tVId == "exode_upgrade_confirmed" ):		
			#Burn card	
			#print("[DEBUG] New burn (upgrade): ", tVJSON)
							
			tInst   = tVJSON[1]
			mTxId   = tInst['tx_id']
			mPlayer = tInst['recipient']
				
			if ( not self.CheckTransaction( mBlock=tBlock, mType=tVId, mTxId=mTxId, mUId="", mPlayer=mPlayer, mFrom=tVAuth, mAuth=tVAuth, mTransaction=tInst, mysql=mysql) ):
				return [ cst_exode.NO_ALERT, tMSGOut ]
				
			l_card_owner     = tInst['recipient']
			l_card_id        = tInst['globalid']
			l_card_uid       = tInst['cardid']
				
			if ( "burnedid" in tInst ):
				l_card_burn_uids = tInst['burnedid'].split(',')
			else:
				l_card_burn_uids = tInst['burnedids'].split(',')	
								
			#print( 'burn', mTxId, l_card_owner, l_card_uid, l_card_id,  l_card_burn_uids )					
			
			for iCard in range( len(l_card_burn_uids) ):
				lib_database.db_TransferTX_Add( tx_auth=tVAuth, tx_type=tVId, tx_block=tBlock, tx_id=mTxId, player_from=l_card_owner, player_to="burn", card_id=l_card_id, card_uid=l_card_burn_uids[iCard], price=0.0, mysql=mysql )
				
			if ( not self.fLoadMintOnly ):
				for iCard in range( len(l_card_burn_uids) ):
					lOut = self.db_Card_Apply_Burn( card_burner=l_card_owner, card_id=l_card_id, card_uid=l_card_burn_uids[iCard], card_block=tBlock, tx_id=mTxId, bypass=self.CheckByPass( tBlock ), mysql=mysql )					
					if ( lOut != "" ):
						tMSGOut.append(lOut)	
						
			return [ cst_exode.ALERT_MINT, tMSGOut ]
				
		else:	
			with open('logs/log_unknown.log', 'a') as f:
				f.write("Type: {del_type}, Block: {block}, transaction: {del_txt}\n".format(del_type=tVId,block=tBlock,del_txt=tVJSON) )
				
		return [ cst_exode.NO_ALERT, tMSGOut ]
	
	def CheckJSON_Player( self, tVId, tValue, tBlock, tVAuth, mysql: lib_mysql ):
				
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
				return [ cst_exode.NO_ALERT, tMSGOut ]			
							
			if ( not self.CheckTransaction(mBlock=tBlock, mType=tVId, mTxId=l_sale_txid, mUId="", mPlayer=tVAuth, mFrom=tVAuth, mAuth=tVAuth, mTransaction=tInst, mCancel=True, mysql=mysql) ):
				return [ cst_exode.NO_ALERT, tMSGOut ]			
			
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
				
					cInfo = lib_database.db_Card_GetDetails( card_uid=l_asset_uids[iAsset], mysql=mysql )
					# Fix card_id if possible
					if ( cInfo['id'] == "" and l_asset_id != "" ):
						cInfo['id'] = l_asset_id
						cInfo['elite'] = lib_exode.ex_IsElite(l_asset_id)
					
					l_asset_ids.append(cInfo['id'])
					l_asset_elite.append(cInfo['elite'])
					l_asset_mint.append(cInfo['mint'])
					
			print( 'sell', l_sale_txid, l_asset_seller, l_asset_ids, l_asset_uids, l_sale_price, tMarketType_Pack )	
			
			bOK = False
			for iAsset in range(len(l_asset_uids)):
				lib_database.db_TransferTX_Add( tx_auth=tVAuth, tx_type=tVId, tx_block=tBlock, tx_id=l_sale_txid, player_from=l_asset_seller, player_to="market", card_id=l_asset_ids[iAsset], card_uid=l_asset_uids[iAsset], price=l_sale_price, mysql=mysql )
			if ( not self.fLoadMintOnly ):
				tTime = Block(tBlock).time()
				for iAsset in range(len(l_asset_uids)):
					bOK = self.db_Sale_Apply_New( sale_seller=l_asset_seller, asset_id=l_asset_ids[iAsset], asset_uid=l_asset_uids[iAsset], sale_block=tBlock, sale_time=tTime, sale_tx=l_sale_txid, sale_price=l_sale_price, sale_sold=0, sale_buyer="", mysql=mysql )

			if ( not bOK ):
				return [ cst_exode.NO_ALERT, tMSGOut ]
			
			(is_pack, asset_name, asset_rank, asset_num) = lib_exode.ex_GetAssetDetails(l_asset_ids[0]) 
			

			if ( is_pack ):
										
				pack_name = asset_name
				if ( tIDUnknown ):
					pack_name = pack_name + " (?)"
				
				lOut = self.MakeMessage_List(sale_seller=l_asset_seller, asset_id=l_asset_ids[0], asset_nb=len(l_asset_uids), asset_uid="", asset_mint=-1, asset_elite=0, sale_price=l_sale_price, mysql=mysql)
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
						
						lOut = self.MakeMessage_List(sale_seller=l_asset_seller, asset_id=prev_id, asset_nb=card_nb, asset_uid=card_uid_low, asset_mint=card_mint_low, asset_elite=card_elite, sale_price=l_sale_price, mysql=mysql)
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
					lOut = self.MakeMessage_List(sale_seller=l_asset_seller, asset_id=prev_id, asset_nb=card_nb, asset_uid=card_uid_low, asset_mint=card_mint_low, asset_elite=card_elite, sale_price=l_sale_price, mysql=mysql)
					tMSGOut.append(lOut)
			
			return [ cst_exode.ALERT_MARKET, tMSGOut ]
							
						
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
				return [ cst_exode.ALERT_KILL, tMSGOut ]	
				
			if ( not self.CheckTransaction(mBlock=tBlock, mType=tVId, mTxId=l_sale_txid, mUId=l_asset_uid, mPlayer=tVAuth, mFrom=tVAuth, mAuth=tVAuth, mTransaction=tInst, mCancel=True, mysql=mysql) ):
				return [ cst_exode.NO_ALERT, tMSGOut ]	
				
			print( 'cancelsell', l_sale_txid, l_asset_seller, l_asset_id, l_asset_uid )
			
			bOK = False
			lib_database.db_TransferTX_Add( tx_auth=tVAuth, tx_type=tVId, tx_block=tBlock, tx_id=l_sale_txid, player_from=l_asset_seller, player_to=l_asset_seller, card_id=l_asset_id, card_uid=l_asset_uid, price=0.0, mysql=mysql )
			
			if ( not self.fLoadMintOnly ):	
				tTime = Block(tBlock).time()
				bOK = self.db_Sale_Apply_Cancel( sale_seller=l_asset_seller, asset_id=l_asset_id, asset_uid=l_asset_uid, sale_block=tBlock, sale_time=tTime, sale_tx=l_sale_txid, mysql=mysql )
				
			if ( not bOK ):
				return [ cst_exode.NO_ALERT, tMSGOut ]
				
			(is_pack, asset_name, asset_rank, asset_num) = lib_exode.ex_GetAssetDetails(l_asset_id) 

			if ( is_pack ):
						
				pack_name                               = asset_name
				
				lOut = ":purple_square: {seller} delisted {nb} **{name}** from the market".format(seller=l_asset_seller, nb=1, name=pack_name)
				tMSGOut.append(lOut)
							
			else:
						
				card_name = asset_name
				card_muid = l_asset_uid
				cInfo = lib_database.db_Card_GetDetails( card_uid=card_muid, mysql=mysql )
				
				card_elite     = cInfo['elite']
				card_mint      = cInfo['mint']	
				try:
					card_ntot_mint = self.MINT_NUM[ l_asset_id ]
				except:
					self.MINT_NUM[ l_asset_id ] = 0
					card_ntot_mint = 0
										
				try:
					card_ntot_mint_no_source = self.MINT_NUM_NOSOURCE[l_asset_id]
				except:
					self.MINT_NUM_NOSOURCE[ l_asset_id ] = 0
					card_ntot_mint_no_source = 0

				msg_missing_mint = ""
				if ( card_ntot_mint_no_source > 0 ):
					msg_missing_mint = f"(+{card_ntot_mint_no_source})"
																						
				card_elite_msg = ""
				if ( card_elite == 1 ):
					card_elite_msg = "<:exoelite:716334248524775485> Elite "
					
				msg_rarity = "Common"
				if ( asset_rank == 1 ):
					msg_rarity = "Rare"
				elif ( asset_rank == 2 ):
					msg_rarity = "Epic"
				elif ( asset_rank == 3 ):
					msg_rarity = "Legendary"
				elif ( asset_rank == -1 ):
					msg_rarity = "???"
				
				lOut = ":purple_square: {seller} delisted 1 **{elite}{name}** [*{rarity}*] (**{mint}**/{ntot_mint}{missing_mint} *uid={muid}*)".format(seller=l_asset_seller, 
								name=card_name, rarity=msg_rarity, mint=card_mint, missing_mint=msg_missing_mint, elite=card_elite_msg, ntot_mint=card_ntot_mint, 
								muid=card_muid)
				tMSGOut.append(lOut)
						
			return [ cst_exode.ALERT_MARKET, tMSGOut ]
						
							
		elif ( tVId == "exode_market_transfer" ):
			# Ownership is set by exodegame, ignore
			return [ cst_exode.NO_ALERT, tMSGOut ]
			
		return [ cst_exode.NO_ALERT, tMSGOut ]		
	
	
	def CheckTransaction( self, mBlock, mType, mTxId, mUId, mPlayer, mFrom, mAuth, mTransaction, mysql: lib_mysql, mCancel=False ):
		if ( mTxId == "" ):
			mTxId = "{player}.{block}".format(player=mPlayer,block=mBlock)

		tInfo = lib_database.db_TX_GetDetails(tx_id=mTxId, tx_uid=mUId, tx_type=mType, tx_target=mPlayer, mysql=mysql)
		if ( tInfo['exist'] ):					
			if ( not self.CheckByPass( mBlock ) ):
				with open('logs/transaction_duplicate.json', 'a') as f:
					err_msg = { "transaction": { "type": mType, "block": mBlock, "tx_id": mTxId }, "issue": "duplicate_transaction", 
						"transaction_details": mTransaction }
					json.dump( err_msg, f ) 
					f.write("\n")
			return False
				
		lib_database.db_TX_Add( tx_id=mTxId, tx_uid=mUId, tx_type=mType, tx_block=mBlock, tx_player=mPlayer, tx_from=mFrom, tx_auth=mAuth, mysql=mysql )
		
		if ( mTxId in self.fCancelTransactionList and not mCancel ):
			print("[WARNING] Cancelled transaction ", mType, mTxId)
			self.fCancelTransactionList.remove(mTxId)
			lib_database.db_TX_Cancel( tx_id=mTxId, tx_uid=mUId, tx_type=mType, tx_target=mPlayer, mysql=mysql )
		
			with open('logs/transaction_cancelled.json', 'a') as f:
				err_msg = { "transaction": { "type": mType, "block": mBlock, "tx_id": mTxId }, "issue": "transaction_cancelled", 
					"transaction_details": mTransaction }
				json.dump( err_msg, f ) 
				f.write("\n")
			return False	
					
		return True
		
	def ReadJSONTransaction(self, tValue, tBlock, mysql: lib_mysql):
		
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
				
				if ( not self.CheckTransaction(mBlock=tBlock, mType=tVId, mTxId=mTxId, mUId="", mPlayer=mPlayer, mFrom=tVAuth, mAuth=tVAuth, mTransaction=tInst, mysql=mysql) ):
					return [ cst_exode.NO_ALERT, tMSGOut ]
												
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
				elif (	   l_source_id == "exode_beta_starter_3"
					or l_source_id == "exode_beta_starter_2"
					or l_source_id == "exode_beta_starter_1" ):
					iPack_nb = len(l_card_ids)/9					
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
					return [ cst_exode.ALERT_KILL, tMSGOut ]
					
				if ( iPack_nb > 0 ):
					lib_database.db_Pack_Apply_Update(pack_owner=l_owner, pack_id=l_source_id, pack_nb=-1*iPack_nb, pack_open=iPack_nb, mysql=mysql )
				
				for iPack in range( len(l_pack_ids) ):
					if ( l_pack_ids[iPack] == "" ):
						continue						
					lib_database.db_Pack_Apply_Update(pack_owner=l_owner, pack_id=l_pack_ids[iPack], pack_nb=1, pack_open=0, mysql=mysql )
					
				for iCard in range( len(l_card_ids) ):
					if ( l_card_ids[iCard] == "" ):
						continue
					card_mint = self.GetCardMintId(card_owner=l_owner, card_id=l_card_ids[iCard], card_uid=l_card_uids[iCard])
					lOut = lib_database.db_Card_Apply_Mint( card_owner=l_owner, card_id=l_card_ids[iCard], card_uid=l_card_uids[iCard], card_mint=card_mint, card_elite=l_card_elite[iCard], card_bound=0, card_block=tBlock, tx_id=mTxId, bypass=self.CheckByPass( tBlock ), mysql=mysql )
					
					if ( lOut != "" and tBlock >= cst_exode.NO_MINT_ALERT_BELOW_BLOCK ):
						tMSGOut.append(lOut)
						
				return [ cst_exode.ALERT_MINT, tMSGOut ]
				#end = timer()				
				#print ( "New pack took ", (end-start) )										
			
			elif ( tVId == "exode_contract_dropready" ):
				# contract dropready
				# SKIP!
				return [ cst_exode.NO_ALERT, tMSGOut ]
				
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
				
				if ( not self.CheckTransaction(mBlock=tBlock, mType=tVId, mTxId=mTxId, mUId="", mPlayer=mPlayer, mFrom=tVAuth, mAuth=tVAuth, mTransaction=tInst, mysql=mysql) ):
					return [ cst_exode.NO_ALERT, tMSGOut ]
						
				#print( 'pack', mTxId, tInst['recipient'], tInst['typeids'].split(','), tInst['typenbs'].split(',') ) 
				
				l_player  = mPlayer
				l_pack_id = tInst['typeids'].split(',')
				l_pack_nb = tInst['typenbs'].split(',')
				
				for iPack in range( len(l_pack_id) ):
					if ( l_pack_id[iPack] == "" or l_pack_nb[iPack] == "" ):
						continue
							
					lib_database.db_Pack_Apply_Update(pack_owner=l_player, pack_id=l_pack_id[iPack], pack_nb=l_pack_nb[iPack], pack_open=0 )
					
			elif ( tVId == "exode_reward_medal" ):
				#exode_reward_medal ['exode_reward_medal', {'recipient': 'raudell', 'medal_title': 'Winner of the Ocean World (Planetary Challenge, July 2020)', 'medal_globalid': '', 'medal_nft': '', 'medal_picture': '', 'tx_id': '', 'app_tx': '3b45b4392dcf1957ead42082a0628552'}]
				return [ cst_exode.NO_ALERT, tMSGOut ]
				#TODO
			elif ( tVId == "exode_cancel_test_transaction" ):
				tInst   = tVJSON[1]
				mTxId   = tInst['tx_id']
				
				if ( not self.CheckTransaction(mBlock=tBlock, mType=tVId, mTxId=mTxId, mUId="", mPlayer=tVAuth, mFrom=tVAuth, mAuth=tVAuth, mTransaction=tInst, mCancel=True, mysql=mysql) ):
					return [ cst_exode.NO_ALERT, tMSGOut ]
								
				lib_database.db_Cancel_FillTX( tTxId=mTxId, tBlock=tValue['block'], mysql=mysql )	
				
			elif (	   tVId == "for_development_test" 	or tVId == "for_development"
				or tVId == "artist_payment" 		or tVId == "follow" 
				or tVId == "market_test_booster" 	or tVId == "exode_delivery" ):		
				# SKIP
				return [ cst_exode.NO_ALERT, tMSGOut ]
			else:
				#Deal with burn
				return self.CheckJSON_Transfer( tVId=tVId, tVJSON=tVJSON, tBlock=tBlock, tVAuth=tVAuth, mysql=mysql)
		else:
			return self.CheckJSON_Player( tVId=tVId, tValue=tValue, tBlock=tBlock, tVAuth=tVAuth, mysql=mysql )
				
		return [ cst_exode.NO_ALERT, tMSGOut ]

	######################################################################################

	def ReadTransfert(self, tValue, tBlock, mysql: lib_mysql):

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
					
					
					if ( not self.CheckTransaction(mBlock=tBlock, mType=tType, mTxId=mTxId, mUId=mUID, mPlayer=tTo, mFrom=mFrom, mAuth=tAuth, mTransaction=tMemo, mysql=mysql) ):
						return [ cst_exode.NO_ALERT, tMSGOut ]	
					
					lib_database.db_TransferTX_Add( tx_auth=tFrom, tx_type=tType, tx_block=tBlock, tx_id=mTxId, player_from=mFrom, player_to=tTo, card_id=mID, card_uid=mUID, price=0.0, mysql=mysql )
					
					if ( not self.fLoadMintOnly ):
						# Cancel sale if any			
						tTime = Block(tBlock).time()
						
						bOK = self.db_Sale_Apply_Cancel( sale_seller=mFrom, asset_id=mID, asset_uid=mUID, sale_block=tBlock, sale_time=tTime, sale_tx=mTxId, transfert_cancel=True, mysql=mysql )
						
						lOut = ""
						(is_pack, asset_name, asset_rank, asset_num) = lib_exode.ex_GetAssetDetails( mID )
						if ( is_pack ):
							print('pack-transfer', mTxId, mFrom, tTo, mID, mUID )
							lib_database.db_Pack_Apply_Transfer( pack_prev_owner=mFrom, pack_new_owner=tTo, pack_id=mID, pack_nb=1, mysql=mysql )
							
							if ( tTo == "exoderewardspool" ):
								lOut = ":gift: {giver} gave 1 **{name}** to the EXODE Reward Pool  (*@exoderewardspool*)! :tada:".format(giver=mFrom, name=asset_name)
						else:
							print('card-transfer', mTxId, mFrom, tTo, mID, mUID )						
							lOut = self.db_Card_Apply_Transfer( card_prev_owner=mFrom, card_new_owner=tTo, card_id=mID, card_uid=mUID, card_block=tBlock, tx_id=mTxId, bypass=self.CheckByPass( tBlock ), mysql=mysql )
							
						if ( lOut != "" ):
							tMSGOut.append(lOut)					
					return [ cst_exode.ALERT_GIFT, tMSGOut ]
					
				elif ( tType == "exode_market_purchase" ):
					
					mFrom = "market"
					mUID  = tMemo[4]
					mID   = tMemo[5]
					mTxId = tMemo[8]
					
					if ( not self.CheckTransaction(mBlock=tBlock, mType=tType, mTxId=mTxId, mUId=mUID, mPlayer=tTo, mFrom=mFrom, mAuth=tAuth, mTransaction=tMemo, mysql=mysql) ):
						return [ cst_exode.NO_ALERT, tMSGOut ]	
					
					lib_database.db_TransferTX_Add( tx_auth=tFrom, tx_type=tType, tx_block=tBlock, tx_id=mTxId, player_from=mFrom, player_to=tTo, card_id=mID, card_uid=mUID, price=0.0, mysql=mysql )
						
					if ( not self.fLoadMintOnly ):				
						tTime = Block(tBlock).time()
						(is_pack, asset_name, asset_rank, asset_num) = lib_exode.ex_GetAssetDetails(mID) 
					
						sInfo = self.db_Sale_Apply_Sold( sale_seller=mFrom, asset_id=mID, asset_uid=mUID, sale_block=tBlock, sale_time=tTime, sale_tx=mTxId, sale_sold=1, sale_buyer=tTo, mysql=mysql )

						bOK          = sInfo[0]
						asset_seller = sInfo[1]
						asset_price  = sInfo[2]
											
						if ( not bOK ):
							return [ cst_exode.NO_ALERT, tMSGOut ]	
							
		
						if ( self.fLoadExodeGame ):
							mSoldPrice = 0.0
						else:
							mSoldPrice = lib_database.db_Sale_GetAverageSoldPrice(mID=mID, mysql=mysql)
						
						if ( is_pack ):
							print('pack-buy', mTxId, mFrom, tTo, mID, mUID )
							
							pack_name = asset_name
							
							lib_database.db_Pack_Apply_Transfer( pack_prev_owner=asset_seller, pack_new_owner=tTo, pack_id=mID, pack_nb=1, mysql=mysql )
							
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
							
							cInfo = lib_database.db_Card_GetDetails( card_uid=mUID, mysql=mysql )
							
							card_elite     = cInfo['elite']
							card_mint      = cInfo['mint']					
							card_name      = asset_name
							try:
								card_ntot_mint = self.MINT_NUM[ mID ]
							except:
								card_ntot_mint = 0
								self.MINT_NUM[ mID ] = 0

							try:
								card_ntot_mint_no_source = self.MINT_NUM_NOSOURCE[ mID ]
							except:
								card_ntot_mint_no_source = 0
								self.MINT_NUM_NOSOURCE[ mID ] = 0
												
							self.db_Card_Apply_Transfer( card_prev_owner=asset_seller, card_new_owner=tTo, card_id=mID, card_uid=mUID, card_block=tBlock, tx_id=mTxId, bypass=self.CheckByPass( tBlock ), mysql=mysql )
													
							msg_missing_mint=""
							if ( card_ntot_mint_no_source > 0 ):
								msg_missing_mint = f"(+{card_ntot_mint_no_source})"
									
							card_elite_msg = ""
							if ( card_elite == 1 ):
								card_elite_msg = "<:exoelite:716334248524775485> Elite "
								
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
						
					
					return [ cst_exode.ALERT_MARKET, tMSGOut ]
					
				elif ( tType == "exode_delivery" or tType == "exode_delivery_update" ):	
				
					mTxId = ""
					
					if ( tMemo[2] == "NFT" ):
						mUID = tMemo[3]
					elif ( tMemo[3] == "NFT" ):
						mUID = tMemo[4]
					else: 
						mUID = ""						
					
					if ( not self.CheckTransaction(mBlock=tBlock, mType=tType, mTxId=mTxId, mUId=mUID, mPlayer=tTo, mFrom=tFrom, mAuth=tAuth, mTransaction=tMemo, mysql=mysql) ):
						return [ cst_exode.NO_ALERT, tMSGOut ]	

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
					
					if ( not self.CheckTransaction(mBlock=tBlock, mType=tType, mTxId=mTxId, mUId=mUID, mPlayer=tTo, mFrom=tFrom, mAuth=tAuth, mTransaction=tMemo, mysql=mysql) ):
						return [ cst_exode.NO_ALERT, tMSGOut ]	
						
					lib_database.db_Player_Add(mPlayer=tTo, mysql=mysql)
			
				elif ( tType == "exode_market_sale_manual" ):			
					#Add player to list, just in case
					mFrom = "market"
					mUID  = tMemo[2]
					mID   = tMemo[3]
					mTxId = tMemo[0]
					
					if ( not self.CheckTransaction(mBlock=tBlock, mType=tType, mTxId=mTxId, mUId=mUID, mPlayer=tTo, mFrom=tFrom, mAuth=tAuth, mTransaction=tMemo, mysql=mysql) ):
						return [ cst_exode.NO_ALERT, tMSGOut ]	
						
					lib_database.db_Player_Add(mPlayer=tTo, mysql=mysql)
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
			
				if ( not self.CheckTransaction(mBlock=tBlock, mType=tType, mTxId="", mUId="", mPlayer=mTo, mFrom=tFrom, mAuth=tAuth, mTransaction=tnMemo, mysql=mysql) ):
					return [ cst_exode.NO_ALERT, tMSGOut ]	
					
				pack_id = tnMemo[1].strip()
				pack_nb = int(tnMemo[2])
				
						
				print( 'mass-transfer-pack', 0, tFrom, mTo, pack_id, pack_nb )		
				
				lib_database.db_TransferTX_Add( tx_auth=tFrom, tx_type=tType, tx_block=tBlock, tx_id="", player_from=tFrom, player_to=mTo, card_id=pack_id, card_uid="", price=pack_nb, mysql=mysql )
				
				if ( not self.fLoadMintOnly ):
					lib_database.db_Pack_Apply_Transfer( pack_prev_owner=tFrom, pack_new_owner=mTo, pack_id=pack_id, pack_nb=pack_nb, mysql=mysql )
				
			elif ( tType == "confirm_transfer_account" ):
			
				mTo = tnMemo[1].strip()
				
				# fix
				if ( mTo == "birdbeak" ):
					mTo = "birdbeaksd"
					
				if ( not self.CheckTransaction(mBlock=tBlock, mType=tType, mTxId="", mUId="", mPlayer=mTo, mFrom=tFrom, mAuth=tAuth, mTransaction=tnMemo, mysql=mysql) ):
					return [ cst_exode.NO_ALERT, tMSGOut ]	
					
				print( 'mass-transfer-account', 0, tFrom, mTo )
				
				
				lib_database.db_TransferTX_Add( tx_auth=tFrom, tx_type=tType, tx_block=tBlock, tx_id="", player_from=tFrom, player_to=mTo, card_id="", card_uid="", price=0.0, mysql=mysql )
				
				if ( not self.fLoadMintOnly ):
					lib_database.db_Pack_Apply_TransferAll( pack_prev_owner=tFrom, pack_new_owner=mTo, mysql=mysql )
					lib_database.db_Card_Apply_TransferAll( card_prev_owner=tFrom, card_owner=mTo, card_block=tBlock, mysql=mysql )
			else:
				with open('logs/log_unknown_transfert.log', 'a') as f:
					f.write("From: {del_from}, To: {del_to}, Type: {del_type}, Block: {block}, memo: {del_txt}\n".format(del_from=tFrom, del_to=tTo,del_type="unknown",block=tBlock,del_txt=tValue['memo']) )
			

		return [ cst_exode.NO_ALERT, tMSGOut ]
	
	######################################################################################

	def db_Card_IsTransferable( self, card_from, card_to, card_id, card_uid, card_block, tx_id, transfer_action, mysql: lib_mysql, bypass=False ):

		cInfo = lib_database.db_Card_GetDetails( card_uid=card_uid, mysql=mysql )
		
		if ( not cInfo['exist'] ):
			with open('logs/card_error.json', 'a') as f:
				err_msg = { "card": { "id": card_id, "uid": card_uid }, "issue": "no_source", 
						"spotted": { "block": card_block, "tx_id": tx_id, "action": transfer_action, "issue_details": { "player": card_from, "target": card_to } } }
				json.dump( err_msg, f ) 
				f.write("\n")
				
			if ( cst_exode.MINT_IFNOSOURCE and card_id != "" and card_id != "none" ):
				(is_pack, card_name, card_rank, card_num) = lib_exode.ex_GetAssetDetails(card_id)
				card_elite = lib_exode.ex_IsElite(card_id)
				lib_database.db_Card_Mint( card_owner=card_from, card_id=card_id, card_num=card_num, card_uid=card_uid, card_mint=-1, card_elite=card_elite, card_bound=0, card_block=card_block, card_minter="no_source", mysql=mysql )	
				lib_database.db_Card_Add_Missing( card_owner=card_from, card_id=card_id, card_uid=card_uid, card_num=card_num, card_elite=card_elite, card_block=card_block, mysql=mysql )
				
				if ( card_from != "elindos" and card_from != "exolindos" ):
					try:
						self.MINT_NUM_NOSOURCE[card_id] += 1
					except:
						self.MINT_NUM_NOSOURCE[card_id] = 1
				
				return [ True, -1, True, card_block, card_elite ]
			else:
				lib_database.db_Card_Add_Missing( card_owner=card_from, card_id="", card_uid=card_uid, card_num=0, card_elite=0, card_block=card_block, mysql=mysql )
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
		
	def db_Card_Apply_Burn( self, card_burner, card_id, card_uid, card_block, tx_id, mysql: lib_mysql, bypass=False ):
		
		msg = ""	
		cInfo = self.db_Card_IsTransferable( card_from=card_burner, card_to="burn", card_id=card_id, card_uid=card_uid, card_block=card_block, tx_id=tx_id, transfer_action="burn", bypass=bypass, mysql=mysql )
		#if ( not cInfo[0] ):
		#	return msg
		if ( not cInfo[2] or int(card_block) < int(cInfo[3]) ):
			return msg
			
		lib_database.db_Card_Burn( card_uid=card_uid, card_block=card_block, card_burn=1, card_burner=card_burner, mysql=mysql )
		
		card_mint = cInfo[1]
		card_elite = cInfo[4]
		(is_pack, card_name, card_rank, card_num) = lib_exode.ex_GetAssetDetails(card_id)
		if ( (card_mint > 0 and card_mint <= 10) or (int(card_elite) == 1) or (card_rank >= 2) or (card_rank == -1) ):
			if ( card_elite == 1 ):
				msg_elite = "an **<:exoelite:716334248524775485> Elite "
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
		
	def db_Card_Apply_Transfer( self, card_prev_owner, card_new_owner, card_id, card_uid, card_block, tx_id, mysql: lib_mysql, bypass=False ):

		msg = ""
		
		if ( card_new_owner == 'null' ):
			msg = self.db_Card_Apply_Burn( card_burner=card_prev_owner, card_id=card_id, card_uid=card_uid, card_block=card_block, tx_id=tx_id, bypass=bypass, mysql=mysql )
			return msg
		else:
			cInfo = self.db_Card_IsTransferable( card_from=card_prev_owner, card_to=card_new_owner, card_id=card_id, card_uid=card_uid, card_block=card_block, tx_id=tx_id, transfer_action="transfer", bypass=bypass, mysql=mysql )
			#if ( not cInfo[0] ):
			#	return False
			if ( not cInfo[2] or int(card_block) < int(cInfo[3]) ):
				return msg
						
			lib_database.db_Card_Transfer( card_uid=card_uid, card_block=card_block, card_owner=card_new_owner, mysql=mysql )
			
			card_mint = cInfo[1]
			card_elite = cInfo[4]
			(is_pack, card_name, card_rank, card_num) = lib_exode.ex_GetAssetDetails(card_id)
			if ( card_new_owner == "exoderewardspool" ):
				if ( card_elite == 1 ):
					msg_elite = "an **<:exoelite:716334248524775485> Elite "
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
		
	def db_Sale_Apply_Sold( self, sale_seller, asset_id, asset_uid, sale_block, sale_time, sale_tx, sale_sold, sale_buyer, mysql: lib_mysql ):

		# Check asset, created it if needed
		is_pack = lib_exode.ex_IsPack( asset_id )
		if ( not is_pack ):
			cInfo = self.db_Card_IsTransferable( card_from=sale_seller, card_to=sale_buyer, card_id=asset_id, card_uid=asset_uid, card_block=sale_block, tx_id=sale_tx, transfer_action="sale-sold", mysql=mysql )
		
		sInfo = lib_database.db_Sale_GetDetails( asset_uid=asset_uid, sale_sold=0, sale_block=sale_block, mysql=mysql )
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
			lib_database.db_Sale_Sold( asset_uid=asset_uid, asset_id=asset_id, sale_tx=sale_tx, sale_sold=1, sale_buyer=sale_buyer, sale_block=sale_block, sale_time=sale_time, mysql=mysql)
			
		return [ True, sInfo['seller'], sInfo['price'] ]
			
	def db_Sale_Apply_New( self, sale_seller, asset_id, asset_uid, sale_block, sale_time, sale_tx, sale_price, sale_sold, sale_buyer, mysql: lib_mysql ):

		# Check asset
		(is_pack, asset_name, asset_rank, asset_num) = lib_exode.ex_GetAssetDetails(asset_id)
		if ( not is_pack ):
			cInfo = self.db_Card_IsTransferable( card_from=sale_seller, card_to="market", card_id=asset_id, card_uid=asset_uid, card_block=sale_block, tx_id=sale_tx, transfer_action="sale", mysql=mysql )
			if ( not cInfo[0] ):
				return False
			
		sInfo = lib_database.db_Sale_GetDetails( asset_uid=asset_uid, sale_sold=0, sale_block=sale_block, mysql=mysql )		
		if ( sInfo['exist'] and sInfo['cancel'] == 0 ):
		
			if ( sale_seller != sInfo['seller'] ):
				with open('logs/sale_error.json', 'a') as f:
					err_msg = { "sale": { "seller": sale_seller, "buyer": sale_buyer, "sold": sale_sold, "card": { "id": asset_id, "uid": asset_uid } }, "issue": "duplicate_sale", "spotted": {"action": "create_sale", "block": sale_block, "tx_id": sale_tx}, "current_seller": sInfo['seller'] } 
					json.dump( err_msg, f ) 
					f.write("\n")
				return False
			elif( sale_seller != "market" ):
				lib_database.db_Sale_Cancel( asset_uid=asset_uid, sale_seller=sale_seller, sale_block=sale_block, sale_time=sale_time, mysql=mysql )
		
		lib_database.db_Sale_Add( sale_seller=sale_seller, asset_id=asset_id, asset_uid=asset_uid, sale_tx=sale_tx, sale_price=sale_price, sale_sold=sale_sold, sale_buyer=sale_buyer, sale_block=sale_block, sale_time=sale_time, mysql=mysql )
			
		return True
		
	def db_Sale_Apply_Cancel( self, sale_seller, asset_id, asset_uid, sale_block, sale_time, sale_tx, mysql: lib_mysql, transfert_cancel=False ):

		# Check asset
		(is_pack, asset_name, asset_rank, asset_num) = lib_exode.ex_GetAssetDetails(asset_id)
		if ( not is_pack and not transfert_cancel ):
			cInfo = self.db_Card_IsTransferable( card_from=sale_seller, card_to="market", card_id=asset_id, card_uid=asset_uid, card_block=sale_block, tx_id=sale_tx, transfer_action="sale-cancel", mysql=mysql )
			if ( not cInfo[0] ):
				return False
			
		sInfo = lib_database.db_Sale_GetDetails( asset_uid=asset_uid, sale_sold=0, sale_block=sale_block, mysql=mysql )
		
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
			lib_database.db_Sale_Cancel( asset_uid=asset_uid, sale_seller=sale_seller, sale_block=sale_block, sale_time=sale_time, mysql=mysql )
			
		return True
		
	######################################################################################
		
	async def ProcessTransaction(self, tType, tBlock, hTransaction, mysql: lib_mysql ):
	
		lOut = [ cst_exode.NO_ALERT, [] ]
		
		if ( tType == "transfer" or tType == "transfer_operation" ):
			#transfer transaction
						
			#Get transaction From/To
			tFrom   = hTransaction['from']
			tTo     = hTransaction['to']
							
			if ( tFrom == "exodegame" or tTo == "exodegame" ):
				lOut = self.ReadTransfert(tValue=hTransaction, tBlock=tBlock, mysql=mysql)
					
		elif ( tType == "custom_json" or tType == "custom_json_operation" ):
			#JSON transaction
						
			#Get transaction value
			tVAuths = hTransaction['required_posting_auths']
			if ( len(tVAuths) <= 0 ):
				return 0
							
			lOut = self.ReadJSONTransaction(tValue=hTransaction, tBlock=tBlock, mysql=mysql)

		if ( lOut[0] == cst_exode.ALERT_MINT ):
			if( len(lOut[1]) > 0 ):
				for msg in lOut[1]:
					print ( msg )
								
				await self.disc_send_msg_list( lOut[1], self.DISC_CHANNELS_MINT)
				
		elif ( lOut[0] == cst_exode.ALERT_MARKET ):
			if( len(lOut[1]) > 0 ):
				for msg in lOut[1]:
					print ( msg )	
					
				await self.disc_send_msg_list( lOut[1], self.DISC_CHANNELS_MARKET )
							
							
		elif ( lOut[0] == cst_exode.ALERT_GIFT ):
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
				DISC_CHANNEL = self.client.get_channel(ch_id)					
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
				DISC_CHANNEL = self.client.get_channel(ch_id)	
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
				DISC_CHANNEL = self.client.get_channel(ch_id)	
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
				DISC_CHANNEL = self.client.get_channel(ch_id)	
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
			DISC_CHANNEL = self.client.get_channel(DISCORD_CHANNEL_id)
			
			if ( DISC_CHANNEL == None ): 
				continue
				
			for msg in msg_list:
				await DISC_CHANNEL.send(msg)	
				
	async def disc_send_msg(self, msg, CHANNEL_LIST):
		
		if ( not self.fDoDiscord ):
			return
	
		for DISCORD_CHANNEL_id in CHANNEL_LIST:
			DISC_CHANNEL = self.client.get_channel(DISCORD_CHANNEL_id)
			
			if ( DISC_CHANNEL == None ): 
				continue
				
			await DISC_CHANNEL.send(msg)	

	######################################################################################	

	async def rebuild_exode_database(self, iFirstBlock: int, bBlockC, mysql: lib_mysql, from_start: bool = False):
			
		self.fReBuildDataBase = True
		with open('database_rebuild.flag','w') as f:
			json.dump(True, f)

		print ( "Reset transfer database" )
		lib_database.db_TransferTX_Reset(last_block=iFirstBlock, mysql=mysql)
		print( "Calculate Mints" )
		(self.MINT_NUM, self.MINT_NUM_NOSOURCE) = lib_database.db_Card_LoadMint(mysql=mysql)
		lib_database.db_Card_Mint_Missing(mysql=mysql)
		print( "Loading exode history" )
		
		# Load exode history to build the database
		acc = Account("exodegame")
		self.fLoadExodeGame = True
			
		c_last_block_chain = bBlockC.get_current_block_num()
			
		# Load only cancel transaction			
		c_block = int(lib_database.db_Cancel_GetLastBlock(mysql=mysql))	
		if ( c_block < cst_exode.EXODE_BLOCK_MIN_CANCEL ):
			c_block = cst_exode.EXODE_BLOCK_MIN_CANCEL
			
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
					lib_database.db_Cancel_FillTX( tTxId=mTxId, tBlock=tBlock )	
						
				c_block_cur = tBlock
			
		# Set last block seen
		lib_database.db_Cancel_SetLastBlock( tBlock=c_block_cur, mysql=mysql )
			
		# Load list
		self.fCancelTransactionList = lib_database.db_Cancel_GetTXs(mysql=mysql)
			
		print ( self.fCancelTransactionList )			
			
		if from_start:
			iFirstBlock = 0
			
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
					
				lOut = await self.ProcessTransaction( tType=tType, tBlock=tBlock, hTransaction=hTransaction, mysql=mysql )
					
				if ( lOut == cst_exode.ALERT_KILL ):
					raise Exception("ERROR: ALERT_KILL")
											
				with open('logs/file_block_fast.json', 'w') as f:
					json.dump( tBlock, f ) 
			
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
		m_players = lib_database.db_ExodePlayers_List(mysql=mysql)
		iPlayer   = 0
		for player_name in m_players:
			
			iPlayer = iPlayer + 1
					
			try:
				if len(player_name) > 16:
					print("Account ", player_name, " should not exists!")
					continue

				acc = Account(player_name)
			except bexceptions.AccountDoesNotExistsException:
				print("Account ", player_name, " does not exists!")
				continue
					
									
			c_block_1 = lib_database.db_TX_GetLastBlock(mPlayer=player_name, mysql=mysql)
			c_block_2 = lib_database.db_Player_GetLastBlock(mPlayer=player_name, mysql=mysql)
			c_block = max(c_block_1,c_block_2)
								
			if ( c_block < cst_exode.EXODE_BLOCK_MIN ):
				c_block = cst_exode.EXODE_BLOCK_MIN
				
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
							
					lOut = await self.ProcessTransaction(tType=tType, tBlock=tBlock, hTransaction=hTransaction, mysql=mysql )
						
					if ( lOut == cst_exode.ALERT_KILL ):
						raise Exception("ERROR: ALERT_KILL")
						
					c_block_cur = tBlock
				
			hTransactionList.clear() 	
			lib_database.db_Player_SetLastBlock(mPlayer=player_name, mBlock=c_last_block, mysql=mysql)			
				
		self.fLoadPlayerMarket = False
							
		print ( "Build loop done" )						
		if ( os.path.isfile('logs/file_block_fast.json') ):
			with open('logs/file_block_fast.json', 'r') as f:
				self.fFirstBlock = json.load(f) 

		self.fReBuildDataBase = False
		os.remove('database_rebuild.flag')

	async def rebuild_exode_sale_database(self, mysql: lib_mysql):
		self.fRebuildSaleDatabase = True
		with open('database_sale_rebuild.flag','w') as f:
			json.dump(True, f)

		# Rebuild sale/transfer
		lib_database.db_TransferTX_Reset(last_block=None, delete_transfer=False, mysql=mysql)	
		print ( "Add known missing mint" )
		lib_database.db_Card_Mint_Missing(mysql=mysql)
		print( "Calculate Mints" )
		(self.MINT_NUM, self.MINT_NUM_NOSOURCE) = lib_database.db_Card_LoadMint(mysql=mysql)
		print ( "Get last transfer tx block" )	
		c_last_block = lib_database.db_TransferTX_Last(mysql=mysql)	
		lib_database.db_TransferTX_Reset_ToBlock(last_block=c_last_block, mysql=mysql)

		print ("Load transfer from: ", c_last_block )
		mTransferTX = lib_database.db_TransferTX_Get(mBlock=c_last_block, mysql=mysql)
		for mRow in mTransferTX:
			self.ProcessTransfer( tx_auth=mRow[0], tx_type=mRow[1], tx_block=mRow[2], tx_time=mRow[3], tx_id=mRow[4], 
									player_from=mRow[5], player_to=mRow[6], card_id=mRow[7], card_uid=mRow[8], price=mRow[9], mysql=mysql )	
			
		self.fRebuildSaleDatabase = False	
		os.remove('database_sale_rebuild.flag')					
						
	async def first_process_exode(self, bBlockC, mysql: lib_mysql):

		iLastBlock = bBlockC.get_current_block_num()
		iFirstBlock = 0

		try:
			with open('logs/file_block_fast.json', 'r') as f:
				self.fFirstBlock = json.load(f) 
		except:
			self.fFirstBlock = 0
	
		iFirstBlock = self.fFirstBlock
		print("Last block is:", iFirstBlock)

		from_start = False
		if ( iFirstBlock < cst_exode.EXODE_BLOCK_MIN ):
			iFirstBlock = cst_exode.EXODE_BLOCK_MIN
			from_start = True

		if iLastBlock <= iFirstBlock:
			return

		# Compute card mint numbers:
		(self.MINT_NUM, self.MINT_NUM_NOSOURCE) = lib_database.db_Card_LoadMint(mysql=mysql)
			
		if (self.fReBuildDataBase or (self.fFirstBlock + 2000 < iLastBlock and self.fIterator == 0 and not self.fFast)):
			print("Rebuild eXode database")

			##########################################################################
			msg = "Rebuilding Blockchain Transactions database..."
			await self.disc_send_msg(msg, self.DISC_CHANNELS_MINT)
			await self.rebuild_exode_database(iFirstBlock=iFirstBlock, bBlockC=bBlockC, mysql=mysql, from_start=from_start)
			msg = "Blockchain Transactions database rebuilding completed!"
			await self.disc_send_msg(msg, self.DISC_CHANNELS_MINT)
			##########################################################################

			# Rebuild Sale database
			self.fRebuildSaleDatabase = True
		
		if (self.fRebuildSaleDatabase):
			print("Rebuild eXode sale database")

			##########################################################################
			msg = "Rebuilding Sales database..."
			await self.disc_send_msg(msg, self.DISC_CHANNELS_MINT)
			await self.rebuild_exode_sale_database(mysql=mysql)
			msg = "Sales database rebuilding completed!"
			await self.disc_send_msg(msg, self.DISC_CHANNELS_MINT)
			##########################################################################

		if ( not self.fLoadMintOnly ):
			print ( "Add known new missing mint" )
			lib_database.db_Card_Mint_Missing_New(mysql=mysql)
		
	async def process_exode(self, bBlockC, mysql: lib_mysql):
			
		block_step = 200
		
		while True:

			# Get first block
			iFirstBlock = 0
			if ( os.path.isfile('logs/file_block_fast.json') ):
				with open('logs/file_block_fast.json', 'r') as f:
					iFirstBlock = json.load(f) 
			
			if ( iFirstBlock < cst_exode.EXODE_BLOCK_MIN ):
				iFirstBlock = cst_exode.EXODE_BLOCK_MIN
			
			# Get last block
			iLastBlock = bBlockC.get_current_block_num()
			
			if iLastBlock <= iFirstBlock:
				return
			iLastBlock = min(iLastBlock,iFirstBlock+block_step)
			print(f"Loading from {iFirstBlock} to {iLastBlock}")
			# Loop over blocks
			for fBlock in Blocks(iFirstBlock, count=block_step):
				tBlock = fBlock.block_num

				if ( int(tBlock) > int(iLastBlock) ):
					break
											
				# Check if need to reconnect or to ping
				if ( self.fIterator % 100 == 0 ):					
					
					# Update player table
					lib_database.db_Player_CompleteList(mysql=mysql)
					lib_database.db_Player_SetLastBlock_all(mBlock=tBlock-1, mysql=mysql)
						
					print("Discord: reconnect")
					# Reconnect
					await self.disc_connect()

					print("Discord: ping")
					# Ping
					msg = "[PING] Reading block {block}".format(block=tBlock)
					await self.disc_send_msg(msg, self.DISC_CHANNELS_PING)
						
				# Check if need to reconnect or to ping
				if ( self.fIterator % 30000 == 0 ):	
										
					msg = "Listing :blue_square:, delisting :purple_square:, and buy :green_square: alert messages are displayed in this channel.\n**[NOTE]** Mint numbers are estimated from the *currently incomplete* blockchain minting broadcasts. They are not an official information."
					await self.disc_send_msg(msg, self.DISC_CHANNELS_MARKET)
					msg = "**[NOTE]** Mint numbers are estimated from the *currently incomplete* blockchain minting broadcasts. They are not an official information."
					await self.disc_send_msg(msg, self.DISC_CHANNELS_MINT)

					self.fIterator = 0
																			
				# Increase Iterator
				self.fIterator += 1
					
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
						lOut = await self.ProcessTransaction( tType=tType, tBlock=tBlock, hTransaction=tOperation['value'], mysql=mysql )
							
						if ( lOut == cst_exode.ALERT_KILL ):
							raise Exception("ERROR: ALERT_KILL")
				
				tLastBlock = tBlock
				with open('logs/file_block_fast.json', 'w') as f:
					json.dump( tLastBlock, f ) 

			return tLastBlock


	async def read_exode(self):
	
		if ( self.Hive == None ):
			self.LoadHiveBlockChain()

		if ( not self.Hive.is_hive ):
			print("[FATAL] Hive is not loaded")
			quit()
			
		if ( self.fIterator % 100 == 0 ):
			await self.disc_connect()
			
		#Get get_current_block
		bBlockC = Blockchain()
		mysql = lib_mysql(db_user=cst_exode.DB_USER, db_version=cst_exode.DB_NAME, db_password=cst_exode.DB_PASS)

		if self.fStart:
			print ( "DISCORD_BOT: read_exode" ) 
			
			# First processing
			await self.first_process_exode(bBlockC=bBlockC, mysql=mysql)

			# Change flag	
			self.fFast            = False
			self.fReBuildDataBase = False
			try: 
				os.remove('database_rebuild.flag')
			except:
				pass
			
			self.fLoadMintOnly    = False
			self.fStart 		  = False
		
		# Normal processing
		# It's running! 
		iBlock = await self.process_exode(bBlockC=bBlockC, mysql=mysql)

		lib_database.db_Player_CompleteList(mysql=mysql)
		lib_database.db_Player_SetLastBlock_all(mBlock=iBlock-1, mysql=mysql)

		mysql.close_cursor()
		
	
	


		
