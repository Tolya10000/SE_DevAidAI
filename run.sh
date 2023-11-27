#!/bin/bash

parentDir=$(dirname "$(realpath $0)")
pip list > $parentDir/tmp.file
IFS=$'\n' read -rd $'\0' array <<< "$(cat $parentDir/requirements.in)"

function main() {
    for i in ${array[@]}
    do
       grep "${i}" $parentDir/tmp.file > /dev/null || pip install "${i}"
    done
    uvicorn app:app --host 0.0.0.0 --port 8080
}

main