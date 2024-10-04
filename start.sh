#!/bin/bash

source env.sh

screen -S EXODE_READ -X quit
screen -S EXODE_ANALYSIS -X quit

screen -dmS EXODE_READ ./start_read.sh
screen -dmS EXODE_ANALYSIS ./start_analysis.sh
