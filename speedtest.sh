while :; do
	timedatectl | grep 'Local time' | sed 's/^.*: //' >>result.txt
	speedtest | grep "Download\|Upload" >>result.txt
	printf "\n" >>result.txt
	echo added
	sleep 300
done
