#!/bin/bash

version=`awk -F "=" '/version/ {print $2}' pkg_info.ini`
author=`awk -F "=" '/author/ {print $2}' pkg_info.ini`
email=`awk -F "=" '/email/ {print $2}' pkg_info.ini`
website=`awk -F "=" '/website/ {print $2}' pkg_info.ini`

echo
echo "MEERA (Multi-value Event-driven Expert in Real-time Assistance)"
echo "${version}"
echo
echo "OS: $(uname -o), Arch: $(uname --m), Kernel: $(uname -r)"
echo
echo "Author: ${author}"
echo "Email: ${email}"
echo "Website: ${website}"
