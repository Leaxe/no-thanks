import random


def i_dont_want_cards(game, state):
    if state.moves == []:
        return None
    if state.moves == ['take']:
        return 'take'
    return 'noty'


def simple_strat(game, state):
    if state.moves == []:
        return None
    if state.moves == ['take']:
        return 'take'

    board = state.board

    # sequential card
    if any([abs(hand_card - board.card) == 1 for hand_card in board.hands[state.to_move].cards]):
        return 'take'

    # lots of counters
    if board.counters * 2 > board.card:
        return 'take'

    return 'noty'


def medium_strat(game, state):
    if state.moves == []:
        return None
    if state.moves == ['take']:
        return 'take'

    def lotta_counters(card, counters, mult=1):
        # true if the value of the counters alone makes it worth taking
        return counters * 2 * mult > card

    def sequential(card, hand):
        return any([abs(hand_card - card) == 1 for hand_card in hand])

    board = state.board
    deal_card = board.card
    deal_counters = board.counters
    my_hand = board.hands[state.to_move].cards
    my_counters = board.hands[state.to_move].counters
    opp_hands = set().union(*map(lambda x: x.cards, board.hands))
    deck_possibilities = set(range(3, 36)) - opp_hands
    ave_card_in_deck = sum(deck_possibilities)/len(deck_possibilities)

    # streak connection
    if any([hand_card - deal_card == 1 and deal_card - 1 in my_hand for hand_card in my_hand]):
        # print('streak: ', my_hand, deal_card)
        return 'take'

    # sequential card
    if sequential(deal_card, my_hand):
        # take it if someone else wants it
        if sequential(deal_card, opp_hands):
            return 'take'
        # take it if its worth a bit
        if lotta_counters(deal_card, deal_counters, 2):
            return 'take'

    if lotta_counters(deal_card, deal_counters):
        # print('lotta counters')
        return 'take'

    return 'noty'


def random_player_weighted(game, state):
    actions = game.actions(state)
    if not actions:
        return None
    if len(actions) == 1:
        return random.choice(actions)
    else:
        return random.choices(actions, weights=[5, 1])


def query_player_custom(game, state):
    """Make a move by querying standard input."""
    board = state.board
    print(game.print(state))
    print("available moves: {}".format(game.actions(state)))
    print("")
    move = None
    while True:
        if game.actions(state):
            move_string = input('Your move? [(t)ake or (n)oty]: ')
            try:
                move = move_string  # was eval here
            except NameError:
                move = move_string
            if move == 't':
                move = 'take'
            if move == 'n':
                move = 'noty'
        else:
            print('no legal moves: passing turn to next player')
        if move in game.actions(state):
            print('\n------------------\n')
            break
        else:
            print('invalid move')
    return move
