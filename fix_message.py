import os
import nextcord
from nextcord.ext import commands
import exode_const as excst

def main():
	
	client = commands.Bot(	command_prefix="&",
				case_insensitive=True,
				help_command=None)
				
	@client.event
	async def on_ready():
		print('We have logged in as {0.user}'.format(client))
		
		# Get message:
		#channel = client.get_channel(883253237090746409)
		#message = await channel.fetch_message(932058318745260103)
		#await message.edit(content=":tada: cryptoeater found a **FIREWORKS** [*Legendary*] (**1**/1 *uid=8ac5b8ab9313e86d33c6621d70b691cc*)")



	client.run(excst.BOT_TOKEN_ALERT)


if __name__ == '__main__':
	main()


	


		
