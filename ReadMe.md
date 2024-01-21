First, install CARLA 0.9.10 in your computer, and then download the file best_model.ckpt (it is too big to upload to github) through https://drive.google.com/file/d/1ZVSG-RGZwBRQqcioZ1IEbTjJrgvBBZk4/view?usp=sharing and save it in the AttackLa folder.

Second, create an conda enviroment by the following commands

conda env create -f environment.yml --name AttackLa

conda activate TCP

Third, open an terminal and start CARLA by the following commands

cd \$ carla\_root \$

./CarlaUE4.sh --world-port=2000 -opengl

Fourth, run the simulation and evaluation process by the following commands

conda activate AttackLa

cd AttackLa

sh leaderboard/scripts/run_evaluation.sh

Then you can see the black screen attack generated in the simulation, and once the simulation is completed you can see the evaluation result printed.

Note:
If you want to generate you own attack model, please find the file 'attack1.yml' in folder 'description and interpreter' and then modify the attack model as described in my thesis.

If you want to change the weather parameters, please find the file 'weather.yml' in folder 'description and interpreter' and then modify the parameters as described in my thesis.
