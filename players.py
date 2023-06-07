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


def good_strat(game, state):
    if state.moves == []:
        return None
    if state.moves == ['take']:
        return 'take'

    def counter_value(card, counters, my_counters, deck_count, mult=1):
        # true if the value of the counters alone makes it worth taking
        if not counters:
            # print('dont take without counters')
            return False
        # print(card, counters, card/counters, 100/(deck_count + 45))
        # mult * card / counters < 100/(deck_count + 45)+1
        x = 23 - deck_count
        c = 0.05/(my_counters - 0.7) + 1
        val = mult * card / counters
        if x < 18:
            # print('1', val, c, x, 100 * c / (x + 45) + 1)
            take = val < 100 * c / (x + 45) + 1
        else:
            # print('2', card, counters, my_counters,
            #       x, 1.8 * c / (x - 25) + 1.8 * c + 1)
            take = val < 1.8 * c / (x - 25) + 1.8 * c + 1
        # if take:
        #     print(card, counters, my_counters, deck_count)
        return take

    def sequential(card, hand):
        return any([abs(hand_card - card) == 1 for hand_card in hand])

    board = state.board
    deal_card = board.card
    deal_counters = board.counters
    my_hand = board.hands[state.to_move].cards
    my_counters = board.hands[state.to_move].counters
    opp_hands = set().union(*map(lambda x: x.cards, board.hands))
    deck_possibilities = set(range(3, 36)) - opp_hands
    deck_count = board.deck.count()
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
        if counter_value(deal_card, deal_counters, my_counters, deck_count, 2):
            return 'take'

    if counter_value(deal_card, deal_counters, my_counters, deck_count):
        # print('lotta counters')
        return 'take'

    return 'noty'


def cheat_strat(game, state):
    if state.moves == []:
        return None
    if state.moves == ['take']:
        return 'take'

    def counter_value(card, counters, deck_count, mult=1):
        # true if the value of the counters alone makes it worth taking
        if not counters:
            return False
        # print(card, counters, card/counters, 100/(deck_count + 45))
        return mult * card / counters < 100/(deck_count + 45)+1

    def sequential(card, hand):
        return any([abs(hand_card - card) == 1 for hand_card in hand])

    board = state.board
    deal_card = board.card
    deal_counters = board.counters
    my_hand = board.hands[state.to_move].cards
    my_counters = board.hands[state.to_move].counters
    opp_hands = set().union(*map(lambda x: x.cards, board.hands))
    deck_possibilities = set(range(3, 36)) - opp_hands
    deck_count = board.deck.count()
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
        # take if someone will be forced to take
        if 0 in [x.counters for x in opp_hands]:
            return 'take'

        # take it if its worth a bit
        if counter_value(deal_card, deal_counters, deck_count, 2):
            return 'take'
        # leave if

    if counter_value(deal_card, deal_counters, deck_count):
        # print('lotta counters')
        return 'take'

    return 'noty'


def good_strat1(game, state):
    if state.moves == []:
        return None
    if state.moves == ['take']:
        return 'take'

    def counter_value(card, counters, deck_count, mult=1):
        # true if the value of the counters alone makes it worth taking
        if not counters:
            return False
        # print(card, counters, card/counters, 100/(deck_count + 45))
        return mult * card / counters < 100/(deck_count + 45)+1

    def sequential(card, hand):
        return any([abs(hand_card - card) == 1 for hand_card in hand])

    board = state.board
    deal_card = board.card
    deal_counters = board.counters
    my_hand = board.hands[state.to_move].cards
    my_counters = board.hands[state.to_move].counters
    opp_hands = set().union(*map(lambda x: x.cards, board.hands))
    deck_possibilities = set(range(3, 36)) - opp_hands
    deck_count = board.deck.count()
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
        if counter_value(deal_card, deal_counters, deck_count, 2):
            return 'take'

    if counter_value(deal_card, deal_counters, deck_count):
        # print('lotta counters')
        return 'take'

    return 'noty'


def griefing(game, state):
    if state.moves == []:
        return None
    if state.moves == ['take']:
        return 'take'

    board = state.board
    opp_hands = board.hands[(state.to_move + 1) % len(board.hands)].cards

    def sequential(card, hand):
        return any([abs(hand_card - card) == 1 for hand_card in hand])

    # sequential card
    if sequential(board.card, board.hands[state.to_move].cards):
        return 'take'

    # opponent sequential card
    if sequential(board.card, opp_hands):
        return 'take'

    return 'noty'


def good_grief(game, state):
    if state.moves == []:
        return None
    if state.moves == ['take']:
        return 'take'

    board = state.board
    board = state.board
    deal_card = board.card
    deal_counters = board.counters
    my_hand = board.hands[state.to_move].cards
    my_counters = board.hands[state.to_move].counters
    target_hand = board.hands[(state.to_move + 1) % len(board.hands)].cards
    friend_hand = set().union(*map(lambda x: x.cards, board.hands))

    def sequential(card, hand):
        return any([abs(hand_card - card) == 1 for hand_card in hand])

    def lotta_counters(card, counters, mult=1):
        # true if the value of the counters alone makes it worth taking
        return counters * 2 * mult > card

    # sequential card
    if sequential(board.card, board.hands[state.to_move].cards):
        return 'take'

    # opponent sequential card
    if sequential(board.card, target_hand):
        return 'take'

    # streak connection
    if any([hand_card - deal_card == 1 and deal_card - 1 in my_hand for hand_card in my_hand]):
        # print('streak: ', my_hand, deal_card)
        return 'take'

    # sequential card
    if sequential(deal_card, my_hand):
        # take it if target else wants it
        if sequential(deal_card, target_hand):
            return 'take'
        if sequential(deal_card, friend_hand):
            return 'noty'
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
