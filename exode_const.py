
import os.path
from dotenv import load_dotenv

# Flag
RASPBERRY_PI = False
MINT_IFNOSOURCE = True

# Store Max Mint
MINT_NUM = {}
MINT_NUM_NOSOURCE = {}

# Block
EXODE_BLOCK_MIN        = 42233330
EXODE_BLOCK_MIN_CANCEL = 45975275 # Minimum block for cancellation broadcast

# Tokens
load_dotenv()
BOT_TOKEN_ALERT    = os.getenv('EXODE_DISCORD_TOKEN_ALERT')
BOT_TOKEN_ANALYSER = os.getenv('EXODE_DISCORD_TOKEN_ANALYSER')
DB_PASS            = os.getenv('EXODE_DB_PASS')
DB_NAME            = "exode_db"

RASPBERRY_PI = False

# Channel names

CHANNEL_MARKET_NAME  = "exode-market-preprod"
CHANNEL_MINT_NAME    = "new-mints-preprod"
CHANNEL_PING_NAME    = "exode-bot-ping-preprod"
CHANNEL_ANALYSE_NAME = "exode-market-data-preprod"
"""	
CHANNEL_MARKET_NAME  = "exode-market"
CHANNEL_MINT_NAME    = "new-mints"
CHANNEL_PING_NAME    = "exode-bot-ping"
CHANNEL_ANALYSE_NAME = "exode-market-data"
"""
# Message level
NO_ALERT     = 0
ALERT_MARKET = 1
ALERT_MINT   = 2
ALERT_KILL   = -1
