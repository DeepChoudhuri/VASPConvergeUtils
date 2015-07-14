#!/bin/sh

# Be sure to check the range of Ecuts used for the convenrgence test, then implelent the same range in the for loop below

for i in $(ls -d */); 
do 
	echo ${i%%/};
	#${i%%/} | head -c3 
	cd ${i%%/};
	#pwd
     	E=`grep 'energy without entropy' OUTCAR | tail -n1 | awk '{print $8}'`
     	echo ${i%%/} ' 	 ' $E >> ../convergenceData.txt  	
	cd ../ 
done

