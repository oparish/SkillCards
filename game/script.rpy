init python:
    import json
    from _enum import Enum
    SKILL = Enum('Skill','FIGHTING STEALTH')
    RESOURCE = Enum('Resource','MONEY ENERGY')
    DICETYPE = 10
    INIT_SKILL = 0
    INIT_RESOURCE = 100
    LOCATIONS = []
    class Location:
       def __init__(self, data):
            self.opportunityList = []
            self.dangerList = []
            self.trialList = []
            self.name = data['name']
            self.x = data['x']
            self.y = data['y']
            for card in data['cards']:
                if card['type'] == 'opportunity':
                    self.opportunityList.append(Opportunity(card))
                elif card['type'] == 'danger':
                    self.dangerList.append(Danger(card))
                elif card['type'] == 'trial':
                    self.trialList.append(Trial(card))
    class CharacterData:
       def __init__(self, data):
            self.skills = {}
            self.resources = {}
            for skill in SKILL:
                self.skills[skill] = INIT_SKILL
            for resource in RESOURCE:
                self.resources[resource] = INIT_RESOURCE
    class Card:
        def __init__(self, data):
            self.text = data['text']
            self.type = data['type']
    class Opportunity(Card):
        def __init__(self, data):
            Card.__init__(self, data)
            self.skill = SKILL[data['skill']]
            self.amount = data['amount']
            self.resource = RESOURCE[data['resource']]
            self.reward = loadReward(data['reward'])
    class Danger(Card):
        def __init__(self, data):
            Card.__init__(self, data)
            self.difficulty = data['difficulty']
            self.skill = SKILL[data['skill']]
            self.reward = loadReward(data['reward'])
            self.loss = loadLoss(data['loss'])
    class Trial(Card):
        def __init__(self, data):
            Card.__init__(self, data)
                self.difficulty = data['difficulty']
                self.skill = SKILL[data['skill']]
    class Reward():
        def __init__(self, data):
            self.text = data['text']
    class ResourceReward(Reward):
        def __init__(self, data):
            Reward.__init__(self, data)
            self.resource = RESOURCE[data['resource']]
            self.amount = data['amount']
    class Loss():
        def __init__(self, data):
            self.text = data['text']
    class ResourceLoss(Loss):
        def __init__(self, data):
            Loss.__init__(self, data)
            self.resource = RESOURCE[data['resource']]
            self.amount = data['amount']
    def drawFromList(list):
        rnd = renpy.random.randint(0, len(list) - 1)
        return list[rnd]
    def loadLocations():
        testFile = renpy.file('test.txt')
        locationData = json.load(testFile)
        for location in locationData:
            LOCATIONS.append(Location(location))
    def loadReward(data):
        if data['type'] == 'resourceReward':
            reward = ResourceReward(data)
        return reward
    def loadLoss(data):
        if data['type'] == 'resourceLoss':
            loss = ResourceLoss(data)
        return loss
    def gainReward(characterData, reward):
        renpy.say(None, reward.text)
        if isinstance(reward, ResourceReward):
            gainResourceReward(characterData, reward)
        return reward
    def gainResourceReward(characterData, reward):
        adjustResource(characterData, reward.resource,reward.amount)
    def takeLoss(characterData, loss):
        renpy.say(None, loss.text)
        if isinstance(loss, ResourceLoss):
            takeResourceLoss(characterData, loss)
        return loss
    def takeResourceLoss(characterData, loss):
        adjustResource(characterData, loss.resource, -loss.amount)
    def adjustResource(characterData, resource, amount):
        characterData.resources[resource] += amount
        renpy.say(None, resource.name + " changed by " + str(amount))
    def tryChallenge(characterData, skill, difficulty):
        result = characterData.skills[skill] + renpy.random.randint(0, DICETYPE)
        return result >= difficulty     
    loadLocations()

label start:
    call screen locationMap(LOCATIONS)
    return

label tryLocation(character, location):
    python:
        opportunity = drawFromList(location.opportunityList)
        danger = drawFromList(location.dangerList)
    call runOpportunity(opportunity, character)
    call runDanger(danger, character)
    return

label runOpportunity(opportunity, characterData):
    python:
        renpy.say(None, opportunity.text)
        result = renpy.display_menu([("Spend " + str(opportunity.amount) + " " + opportunity.resource.name.lower() + "?", None),("Yes", True),("No", False)])
        if result:
            adjustResource(characterData, opportunity.resource,-opportunity.amount)
            gainReward(characterData, opportunity.reward)
    return
    
label runDanger(danger, characterData):
    python:
        renpy.say(None, danger.text)
        result = tryChallenge(characterData, danger.skill, danger.difficulty)
        if result:
            gainReward(characterData, danger.reward)
        else:
            takeLoss(characterData, danger.loss)
    return

