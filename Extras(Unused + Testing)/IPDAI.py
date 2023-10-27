import tensorflow as tf
import numpy as np
import pandas as pd
import random
from data_gen import *
import os

def getAction(strat_name):
    print(f"Current Strategy: {strat_name}")
    print("Action\t\tAction Number\n-----------------------------")
    action = int(input("Cooperate\t0\nDefect\t\t1\nAbstain\t\t2\n\nChoose an action from above: "))
    if action not in [0, 1, 2]:
        print("Invalid action, please select a number between 0 and 2 corresponding to Cooperate, Defect, Abstain.")
        action = getAction()
    return action

def play_game():
    os.system("cls")#replace with cls on windows
    rounds = int(input("Enter number of rounds after the first 6: ")) + 6
    possible_strategies = [Strategies.Cooperator(0.3), Strategies.Defector(0.3), Strategies.Alternator(0.2), Strategies.Abstainer(0.2), Strategies.TitForTat(0.2)]
    strategy_names = ["Cooperator", "Defector", "Alternator", "Abstainer", "TitForTat"]
    early_p2_strat = random.choice(possible_strategies)
    strat_name = strategy_names[possible_strategies.index(early_p2_strat)]
    model = tf.keras.models.load_model("COMPSCI-Project\model.h5")
    ACTIONS = ["Cooperated", "Defected", "Abstained"]
    p1_actions = []
    p2_actions = []
    p1_years = []
    p2_years = []
    os.system("cls")#replace with cls on windows
    for i in range(rounds):
        print("-----------------------------")
        if i <= 4:
            p1 = getAction(strat_name)
            p1_actions.append(p1)
            try:
                p2 = early_p2_strat.play_move(p1_actions[-1])
            except IndexError:
                p2 = early_p2_strat.play_move(None)
            p2_actions.append(p2)
            evaluation = evaluate_position(p1, p2)
            p1_years.append(evaluation[0])
            p2_years.append(evaluation[1])
            os.system("cls")#replace with cls on windows
            print(f"\nRound {i+1}:\n\t\tPlayer\t\tAI".upper())
            print(f"Action\t\t{ACTIONS[p1]}\t{ACTIONS[p2]}")
            print(f"Total Years\t{sum(p1_years)}\t\t{sum(p2_years)}\n")
        else:
            if i == 5:
                p1_years = []
                p2_years = []
            input_data = []
            input_data.extend(p2_actions[-4:])
            input_data.extend(p1_actions[-4:])
            input_data = np.array([input_data])
            prediction = model(input_data).numpy().tolist()
            most_likely_action = prediction[0].index(max(prediction[0]))
            if most_likely_action == 0:
                p2 = random.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 2])
            elif most_likely_action == 1:
                p2 = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 1])
            elif most_likely_action == 2:
                p2 = random.choice([0, 0, 0, 0, 2, 1])
            p1 = getAction("AI")
            p1_actions.append(p1)
            p2_actions.append(p2)
            evaluation = evaluate_position(p1, p2)
            p1_years.append(evaluation[0])
            p2_years.append(evaluation[1])
            os.system("cls")#replace with cls on windows
            print(f"\nRound {i+1}:\n\t\tPlayer\t\tAI".upper())
            print(f"Action\t\t{ACTIONS[p1]}\t{ACTIONS[p2]}")
            print(f"Total Years\t{sum(p1_years)}\t\t{sum(p2_years)}\n")

    if sum(p1_years) < sum(p2_years):
        print(f"\nThe Player won the game with {sum(p2_years)-sum(p1_years)} less years.")
    elif sum(p1_years) > sum(p2_years):
        print(f"\nThe AI won the game with {sum(p1_years)-sum(p2_years)} less years.")
    elif sum(p1_years) == sum(p2_years):
        print(f"\nThe game ended in a tie.")
    
    repeat = input("Play again?(Y/n): ")
    if repeat.lower() == "y":
        play_game()
    else:
        return

play_game()
        