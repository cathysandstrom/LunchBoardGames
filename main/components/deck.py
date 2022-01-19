from abc import ABC, abstractmethod
import random


class Card(ABC):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    @abstractmethod
    def compare(self, card):
        return self.value - card.value

    def __cmp__(self, other):
        return self.name == other.name and self.value == other.value

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.name == other.name and self.value == other.value
        return False

    def __str__(self):
        return self.name


class PlayingCard(Card):
    values = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10)
    symbols = ('A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K')
    types = ('H', 'C', 'D', 'S')

    def __init__(self, tp, sym, value=None):
        self.type = tp
        self.symbol = sym
        value = value if value is not None else PlayingCard.values[PlayingCard.symbols.index(sym)]
        super(PlayingCard, self).__init__(str(sym) + tp, value)

    def get_type(self):
        return self.type

    def compare(self, card):
        return (
            self.type == card.type,
            self.value - card.value
        )


class Deck(ABC):
    """
    Generic class for managing a deck of cards <any type>
    (Rename to or separate from UniqueDeck?)
    """

    def __init__(self, stack, max_count=None):
        self.stack = stack
        self.max_count = len(stack) if max_count is None else max_count
        pass

    @abstractmethod
    def remove_cards(self, cards):
        '''
        Remove the listed cards from the deck.

        :param cards: the list of cards to remove
        :return: the cards that were removed
        '''
        stack = self.stack
        self.stack = [x for x in stack if x not in cards]
        return [x for x in cards if x not in self.stack]

    @abstractmethod
    def add_cards(self, cards):
        '''
        Add the listed cards to the deck

        :param cards: the list of cards to add
        :return: the cards that were not added.
        '''
        non_duplicates = [x for x in cards if x not in self.stack]
        count = (self.max_count - len(self.stack))

        appending = non_duplicates[:count] if count < len(cards) else non_duplicates
        self.stack = self.stack + appending
        return [c for c in cards if c not in appending]

    def shuffle(self):
        random.shuffle(self.stack)

    def push_end(self, cards):
        return self.add_cards(cards)

    def pop_end(self, count):
        if count > len(self.stack):
            return []

        return self.remove_cards(self.stack[-count:])

    def random_draw(self, count):
        count = count - (count - len(self.stack)) if count > len(self.stack) else count
        return self.remove_cards(random.sample(self.stack, count))

    def random_insert(self, cards):
        # primitive way first
        inserted = []  # ;)
        for card in cards:
            if card not in self.stack and len(self.stack) < self.max_count:
                self.stack.insert(card, random.randrange(0, self.max_count-1))
                inserted.append(card)  # ._.
        return inserted

    def peak(self):
        return self.stack[-1:]

    def draw_cards(self, count):
        return self.pop_end(count)


class CardDeck(Deck):
    """
    A normal deck of cards
    (Rename or inherit from UniqueDeck - all cards must be unique?)
    """

    def __init__(self, ace_high=False):
        self.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        if ace_high:
            self.values[0] = 11
        stack = []
        for type in PlayingCard.types:
            for symbol in PlayingCard.symbols:
                stack.append(PlayingCard(
                    type,
                    symbol,
                    self.values[PlayingCard.symbols.index(symbol)]
                ))
        super().__init__(stack)

    def add_cards(self, cards):
        return super().add_cards(cards)

    def remove_cards(self, cards):
        return super().remove_cards(cards)

# TO ADD: Other deck types (non-unique)
