from Shared_Resources import RANK_NAMES
from datetime import datetime
import json

class Client:
    def __init__(self, name, password):
        now = datetime.now()
        self.name = name
        self.password = password
        self.account_created = now.strftime("%m/%d/%Y %H:%M:%S")
        self.mmr = 800
        rnk = (self.mmr - 1000) // 500
        rnk = rnk if rnk > 0 else 0
        rnk = 14 if rnk > 14 else rnk
        self.rank = RANK_NAMES[rnk]
        self.max_Score = 0.0
        self.friends = []  # List to store friends

    # Name & Password
    def change_Name(self, newName):
        self.name = newName

    def change_Pass(self, newpass):
        self.password = newpass

    # Friend Section
    def search_Friend(self, friend_name):
        return friend_name in self.friends

    def add_Friend(self, friend_name):
        if friend_name not in self.friends:
            self.friends.append(friend_name)

    def remove_Friend(self, friend_name):
        if friend_name in self.friends:
            self.friends.remove(friend_name)

    # Max Score
    def update_max_score(self, new_max_score):
        self.max_Score = max(new_max_score, self.max_Score)
        self.mmr = new_max_score * 0.001819
        rnk = (self.mmr - 1000) // 500
        rnk = rnk if rnk > 0 else 0
        rnk = 14 if rnk > 14 else rnk
        self.rank = RANK_NAMES[int(rnk)]