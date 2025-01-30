from Shared_Resources import  RANK_NAMES
from datetime import datetime

class Client:
    def __init__(self, name, password):
        now = datetime.now()
        self.name = name
        self.password = password
        self.account_created =  now.strftime("%m/%d/%Y, %H:%M:%S")
        self.mmr = 800
        rnk = (self.mmr - 1000) // 500 if (self.mmr - 1000) // 500 >= 0 else 0
        self.rank = RANK_NAMES[rnk]
        self.max_Score = 0.0
        self.friends = []

    # Name & Password 
    def change_Name(self, newName):
        self.name = newName

    def change_Pass(self, newpass):
        self.password = newpass

    # Friend Section
    def search_Friend(self, friend_client):
        for friend in range (self.friends):
            if (friend_client.name == friend.name):
                return True
        return False

    def add_Friend(self, friend_client):
        self.friends.append(friend_client)

    def remove_Friend(self, friend_client):
        self.friends.remove(friend_client)
    
    # Max Score
    def update_max_score(self, new_max_score):
        self.max_Score = max(new_max_score, self.max_Score)
        self.mmr = new_max_score * 0.001819
        rnk = (self.mmr - 1000) // 500 if (self.mmr - 1000) // 500 >= 0 else 0
        self.rank = RANK_NAMES[rnk]



