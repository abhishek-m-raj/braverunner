import os
import pickle

game_folder = os.path.dirname(__file__)
progress_folder = os.path.join(game_folder, "progress")


class rank:
    def __init__(self):
        self.ranklevels = {}
        self.current_ranklevel = 0

    def ReturnrankLevel(self):
        try:
            saved_ranklevel = pickle.load(os.path.join(progress_folder, 'ranklevel.txt'))
            return saved_ranklevel
        except:
            saved_ranklevel = pickle.dump(self.current_ranklevel, os.path.join(progress_folder, 'ranklevel.txt'))
            return saved_ranklevel

    def Ranklevel():
        pass


Rank = rank()
cure = Rank.ReturnrankLevel()
print(cure)
