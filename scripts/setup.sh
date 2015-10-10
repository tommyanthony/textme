cd ../
if [ ! -d logs ]; then
    mkdir logs
fi
nohup python gmaps_client/gmaps.py > logs/gmaps_out.txt &
nohup python sms_client.py > logs/sms_client_out.txt &
