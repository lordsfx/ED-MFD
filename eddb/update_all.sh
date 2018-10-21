echo "Downloading Systems..."
curl -OJ https://eddb.io/archive/v5/systems_populated.json
echo "Downloading Stations..."
curl -OJ https://eddb.io/archive/v5/stations.json
echo "Filtering Stations..."
./filter_stations.sh  > stations_filtered.json
