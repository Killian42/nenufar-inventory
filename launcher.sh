#! /bin/bash

SHORT=s:,e:,h
LONG=scope:,email:,help
OPTS=$(getopt --alternative --name inventory --options $SHORT --longoptions $LONG -- "$@")

eval set -- "$OPTS"

while :
do
  case "$1" in
    -s | --scope )
      scope="$2"
      shift 2
      ;;
    -e | --email )
      email="$2"
      shift 2
      ;;
    -h | --help)
      "Choose all or thisweek"
      exit 2
      ;;
    --)
      shift;
      break
      ;;
    *)
      echo "Unexpected option: $1"
      ;;
  esac
done

bash ./inventory.sh

python3 inventory-follow-up.py

python3 obs-timeline.py -s $scope -e $email