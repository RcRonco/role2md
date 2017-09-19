#!/bin/bash

# Install python3 and pip3.
os_type="$(grep -i -r \^ID= '/etc/os-release')"

if [ "$os_type" = "ID=ubuntu" ]; then
	echo "Ubuntu"
	apt-get install python3 python3-pip
elif [ "$os_type" = "ID=fedora" ]; then
	echo "Fedora"
	dnf install python3 python3-pip 
elif [ "$os_type" = "ID=rhel" ]; then
	echo "Red Hat Enterprise Linux"
	yum install python34 python34-pip	
else
	echo Not detected $os_type
	exit -1
fi

# Install needed python packages
pip3 install -U pyYAML
pip3 install -U jinja2

# Add execute permissions to the script
chmod +x role2md.py

# Add role2md package path to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$PWD
