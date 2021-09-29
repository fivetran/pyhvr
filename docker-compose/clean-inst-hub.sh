#!/bin/bash

echo "About to install HVR Software"
sudo mkdir -p -m 01777 /opt/hvr/hvr_config /opt/hvr/hvr_tmp
sudo mkdir /opt/hvr/hvr_home
sudo chown -R hvr:hvr /opt/hvr
cd /opt/hvr/hvr_home
gzip -dc /install/$HVR_INSTALL_FILE | tar xf -

mkdir -p $HVR_CONFIG/etc

echo "Configure Hub"
$HVR_HOME/bin/hvrhubserverconfig HTTP_Port=4340 
#Repository_Class=postgresql License_Agreement_Accepted=true Database_Host=$HUB_DATABASE_HOST Database_Port=$HUB_DATABASE_PORT Database_Name=$HUB_DATABASE_NAME Database_User=$OVERRIDE_HUB_DATABASE_USER "Database_Password=$OVERRIDE_HUB_DATABASE_PASSWORD"
echo "Start Hub"
$HVR_HOME/bin/hvrhubserver -d
tail -F -n 6 $HVR_CONFIG/logs/hvragentlistener4343.log $HVR_CONFIG/logs/hvrhubserver.out $HVR_CONFIG/hubs/hvrhub/logs/hvr.out &
wait