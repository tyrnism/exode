import os.path

import nextcord
from nextcord.ext import commands

##############################################################################################
	
def main():
	intents = nextcord.Intents.default()
	intents.message_content = True

	client = commands.Bot(command_prefix="$", case_insensitive=True, help_command=None, intents=intents)

	for folder in os.listdir("commands_analyse"):
		if os.path.exists(os.path.join("commands_analyse", folder, "cog.py")):
			client.load_extension(f"commands_analyse.{folder}.cog")

	@client.event
	async def on_ready():
		print('We have logged in as {0.user}'.format(client))

##############################################################################################
"""
DISC_CHANNELS = []

@DISC_BOT.event
async def on_ready():
	print('Discord bot ready')
	global DISC_CHANNELS
	
	DISC_CHANNELS_TMP   = []			
	with open('channel/ch_analysis.list', 'r') as f:
		for line in f:
			if ( line[0] == "#" or line == "\n" ):
				continue
				
			ch_id = int(line)
			DISC_CHANNELS_TMP.append(ch_id)
						
			if ( ch_id not in DISC_CHANNELS):	
				DISC_CHANNEL = DISC_BOT.get_channel(ch_id)				
				print ( "DISCORD BOT:eXode bot [MARKET-ANALYSER] connected to {guild_name}".format(guild_name=DISC_CHANNEL.guild.name) )
				await DISC_CHANNEL.send("*eXode BOT [MARKET-ANALYSER] is connected here!*")    
	DISC_CHANNELS = DISC_CHANNELS_TMP
    
@DISC_BOT.event
async def on_message(message):
	if message.channel.id in DISC_CHANNELS:
		await DISC_BOT.process_commands(message)
"""
##############################################################################################
