init python:
    import json
    class Card:
        def __init__(self, data):
            self.text = data['text']
            self.type = data['type']
    class Opportunity(Card):
        def __init__(self, data):
            Card.__init__(self, data)
            self.increase = data['increase']
    class Danger(Card):
        def __init__(self, data):
            Card.__init__(self, data)
            self.chance = data['chance']
    testFile = renpy.file('test.txt')
    cards = json.load(testFile)
    opportunityList = []
    dangerList = []
    for card in cards:
        if card['type'] == 'opportunity':
            opportunityList.append(Opportunity(card))
        elif card['type'] == 'danger':
            dangerList.append(Danger(card))

label start:
    python:
        def drawFromList(list):
            rnd = renpy.random.randint(0, len(list) - 1)
            return list[rnd]
        opportunity = drawFromList(opportunityList)
        danger = drawFromList(dangerList)
    call runOpportunity(opportunity)
    call runDanger(danger)
    return

label runOpportunity(opportunity):
    python:
        renpy.say(None, opportunity.increase)
    return
    
label runDanger(danger):
    python:
        renpy.say(None, danger.chance)
    return
