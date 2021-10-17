#!/bin/bash

echo "About to install HVR Software"
sudo mkdir -p -m 01777 /opt/hvr/hvr_config /opt/hvr/hvr_tmp
sudo mkdir /opt/hvr/hvr_home
sudo chown -R hvr:hvr /opt/hvr
cd /opt/hvr/hvr_home
gzip -dc /install/$HVR_INSTALL_FILE | tar xf -

mkdir -p $HVR_CONFIG/etc

echo "Start agent"
$HVR_HOME/bin/hvragentlistener -i 4343