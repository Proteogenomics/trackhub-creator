#!/usr/bin/env bash

# Publish a trackhub described by the given json formatted input file
#   usage: launcher.sh <trackhub_registry_url> <trackhub_registry_username> <trackhub_registry_password> <trackhub_description_data.json>
#
# Manuel Bernal Llinares <mbdebian@gmail.com>

# Include helpers
source scripts/commons/helper_functions.sh

# Commands
PWD=$(which pwd)

# Logging with prefix
function mylogger() {
    logger "[Publish_Trackhub] $@"
}

# Command line parameters
#CMD_PARAM_TRACKHUB_REGISTRY_URL=$1
CMD_PARAM_TRACKHUB_REGISTRY_USERNAME=$1
CMD_PARAM_TRACKHUB_REGISTRY_PASSWORD=$2
CMD_PARAM_TRACKHUB_DESCRIPTION_DATA_FILE=$3

mylogger "Publishing Trackhub described by '${CMD_PARAM_TRACKHUB_DESCRIPTION_DATA_FILE}'"
mylogger "Current directory is $($PWD)"
mylogger "<--- Running publish_trackhub --->"
#time python_install/bin/python ./main_app.py -a trackhub_registry_url=${CMD_PARAM_TRACKHUB_REGISTRY_URL},trackhub_registry_username=${CMD_PARAM_TRACKHUB_REGISTRY_USERNAME},trackhub_registry_password=${CMD_PARAM_TRACKHUB_REGISTRY_PASSWORD},trackhub_description=${CMD_PARAM_TRACKHUB_DESCRIPTION_DATA_FILE} publish_trackhub
time python_install/bin/python ./main_app.py -a trackhub_registry_username=${CMD_PARAM_TRACKHUB_REGISTRY_USERNAME},trackhub_registry_password=${CMD_PARAM_TRACKHUB_REGISTRY_PASSWORD},trackhub_description=${CMD_PARAM_TRACKHUB_DESCRIPTION_DATA_FILE} publish_trackhub