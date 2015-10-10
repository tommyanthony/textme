cd ../
if [ ! -d logs ]; then
    mkdir logs
fi
python gmaps_client/gmaps.py > logs/gmaps_out.txt &
python sms_client.py > logs/sms_client_out.txt &
