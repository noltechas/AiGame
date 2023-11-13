import random

from Player import Player


class SecretHitlerGame:
    def __init__(self):
        self.players = self.initialize_players()
        self.liberal_policies = 0
        self.fascist_policies = 0
        self.election_tracker = 0
        self.policy_deck = self.create_policy_deck()
        self.current_president_index = 0
        self.failed_elections = 0

    def initialize_players(self):
        roles = ['Hitler', 'Fascist', 'Fascist', 'Liberal', 'Liberal', 'Liberal', 'Liberal']
        random.shuffle(roles)
        return [Player(i, roles[i]) for i in range(7)]

    def create_policy_deck(self):
        return random.shuffle(['Liberal'] * 6 + ['Fascist'] * 11)

    def next_president(self):
        self.current_president_index = (self.current_president_index + 1) % 7
        while not self.players[self.current_president_index].is_alive:
            self.current_president_index = (self.current_president_index + 1) % 7
        return self.players[self.current_president_index]

    def nominate_chancellor(self, president):
        eligible = [p for p in self.players if p.is_alive and not p.is_last_president and not p.is_last_chancellor]
        return random.choice(eligible)  # In an actual game, this would be chosen by the current president

    def vote(self):
        # Simplified voting, assuming random votes
        votes = ['Ja' if random.choice([True, False]) else 'Nein' for _ in self.players]
        return votes.count('Ja') > votes.count('Nein')

    def legislative_session(self, president, chancellor):
        hand = [self.policy_deck.pop() for _ in range(3)]
        # President discards one policy
        president_discard = random.choice(hand)
        hand.remove(president_discard)

        # Chancellor chooses policy to enact
        enacted_policy = random.choice(hand)
        self.execute_policy(enacted_policy)
        return enacted_policy

    def execute_policy(self, policy):
        if policy == 'Liberal':
            self.liberal_policies += 1
        elif policy == 'Fascist':
            self.fascist_policies += 1

    def check_win_condition(self):
        if self.liberal_policies == 5:
            return "Liberals Win"
        elif self.fascist_policies == 6:
            return "Fascists Win"
        elif any(p.role == 'Hitler' and p.is_last_chancellor for p in self.players if self.fascist_policies >= 3):
            return "Fascists Win"
        return None

    def play_round(self):
        president = self.next_president()
        chancellor = self.nominate_chancellor(president)
        if self.vote():
            policy = self.legislative_session(president, chancellor)
            print(f"Policy enacted: {policy}")
        else:
            self.failed_elections += 1
            if self.failed_elections == 3:
                top_policy = self.policy_deck.pop()
                self.execute_policy(top_policy)
                self.failed_elections = 0

    def play_game(self):
        while self.check_win_condition() is None:
            self.play_round()
        return self.check_win_condition()
