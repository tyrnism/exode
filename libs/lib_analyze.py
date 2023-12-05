from lib_mysql import lib_mysql

##############################################################################################

def db_Pack_GetDetails( pack_id, mysql: lib_mysql ):
	
	query = ("SELECT SUM(opened), SUM(nb) FROM exode_pack "
			 "WHERE type = %s and player != %s and player != %s" )	
		
	m_output = mysql.select(query, (pack_id,"elindos","exolindos"), mysql_continue=True)
	
	
	tOpened = 0
	tExist  = 0
	
	if ( m_output[0][0] != None ):
			
		tOpened = int(m_output[0][0])
		tExist  = int(m_output[0][1])
	
	output = { 'nb': tExist, 'open': tOpened }
				
	return output
		
def db_Pack_GetOwners( mID, mVar, mMax, mysql: lib_mysql, sPlayer = "elindos" ):
	
	if ( mVar == "nb" ):
		if sPlayer == "elindos":		
			query = ("SELECT player, nb, opened FROM exode_pack "
				 "WHERE type = %s and nb > 0 and player != %s ORDER BY nb DESC LIMIT %s" )
		else:
			query = ("SELECT player, nb, opened FROM exode_pack "
				 "WHERE type = %s and nb > 0 and player = %s ORDER BY nb DESC LIMIT %s" )	
	else:
		if sPlayer == "elindos":
			query = ("SELECT player, nb, opened FROM exode_pack "
				 "WHERE type = %s and opened > 0 and player != %s ORDER BY opened DESC LIMIT %s" )	
		else:
			query = ("SELECT player, nb, opened FROM exode_pack "
				 "WHERE type = %s and opened > 0 and player = %s ORDER BY opened DESC LIMIT %s" )
		
		
	m_output = mysql.select(query, (mID,sPlayer,mMax), mysql_continue=True)
	
	tPack_owners = []
	tPack_nbs    = []
	tPack_open   = []
	tPacks = 0
		
	for row in m_output: 
		tPacks += 1
		
		tPack_owners.append( row[0] )
		tPack_nbs.append( row[1] - row[2] )
		tPack_open.append( row[2] )
				
	if ( mVar == "nb" ):	
		if sPlayer == "elindos":
			query = ("SELECT COUNT(*) FROM exode_pack "
				 "WHERE type = %s and nb > 0 and player != %s" )	
		else:
			query = ("SELECT COUNT(*) FROM exode_pack "
				 "WHERE type = %s and nb > 0 and player = %s" )
	else:
		if sPlayer == "elindos":
			query = ("SELECT COUNT(*) FROM exode_pack "
				 "WHERE type = %s and opened > 0 and player != %s" )	
		else:
			query = ("SELECT COUNT(*) FROM exode_pack "
				 "WHERE type = %s and opened > 0 and player = %s" )	
	
	m_output = mysql.select(query, (mID,sPlayer), mysql_continue=True)
	
	tPacks_n = m_output[0][0]
	
	return (tPacks, tPack_owners, tPack_nbs, tPack_open, tPacks_n)
	
def db_Card_GetDetails( card_uid, mysql: lib_mysql ):
	
	query = ("SELECT owner, type, mint_num, elite, burn, block_update FROM exode_cards "
			 "WHERE uid = %s" )	
		
	m_output = mysql.select(query, (card_uid, ), mysql_continue=True)
	
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
	
def db_Card_GetNMintTot( card_id, card_elite, mysql: lib_mysql ):

	query = ("SELECT COUNT(*) FROM exode_cards "
		 "WHERE type = %s AND elite = %s AND mint_num != -1")	
	
	m_output = mysql.select(query, (card_id, card_elite), mysql_continue=True)
	
	card_ntot_mint  = int(m_output[0][0])
		
	return card_ntot_mint
	
#########################################################################################

def db_Sale_GetInfo(mID, mysql: lib_mysql): 

	if ( mID == "" ):
		return (-1.0, -1.0, 0, [], [])
		
	
	query = ("SELECT price, block_update, time_update from exode_sales "
		"WHERE asset_type = %s and sold = %s and price != 0. ORDER BY block_update")  
	 
	m_out = mysql.select(query, (mID,1), mysql_continue=True )
	
	tSale_times  = []
	tSale_prices = []
	tSale_lastB  = 0
	tSale_lastP  = -1.0
	tSale_avgP   = -1.0
	tSales       = 0
	
	tSale_avgP = 0.0
	for row in m_out:
		tSales += 1
			
		tPrice = float(row[0])
		tBlock  = int(row[1])
		tTime  = row[2]
		
		tSale_prices.append( tPrice )
		tSale_times.append( tTime )
			
		if ( tBlock > tSale_lastB ):
			tSale_lastB = tBlock
			tSale_lastP = tPrice
			
		tSale_avgP = tSale_avgP + tPrice / float(tSales)
				
	return (tSale_avgP, tSale_lastP, tSales, tSale_times, tSale_prices)

def db_Card_Owners(mID, mMax, mysql: lib_mysql):

	
	query = ("SELECT owner, COUNT(*) as co_cards FROM exode_cards "
			 "WHERE type = %s and burn = 0 and mint_num > 0 GROUP BY owner ORDER BY co_cards DESC LIMIT %s" )	
		
	m_output = mysql.select(query, (mID,mMax), mysql_continue=True)
	
	tCard_owners = []
	tCard_nbs    = []
	tCards = 0
	
	for row in m_output:
		tCards += 1
		tCard_owners.append( row[0] )
		tCard_nbs.append( row[1] )
			
	
	query = ("SELECT COUNT(*) FROM exode_cards "
			 "WHERE type = %s and burn = 0 and mint_num > 0 GROUP BY owner" )	
		
	m_output = mysql.select(query, (mID,), mysql_continue=True)
	
	tOwners = m_output[0][0]
	
	return (tCards, tCard_owners, tCard_nbs, tOwners)
	
def db_Card_Owners_Mint(mID, mMax, mysql: lib_mysql):
			
	
	query = ("SELECT owner, mint_num as co_cards FROM exode_cards "
			 "WHERE type = %s and burn = 0 and mint_num > 0 ORDER BY mint_num LIMIT %s" )	
		
	m_output = mysql.select(query, (mID,mMax), mysql_continue=True)
	
	tCard_owners = []
	tCard_mints  = []
	tCards = 0
	
	for row in m_output:
		tCards += 1
		
		tCard_owners.append( row[0] )
		tCard_mints.append( row[1] )
	
	
	query = ("SELECT COUNT(*) FROM exode_cards "
			 "WHERE type = %s and burn = 0 and mint_num > 0 ORDER BY mint_num" )	
		
	m_output = mysql.select(query, (mID,), mysql_continue=True)
	tCards_all = m_output[0][0]
	
	return (tCards, tCard_owners, tCard_mints, tCards_all)

	
def db_TransferTX_Last(mysql: lib_mysql):

	
	query = ("SELECT MAX(block_update) FROM exode_sales")
		
	m_out = mysql.select(query, value_tuple=None, mysql_continue=True)
		
	if ( m_out[0][0] != None ):
		m_out_sale = int(m_out[0][0])
	else: 
		m_out_sale = 0
			
	query = ("SELECT MAX(block_update) FROM exode_cards WHERE block != block_update")
		
	m_out = mysql.select(query, value_tuple=None, mysql_continue=True)
		
	if ( m_out[0][0] != None ):
		m_out_card = int(m_out[0][0])
	else: 
		m_out_card = 0
		
	return max(m_out_sale,m_out_card)
	
def db_TransferTX_LastTX(mysql: lib_mysql):

	query = ("SELECT MAX(block) FROM exode_tx")
	m_out = mysql.select(query, value_tuple=None, mysql_continue=True)
		
	if ( m_out[0][0] != None ):
		m_out_block = int(m_out[0][0])
	else: 
		m_out_block = 0
	
	return m_out_block
	
def db_TransferTX_Remain(mBlock, mysql: lib_mysql):
	
	query = ("SELECT COUNT(*) FROM exode_tx_transfer WHERE tx_block > %s")
	m_out = mysql.select(query, value_tuple=(mBlock,), mysql_continue=True)
		
	
	m_out = m_out[0][0]
	
	return m_out
