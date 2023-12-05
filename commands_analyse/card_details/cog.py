from nextcord.ext import commands
import cst_exode, lib_analyze, lib_exode
from lib_mysql import lib_mysql
import nextcord

class card_details(commands.Cog, name='card_details'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@nextcord.slash_command(description="Display info about a specific card.", dm_permission=False, force_global=True)
	async def card_details(self, interaction: nextcord.Interaction, card: str = nextcord.SlashOption(
        name="card", description="Card's UID", required=True
    ),):
		await interaction.response.defer(with_message=True)

		print ("card_details", card)
		tUID = card

		mysql = lib_mysql(db_user=cst_exode.DB_USER, db_version=cst_exode.DB_NAME, db_password=cst_exode.DB_PASS)
		
		cInfo = lib_analyze.db_Card_GetDetails( tUID, mysql=mysql )
		
		if ( not cInfo['exist' ] ):
			msg = "Unknown uid"
		else:
			tMintTot = lib_analyze.db_Card_GetNMintTot( cInfo['id'], cInfo['elite'], mysql=mysql )		
			(is_pack, card_name, card_rank, card_num) = lib_exode.ex_GetAssetDetails(cInfo['id'])
			
			card_rank_name = "Common"
			if ( card_rank == 1 ):
				card_rank_name = "Rare"
			if ( card_rank == 2 ):
				card_rank_name = "Epic"
			if ( card_rank == 3 ):
				card_rank_name = "Legendary"
			
			msg_elite = "a **"
			if ( cInfo['elite'] == 1 ):
				msg_elite = "an **Elite "
				
			msg = "*{uid}* is a {elite}{name}** [*{rank}*], owned by **{player}** with mint **{mint}**/{mint_tot}".format(uid=tUID, elite=msg_elite, player=cInfo['owner'],name=card_name, rank=card_rank_name, mint=cInfo['mint'], mint_tot=tMintTot)
		
		mysql.close_cursor()
		message = await interaction.original_message()
		await message.edit(content=msg)

def setup(bot: commands.Bot):
	bot.add_cog(card_details(bot))
