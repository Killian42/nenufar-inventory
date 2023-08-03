#! /bin/bash

SHORT=s:,h
LONG=scope:,help
OPTS=$(getopt --alternative --name inventory --options $SHORT --longoptions $LONG -- "$@")

eval set -- "$OPTS"

while :
do
  case "$1" in
    -s | --scope )
      city1="$2"
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

echo $scope

bash ./inventory.sh

python3 inventory-follow-up.py

python3 obs-timeline.py -s $scope