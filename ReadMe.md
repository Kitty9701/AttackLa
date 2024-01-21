First, download the file best_model.ckpt (it is too big to upload to github) and save it in the AttackLa folder.


Second, open an terminal and start CARLA

cd /home/yeda/carla

./CarlaUE4.sh --world-port=2000 -opengl

Third, run the simulation and evaluation process

cd /home/yeda/TCP

conda activate TCP

sh leaderboard/scripts/run_evaluation.sh

Then you can see the black screen attack generated in the simulation, and once the simulation is completed you can see the evaluation result printed.

If you want to generate you own attack, please find the file attack1.yml in folder 'description and interpreter' and then modify the attack model as described in my thesis.

If you want to change the enviroment parameters such as whether, please find the file enviroment.yml in folder 'description and interpreter' and then modify the parameters as described in my thesis.
