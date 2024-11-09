# COMP6015_project
SWAT testbed project 

# Run this command to run the backend code:
1.go to 
cd /Downloads/Project-comp6016/COMP6016_project2/backend/
run this below : 
source venv/bin/activate
gunicorn --bind 0.0.0.0:8001 --timeout 300 app:app

or just run below command
gunicorn --bind 0.0.0.0:8000 --timeout 300 wsgi:app

# Command to run pox controller:
cd ../../pox/pox/
./pox.py forwarding.l2_learning
./pox.py log.level --DEBUG openflow.of_01 --port=6637 pox_controller

# To run the mininet traffic injection script: 
sudo python3 mn_traffic_injection.py /home/vikas/Downloads/Project-comp6016/COMP6016_project2/backend/venv/modified_SWaT_Dataset.csv

# to run ml server :
gunicorn --bind 0.0.0.0:5003 ml_server:app

# to check which process is running on port and killing it.
# for example on port 8001
sudo lsof -i :8001
sudo kill -9 <pid>

# To see all nodes in mininet; use below command
dump
