#!/usr/bin/env

#Run me to download and unzip the GeoLite Librarys neccesary

wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
gunzip *.gz
