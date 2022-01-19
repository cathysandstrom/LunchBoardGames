from main.components.deck import CardDeck, PlayingCard
from main.components.user import BasePlayer
from typing import List
from enum import Enum
import random


class CribbageBoard:
    class Configuration:
        def __init__(self):
            self.max_count = 121

    def __init__(self):
        """
        Responsible for tracking score and cribbage user
        """
        self.players = {}
        self.config = CribbageBoard.Configuration()

    def set_config(self, config):
        self.config = config

    def add_player(self, name: str):
        if name in self.players.keys():
            return False
        self.players[name] = BasePlayer(name)
        return True

    def set_crib_holder(self, name: str):
        if name is None:
            name = random.choice(list(self.players.keys()))

        for player in self.players:
            # primitive way first
            self.players[player].is_active = False
        self.players[name].is_active = True

    def get_crib_holder(self):
        player_list = list(self.players.values())
        holder = None
        try:
            holder = player_list[player_list.index(True)].name
        except ValueError:
            print("no crib holder present")
        return holder

    def rotate_crib_holder(self):
        player_list = list(self.players.values())
        current_holder = player_list.index(True)
        next_holder = 0 if current_holder == len(player_list) + 1 else current_holder

        # probably not best way to do this
        self.players[player_list[current_holder].name].is_active = False
        self.players[player_list[next_holder].name].is_active = True

    def peg_user(self, name: str, difference):
        """
        Peg the board, of course. Score the points specified.
        :param name: the name of the player
        :param difference: the score change
        """
        selected = -1
        try:
            selected = self.players[name]
        except KeyError:
            print("ERROR - Failed to find user")
            return False

        selected.change_score(difference)
        return True

    def get_score(self, name: str):
        return self.players[name].score


class CribbageGame:
    class Sections(Enum):
        START = 0
        CRIB = 1
        COUNTING = 2
        SCORING = 3

    class Scoring:
        """
        Static class for evaluating scores
        """
        fifteen_score = 2

        @staticmethod
        def runs(cards: List[PlayingCard], drawn: PlayingCard):
            """
            From a given set, find all sequential subsets of length 3 or more.
            https://stackoverflow.com/questions/39102260/finding-all-sequential-subsets-from-a-large-set-with-a-particular-element

            a hand will always be 4 cards + 1 drawn card so 5 cards.
            For a hand to have a run, there needs to be three or more cards where x = x + 1
            each duplicate in the hand is a multiplier for the run
                example: {3, 4, 5H, 5D}, 6 = {3, 4, 5H, 6}[4] + {3, 4, 5D, 6}[4] = 8
            only works in sorted hand
            """
            full_set = cards.copy()
            full_set.append(drawn)
            full_set.sort(key=lambda card: PlayingCard.symbols.index(card.symbol)+1)

            mult = 1
            run = 1
            score = 0
            for i in range(1, len(full_set)):
                c1 = PlayingCard.symbols.index(full_set[i-1].symbol)+1
                c2 = PlayingCard.symbols.index(full_set[i].symbol)+1

                if c1 == c2 - 1:
                    run = run+1
                elif c1 == c2:
                    mult = mult+1
                else:
                    score = (score + (run * mult)) if run > 2 else score
                    run = 1
                    mult = 1

            score = (score + (run * mult)) if run > 2 else score

            return score

        @staticmethod
        def fifteens(cards: List[PlayingCard], drawn: PlayingCard):
            """
            From a given set, find all subsets where the sum value is equal to 15
            https://www.geeksforgeeks.org/perfect-sum-problem-print-subsets-given-sum/
            """
            full_set = cards.copy()
            full_set.append(drawn)

            total = 15
            if len(full_set) == 0:
                return 0

            dp = [None] * len(full_set)
            for i in range(len(full_set)):
                dp[i] = [False] * (total+1)
                dp[i][0] = True

            if full_set[0].value <= total:
                dp[0][full_set[0].value] = True

            for i in range(1, len(full_set)):
                for j in range(1, total + 1):
                    dp[i][j] = dp[i - 1][j] or dp[i - 1][j - full_set[i].value] \
                        if full_set[i].value <= j else dp[i - 1][j]

            if not dp[len(full_set) - 1][total]:
                return 0

            talley = 0

            def display(v: List[PlayingCard]):
                nonlocal talley
                for ii in range(len(v)):
                    print(str(v[ii].name), end=" ")
                print("")
                talley += 2

            def recurse_fifteens(ii, new_total, pp: List[PlayingCard]):
                nonlocal dp
                nonlocal full_set
                if ii == 0 and new_total != 0 and dp[0][new_total]:
                    pp.append(full_set[ii])
                    if full_set[ii].value == new_total:
                        display(pp)
                        return

                if ii == 0 and new_total == 0:
                    display(pp)
                    return

                if dp[ii - 1][new_total]:
                    b = pp.copy()
                    recurse_fifteens(ii - 1, new_total, b)

                if new_total >= full_set[ii].value and dp[ii - 1][new_total - full_set[ii].value]:
                    pp.append(full_set[ii])
                    recurse_fifteens(ii - 1, new_total - full_set[ii].value, pp)

            p = []
            recurse_fifteens(len(full_set) - 1, total, p)
            return talley

        @staticmethod
        def pairs(cards: List[PlayingCard], drawn: PlayingCard):
            """
            For a given set, find all subsets where the each element is equal
            Check to see if a value is duplicated;
            2: 2 (+2)
            3: 6 (+4)
            4: 12 (+6)
            """
            full_set = cards.copy()
            full_set.append(drawn)
            full_set.sort(key=lambda card: PlayingCard.symbols.index(card.symbol) + 1)

            repeat = 0
            score = 0
            for i in range(1, len(full_set)):
                if full_set[i-1].symbol == full_set[i].symbol:
                    repeat += 1
                    score += repeat*2
                else:
                    repeat = 0
            return score

        @staticmethod
        def flush(cards: List[PlayingCard], drawn: PlayingCard):
            """
            For a given set, find all subsets where there are 4 or more of the same type
            """
            type = cards[0].type
            for card in cards:
                if card.type != type:
                    return 0

            return 4 if drawn.type != type else 5

        @staticmethod
        def match_jack(cards: List[PlayingCard], drawn: PlayingCard):
            """
            For a given subset, get two points if one jack symbol card matches the
            type of the drawn card
            """
            for card in cards:
                if card.symbol == 'J' and card.type == drawn.type:
                    return 1
            return 0

        @staticmethod
        def flip_jack(card: PlayingCard):
            """ Get two points if a jack is flipped"""
            # TODO: replace symbol with enum
            return 2 if card.symbol == 'J' else 0

    class Configuration:
        def __init__(self):
            self.auto_evaluate = True

    class Hand:
        """
        record cards given to user and evaluate score
        """

        def __init__(self):
            self.cards = []
            self.has_drawn = False

        def set_cards(self, cards):
            old_hand = self.cards
            self.cards = cards
            return old_hand

        def evaluate_score(self, drawn: PlayingCard):
            # primitive version first
            return \
                CribbageGame.Scoring.runs(self.cards, drawn) + \
                CribbageGame.Scoring.fifteens(self.cards, drawn) + \
                CribbageGame.Scoring.pairs(self.cards, drawn) + \
                CribbageGame.Scoring.flush(self.cards, drawn) + \
                CribbageGame.Scoring.match_jack(self.cards, drawn)

        def remove_cards(self, selection: List[PlayingCard]):
            if self.has_drawn:
                return None
            self.has_drawn = True

            cards = self.cards.copy()
            self.cards = [c for c in self.cards if c not in selection]
            return [c for c in selection if c not in cards]

        def reset(self):
            self.has_drawn = False
            cards = self.cards.copy()
            self.cards.clear()
            return cards

    def __init__(self):
        self.deck = CardDeck()
        self.board = CribbageBoard()
        self.crib = CribbageGame.Hand()
        self.config = CribbageGame.Configuration()
        self.started = False
        self.players = {}
        self.section = None
        self.responses = 0

    def start_game(self):
        if len(self.players) < 2:
            return False
        self.started = True
        self.deck.shuffle()

        self.next_section(CribbageGame.Sections.START)
        return True

    def next_section(self, section):
        self.section = section
        self.responses = 0


    def end_game(self):
        pass

    def next_round(self):
        pass

    def pause(self):
        pass

    def reset_game(self):
        pass

    def add_competitor(self, name):
        if self.started or not self.board.add_player(name):
            return False
        self.player_hands[name] = CribbageGame.Hand()
        return True

    def remove_competitor(self, name: str):
        if self.started:
            self.abort_game()
            return


    def abort_game(self):
        pass

    # ----- #

    def set_auto_scoring(self, auto_evaluate):
        self.config.auto_evaluate = auto_evaluate

    def draw_for_crib(self):
        pass

    def deal_hands(self):
        pass

    def add_to_crib(self, name, selection):
        # error handling to prevent multi call?
        pass