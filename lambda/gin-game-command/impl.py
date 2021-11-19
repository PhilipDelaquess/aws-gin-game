import dynamo
from card import findMeldings

def setStates (player, playerState, opponent, opponentState):
    player['state'] = playerState
    player['opponentState'] = opponentState
    opponent['state'] = opponentState
    opponent['opponentState'] = playerState

def takeFromPack (player, opponent, game):
    # TODO - if pack is empty, shuffle all but the top discard and recycle
    card = game['deck'].pop()
    cards = player['hand']['cards']
    cards.append(card)
    player['hand']['meldings'] = findMeldings(cards)
    player['lastDraw'] = card
    player['fromDiscard'] = False
    opponent['opponentLastDraw'] = None
    size = len(game['deck'])
    player['packSize'] = size
    opponent['packSize'] = size

def drawDiscard (table, player, opponent, game, card):
    discards = game['discard']
    card = discards.pop()
    cards = player['hand']['cards']
    cards.append(card)
    player['hand']['meldings'] = findMeldings(cards)
    player['lastDraw'] = card
    player['fromDiscard'] = True
    opponent['opponentLastDraw'] = card
    top = discards[-1] if len(discards) > 0 else None
    player['topDiscard'] = top
    opponent['topDiscard'] = top
    setStates(player, 'DISCARD_OR_KNOCK', opponent, 'AWAITING_OPPONENT_ACTION')
    dynamo.put_item(table, player)
    dynamo.put_item(table, opponent)
    dynamo.put_item(table, game)
    return player

def poneReject (table, player, opponent, game, card):
    setStates(player, 'AWAITING_OPPONENT_ACTION', opponent, 'DEALER_INITIAL_DRAW')
    dynamo.put_item(table, player)
    dynamo.put_item(table, opponent)
    return player

def dealerReject (table, player, opponent, game, card):
    takeFromPack(opponent, player, game)
    setStates(player, 'AWAITING_OPPONENT_ACTION', opponent, 'DISCARD_OR_KNOCK')
    dynamo.put_item(table, player)
    dynamo.put_item(table, opponent)
    dynamo.put_item(table, game)
    return player

def discard (table, player, opponent, game, card):
    cards = player['hand']['cards']
    cards.remove(card)
    player['hand']['meldings'] = findMeldings(cards)
    player['lastDraw'] = None
    game['discard'].append(card)
    player['topDiscard'] = card
    opponent['topDiscard'] = card
    setStates(player, 'AWAITING_OPPONENT_ACTION', opponent, 'NORMAL_DRAW')
    dynamo.put_item(table, player)
    dynamo.put_item(table, opponent)
    dynamo.put_item(table, game)
    return player

def knock (table, player, opponent, game, card):
    cards = player['hand']['cards']
    cards.remove(card)
    player['hand']['meldings'] = findMeldings(cards)
    player['lastDraw'] = None
    summary = {
        'knockerId': player['id'],
        'gin': False,
        'undercut': False
    }
    player['summary'] = summary
    opponent['summary'] = summary

    playerMelding = player['hand']['meldings'][0]
    summary['knockerMelding'] = playerMelding
    pmScore = playerMelding['score']

    opponentMelding = opponent['hand']['meldings'][0]
    summary['otherMelding'] = opponentMelding
    omScore = opponentMelding['score']

    playerScore = 0
    opponentScore = 0
    if pmScore < omScore:
        playerScore = omScore - pmScore
        if pmScore == 0:
            playerScore += 25
            summary['gin'] = True
        summary['score'] = playerScore
    else:
        opponentScore = pmScore - omScore + 25
        summary['undercut'] = True
        summary['score'] = opponentScore

    player['score'] += playerScore
    player['opponentScore'] += opponentScore
    opponent['score'] += opponentScore
    opponent['opponentScore'] += playerScore

    setStates(player, 'ACKNOWLEDGE_DEAL', opponent, 'ACKNOWLEDGE_DEAL')
    dynamo.put_item(table, player)
    dynamo.put_item(table, opponent)
    return player

def drawPack (table, player, opponent, game, card):
    takeFromPack(player, opponent, game)
    setStates(player, 'DISCARD_OR_KNOCK', opponent, 'AWAITING_OPPONENT_ACTION')
    dynamo.put_item(table, player)
    dynamo.put_item(table, opponent)
    dynamo.put_item(table, game)
    return player

def acknowledge (table, player, opponent, game, card):
    return player

_dispatcher = {
    'PONE_INITIAL_DRAW': {
        'DRAW_DISCARD': drawDiscard,
        'REJECT_INITIAL': poneReject
    },
    'DEALER_INITIAL_DRAW': {
        'DRAW_DISCARD': drawDiscard,
        'REJECT_INITIAL': dealerReject
    },
    'DISCARD_OR_KNOCK': {
        'DISCARD': discard,
        'KNOCK': knock
    },
    'NORMAL_DRAW': {
        'DRAW_PACK': drawPack,
        'DRAW_DISCARD': drawDiscard
    },
    'ACKNOWLEDGE_DEAL': {
        'ACKNOWLEDGE': acknowledge
    }
}

def performCommand (playerId, command, card):
    table = dynamo.get_table()
    player = dynamo.get_item(table, playerId)
    opponent = dynamo.get_item(table, player['opponentId'])
    game = dynamo.get_item(table, player['gameId'])

    return _dispatcher[player['state']][command](table, player, opponent, game, card)
