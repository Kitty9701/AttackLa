## Setup

First, install CARLA 0.9.10 in your computer, and then download the file best_model.ckpt (it is too big to upload to github) through https://drive.google.com/file/d/1ZVSG-RGZwBRQqcioZ1IEbTjJrgvBBZk4/view?usp=sharing and save it in the AttackLa folder.

Second, create an conda enviroment by the following commands

```
conda env create -f environment.yml --name AttackLa
conda activate TCP
```
Third, open an terminal and start CARLA by the following commands
```
cd $CARLA_ROOT$
./CarlaUE4.sh --world-port=2000 -opengl
```
Fourth, run the simulation and evaluation process by the following commands
```
conda activate AttackLa
cd AttackLa
sh leaderboard/scripts/run_evaluation.sh
```
Then you can see the black screen attack generated in the simulation, and once the simulation is completed you can see the evaluation result printed.

## Advanced

The default attack conducted is black screen attack. If you want to try the other two attacks(strong light exposure attack and laser beam attack),you can interpret the description file by the following commands
```
cd description_and_interpreter
python attack_interpreter.py --attack_description_file attack2.py
```
or 
```
cd description_and_interpreter
python attack_interpreter.py --attack_description_file attack3.py
```
Then run the commands mentiond in section 'Setup'
```
cd $CARLA_ROOT$
./CarlaUE4.sh --world-port=2000 -opengl
```
```
conda activate AttackLa
cd AttackLa
sh leaderboard/scripts/run_evaluation.sh
```

If you want to generate you own attack model, please find the file 'attack1.yml' in folder 'description_and_interpreter' and then modify the attack model as described in my thesis. Then run the following commands.
```
cd description_and_interpreter
python attack_interpreter.py --attack_description_file attack1.py
```

## Citation

If you find our repo or our paper useful, please use the following citation:

```
@mastersthesis{cheng2024Cybersecurity,
 title={Cybersecurity Testing and Evaluation of Autonomous Driving Sensors}, 
 author={Jingyue Cheng},
 year={2024},
}
```

## License
All code within this repository is under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Acknowledgements

Our code is based on several repositories:
- [TCP](https://github.com/OpenDriveLab/TCP/tree/main)
- [CARLA Leaderboard](https://github.com/carla-simulator/leaderboard)
- [Scenario Runner](https://github.com/carla-simulator/scenario_runner)
