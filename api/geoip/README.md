GeoIp
---------------------------------------------------------------------

In order to map IP addresses of voters onto a world map, it is neccesary
to use a database of mappings from ip to location. WhoseOpinion uses the
MaxMind GeoLite data, which you can find on [their website here].

Also, to run locally you may need to run the following (for a linux
debian based system)

    sudo apt-get install binutils libproj-dev gdal-bin libgeoip1 

If you run mac,windows, or anything besides debian, please consult the
appropriate tutorials/documentation for installing those libraries.

[their website here]:http://www.maxmind.com



####Attribution requirement of MaxMind:

This product includes GeoLite data created by MaxMind, available from 
<a href="http://www.maxmind.com">http://www.maxmind.com</a>.
