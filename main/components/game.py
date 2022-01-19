from abc import ABC, abstractmethod


class BaseGame(ABC):
    @abstractmethod
    def start_game(self):
        pass

    @abstractmethod
    def end_game(self):
        pass

    @abstractmethod
    def next_round(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def reset_game(self):
        pass

    @abstractmethod
    def add_competitor(self, name: str):
        pass

    @abstractmethod
    def remove_competitor(self, name: str):
        pass

    @abstractmethod
    def abort_game(self):
        pass
