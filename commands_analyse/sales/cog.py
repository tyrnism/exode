from nextcord.ext import commands
import cst_exode, lib_analyze, lib_exode
from lib_mysql import lib_mysql
import nextcord

class sales(commands.Cog, name='sales'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@nextcord.slash_command(description="Display the average and last sold prices.", dm_permission=False, force_global=True)
	async def sales(self, interaction: nextcord.Interaction, asset: str = nextcord.SlashOption(
        name="card", description="Card's or Pack's ID or number", required=True
    ), is_elite: bool = nextcord.SlashOption(
        name="is_elite", description="Indicate if the result should be for the elite version of the card", required=False, default=False
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

		mysql = lib_mysql(db_user=cst_exode.DB_USER, db_version=cst_exode.DB_NAME, db_password=cst_exode.DB_PASS)
		(tSale_avgP, tSale_lastP, tSales, tSale_times, tSale_prices) = lib_analyze.db_Sale_GetInfo( tID, mysql=mysql )
		
		msg_elite = ""
		if ( tElite == 1 ):
			msg_elite = "Elite "
		
		msg = " **{elite}{name}** ({asset_id}) was sold {nSales} times for an average price of **${price_avg:.2f}**, the last was sold at **${price_last}** ".format(elite=msg_elite,name=asset_name,nSales=tSales,price_avg=tSale_avgP,price_last=tSale_lastP,asset_id=tID)
		
		mysql.close_cursor()
		message = await interaction.original_message()
		await message.edit(content=msg)		
		

def setup(bot: commands.Bot):
	bot.add_cog(sales(bot))
