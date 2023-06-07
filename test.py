from nothanks import *


def test_rand_order(trials):
    players = [random_player_weighted, simple_strat,
               medium_strat, good_strat1, good_strat]
    player_names = [x.__name__ for x in players]
    tally = {x: 0 for x in player_names}

    for i in range(trials):
        print('Game', i)
        gam = NoThanks(len(players))
        random.shuffle(players)
        # print('order', str(players))
        score = gam.play_game(*players)
        # score = gam.play_game(random_player_weighted,
        #                       random_player_weighted, random_player_weighted)
        if len(score) == 1:
            winner = players[score[0]].__name__
            tally[winner] += 1
        else:
            winners = [players[x].__name__ for x in score]
            tally = {
                k: v + 1/len(score) if k in winners else v for (k, v) in tally.items()}

    print('Final tally: ', tally)


def test_fixed_order(trials):
    players = [simple_strat, griefing, good_strat]
    player_names = [x.__name__ for x in players]
    tally = {x: 0 for x in player_names}

    for i in range(trials):
        print('Game', i)
        gam = NoThanks(3)
        score = gam.play_game(*players)
        if len(score) == 1:
            winner = players[score[0]].__name__
            tally[winner] += 1
        else:
            winners = [players[x].__name__ for x in score]
            tally = {
                k: v + 1/len(score) if k in winners else v for (k, v) in tally.items()}

    print('Final tally: ', tally)


def good_luck():
    players = [query_player_custom, good_strat, good_grief]
    gam = NoThanks(3)
    score = gam.play_game(*players)


test_rand_order(10000)
