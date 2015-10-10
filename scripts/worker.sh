for i in $(seq ${1-1})
do
    nohup python3 rqworker.py > logs/worker$i.txt &
done
