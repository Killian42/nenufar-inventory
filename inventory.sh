#! /bin/bash

### This script creates an inventory of the data available of nenufar pulsar observations
### Input: None 									  
### Output: A CSV file containing basic information about the observed pulsars (POS,DM,P0,RM)
###	    and information on the observation files (number of files, number of unique 
###	    observations, starting day and time, duration, center frequency, bandwidth) 

today=$(date -I)
main_path=/databf/nenufar-pulsar/DATA/*/
current_path=$(pwd)
file_name=/pulsar-obs-inventory-${today}.csv
save_path="${current_path}${file_name}"
file_header=";Pulsar name;Filename;Mode;Observation day;Observation time;Observation duration (s);Center frequency (MHz);Bandwidth (MHz)"

echo ${file_header} >> ${save_path}

for dir in ${main_path}
do
    psr=`basename ${dir}`

    cd $dir
    list_subdir=`ls`
    for sub_dir in ${list_subdir}
    do
	cd $sub_dir

	list_files=`ls *.fits`

	if [ $sub_dir == "SEARCH" ]
	then

	for file in ${list_files}
	do
		file_info=$(psredit -qc "name,file,ext:obs_mode,ext:stt_date,ext:stt_time,freq,bw" -Q ${file})

		file_duration_info=`psredit -qc "sub:tsamp,sub:nsblk,sub:nrows" -Q ${file}`
		arr=( $file_duration_info )
		duration=`echo ${arr[0]}*${arr[1]}*${arr[2]} | bc -l`

		b1=$(cut -d ' ' -f 1-6 <<< ${file_info})
		b2=$(cut -d ' ' -f 7-9 <<< ${file_info})

		echo "${b1// /;};${duration};${b2// /;}" >> ${save_path}
	done

	else

	for file in ${list_files}
	do
		file_info=$(psredit -qc "name,file,ext:obs_mode,ext:stt_date,ext:stt_time,length,freq,bw" -Q ${file})
		echo "${file_info// /;}" >> ${save_path}
	done

	fi

	cd ..
    done
    
    cd /databf/nenufar-pulsar/DATA
done