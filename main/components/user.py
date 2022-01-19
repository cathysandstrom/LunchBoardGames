from abc import ABC


class BasePlayer(ABC):
    def __init__(self, name: str):
        self._name = name
        self._score = 0
        self._active = False

    @property
    def is_active(self):
        return self._active

    @is_active.setter
    def is_active(self, active):
        self._active = active

    @property
    def name(self):
        return self._name

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    def change_score(self, difference):
        self._score = self.score + difference

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score

    def __le__(self, other):
        return self.score <= other.score

    def __ge__(self, other):
        return self.score >= other.score

    def __eq__(self, other):
        if isinstance(other, BasePlayer):
            return self.score == other.score
        if isinstance(other, str):
            return self._name == other
        if isinstance(other, bool):
            return self._active == other
        return False
