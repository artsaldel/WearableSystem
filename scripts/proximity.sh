while :; do
	b=`hcitool rssi 70:77:81:76:33:66`
	if [ "$b" == "RSSI return value: 0" ]; then
		echo "Lejos"
	else
		echo "Cerca"
	fi
	sleep 1
done