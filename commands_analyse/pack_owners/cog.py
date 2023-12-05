from nextcord.ext import commands
import cst_exode, lib_analyze, lib_exode
from lib_mysql import lib_mysql
import nextcord

class pack_owners(commands.Cog, name='pack_owners'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@nextcord.slash_command(description="Display list of owners for a pack.", dm_permission=False, force_global=True)
	async def pack_owners(self, interaction: nextcord.Interaction, pack: str = nextcord.SlashOption(
        name="pack", description="Pack's name or ID", required=True
    ),):
		await interaction.response.defer(with_message=True)

		print ("pack_owners", pack)
		tID = pack

		tID = lib_exode.ex_GetAssetID( pack, False )
		if tID == "" or tID == None:
			message = await interaction.original_message()
			await message.edit(content="Unknown card or pack")	

		(is_pack, asset_name, asset_rank, asset_num) = lib_exode.ex_GetAssetDetails( tID )
			
		if ( not is_pack ):
			message = await interaction.original_message()
			await message.edit(content="This is not a pack")	
			
		mysql = lib_mysql(db_user=cst_exode.DB_USER, db_version=cst_exode.DB_NAME, db_password=cst_exode.DB_PASS)
		mMax = 10
		(tPacks, tPack_owners, tPack_nbs, tPack_open, tPacks_n) = lib_analyze.db_Pack_GetOwners( tID, "nb", mMax, mysql=mysql )
		mysql.close_cursor()
			
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
			
		message = await interaction.original_message()
		await message.edit(content=msg)

def setup(bot: commands.Bot):
	bot.add_cog(pack_owners(bot))

	