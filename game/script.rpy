init python:
    import json
    from _enum import Enum
    Skill = Enum('Skill','FIGHTING STEALTH')
    Resource = Enum('Resource','MONEY ENERGY')
    class Card:
        def __init__(self, data):
            self.text = data['text']
            self.type = data['type']
    class Opportunity(Card):
        def __init__(self, data):
            Card.__init__(self, data)
            self.skill = Skill[data['skill']]
            self.amount = data['amount']
            self.resource = Resource[data['resource']]
            self.reward = loadReward(data['reward'])
    class Danger(Card):
        def __init__(self, data):
            Card.__init__(self, data)
            self.chance = data['chance']
    class Reward():
        def __init__(self, data):
            self.text = data['text']
    class ResourceReward(Reward):
        def __init__(self, data):
            Reward.__init__(self, data)
            self.resource = Resource[data['resource']]
            self.amount = data['amount']
    def drawFromList(list):
        rnd = renpy.random.randint(0, len(list) - 1)
        return list[rnd]
    def loadCards():
        testFile = renpy.file('test.txt')
        cards = json.load(testFile)
        for card in cards:
            if card['type'] == 'opportunity':
                opportunityList.append(Opportunity(card))
            elif card['type'] == 'danger':
                dangerList.append(Danger(card))
    def loadReward(data):
        if data['type'] == 'resourceReward':
            reward = ResourceReward(data)
        return reward
    def gainReward(reward):
        if isinstance(reward, ResourceReward):
            gainResourceReward(reward)
        return reward
    def gainResourceReward(reward):
        adjustResource(reward.resource,reward.amount)
    def adjustResource(resource, amount):
        resources[resource] += amount
        renpy.say(None, resource.name + " changed by " + str(amount))
    skills = {}
    for skill in Skill:
        skills[skill] = 0
    resources = {}
    for resource in Resource:
        resources[resource] = 100
    opportunityList = []
    dangerList = []
    loadCards()

label start:
    python:
        opportunity = drawFromList(opportunityList)
        danger = drawFromList(dangerList)
    call runOpportunity(opportunity)
    call runDanger(danger)
    return

label runOpportunity(opportunity):
    python:
        renpy.say(None, opportunity.text)
        result = renpy.display_menu([("Spend " + str(opportunity.amount) + " " + opportunity.resource.name.lower() + "?", None),("Yes", True),("No", False)])
        if result:
            adjustResource(opportunity.resource,-opportunity.amount)
            gainReward(opportunity.reward)
    return
    
label runDanger(danger):
    python:
        renpy.say(None, danger.chance)
    return

