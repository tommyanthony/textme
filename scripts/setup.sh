cd ../
if [ ! -d logs ]; then
    mkdir logs
fi
nohup python3 gmaps_client/gmaps.py > logs/gmaps_out.txt &
cd weather_client/
nohup python3 forecast.py > ../logs/weather_out.txt &
cd ../
nohup python3 sms_client.py > logs/sms_client_out.txt &
