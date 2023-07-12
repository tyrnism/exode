
import os.path
import os

# Flag
MINT_IFNOSOURCE = True
DO_DISCORD      = True

# Block
EXODE_BLOCK_MIN        = 42233330
EXODE_BLOCK_MIN_CANCEL = 45975275 # Minimum block for cancellation broadcast

# Tokens
BOT_TOKEN_ALERT    = os.environ['EXODE_DISCORD_TOKEN_ALERT']
BOT_TOKEN_ANALYSER = os.environ['EXODE_DISCORD_TOKEN_ANALYSER']
DB_PASS            = os.environ['EXODE_DB_PASS']
DB_NAME            = "exode_db"
DB_USER            = "exode"

# Message level
NO_ALERT     = 0
ALERT_MARKET = 1
ALERT_MINT   = 2
ALERT_GIFT   = 3
ALERT_KILL   = -1
