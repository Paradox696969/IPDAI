# imports
import pandas
import random

# Optional Iterated Prisoners Dilemma
class Strategy:
    def __init__(self):
        pass

    def play_move(self, last_move):
        return random.choice([0, 1, 2])

# class for all strategies
class Strategies:
    # always cooperates
    class Cooperator(Strategy):
        def __init__(self, noise):
            self.noise = noise

        def play_move(self, last_move):
            if not random.random() < self.noise:
                return 0
            else:
                return random.choice([0, 1, 2])

    # always defects
    class Defector(Strategy):
        def __init__(self, noise):
            self.noise = noise

        def play_move(self, last_move):
            if not random.random() < self.noise:
                return 1
            else:
                return random.choice([0, 1, 2])

    # always abstains
    class Abstainer(Strategy):
        def __init__(self, noise):
            self.noise = noise

        def play_move(self, last_move):
            if not random.random() < self.noise:
                return 2
            else:
                return random.choice([0, 1, 2])

    # alternates between all three moves
    class Alternator(Strategy):
        def __init__(self, noise, S="D"):
            self.noise = noise
            super().__init__()
            if S == "C":
                self.last_move = 2
            elif S == "D":
                self.last_move = 0
            elif S == "A":
                self.last_move = 1

        def play_move(self, last_move):
            if not random.random() < self.noise:
                if self.last_move == 0:
                    self.last_move = 1
                    return 1
                elif self.last_move == 1:
                    self.last_move = 2
                    return 2
                elif self.last_move == 2:
                    self.last_move = 0
                    return 0
            else:
                return random.choice([0, 1, 2])
    
    # changes strategy upon opponent move change
    class TitForTat(Strategy):
        def __init__(self, noise):
            self.noise = noise
        
        def play_move(self, last_move):
            if not random.random() < self.noise:
                if last_move == 0:
                    return 0
                elif last_move == 1:
                    return 1
                elif last_move == 2:
                    return 1
                elif last_move == None:
                    return random.choice([0, 1, 2])
            else:
                return random.choice([0, 1, 2])

# evaluate a position
def evaluate_position(p1, p2):
    years = [0, 0]
    if p1 == 0 and p2 == 0:
        years = [1, 1]
    elif p1 == 0 and p2 == 1:
        years = [5, 0]
    elif p1 == 1 and p2 == 0:
        years = [0, 5]
    elif p1 == 1 and p2 == 1:
        years = [3, 3]
    elif p1 == 2 or p2 == 2:
        years = [2, 2]
    
    return tuple(years)

# define a match between two strategies
def Match(strat1, strat2, num_iterations):
    results = []
    strat1_moves = []
    strat2_moves = []
    for i in range(num_iterations):
        try:
            p1 = strat1.play_move(strat2_moves[-1])
            p2 = strat2.play_move(strat1_moves[-1])
        except IndexError:
            p1 = strat1.play_move(None)
            p2 = strat2.play_move(None)
        strat1_moves.append(p1)
        strat2_moves.append(p2)
        results.append((evaluate_position(p1, p2), (p1, p2)))
    
    return results, [strat1_moves, strat2_moves]

# evaluate a math result
def evaluate_results(results):
    p1_scores = []
    p2_scores = []
    for i in results:
        p1_scores.append(i[0][0])
        p2_scores.append(i[0][1])
    
    p1_avg = sum(p1_scores) / len(p1_scores)
    p2_avg = sum(p2_scores) / len(p2_scores)

    return (p1_avg, p2_avg), (p1_scores, p2_scores)

# if this program is run(not imported)
# run a number of matches with varying noise
# and store the data
if __name__ == "__main__":
    strategies = [Strategies.Cooperator, Strategies.Defector, Strategies.Abstainer, Strategies.Alternator, Strategies.TitForTat]
    noise_levels = [0, 0.1, 0.3, 0.5, 0.7, 0.9, 1]
    noise_mod = [3, 0.75, 0.3, 0.188, 0.12, 0.08, 0.06]
    strat_names = [1, 2, 3, 4, 5]

    dataframe_dict = {"Strategy":[], "Move1A": [], "Move2A": [], "Move3A": [], "Move4A": [], "Move5A": [],
                        "Move1B": [], "Move2B": [], "Move3B": [], "Move4B": []}

    for strat1 in strategies:
        i1 = strategies.index(strat1)
        for strat2 in strategies:
            i2 = strategies.index(strat2)
            for noise in noise_levels:
                for i in range(round((noise_mod[noise_levels.index(noise)])*20000)):
                    results = Match(strat1(noise), strat2(noise), 5)[1]
                    dataframe_dict["Strategy"].append(strat_names[i1])
                    dataframe_dict["Move1A"].append(results[0][0])
                    dataframe_dict["Move2A"].append(results[0][1])
                    dataframe_dict["Move3A"].append(results[0][2])
                    dataframe_dict["Move4A"].append(results[0][3])
                    dataframe_dict["Move5A"].append(results[0][4])
                    dataframe_dict["Move1B"].append(results[1][0])
                    dataframe_dict["Move2B"].append(results[1][1])
                    dataframe_dict["Move3B"].append(results[1][2])
                    dataframe_dict["Move4B"].append(results[1][3])

    dataframe = pandas.DataFrame(dataframe_dict)
    dataframe.to_csv("train.csv", index=False)


    for noise in noise_levels:
        dataframe_dict = {"Strategy":[], "Move1A": [], "Move2A": [], "Move3A": [], "Move4A": [], "Move5A": [],
                            "Move1B": [], "Move2B": [], "Move3B": [], "Move4B": []}
        for strat1 in strategies:
            i1 = strategies.index(strat1)
            for strat2 in strategies:
                i2 = strategies.index(strat2)
                for i in range(10000):
                    results = Match(strat1(noise), strat2(noise), 5)[1]
                    dataframe_dict["Strategy"].append(strat_names[i1])
                    dataframe_dict["Move1A"].append(results[0][0])
                    dataframe_dict["Move2A"].append(results[0][1])
                    dataframe_dict["Move3A"].append(results[0][2])
                    dataframe_dict["Move4A"].append(results[0][3])
                    dataframe_dict["Move5A"].append(results[0][4])
                    dataframe_dict["Move1B"].append(results[1][0])
                    dataframe_dict["Move2B"].append(results[1][1])
                    dataframe_dict["Move3B"].append(results[1][2])
                    dataframe_dict["Move4B"].append(results[1][3])

        dataframe = pandas.DataFrame(dataframe_dict)
        dataframe.to_csv(f"test_noise_{noise}.csv", index=False)


            

