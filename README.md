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

## MySQL tables

The following tables are needed:

```
CREATE TABLE `exode_tx` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tx_id` varchar(100) NOT NULL,
  `block` bigint DEFAULT NULL,
  `type` varchar(100) NOT NULL,
  `uid` varchar(100) DEFAULT NULL,
  `cancel` tinyint DEFAULT (0),
  `player` varchar(100) DEFAULT NULL,
  `player_from` varchar(100) DEFAULT NULL,
  `auth` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
)
```

```
CREATE TABLE `exode_cancel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cancelled_tx_id` varchar(100) NOT NULL,
  `block` bigint DEFAULT NULL,
  PRIMARY KEY (`id`)
)
```

```
CREATE TABLE `exode_player` (
  `id` int NOT NULL AUTO_INCREMENT,
  `player` varchar(100) NOT NULL,
  `last_block` bigint NOT NULL,
  PRIMARY KEY (`id`)
)
```

```
CREATE TABLE `exode_pack` (
  `id` int NOT NULL AUTO_INCREMENT,
  `player` varchar(100) NOT NULL,
  `type` varchar(100) NOT NULL,
  `nb` mediumint DEFAULT NULL,
  `opened` mediumint DEFAULT (0),
  PRIMARY KEY (`id`)
)
```

```
CREATE TABLE `exode_cards` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(100) NOT NULL,
  `num` mediumint DEFAULT (0),
  `uid` varchar(100) NOT NULL,
  `owner` varchar(100) NOT NULL,
  `burn` tinyint DEFAULT NULL,
  `bound` tinyint DEFAULT NULL,
  `elite` tinyint DEFAULT NULL,
  `mint_num` mediumint DEFAULT NULL,
  `block_update` bigint DEFAULT (0),
  `block` bigint DEFAULT (0),
  `minter` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
)
```

```
CREATE TABLE `exode_sales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `seller` varchar(100) NOT NULL,
  `asset_type` varchar(100) NOT NULL,
  `asset_uid` varchar(100) NOT NULL,
  `price` float(8,3) DEFAULT NULL,
  `tx_id` varchar(100) NOT NULL,
  `block_update` bigint DEFAULT (0),
  `block` bigint DEFAULT (0),
  `sold` tinyint DEFAULT (0),
  `buyer` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
)
```


## Usage

The script can be run with the following command:

```
python3 read_exode.py
```

The script will make several hours (10h as of September 2021) to build the card database, and several hours more to read past sales transaction from players. 
Note that both steps are not needed for simple sale alert, user should modify directly the script if they want to use it for more simple functions. 




