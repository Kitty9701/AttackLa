#!/usr/bin/python3
import textx
import numpy as np
import lxml.etree
import lxml.builder
import sys
import glob
import os
from xml.etree import ElementTree
import xml.etree.ElementTree as ET
from textx.metamodel import metamodel_from_file
from utils import attack_file_generator,parse_routes_file
import csv
import argparse
from argparse import RawTextHelpFormatter
import pandas as pd
import random
from ruamel import yaml
from samplers.GBO import Guided_Bayesian_Optimization
from samplers.RNS import Random_Neighborhood_Search
from samplers.Random import Random_Search
from samplers.Grid import Grid_Search
from samplers.Manual import ManualEntry
from samplers.Halton import Halton_Sequence
import re
import shutil

varying_entities = ['attack_length', 'action', 'road_segments', 'cause_density', 'sensor_faults']
action_parameters = ['cloudiness','precipitation','precipitation_deposits','sun_altitude_angle','wind_intensity','sun_azimuth_angle','wetness','fog_distance','fog_density']


def write_sampler_results(route_path,folder,parameter_values,joined_parameters,data_path):
    """
    Parameters returned by the sampler
    """
    with open(route_path + "sampled_parameters.csv", 'a') as csvfile: #Always save the selected hyperparameters for optimization algorithms
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerow(parameter_values) 


    with open(folder + "/attack_parameters.csv", 'w') as csvfile1: #Always save the selected hyperparameters for optimization algorithms
        writer = csv.writer(csvfile1, delimiter = ',')
        writer.writerows(joined_parameters)



def parameter_sampler(dynamic_parameters,static_parameters,folder,simulation_run,route_path,y,optimizer,sampler,data_path,total_attacks,path,exploration):
    """
    The sampler code that takes in current step hyperparameters and returns new hyperparameter set
    1. Manual Entry by User
    2. Random Search
    3. Bayesian Optimization Search
    4. Hyperband Search
    5. Reinforcement Learning
    """

    if sampler == "Random":
        parameter_values, sampled_parameters = Random_Search(dynamic_parameters,folder,simulation_run,route_path,y,exploration)
    if sampler == "Grid":
        parameter_values, sampled_parameters = Grid_Search(dynamic_parameters,folder,simulation_run,route_path,y,exploration)
    if sampler == "Halton":
        parameter_values, sampled_parameters = Halton_Sequence(dynamic_parameters,folder,simulation_run,route_path,y,total_attacks,exploration)
    elif sampler == "Guided_Bayesian_Optimization":
        if simulation_run == 0:
            shutil.copy(path + "previous_knowledge/cond4/sampled_parameters.csv", route_path)
            shutil.copy(path + "previous_knowledge/cond4/ood_stats.csv", data_path)
            shutil.copy(path + "previous_knowledge/cond4/collision_stats.csv", data_path)
            shutil.copy(path + "previous_knowledge/cond4/scenario_score.csv", data_path)
            shutil.copy(path + "previous_knowledge/cond4/similarity_score.csv", data_path)
        parameter_values, sampled_parameters = Guided_Bayesian_Optimization(dynamic_parameters,folder,simulation_run,route_path,y,path,data_path,exploration)
    elif sampler == "Selective_Sampling":
        parameter_values, sampled_parameters = Random_Neighborhood_Search(dynamic_parameters,folder,simulation_run,route_path,y,path,data_path,exploration)

    joined_parameters = sampled_parameters + static_parameters

    write_sampler_results(route_path,folder,parameter_values,joined_parameters,data_path)

    #print(sampled_param_values)
    return joined_parameters


def get_distribution_values(parameter_name):
    """
    Hard coded min and max values for the parameters
    """
    if parameter_name in attack_parameters:
        min,max = 0,100
    elif parameter_name == "Image brightness":
        min,max = 0,100
    return min, max

def read_attack_parameters(attack_info,varying_attack_entities,varying_attack_parameters):
    """
    Read attack parameters and their distribution ranges entered by the user
    """
    static_parameters = []
    dynamic_parameters = []
    num_entities = len(attack_info.entities)
    for i in range(0,num_entities):
        entity_name = attack_info.entities[i].name
        if entity_name in varying_entities:
            num_parameters = len(attack_info.entities[i].properties)
            for j in range(0,num_parameters):
                parameter_name = attack_info.entities[i].properties[j].name
                parameter_type = attack_info.entities[i].properties[j].type.name
                if parameter_name in varying_attack_parameters:
                    #print(parameter_name)
                    if parameter_type == 'distribution':
                        parameter_min, parameter_max = get_distribution_values(parameter_name)
                        dynamic_parameters.append((parameter_name,parameter_min,parameter_max))
                    static_parameters.append((parameter_name,parameter_value))

    return dynamic_parameters, static_parameters


def organize_parameters(param_vals):
    """
    Organize varying attack parameters
    """
    action_list = []
    #camera_fault_type = 0
    for val in param_vals:
        if val[0] == 'time':
            attack_time = int(val[1])
        elif val[0] == 'cause_density':
            cause_info = int(val[1])
        elif val[0] == 'road_segments':
            road_segment = int(val[1])
            #print(road_segment)
        elif val[0] == 'sensor_faults':
            fault_type = int(val[1])
        else:
            action_list.append(val)

    return action_list,cause_info,road_segment, fault_type


def set_attack_action(attack_info,action_list):
    """
    attack parameters for the attack
    """
    action = []
    for i, entry in enumerate(action_list):
        if entry[0] == 'method':
            attack_info.entities[2].properties[0] = str(int(entry[1]))
        elif entry[0] == 'preconditions':
            attack_info.entities[2].properties[1] = str(int(entry[1]))
    return action

def set_action_preconditions(preconditions_info,preconditions_list):
    """
    precondition parameters for the attack
    """
    preconditions = []
    for i, entry in enumerate(preconditions_list):
        if entry[0][0] == 'the attacker car':
           preconditions_info.entities[2].properties[0] = str(entry[1])
        elif entry[0][0] == 'laser':
            preconditions_info.entities[2].properties[0] = str(entry[1])
        
       if entry[0][1] == 'before the victim car':
           preconditions_info.entities[2].properties[1] = str(entry[1])
        elif entry[0][1] == 'on the roadside':
            preconditions_info.entities[2].properties[1] = str(entry[1])
    return action

def set_attack_cause(cause_info,cause_list):
    """
    cause parameters for the attack
    """
    cause = []
    for i, entry in enumerate(cause_list):
        if entry[0] == 'influenced element':
            attack_info.entities[2].properties[0] = str(int(entry[1]))
        elif entry[0] == 'influence':
            attack_info.entities[2].properties[1] = str(int(entry[1]))
    return cause

def set_cause_influence(influence_info,influence_list):
    """
    influence parameters for the attack
    """
    influence= []
    for i, entry in enumerate(influence_list):
        if entry[0][0] == 'Image brightness':
           influence_info.entities[2].properties[0] = str(int(entry[1]))
    return influence

def set_attack_road_segment(global_route,road_segment):
    """
    Waypoints for the attack
    """
    list = []
    list.append(global_route[road_segment*2])
    list.append(global_route[road_segment*2+1])
    list.append(global_route[road_segment*2+2])

    return list

def write_action_data(action,data_file):
    """
    Write action data into a file for simulator
    """
    with open(data_file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerows(action)

def get_attack_info(scenario_language_path,carla_route, num_attacks, varying_attack_entities, varying_attack_parameters, sampler, manual_attack_specification):
    """
    Invoke the scenario generation language and pull in the language grammer, attack parameters that require sampling
    """
    grammar = metamodel_from_file(scenario_language_path + 'carla.tx') #grammer for the scenario language
    attack_info = grammar.model_from_file(scenario_language_path + 'attack-model.carla') #scenario entities
    agent_info = grammar.model_from_file(scenario_language_path + 'agent-model.carla') #agent entities
    global_route,town = parse_routes_file(carla_route,False) #global route by reading one route from CARLA AD
    dynamic_parameters, static_parameters = read_attack_parameters(attack_info,varying_attack_entities, varying_attack_parameters) #Get the attack parameters that vary

    #print(attack_info.entities)
    return attack_info, dynamic_parameters, static_parameters,global_route,town

def read_yaml(yaml_file):
    """
    Read the input yaml file entered by the user
    """
    with open(yaml_file) as file:
        config = yaml.safe_load(file)

    return config

def decode_attack_description(attack_config):
    """
    Decode the attack description to extract attack related information
    """
    manual_attack_specification = []
    varying_entities = []
    varying_parameters = []
    sampler = []
    num_attacks = attack_config['Simulation Length']
    for entry in attack_config['Threat Description']:
        if entry == 'action':
            val = 0
            for data in attack_config['attack Description']['action']:
                if attack_config['Scene Description']['action'][data] is True:
                    varying_parameters.append(data)
                    val+=1
            if val > 0:
                varying_entities.append(entry)
        else:
            if attack_config['Scene Description'][entry] is True:
                varying_entities.append(entry)
                varying_parameters.append(entry)

    for entry in attack_config['Samplers']:
        if attack_config['Samplers'][entry] is True:
            sampler.append(entry)

    if len(sampler) > 1:
        print("Warning multiple samplers are selected in the specification file!!!!")
        sys.exit(1)
    if len(sampler) == 0:
        print("Warning no samplers are selected in the specification file!!!!")
        sys.exit(1)

    if sampler[0] == 'Manual':
        if not attack_config['Threat Specification']:
            print("Warning: Manual Threat Specification is not provided!!!")
            #quit()
            sys.exit(1)
        else:
            for entry in attack_config['Threat Specification']:
                manual_attack_specification.append(attack_config['Threat Specification'][entry])
                #print(entry)

    print("-----------Running %s Optimizer---------------"%sampler[0])

    return num_attack, varying_entities, varying_parameters, sampler[0], manual_attack_specification

def main(args,root,y,path):
    """
    Main that hosts the scenario generation in loop
    """
    attack_num = args.attack_num
    simulation_run = args.simulation_num
    optimizer = args.optimizer
    total_attacks = args.total_attacks
    exploration = args.exploration_runs
    route_path = root[0]
    data_path = root[1]
    distributions = []
    print("----------------------------------------------")
    print("Attack%d Artifacts Generated"%simulation_run)
    action_data = []
    joined_parameter_list = []
    #data_path = path + "simulation%d"%y + "/"
    carla_route = path + '/carla-challange/leaderboard/data/routes/route_17.xml'
    folder = route_path + "attack%d"%simulation_run #folder to store all the xml generated
    scenario_language_path = 'sdl/attack/'
    os.makedirs(folder, exist_ok=True)
    data_file = folder + "/attack_data.csv"
    attack_description = path + '/carla-challange/sdl/attack/attack_description.yml'
    #agent_description = '/carla-challange/sdl/attack/agent_description.yml'
    attack_config = read_yamlattack_description)
    #agent_config = read_yaml(agent_description)
    num_attacks, varying_attack_entities, varying_attack_parameters, sampler, manual_attack_specification = decode_attack_description(attack_config)
    attack_info,dynamic_parameters, static_parameters,global_route,town = get_attack_info(scenario_language_path,carla_route,num_attacks, varying_attack_entities, varying_attack_parameters, sampler, manual_attack_specification)
    if sampler == 'Manual':
        joined_parameter_list = ManualEntry(manual_attack_specification,folder,simulation_run,route_path,y,dynamic_parameters, static_parameters)
    else:
        if len(dynamic_parameters) == 0:
            joined_parameter_list = static_parameters
            for entry in static_parameters:
                distributions.append(entry[1])
                #joined_parameter_list.append((entry[0],0))
            write_sampler_results(route_path,folder,distributions,joined_parameter_list,data_path)
        else:
            joined_parameter_list = parameter_sampler(dynamic_parameters,static_parameters,folder,simulation_run,route_path,y,optimizer,sampler,data_path,total_attacks,path,exploration)
        #joined_parameter_list = dynamic_parameters + static_parameters
    action_list,cause_info,road_segment, fault_type = organize_parameters(joined_parameter_list) #Organize the selected hyperparameters
    action = set_attack_action(attack_info,action_list) #action description
    action_data.append(action)
    road_segment_list = set_attack_road_segment(global_route,road_segment) #Choose the road segment
    attack_file_generator(attack_info,attack_num,folder,road_segment_list,town) #generated XML each round
    write_action_data(action_data,data_file) #write action to file


def write_folder_number(y,path):
    """
    Write the folder number in which the routes are stored
    """
    file1 = open(path + "tmp.txt","w")
    file1.write(str(y))
    file1.close()

def create_root_folder(sim_number,path):
    paths = []
    roots = []
    folders = ["routes","simulation-data","images","processed_files"]
    for folder in folders:
        root = path + folder + "/"
        dirlist = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root,item))]
        folder_len = len(dirlist)
        if folder_len == 0:
            y = 0
        else:
            if sim_number == 0:
                y = folder_len
            else:
                y = folder_len - 1
        folder_path = root + "simulation%d"%y + "/"
        os.makedirs(folder_path, exist_ok=True) #creates a new dir everytime with max number
        paths.append(folder_path)
        roots.append(root)

    write_folder_number(y,roots[0])

    return paths, y


if __name__ == '__main__':
        description = "CARLA Scene Generation\n"
        parser = argparse.ArgumentParser(description=description, formatter_class=RawTextHelpFormatter)
        parser.add_argument('--project_path', type=str, help='Type the simulation folder to store the data')
        parser.add_argument('--simulation_num', type=int, default=1, help='Type the simulation folder to store the data')
        parser.add_argument('--attack_num', type=int, default=1, help='Type the attack number to be executed')
        parser.add_argument('--optimizer', type=str, default="Random", help='Type the Optimizer to be used for attack selection')
        parser.add_argument('--total_attacks', type=int, help='Total number of attacks')
        parser.add_argument('--asd', type=int, help='Total Exploration Runs')
        args = parser.parse_args()
        path = args.project_path
        root,y = create_root_folder(args.simulation_num,path)

        main(args,root,y,path)
