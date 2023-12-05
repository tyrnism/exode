from nextcord.ext import commands
import cst_exode, lib_analyze, lib_exode
from lib_mysql import lib_mysql
import nextcord
from datetime import datetime, timedelta

import os, random
import matplotlib.dates as pltdates
import matplotlib.pyplot as plt

class sales_graph(commands.Cog, name='sales_graph'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@nextcord.slash_command(description="Display a list of 10 players owning the card.", dm_permission=False, force_global=True)
	async def sales_graph(self, interaction: nextcord.Interaction, asset: str = nextcord.SlashOption(
        name="card", description="Card's or Pack's ID or number", required=True
    ), is_elite: bool = nextcord.SlashOption(
        name="is_elite", description="Indicate if the result should be for the elite version of the card", required=False, default=False
    ), time_range: str =  nextcord.SlashOption(
        name="period", description="Period of the graph", required=False, default="all", choices={"All": "all", "Last year": "year", "Last month": "month", "Last week": "week"}
    ),):
		await interaction.response.defer(with_message=True)

		print ("sales_graph", asset)

		if not is_elite:
			is_elite = lib_exode.ex_IsNameElite(name=asset)
		tElite = 1 if is_elite else 0
		tID = lib_exode.ex_GetAssetID( asset, is_elite )
		if tID == "" or tID == None:
			message = await interaction.original_message()
			await message.edit(content="Unknown card or pack")		

		(is_pack, asset_name, asset_rank, asset_num) = lib_exode.ex_GetAssetDetails( tID )
		
		#######################################

		tTimeFirst = datetime(2020,1,1,0,0)
		tTimeLast  = datetime.now()
		
		tElite = 0	
		if ( time_range == "all" ):
			tTimeCut = ""		
		else:
			
			iDay = 0
			
			if ( time_range == "year" ):
				iDay = 365
			if ( time_range == "month" ):
				iDay = 30
			if ( time_range == "week" ):
				iDay = 7			
			
			ts = datetime.now()
			td = timedelta(days=iDay)
			
			tTimeFirst = ts - td
			tTimeLast  = ts
			
			tTimeCut = (ts - td).isoformat()
			
			
		
		mysql = lib_mysql(db_user=cst_exode.DB_USER, db_version=cst_exode.DB_NAME, db_password=cst_exode.DB_PASS)

		(is_pack, asset_name, asset_rank, asset_num) = lib_exode.ex_GetAssetDetails( tID )
		(tSale_avgP, tSale_lastP, tSales, tSale_times, tSale_prices) = lib_analyze.db_Sale_GetInfo( tID, mysql=mysql )

		mysql.close_cursor()
		
		msg_elite = ""
		if ( tElite == 1 ):
			msg_elite = "Elite "
		
		print("mysql completed")	
		
		tMaxPrice = 0.
		
		for iSale in range(len(tSale_prices)):
			if ( tSale_prices[iSale] > tMaxPrice and tSale_times[iSale] > tTimeFirst and tSale_times[iSale] < tTimeLast ):
				tMaxPrice = tSale_prices[iSale]
				
		print ("max price: ", tMaxPrice)
			
		tSale_dates = pltdates.date2num(tSale_times)
		
		fig, ax = plt.subplots()
			
		plt.plot_date(tSale_dates, tSale_prices, color='green', linestyle='dashed', linewidth = 3,
				marker='o', markerfacecolor='blue', markersize=12)
		plt.xlabel('Time')
		plt.ylabel('Price')
		plt.title("{asset_id} sales: {period}".format(asset_id=tID, period=time_range))
		plt.gcf().autofmt_xdate()
		plt.grid(True)
		plt.ylim(bottom=0.0, top=tMaxPrice*1.1)
		
		if ( tTimeCut != "" ):
			ax.set_xlim([tTimeFirst, tTimeLast])

		#plt.show()
		nRnd = random.randint(0,1000000)
		plt.savefig("./plot_{asset_id}_{rnd}.png".format(asset_id=tID,rnd=nRnd))
		plt.clf()
			
		if ( time_range != "all" ):
			msg = " **{elite}{name}** ({asset_id}) sales during last {period} period were: ".format(elite=msg_elite,name=asset_name,period=time_range,asset_id=tID)
		else:
			msg = " **{elite}{name}** ({asset_id}) sales since the beginning of eXode were: ".format(elite=msg_elite,name=asset_name,period=time_range,asset_id=tID)

		message = await interaction.original_message()
		await message.edit(content=msg, file=nextcord.File("./plot_{asset_id}_{rnd}.png".format(asset_id=tID,rnd=nRnd)))		
		os.remove("./plot_{asset_id}_{rnd}.png".format(asset_id=tID,rnd=nRnd))
		

def setup(bot: commands.Bot):
	bot.add_cog(sales_graph(bot))
