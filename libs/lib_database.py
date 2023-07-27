from lib_mysql import lib_mysql
import lib_exode
from beem.block import Block

def db_TransferTX_Reset(mysql: lib_mysql, last_block: int = None, delete_transfer: bool = True):

	if last_block != None and last_block != 0:
		query = ("delete from exode_cards "
			"where minter = 'no_source' or block > %s")
		values = (last_block, )
		mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
		
		query = ("delete from exode_tx "
			"where block > %s")
		values = (last_block, )
		mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)

		query = ("UPDATE exode_player SET last_block = %s ") 
		values = (last_block, )
		mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	else:
		query = ("delete from exode_cards "
			"where minter = 'no_source'")
		values = None
		mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
	if delete_transfer:
		query = ("UPDATE exode_cards "
			"SET owner = minter, burn = 0, block_update = block ")
		values = None
		mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
				
		query = ("UPDATE exode_pack "
			"SET nb = buy ")
		values = None
		mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
		
		query = ("truncate exode_sales ")
		values = None
		mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)


def db_TransferTX_Reset_ToBlock(mysql: lib_mysql, last_block: int = None):

	query = ("UPDATE exode_cards "
		"SET owner = minter, burn = 0, block_update = block WHERE block_update >= %s")
	values = (last_block,)
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)

	query = ("DELETE FROM exode_sales WHERE block >= %s")
	values = (last_block,)
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)


##############################################################################################

def db_TX_GetDetails( tx_id, tx_uid, tx_type, tx_target, mysql: lib_mysql ):

	query = ("SELECT block, auth FROM exode_tx "
			 "WHERE tx_id = %s and type = %s and uid = %s and player = %s" )	
	
	output = mysql.select(query_str=query, value_tuple=(tx_id, tx_type, tx_uid, tx_target), mysql_continue=True)
	
	try: 
		tx_exist  = True
		tx_block  = int(output[0][0])
		tx_player = tx_target
		tx_auth   = output[0][1]
	except:
		tx_exist  = False
		tx_block  = 0
		tx_player = tx_target
		tx_auth   = ""
	
	output = { 'exist': tx_exist, 'block': tx_block, 'player': tx_player, 'auth': tx_auth }
	return output	

def db_TX_Cancel( tx_id, tx_uid, tx_type, tx_target, mysql: lib_mysql ):
	query = ("UPDATE exode_tx "
		"SET cancel = %s "
		"WHERE tx_id = %s and type = %s and uid = %s and player = %s") 
	mysql.commit(query_str=query, value_tuple=(1, tx_id, tx_type, tx_uid, tx_target), mysql_continue=True)
				
def db_TX_Add( tx_id, tx_uid, tx_type, tx_block, tx_player, tx_from, tx_auth, mysql: lib_mysql ):
	query = ("INSERT INTO exode_tx "
		"(tx_id, type, uid, block, player, player_from, auth) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s)")
	mysql.commit(query_str=query, value_tuple=(tx_id, tx_type, tx_uid, tx_block, tx_player, tx_from, tx_auth), mysql_continue=True)
		
def db_TX_GetLastBlock(mysql: lib_mysql, mPlayer="exodegame"): 

	query = ("SELECT MAX(block) FROM exode_tx where auth = %s ")
	output = mysql.select(query_str=query, value_tuple=(mPlayer,), mysql_continue=True)

	try:
		m_block = int(output[0][0])
	except: 
		m_block = 0	

	return m_block

#########################################################################################

def db_TransferTX_Add( tx_auth, tx_type, tx_block, tx_id, player_from, player_to, card_id, card_uid, mysql: lib_mysql, price=0.0 ):

	tx_time = Block(tx_block).time()
	
	query = ("INSERT INTO exode_tx_transfer "
		"(tx_auth, tx_type, tx_block, tx_time, tx_id, player_from, player_to, card_id, card_uid, price) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
	values = (tx_auth, tx_type, tx_block, tx_time, tx_id, player_from, player_to, card_id, card_uid, price)
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
def db_TransferTX_FixID( card_uid, card_id, mysql: lib_mysql ):
	
	query = ("UPDATE exode_tx_transfer "
		"SET card_id = %s WHERE card_uid = %s and card_id = ''")
		
	values = (card_id, card_uid)
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
	
def db_TransferTX_Get(mysql: lib_mysql, mBlock=0):

	query = ("SELECT tx_auth, tx_type, tx_block, tx_time, tx_id, player_from, player_to, card_id, card_uid, price FROM exode_tx_transfer where tx_block > %s ORDER BY tx_block")	
	values = (mBlock,)
	m_out = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	return m_out

def db_TransferTX_Last(mysql: lib_mysql):

	query = ("SELECT MAX(block_update) FROM exode_sales")
	values = None
	m_out = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
		
	if ( m_out[0][0] != None ):
		m_out_sale = int(m_out[0][0])
	else: 
		m_out_sale = 0
		
	query = ("SELECT MAX(block_update) FROM exode_cards WHERE block != block_update")
	values = None
	m_out = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
		
	if ( m_out[0][0] != None ):
		m_out_card = int(m_out[0][0])
	else: 
		m_out_card = 0
			
	return max(m_out_sale,m_out_card)
	
#########################################################################################

def db_Player_GetLastBlock(mPlayer, mysql: lib_mysql): 
	
	query = ("SELECT last_block FROM exode_player where player = %s ")
		 
	values = (mPlayer,)
	m_out = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	try:	
		m_block = int(m_out[0][0])
	except:
		m_block = 0
		
	return m_block
	
def db_Player_SetLastBlock(mPlayer, mBlock, mysql: lib_mysql): 

	query = ("SELECT last_block FROM exode_player where player = %s ")
		 
	values = (mPlayer,)
	m_out = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	query = ("UPDATE exode_player "
		"SET last_block = %s "
		"WHERE player = %s") 
	values = (mBlock, mPlayer)
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
def db_Player_SetLastBlock_all(mBlock, mysql: lib_mysql):
	
	query = ("UPDATE exode_player "
		"SET last_block = %s "
		"WHERE last_block < %s") 
	values = (mBlock, mBlock)
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)

def db_Player_CompleteList(mysql: lib_mysql, mFull=False):

	query = ("INSERT INTO exode_player (player) "
		"SELECT exode_pack.player FROM exode_pack "
		"WHERE exode_pack.player not in (select exode_player.player from exode_player) "
		"GROUP BY exode_pack.player ") 
	
	values = None
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
	
	query = ("INSERT INTO exode_player (player) "
		"SELECT exode_cards.owner FROM exode_cards "
		"WHERE exode_cards.owner not in (select exode_player.player from exode_player) "
		"GROUP BY exode_cards.owner ") 
	
	values = None
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
	if ( mFull ):

		query = ("INSERT INTO exode_player (player) "
			"SELECT exode_tx_transfer.player_from FROM exode_tx_transfer "
			"WHERE exode_tx_transfer.player_from not in (select exode_player.player from exode_player) "
			"and exode_tx_transfer.player_from != 'exodegame' and exode_tx_transfer.player_from != 'null' and exode_tx_transfer.player_from != 'market' and exode_tx_transfer.player_from != 'burn' and exode_tx_transfer.player_from != '' "
			"GROUP BY exode_tx_transfer.player_from ") 
		
		values = None
		mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)		
	
		query = ("INSERT INTO exode_player (player) "
			"SELECT exode_tx_transfer.player_to FROM exode_tx_transfer "
			"WHERE exode_tx_transfer.player_to not in (select exode_player.player from exode_player) "
			"and exode_tx_transfer.player_to != 'exodegame' and exode_tx_transfer.player_to != 'null' and exode_tx_transfer.player_to != 'market' and exode_tx_transfer.player_to != 'burn' and exode_tx_transfer.player_to != '' "
			"GROUP BY exode_tx_transfer.player_to ") 
		
		values = None
		mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
		
def db_Player_Add(mPlayer, mysql: lib_mysql):

	query = ("SELECT last_block FROM exode_player where player = %s ")
	values = (mPlayer,)
	m_out = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	try:
		last_block = m_out[0][0]
	except:
		query = ("INSERT INTO exode_player "
		"(player) "
		"VALUES (%s)") 
		
		values =  (mPlayer,)
		mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
#########################################################################################

def db_Pack_GetDetails( pack_owner, pack_id, mysql: lib_mysql ):

	query = ("SELECT nb, opened FROM exode_pack "
			 "WHERE player = %s and type = %s" )	
		
	values = (pack_owner, pack_id)
	m_output = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	try:	
		pack_exist = True
		pack_nb    = int(m_output[0][0])
		pack_open  = int(m_output[0][1])
	except:
		pack_exist = False
		pack_nb    = 0
		pack_open  = 0
	
	output = { 'exist': pack_exist, 'nb': pack_nb, 'open': pack_open }
		
	return output
	
def db_Pack_New( pack_owner, pack_id, pack_nb, pack_buy, pack_open, mysql: lib_mysql ):

	query = ("INSERT INTO exode_pack "
		"(player, type, nb, buy, opened) "
		"VALUES (%s, %s, %s, %s, %s)")
		
	values = (pack_owner, pack_id, pack_nb, pack_buy, pack_open)
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
		
def db_Pack_Update( pack_owner, pack_id, pack_nb, pack_buy, pack_open, mysql: lib_mysql ):

	query = ("UPDATE exode_pack "
		"SET nb = nb + %s, buy = buy + %s, opened = opened + %s "
		"WHERE player = %s and type = %s" )	
		
	values = (pack_nb, pack_buy, pack_open, pack_owner, pack_id)
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
def db_Pack_Apply_TransferAll( pack_prev_owner, pack_new_owner, mysql: lib_mysql ):

	query = ("SELECT type, nb FROM exode_pack "
			 "WHERE player = %s" )	
		
	values = (pack_prev_owner, )
	m_output = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	if m_output != None:
		for iRow in range(len(m_output)):
		
			pack_id = m_output[iRow][0]
			pack_nb = m_output[iRow][1]
			db_Pack_Apply_Update(pack_owner=pack_new_owner, pack_id=pack_id, pack_nb=pack_nb, pack_open=0, mysql=mysql)
			
			query = ("UPDATE exode_pack "
				"SET nb = 0 "
				"WHERE player = %s AND type = %s") 					
			values = (pack_prev_owner, pack_id)
			mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
		
def db_Pack_Apply_Transfer( pack_prev_owner, pack_new_owner, pack_id, pack_nb, mysql: lib_mysql ):
	
	db_Pack_Update( pack_owner=pack_prev_owner, pack_id=pack_id, pack_nb=-1 * pack_nb, pack_buy=0, pack_open=0, mysql=mysql )
	db_Pack_Update( pack_owner=pack_new_owner, pack_id=pack_id, pack_nb=pack_nb, pack_buy=0, pack_open=0, mysql=mysql )	
	
def db_Pack_Apply_Update( pack_owner, pack_id, pack_nb, pack_open, mysql: lib_mysql ):

	pInfo = db_Pack_GetDetails( pack_owner=pack_owner, pack_id=pack_id, mysql=mysql )
	if ( pInfo['exist'] ):
		db_Pack_Update( pack_owner=pack_owner, pack_id=pack_id, pack_nb=pack_nb, pack_buy=pack_nb, pack_open=pack_open, mysql=mysql )
	else:
		db_Pack_New( pack_owner=pack_owner, pack_id=pack_id, pack_nb=pack_nb, pack_buy=pack_nb, pack_open=pack_open, mysql=mysql )
	
#########################################################################################

def db_Card_GetDetails( card_uid, mysql: lib_mysql ):

	query = ("SELECT owner, type, mint_num, elite, burn, block_update FROM exode_cards "
			 "WHERE uid = %s" )	
		
	values = (card_uid, )
	m_output = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	try:	
		card_exist = True
		card_owner = m_output[0][0]
		card_id    = m_output[0][1]
		card_mint  = int(m_output[0][2])
		card_elite = int(m_output[0][3])
		card_burn  = int(m_output[0][4])
		card_block = int(m_output[0][5])
	except:
		card_exist = False
		card_owner = ""
		card_id    = ""
		card_mint  = -1
		card_elite = 0	
		card_burn  = 0
		card_block = 0
	
	output = { 'exist': card_exist, 'owner': card_owner, 'id': card_id, 'mint': card_mint, 'elite': card_elite, 'burn': card_burn, 'block': card_block }
			
	return output
	
def db_Card_Mint( card_owner, card_id, card_num, card_uid, card_mint, card_elite, card_bound, card_block, card_minter, mysql: lib_mysql ):
	
	card_burn = 0
	
	query = ("INSERT INTO exode_cards "
		"(type, num, uid, owner, burn, bound, elite, mint_num, block, block_update, minter) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
				
	values = (card_id, card_num, card_uid, card_owner, card_burn, card_bound, card_elite, card_mint, card_block, card_block, card_minter) 
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
def db_Card_Add_Missing( card_owner, card_id, card_uid, card_num, card_elite, card_block, mysql: lib_mysql ):
	
	query = ("INSERT INTO exode_cards_no_source "
		"(card_owner, card_id, card_uid, card_num, card_elite, card_block) "
		"VALUES (%s, %s, %s, %s, %s, %s)")
				
	values = (card_owner, card_id, card_uid, card_num, card_elite, card_block)
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
def db_Card_Mint_Missing(mysql: lib_mysql):

	query = ("SELECT card_owner, card_id, card_uid, card_num, card_elite, card_block FROM exode_cards_no_source where card_id != '' ")
	values = None
	m_output = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	if ( m_output != None ):	
		tCards = len(m_output)
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
		
			db_Card_Mint( card_owner=card_owner, card_id=card_id, card_num=card_num, card_uid=card_uid, card_mint=card_mint, card_elite=card_elite, card_bound=card_bound, card_block=card_block, card_minter=card_minter, mysql=mysql )
		
def db_Card_Mint_Missing_New(mysql: lib_mysql):

	query = ("SELECT card_owner, card_id, card_uid, card_num, card_elite, card_block FROM exode_cards_no_source where card_id != ''"
		"and card_uid not in (SELECT uid from exode_cards)")
	
	values = None
	m_output = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	if ( m_output != None ):	
		
		tCards = len(m_output)

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
		
			db_Card_Mint( card_owner=card_owner, card_id=card_id, card_num=card_num, card_uid=card_uid, card_mint=card_mint, card_elite=card_elite, card_bound=card_bound, card_block=card_block, card_minter=card_minter, mysql=mysql )
	
def db_Card_Burn( card_uid, card_block, card_burn, card_burner, mysql: lib_mysql ):

	query = ("UPDATE exode_cards "
		"SET burn = %s, block_update = %s, owner = %s "
		"WHERE uid = %s") 
		
	values = (card_burn, card_block, card_burner, card_uid)
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
def db_Card_Transfer( card_uid, card_block, card_owner, mysql: lib_mysql ):

	query = ("UPDATE exode_cards "
		"SET owner = %s, block_update = GREATEST( block_update, %s ) "
		"WHERE uid = %s") 
		
	values = (card_owner, card_block, card_uid) 
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
def db_Card_LoadMint(mysql: lib_mysql):

	query = ("SELECT type, COUNT(*) FROM exode_cards "
		 "WHERE mint_num != -1 GROUP BY type ")	
		
	values = None
	m_output = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	mint_num = {}
	mint_num_no_source = {}

	if ( m_output != None ):	
		tCards = len(m_output)
		for iCard in range(tCards):
			mint_num[ m_output[iCard][0] ] = int(m_output[iCard][1])
			
	query = ("SELECT type, COUNT(*) FROM exode_cards "
		 "WHERE minter = 'no_source'  and owner != 'elindos' and owner != 'exolindos' GROUP BY type ")	
		 
	values = None
	m_output = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	if ( m_output != None ):	
		tCards = len(m_output)
		for iCard in range(tCards):
			mint_num_no_source[ m_output[iCard][0] ] = int(m_output[iCard][1])

	return (mint_num, mint_num_no_source)
	
def db_Card_Apply_TransferAll( card_prev_owner, card_owner, card_block, mysql: lib_mysql ):
	
	query = ("UPDATE exode_cards "
		"SET owner = %s, block_update = %s "
		"WHERE owner = %s and burn = 0 and bound = 0") 
		
	values = (card_owner, card_block, card_prev_owner)
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
def db_Card_Apply_Mint( card_owner, card_id, card_uid, card_mint, card_elite, card_bound, card_block, tx_id, mysql: lib_mysql, bypass=False ):
	
	msg = ""
	(is_pack, card_name, card_rank, card_num) = lib_exode.ex_GetAssetDetails(card_id)
	
	# Mint here
	db_Card_Mint( card_owner=card_owner, card_id=card_id, card_num=card_num, card_uid=card_uid, card_mint=card_mint, card_elite=card_elite, card_bound=card_bound, card_block=card_block, card_minter=card_owner, mysql=mysql )
	
	if ( (card_mint > 0 and card_mint <= 10) or (int(card_elite) == 1) or (card_rank >= 2) or (card_rank == -1) ):
		if ( int(card_elite) == 1 ):
			msg_elite = "an **:exoelite: Elite "
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
		
#########################################################################################

def db_Sale_GetDetails( asset_uid, sale_sold, sale_block, mysql: lib_mysql, sale_seller="" ):

	query = ("SELECT seller, price, sold, cancel FROM exode_sales "
		 "WHERE asset_uid = %s and sold = %s and block < %s ORDER BY block DESC LIMIT 1" )	
	
	values = (asset_uid,sale_sold,sale_block)
	m_output = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	try:	
		sale_exist  = True
		sale_seller = m_output[0][0]
		sale_price  = float(m_output[0][1])
		sale_sold   = int(m_output[0][2])
		sale_cancel = int(m_output[0][3])
	except:
		sale_exist  = False
		sale_seller = ""
		sale_price  = 0.0
		sale_sold   = 0
		sale_cancel = 0
		
	output = { 'exist': sale_exist, 'seller': sale_seller, 'price': sale_price, 'sold': sale_sold, 'cancel': sale_cancel }
			
	return output
	
def db_Sale_Add( sale_seller, asset_id, asset_uid, sale_tx, sale_price, sale_sold, sale_buyer, sale_block, sale_time, mysql: lib_mysql ):

	query = ("INSERT INTO exode_sales "
		"(seller, asset_type, asset_uid, price, tx_id, sold, buyer, block, block_update, time_update) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
				
	values = (sale_seller, asset_id, asset_uid, sale_price, sale_tx, sale_sold, sale_buyer, sale_block, sale_block, sale_time)
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
def db_Sale_Sold( asset_uid, asset_id, sale_tx, sale_sold, sale_buyer, sale_block, sale_time, mysql: lib_mysql ):

	query = ("UPDATE exode_sales "
		"SET buyer = %s, sold = %s, asset_type = %s, block_update = %s, time_update = %s "
		"WHERE asset_uid = %s and sold = %s and block < %s and cancel = %s") 
		
	values = (sale_buyer, sale_sold, asset_id, sale_block, sale_time, asset_uid, 0, sale_block, 0) 
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
	
def db_Sale_Cancel( asset_uid, sale_seller, sale_block, sale_time, mysql: lib_mysql ):

	query = ("UPDATE exode_sales "
		"SET cancel = %s, block_update = %s, time_update = %s "
		"WHERE seller = %s and asset_uid = %s and sold = %s and block < %s and block = block_update and cancel = %s")  	
		
	values = (1, sale_block, sale_time, sale_seller, asset_uid, 0, sale_block, 0)
	mysql.commit(query_str=query, value_tuple=values, mysql_continue=True)
	
def db_Sale_GetAverageSoldPrice( mysql: lib_mysql, mID=""): 

	if ( mID == "" ):
		return -1.0

	query = ("SELECT AVG(price) from exode_sales "
		"WHERE asset_type = %s and sold = %s and price != 0.")  
		 
	values = (mID, 1) 
	m_out = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	if ( m_out[0][0] != None ):
		m_price = float(m_out[0][0])
	else: 
		m_price = -1.0
		
	return m_price
	
def db_Sale_GetLastSoldPrice( mysql: lib_mysql, mID="" ): 

	if ( mID == "" ):
		return -1.0

	query = ("SELECT price from exode_sales "
		"WHERE asset_type = %s and sold = %s and price != 0. ORDER BY block_update DESC")  
		 
	values = (mID, 1)
	m_out = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	try:
		m_price = float(m_out[0][0])
	except: 
		m_price = -1.0
		
	return m_price
			
#########################################################################################

def db_ExodePlayers_List( mysql: lib_mysql):
	
	#Complete list first
	db_Player_CompleteList(mysql=mysql, mFull=True)
	
	query = "SELECT player FROM exode_player "	
	values = None
	m_output = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	m_player_out = []
	if ( m_output != None ):
		for iPlayer in range(len(m_output)):
			m_player_out.append( m_output[iPlayer][0] )
				
	print("Found players in exode_player: ", len(m_player_out) )
	return m_player_out
	
	

#########################################################################################

def db_Cancel_GetTXs( mysql: lib_mysql ): 

	query = ("SELECT cancelled_tx_id FROM exode_cancel ")
		 
	values = None
	m_tx = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	m_tx_out = []
	if ( m_tx != None ):
		for iTx in range(len(m_tx)):
			if ( m_tx[iTx][0] != "last_block" ):
				m_tx_out.append( m_tx[iTx][0] )
	
	return m_tx_out
	

def db_Cancel_GetLastBlock( mysql: lib_mysql ): 

	query = ("SELECT MAX(block) FROM exode_cancel ")
		 
	values = None
	m_out = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	try:
		m_block = int(m_out[0][0])
	except: 
		m_block = 0
		
	return m_block
	
def db_Cancel_SetLastBlock( tBlock, mysql: lib_mysql ): 

	dummy_id = "last_block"
	
	query = ("SELECT cancelled_tx_id, block FROM exode_cancel "
		 "WHERE cancelled_tx_id = %s ")
		 
	values = (dummy_id, )
	m_output = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	try:
		tx_id = m_output[0][0]
		query_block = ("UPDATE exode_cancel "
					"SET block = %s "
					"WHERE cancelled_tx_id = %s") 			
	except:
		query_block = ("INSERT INTO exode_cancel "
					"(block, cancelled_tx_id) "
					"VALUES (%s, %s)") 
	
	
	values = (tBlock, dummy_id)
	mysql.commit(query_str=query_block, value_tuple=values, mysql_continue=True)
		
def db_Cancel_FillTX( tTxId, tBlock, mysql: lib_mysql ): 

	query = ("SELECT cancelled_tx_id, block FROM exode_cancel "
		 "WHERE cancelled_tx_id = %s ")
		 
	values = (tTxId, )
	m_output = mysql.select(query_str=query, value_tuple=values, mysql_continue=True)
	
	try:
		tx_id = m_output[0][0]
		print( "transaction already cancelled: ", tTxId )

	except:
		query_add_cancel = ("INSERT INTO exode_cancel "
					"(cancelled_tx_id, block) "
					"VALUES (%s, %s)") 
		      			
		values = (tTxId, tBlock)
		mysql.commit(query_str=query_add_cancel, value_tuple=values, mysql_continue=True)
	
#########################################################################################
	