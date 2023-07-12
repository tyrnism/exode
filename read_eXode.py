
import os, traceback

import nextcord
from nextcord.ext import tasks, commands

import lib_monitoring, cst_exode
from lib_monitoring import lib_monitoring

		
##############################################################################################
error_count = 0

def main():
	intents = nextcord.Intents.default()
	intents.message_content = True

	monitor = lib_monitoring()
	
	client = commands.Bot(case_insensitive=True, help_command=None, intents=intents)

	for folder in os.listdir("commands"):
		if os.path.exists(os.path.join("commands", folder, "cog.py")):
			client.load_extension(f"commands.{folder}.cog")

	@tasks.loop(minutes=1)
	async def read_exode():
		global error_count
		
		try:
			# Check for stop order	
			if ( os.path.isfile('stop.order') ):	
				print("shutdown")
				raise Exception("stop_order")
		
			await monitor.read_exode(client=client)

			error_count = 0

		except ValueError as err:
				
			if ( str(err) == "stop_order" ):
				msg = ":zap: Killing order received, going to shutdown... :zap:"
				with open('stop.order', "r") as f:
					msg = msg + "\n Shutdown reason: " + f.read()
				os.remove('stop.order')
				await monitor.disc_send_msg(msg, monitor.DISC_CHANNELS_MARKET)
				await monitor.disc_send_msg(msg, monitor.DISC_CHANNELS_MINT)
				await monitor.disc_send_msg(msg, monitor.DISC_CHANNELS_PING)

				print("Shuting down")
				raise err
			else:
				print("ValueError", err)
				msg = ":zap: ValueError... Trying to recover :zap:"
				await monitor.disc_send_msg(msg, monitor.DISC_CHANNELS_MARKET)
				await monitor.disc_send_msg(msg, monitor.DISC_CHANNELS_MINT)
				await monitor.disc_send_msg(msg, monitor.DISC_CHANNELS_PING)	

				error_count += 1

			if error_count > 3:
				msg = ":zap: Recovering failed. Calling for support <@!232962122043228160> :zap:"
				await monitor.disc_send_msg(msg, monitor.DISC_CHANNELS_MARKET)
				await monitor.disc_send_msg(msg, monitor.DISC_CHANNELS_MINT)
				await monitor.disc_send_msg(msg, monitor.DISC_CHANNELS_PING)
				raise Exception("Fatal error")

		except:
			err = traceback.format_exc()
			print("Error", err)

			msg = ":zap: Unexpected error... Trying to recover :zap:"
			await monitor.disc_send_msg(msg, monitor.DISC_CHANNELS_MARKET)
			await monitor.disc_send_msg(msg, monitor.DISC_CHANNELS_MINT)
			await monitor.disc_send_msg(msg, monitor.DISC_CHANNELS_PING)	

			error_count += 1

			if error_count > 3:
				msg = ":zap: Recovering failed. Calling for support <@!232962122043228160> :zap:"
				await monitor.disc_send_msg(msg, monitor.DISC_CHANNELS_MARKET)
				await monitor.disc_send_msg(msg, monitor.DISC_CHANNELS_MINT)
				await monitor.disc_send_msg(msg, monitor.DISC_CHANNELS_PING)
				raise Exception("Fatal error")

	@client.event
	async def on_ready():
		print('We have logged in as {0.user}'.format(client))

		if not read_exode.is_running():
			read_exode.start()
			
	client.run(cst_exode.BOT_TOKEN_ALERT)

if __name__ == '__main__':
	main()
