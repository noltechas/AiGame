import random

from Player import Player


class SecretHitlerGame:
    def __init__(self):
        self.players = [Player(i, self.assign_role(i)) for i in range(7)]
        self.liberal_policies = 0
        self.fascist_policies = 0
        self.election_tracker = 0
        self.policy_deck = self.create_policy_deck()
        self.discarded_policies = []
        self.president_index = random.randint(0, 6)
        self.chancellor_index = None
        self.failed_government_count = 0
        self.game_over = False
        self.special_election_president = None

    def assign_role(self, player_id):
        roles = ['Liberal'] * 4 + ['Fascist', 'Fascist', 'Hitler']
        random.shuffle(roles)
        return roles[player_id]

    def create_policy_deck(self):
        deck = ['Liberal'] * 6 + ['Fascist'] * 11
        random.shuffle(deck)
        return deck

    def draw_policies(self):
        if len(self.policy_deck) < 3:
            self.policy_deck += self.discarded_policies
            self.discarded_policies = []
            random.shuffle(self.policy_deck)
        return [self.policy_deck.pop() for _ in range(3)]

    def enact_policy(self, policy):
        if policy == 'Liberal':
            self.liberal_policies += 1
        elif policy == 'Fascist':
            self.fascist_policies += 1
        self.check_win_condition()

    def check_win_condition(self):
        if self.liberal_policies >= 5:
            print("Liberals win by enacting 5 liberal policies!")
            self.game_over = True
        elif self.fascist_policies >= 6:
            print("Fascists win by enacting 6 fascist policies!")
            self.game_over = True
        # Check if Hitler is elected Chancellor after 3 fascist policies
        if self.fascist_policies >= 3 and self.players[self.chancellor_index].role == 'Hitler':
            print("Fascists win by electing Hitler as Chancellor!")
            self.game_over = True

    def next_president(self):
        if self.special_election_president is not None:
            self.president_index = self.special_election_president
            self.special_election_president = None
        else:
            self.president_index = (self.president_index + 1) % 7
        while not self.players[self.president_index].is_alive:
            self.president_index = (self.president_index + 1) % 7

    def nominate_chancellor(self, chancellor_candidate):
        # Check if the candidate is eligible to be Chancellor
        if self.players[chancellor_candidate].is_last_chancellor or \
                self.players[chancellor_candidate].is_last_president or \
                not self.players[chancellor_candidate].is_alive:
            return False  # Candidate is not eligible
        self.chancellor_index = chancellor_candidate
        return True  # Successful nomination

    def vote_government(self):
        votes = 0
        for player in self.players:
            # In an AI implementation, this would be where the AI decides to vote Ja or Nein
            player_vote = player.vote()  # player.vote() needs to be defined in the Player class
            votes += 1 if player_vote == 'Ja' else -1

        if votes > 0:
            # Government is elected
            self.players[self.president_index].is_last_president = True
            self.players[self.chancellor_index].is_last_chancellor = True
            self.failed_government_count = 0
            return True
        else:
            # Government is not elected
            self.failed_government_count += 1
            self.next_president()
            if self.failed_government_count == 3:
                self.enact_policy(self.policy_deck.pop())
            return False

    def legislative_session(self, president, chancellor):
        drawn_policies = self.draw_policies()
        # President discards one policy
        discarded_policy = president.discard_policy(drawn_policies)
        drawn_policies.remove(discarded_policy)
        self.discarded_policies.append(discarded_policy)

        # Chancellor enacts one of the remaining policies
        enacted_policy = chancellor.choose_policy(drawn_policies)
        self.enact_policy(enacted_policy)


    def execute_presidential_power(self):
        president = self.players[self.president_index]
        power_to_execute = ["Investigate Loyalty", "Special Election", "Policy Peek", "Execution"][self.fascist_policies - 1]

        if power_to_execute == "Investigate Loyalty":
            target_player = president.choose_player_to_investigate(self.players)  # AI chooses a player to investigate
            president.investigate_player_loyalty(target_player)

        elif power_to_execute == "Special Election":
            next_president_candidate = president.choose_next_president(self.players)  # AI chooses the next Presidential candidate
            self.special_election_president = next_president_candidate.player_id

        elif power_to_execute == "Policy Peek":
            top_policies = self.policy_deck[:3]
            president.peek_at_policies(top_policies)  # AI gets to see the top 3 policies

        elif power_to_execute == "Execution":
            target_player = president.choose_player_to_execute(self.players)  # AI chooses a player to execute
            target_player.is_alive = False
            if target_player.role == 'Hitler':
                print("Hitler has been executed. Liberals win!")
                self.game_over = True

    def reset_game(self):
        self.liberal_policies = 0
        self.fascist_policies = 0
        self.election_tracker = 0
        self.policy_deck = self.create_policy_deck()
        self.discarded_policies = []
        self.president_index = random.randint(0, 6)
        self.chancellor_index = None
        self.failed_government_count = 0
        self.game_over = False
        self.special_election_president = None
        for player in self.players:
            player.is_alive = True
            player.is_last_president = False
            player.is_last_chancellor = False
