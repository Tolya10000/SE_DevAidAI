#!/bin/bash

parentDir=$(dirname "$(realpath $0)")

streamlit run $parentDir/app.py