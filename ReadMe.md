first, open an terminal and start CARLA
cd /home/yeda/carla
./CarlaUE4.sh --world-port=2000 -opengl

second, run the simulation and evaluation process
cd /home/yeda/TCP
conda activate TCP
sh leaderboard/scripts/run_evaluation.sh
