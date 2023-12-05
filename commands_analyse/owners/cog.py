from nextcord.ext import commands
import cst_exode, lib_analyze, lib_exode
from lib_mysql import lib_mysql
import nextcord

class owners(commands.Cog, name='owners'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@nextcord.slash_command(description="Display a list of 10 players owning the card.", dm_permission=False, force_global=True)
	async def owners(self, interaction: nextcord.Interaction, card: str = nextcord.SlashOption(
        name="card", description="Card's ID or number", required=True
    ), is_elite: bool = nextcord.SlashOption(
        name="is_elite", description="Indicate if the result should be for the elite version of the card", required=False, default=False
    ),):
		await interaction.response.defer(with_message=True)

		print ("owners_topmint", card)

		if not is_elite:
			is_elite = lib_exode.ex_IsNameElite(name=card)
		tElite = 1 if is_elite else 0
		tID = lib_exode.ex_GetAssetID( card, is_elite )

		(is_pack, asset_name, asset_rank, asset_num) = lib_exode.ex_GetAssetDetails( tID )
			
		if ( is_pack ):
			return
				
		mysql = lib_mysql(db_user=cst_exode.DB_USER, db_version=cst_exode.DB_NAME, db_password=cst_exode.DB_PASS)

		mMax = 10
		(tCards, tCard_Owner, tCard_Num, tOwners) = lib_analyze.db_Card_Owners( tID, mMax, mysql=mysql )

		mysql.close_cursor()
			
		msg_elite = ""
		if ( tElite == 1 ):
			msg_elite = "Elite "
		
		
		msg = " **{elite}{name}** ({asset_id}) owners are: \n".format(elite=msg_elite,name=asset_name,asset_id=tID)
		if ( tCards > 0 ):
			for i in range(tCards):
				msg = msg + " - **{owner}** who owns {card_count} cards \n".format(owner=tCard_Owner[i],card_count=tCard_Num[i])
			if ( tOwners > mMax ):
				msg = msg + " ... and {own_num} others".format(own_num=(tOwners-mMax))
		
		
		message = await interaction.original_message()
		await message.edit(content=msg)

def setup(bot: commands.Bot):
	bot.add_cog(owners(bot))
