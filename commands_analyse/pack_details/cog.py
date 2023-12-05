from nextcord.ext import commands
import cst_exode, lib_analyze, lib_exode
from lib_mysql import lib_mysql
import nextcord

class pack_details(commands.Cog, name='pack_details'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@nextcord.slash_command(description="Display info about a pack.", dm_permission=False, force_global=True)
	async def pack_details(self, interaction: nextcord.Interaction, pack: str = nextcord.SlashOption(
        name="pack", description="Pack's name or ID", required=True
    ),):
		await interaction.response.defer(with_message=True)

		print ("pack_details", pack)
		
		tID = lib_exode.ex_GetAssetID( pack, False )
		if tID == "" or tID == None:
			message = await interaction.original_message()
			await message.edit(content="Unknown card or pack")	

		(is_pack, asset_name, asset_rank, asset_num) = lib_exode.ex_GetAssetDetails( tID )
			
		if ( not is_pack ):
			message = await interaction.original_message()
			await message.edit(content="This is not a pack")	
	
		mysql = lib_mysql(db_user=cst_exode.DB_USER, db_version=cst_exode.DB_NAME, db_password=cst_exode.DB_PASS)
		cInfo = lib_analyze.db_Pack_GetDetails( tID, mysql=mysql )
		mysql.close_cursor()
			
		msg = "**{name}** ({asset_id}) was distributed **{num}** times and opened **{num_o}** times, **{num_l}** are left\n".format(name=asset_name,asset_id=tID, num=(cInfo['nb']+cInfo['open']), num_o=cInfo['open'], num_l=cInfo['nb'])
		msg = msg + "**[Note]** distributed pack number is incorrect"
		message = await interaction.original_message()
		await message.edit(content=msg)

def setup(bot: commands.Bot):
	bot.add_cog(pack_details(bot))
