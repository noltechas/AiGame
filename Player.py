import random

class Player:
    def __init__(self, player_id, role):
        self.player_id = player_id
        self.role = role  # 'Liberal', 'Fascist', or 'Hitler'
        self.is_alive = True
        self.is_last_president = False
        self.is_last_chancellor = False

    def vote(self, game_state):
        # AI makes a decision to vote 'Ja' or 'Nein'
        # Placeholder logic: Randomly voting Ja or Nein
        return 'Ja' if random.choice([True, False]) else 'Nein'