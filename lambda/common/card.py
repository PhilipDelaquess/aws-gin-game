import random

_suits = 'CDHS'
_faces = ['10' if f == 'T' else f for f in 'A23456789TJQK']
_ordinals = {k:v+1 for k,v in zip(_faces, range(13))}
_scores = {k:10 if v > 8 else v + 1 for k,v in zip(_faces, range(13))}

def shuffledDeck ():
    deck = [f + s for f in _faces for s in _suits]
    random.shuffle(deck)
    return deck

def suit (card):
    return card[-1:]

def ordinal (card):
    return _ordinals[card[:-1]]

def score (card):
    return _scores[card[:-1]]

def sortedByFace (cards):
    return sorted(cards, key=ordinal)

def sortedBySuit (cards):
    return sorted(sorted(cards, key=ordinal), key=suit)

def findSuitMelds (cards, melds):
    i = 0
    sortedCards = sortedBySuit(cards)
    while i < len(sortedCards):
        crdz = [sortedCards[i]]
        s = suit(sortedCards[i])
        o = ordinal(sortedCards[i])
        j = i + 1
        while j < len(sortedCards) and suit(sortedCards[j]) == s and ordinal(sortedCards[j]) == o + 1:
            crdz.append(sortedCards[j])
            o = o + 1
            j = j + 1
        if len(crdz) >= 3:
            melds.append(crdz)
        i = j

def findFaceMelds (cards, melds):
    i = 0
    sortedCards = sortedByFace(cards)
    while i < len(sortedCards):
        crdz = [sortedCards[i]]
        o = ordinal(sortedCards[i])
        j = i + 1
        while j < len(sortedCards) and ordinal(sortedCards[j]) == o:
            crdz.append(sortedCards[j])
            j = j + 1
        if len(crdz) >= 3:
            melds.append(crdz)
        i = j

def makeMelding (melds, deadwood):
    dwScore = sum([score(c) for c in deadwood])
    return {
        'melds': [{'cards': m, 'key': ''.join(m)} for m in melds],
        'deadwood': deadwood,
        'score': dwScore,
        'knockables': [c for c in deadwood if dwScore - score(c) <= 10] # empty unless 11?
    }

def _findMeldingsAux (cards, melds, meldings):
    # find all possible melds regardless of overlap
    localMelds = []
    findSuitMelds(cards, localMelds)
    findFaceMelds(cards, localMelds)

    # map each card to a list of the melds containing it
    meldsPerCard = {c : [] for c in cards}
    for m in localMelds:
        for c in m:
            meldsPerCard[c].append(m)

    # bad cards, or badz, are those belonging to more than one meld
    badz = [c for c in cards if len(meldsPerCard[c]) > 1]

    # clean melds have no bad cards; dirty melds have at least one
    cleanMelds = []
    dirtyMelds = []
    for m in localMelds:
        dirty = False
        for c in m:
            if c in badz:
                dirty = True
        if dirty:
            dirtyMelds.append(m)
        else:
            cleanMelds.append(m)

    # add clean melds to output, and remove their cards from consideration
    for m in cleanMelds:
        for c in m:
            cards.remove(c)
        melds.append(m)

    if len(dirtyMelds) == 0:
        # recursion bottoms out - emit a melding
        meldings.append(makeMelding(melds, sorted(cards, key=ordinal)))
    else:
        # pick the first bad card and recurse on each of its candidate melds
        bad = badz[0]
        for m in meldsPerCard[bad]:
            melds2 = melds[:]
            melds2.append(m)
            cards2 = cards[:]
            for c in m:
                cards2.remove(c)
            _findMeldingsAux(cards2, melds2, meldings)

def findMeldings (cards):
    crdz = cards[:]
    melds = []
    meldings = []
    _findMeldingsAux(crdz, melds, meldings)
    meldings.sort(key=lambda m : m['score'])
    return meldings
