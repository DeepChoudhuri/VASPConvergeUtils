#!/bin/bash

for i in $(ls -d */); do 
	echo ${i%%/};
	cd ${i%%/};
	pwd
        dos2unix * *
	qsub VASP.qsub
	cd ../ 
done
