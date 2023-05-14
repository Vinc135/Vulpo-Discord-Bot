#!/bin/bash
echo "Start eingeleitet. Vulpo wird gestartet."
screen -dmS Vulpo bash -c "python3 main.py; screen -XS $STY quit"
while true; do
	if ! screen -ls | grep -q "Vulpo"; then
		echo "Vulpo ist gecrasht. Ich starte Vulpo neu."
		screen -dmS Vulpo bash -c "python3 main.py; screen -XS $STY quit"
	fi
	sleep 1
done