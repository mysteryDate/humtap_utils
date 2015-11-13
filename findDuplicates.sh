for arr in *.json; do
	for arr2 in new/*.json; do
		if cmp $arr $arr2; then
			echo "$arr" + "$arr2" >> output.txt
		fi
	done
done