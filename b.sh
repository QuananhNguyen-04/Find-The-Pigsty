python DQN.py > state0.data & 
python DQN.py > state1.data & 
python DQN.py > state2.data & 
python DQN.py > state4.data & 
python DQN.py > state5.data & 
python DQN.py > state3.data & wait; 
timeout 10s python sys.py &&
echo "Combined Done"
python model.py
sh ./b.sh