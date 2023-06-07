import copy


def sequential(card, hand_cards):
    return any([abs(hand_card - card) == 1 for hand_card in hand_cards])


def connection(card, hand_cards):
    any([hand_card - card == 1 and card - 1 in hand_cards for hand_card in hand_cards])


def new_hand_value(card, counters, hand):
    new_hand = set().union(hand.cards, {card})
    total = 0
    previous = 0
    for card in sorted(new_hand):
        if card > previous + 1:
            total += card
        previous = card

    total -= counters
    return total


def calc_deck_value(cards, counters, hand):
    values = [new_hand_value(card, counters, hand) for card in cards]
    return sum(values)/len(values)


def calc_min_opp_deck_value(cards, hands):
    return min([calc_deck_value(cards, hand.counters, hand) - hand.value() for hand in hands])


# def min_ave_opp_value_change(cards, counters, hands):
#     return min([calc_deck_value(cards, counters, hand) - hand.value() for hand in hands])


def calc_min_opp_value(opp_hands):
    return min([hand.value for hand in opp_hands])


# def min_new_opp_value(card, counters, opp_hands):
#     return min([new_hand_value(card, counters+i+1, hand.cards) for i, hand in enumerate(opp_hands)])


# def value_change(card, counters, hand):
#     return new_hand_value(card, counters, hand) - hand.value()


# def min_opp_value_change(card, counters, opp_hands):
#   # counters+i+1 since counters get added
#     return min([value_change(card, counters+i+1, hand.cards) for i, hand in enumerate(opp_hands)])


def strategic(game, state):
    if state.moves == []:
        return None
    if state.moves == ['take']:
        return 'take'

    board = copy.deepcopy(state.board)
    deal_card = board.card
    deal_counters = board.counters
    deck_count = board.deck.count()
    hands = board.hands
    all_cards = set().union(*map(lambda x: x.cards, hands))
    deck_possibilities = set(range(3, 36)) - all_cards
    ave_card_in_deck = sum(deck_possibilities)/len(deck_possibilities)

    my_hand = hands[state.to_move]
    my_cards = my_hand.cards
    my_counters = my_hand.counters
    my_value = my_hand.value()

    opp_hands = hands[state.to_move:] + board.hands[:state.to_move]
    opp_hands.remove(0)
    opp_cards = set().union(*map(lambda x: x.cards, opp_hands))

    # streak connection
    if connection(deal_card, my_cards):
        # print('streak: ', my_hand, deal_card)
        return 'take'

    min_opp_value = calc_min_opp_value(opp_hands)
    new_my_value = new_hand_value(deal_card, deal_counters, my_hand)
    my_value_change = new_my_value - my_value
    my_deck_value = calc_deck_value(
        deck_possibilities, my_counters, my_hand) - my_value
    min_opp_deck_value = calc_min_opp_deck_value(deck_possibilities, opp_hands)
    # last card
    if deck_count == 0:
        # take if wins game
        if new_my_value < min_opp_value:
            return 'take'
        return 'noty'

    # second to last
    if deck_count == 1:
        # if last card likely worse for me, get enough counters
        if my_deck_value > min_opp_deck_value:
            # if this card will give me more counters than anyone else
            max_opp_counters = max([hand.counters for hand in opp_hands])
            if my_counters + deal_counters > max_opp_counters:
                if

        return 'noty'

    return 'noty'
