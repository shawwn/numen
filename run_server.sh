#!/bin/sh
set -x

port="${1}"
shift 1

if [ -z $port ]
then
  mkfifo stdin
  mkfifo stdout
  # nvm use 0.12
  exec node --expose_debug_as=v8debug -e "require('./numen.js'); launchNumen('js');" < stdin 1>stdout
else
  exec node --expose_debug_as=v8debug -e "require(\"./numen.js\"); launchNumen(\"js\",$port);"
fi
