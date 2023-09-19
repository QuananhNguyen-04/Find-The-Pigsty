start "python DQN.py > state0.data" ^& timeout /t 5 ^& python sys.py
start cmd.exe /c "python DQN.py > state1.data" &
start cmd.exe /c "python DQN.py > state2.data" &
start cmd.exe /c "python DQN.py > state3.data" &
start cmd.exe /c "python DQN.py > state4.data" 