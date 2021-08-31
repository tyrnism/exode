# eXode Market bot
author: Tyrnis 

Script for eXode discord bot, reading Hive blockchain and sending market alert on Discord.

Use BEEM in order to read Hive blockchain:
https://beem.readthedocs.io/en/latest/

Use discord.py in order to communication with Discord

https://discordpy.readthedocs.io/en/stable/

## Installation

The following package are needed (list is maybe incomplete):
```
sudo apt install build-essential libssl-dev python-dev curl
sudo apt install mysql-client-core-8.0
sudo apt install mysql-server
sudo mysql_secure_installation
```

Install python packages with the following command: 
```
./scripts/install_pip.sh 
```

## Usage

The script can be run with the following command:

```
python3 read_exode.py
```

The script will make several hours (10h as of September 2021) to build the card database, and several hours more to read past sales transaction from players. 
Note that both steps are not needed for simple sale alert, user should modify directly the script if they want to use it for more simple functions. 




