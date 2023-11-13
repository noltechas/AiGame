class Player:
    def __init__(self, player_id, role):
        self.player_id = player_id
        self.role = role  # 'Liberal', 'Fascist', or 'Hitler'
        self.is_alive = True
        self.is_last_president = False
        self.is_last_chancellor = False

    def __repr__(self):
        return f"Player {self.player_id} ({self.role})"