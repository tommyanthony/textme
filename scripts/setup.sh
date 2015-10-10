cd ../
if [ ! -d logs ]; then
    mkdir logs
fi
python3 gmaps_client/gmaps.py > logs/gmaps_out.txt &
python3 sms_client.py > logs/sms_client_out.txt &

