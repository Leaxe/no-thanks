import copy
import random
import types
import numpy as np
from collections import namedtuple

from players import *

GameState = namedtuple('GameState', 'to_move, utility, board, moves')


class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def winner(self, state):
        raise NotImplementedError

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                cur_move = state.to_move
                while state.to_move == cur_move:
                    move = player(self, state)
                    state = self.result(state, move)
                    if self.terminal_test(state):
                        self.display(state)
                        return self.winner(state)
                        '''return self.utility(state, self.to_move(self.initial))'''


class Hand(object):
    def __init__(self, cards=None, counters=11):
        if cards is None:
            cards = set()
        self.cards = cards

        self.counters = counters

    def __repr__(self):
        return 'Cards: ' + str(self.cards) + \
               '\nCounters: ' + str(self.counters) + \
               '\nValue: ' + str(self.value()) + '\n'

    def print(self):
        return str(self.cards) if self.cards != set() else '{}'

    def value(self):
        total = 0
        previous = 0
        for card in sorted(self.cards):
            if card > previous + 1:
                total += card
            previous = card

        total -= self.counters
        return total

    def take(self, card, counters):
        self.cards.add(card)
        self.counters += counters

    def noty(self):
        self.counters -= 1


class Deck:
    def __init__(self, deck=None):
        if deck is None:
            deck = random.sample(range(3, 36), 24)
        self.deck = deck

    def __repr__(self):
        return str(self.count()) + ' cards: ' + str(self.deck)

    # def __copy__(self):
    #     cls = type(self)()
    #     cls.__dict__.update(self.__dict__)

    def count(self):
        return len(self.deck)

    def draw(self):
        return self.deck.pop(0)


class NoThanks(Game):
    def __init__(self, players, deck=None, card=0, counters=0):
        if deck is None:
            deck = Deck()
        self.deck = deck
        self.card = self.deck.draw() if not card else card
        self.counters = counters
        self.hands = [Hand() for i in range(players)]
        board = types.SimpleNamespace(
            deck=self.deck, card=self.card, counters=self.counters, hands=self.hands)
        moves = ['take', 'noty']
        self.initial = GameState(to_move=0, utility=self.hands[0].value(),
                                 board=board, moves=moves)

    def actions(self, state):
        return self.compute_actions(state.board, state.to_move)

    def result(self, state, move):
        board = copy.deepcopy(state.board)
        to_move = state.to_move
        if move == 'take':
            board.hands[state.to_move].take(board.card, board.counters)
            if board.deck.count():
                board.card = self.draw(board)
            else:
                board.card = 0
        else:
            board.hands[state.to_move].noty()
            board.counters += 1
            to_move = (state.to_move + 1) % len(self.hands)
        moves = self.compute_actions(board, to_move)
        return GameState(to_move, utility=self.compute_utility(board, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        return self.compute_utility(state.board, player)

    def terminal_test(self, state):
        return not state.board.card

    def compute_actions(self, board, to_move):
        # if not board.deck.count() + 1:
        #     return []
        if board.hands[to_move].counters == 0:
            return ['take']
        return ['take', 'noty']

    def compute_utility(self, board, player):
        return board.hands[player].value()

    def draw(self, board):
        board.counters = 0
        return board.deck.draw()

    def printHands(self):
        s = ''
        for i, hand in enumerate(self.hands):
            s += 'Player ' + str(i) + ':\n' + str(hand) + '\n'
        return s

    def printHandsOther(self, hands, to_move, you=True, counters=False, value=False):
        s = ''
        if you:
            s += 'You: ' + str(hands[to_move].print()) + '\n'
            s += '   counters: ' + str(hands[to_move].counters) + '\n'
            s += '   value: ' + str(hands[to_move].value()) + '\n'
        for i, hand in enumerate(hands):
            if i == to_move and you:
                continue
            s += 'Player ' + str(i) + ': ' + str(hand.print()) + '\n'
            if counters:
                s += '   counters: ' + str(hand.counters) + '\n'
            if value:
                s += '   value: ' + str(hand.value()) + '\n'
        return s

    def print(self, state):
        board = state.board
        return '\nCards left: ' + str(board.deck.count()) + \
            '\n   Drawn card: ' + str(board.card) + \
            '\n   Counters: ' + str(board.counters) + \
            '\n\nHands: \n' + self.printHandsOther(board.hands, state.to_move, counters=True, value=True) + \
            '\n'

    def display(self, state):
        prnt = True
        if prnt:
            board = state.board
            to_move = (state.to_move - 1) % len(board.hands)
            print('Hands: \n' + self.printHandsOther(board.hands,
                                                     to_move, False, True))
            s = ''
            # s += 'You: ' + str(board.hands[to_move].value()) + '\n'
            for i, hand in enumerate(board.hands):
                # if i == to_move:
                #     continue
                s += 'Player ' + str(i) + ': ' + str(hand.value()) + '\n'
            print('Final score:\n' + s)
            win = self.winner(state)
            if len(win) == 1:
                print('WINNER: PLAYER ' + str(win[0]))
            else:
                print('TIE BETWEEN PLAYERS ' + str(win))
            print('\n----------\n')

    def winner(self, state):
        values = list(map(lambda hand: hand.value(), state.board.hands))
        m = min(values)
        return [i for i, val in enumerate(values) if val == m]

    def __repr__(self):
        return str(Deck()) + \
            '\nDrawn card: ' + str(self.card) + \
            '\nCounters: ' + str(self.counters) + \
            '\nHands: \n' + self.printHands() + \
            '\n'
