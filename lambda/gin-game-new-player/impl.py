import uuid
import card
import dynamo

def makePlayerWaitForOpponent (table, player):
    player['state'] = 'AWAITING_OPPONENT_ARRIVAL'
    dynamo.put_item(table, player)

    pendingGame = {
        'id': 'PendingGame',
        'playerId': player['id']
    }
    dynamo.put_item(table, pendingGame)

def startGameWithPlayer (table, pendingGame, player):
    deck = card.shuffledDeck()
    myCards = deck[0:10]
    hisCards = deck[10:20]
    topCard = deck[20]
    deck = deck[21:]

    gameId = str(uuid.uuid4())
    game = {
        'id': gameId,
        'deck': deck,
        'discard': [topCard]
    }

    opponent = dynamo.get_item(table, pendingGame['playerId'])
    opponent['gameId'] = gameId
    opponent['state'] = 'AWAITING_OPPONENT_ACTION'
    opponent['score'] = 0
    opponent['packSize'] = 31
    opponent['topDiscard'] = topCard
    opponent['hand'] = {
        'cards': hisCards,
        'meldings': card.findMeldings(hisCards)
    }
    opponent['opponentName'] = player['name']
    opponent['opponentId'] = player['id']
    opponent['opponentState'] = 'PONE_INITIAL_DRAW'
    opponent['opponentScore'] = 0

    player['gameId'] = gameId
    player['state'] = 'PONE_INITIAL_DRAW'
    player['score'] = 0
    player['packSize'] = 31
    player['topDiscard'] = topCard
    player['hand'] = {
        'cards': myCards,
        'meldings': card.findMeldings(myCards)
    }
    player['opponentName'] = opponent['name']
    player['opponentId'] = opponent['id']
    player['opponentState'] = 'AWAITING_OPPONENT_ACTION'
    player['opponentScore'] = 0

    dynamo.put_item(table, player)
    dynamo.put_item(table, opponent)
    dynamo.put_item(table, game)
    table.delete_item(Key={'id': 'PendingGame'})

def createNewPlayer (playerName):
    playerId = str(uuid.uuid4())
    player = {
        'id': playerId,
        'name': playerName
    }

    table = dynamo.get_table()
    pendingGame = dynamo.get_item(table, 'PendingGame', failIfMissing=False)
    if pendingGame == None:
        makePlayerWaitForOpponent(table, player)
    else:
        startGameWithPlayer(table, pendingGame, player)

    return player
