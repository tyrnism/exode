from nextcord.ext import commands
import cst_exode, lib_analyze
from lib_mysql import lib_mysql
import nextcord

class database_status(commands.Cog, name='database_status'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@nextcord.slash_command(description="Display the status of the database.", dm_permission=False, force_global=True)
	async def database_status(self, interaction: nextcord.Interaction):
		print ("database_status")
		m_last_block = 0
		m_last_tx_block = 0
		m_remains = 0

		await interaction.response.defer(with_message=True)

		mysql = lib_mysql(db_user=cst_exode.DB_USER, db_version=cst_exode.DB_NAME, db_password=cst_exode.DB_PASS)
		m_last_block = lib_analyze.db_TransferTX_Last(mysql=mysql)
		m_last_tx_block = lib_analyze.db_TransferTX_LastTX(mysql=mysql)
		m_remains = lib_analyze.db_TransferTX_Remain(m_last_block, mysql=mysql)
		mysql.close_cursor()
		
		print ( m_last_block, m_last_tx_block, m_remains )
		
		msg = "The sale and ownership database is build up to block **{block_last}** / **{block_real}**, still **{tx_rem}** transactions to process".format(block_last=m_last_block, block_real=m_last_tx_block, tx_rem=m_remains)		

		message = await interaction.original_message()
		await message.edit(content=msg)

def setup(bot: commands.Bot):
	bot.add_cog(database_status(bot))
