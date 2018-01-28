init python:
    import json
    from _enum import Enum
    SKILL = Enum('Skill','FIGHTING STEALTH')
    RESOURCE = Enum('Resource','MONEY ENERGY')
    DICETYPE = 10
    INIT_SKILL = 0
    INIT_RESOURCE = 100
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
    class Reward():
        def __init__(self, data):
            self.text = data['text']
    class ResourceReward(Reward):
        def __init__(self, data):
            Reward.__init__(self, data)
            self.resource = RESOURCE[data['resource']]
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
    def gainReward(characterData, reward):
        if isinstance(reward, ResourceReward):
            gainResourceReward(characterData, reward)
        return reward
    def gainResourceReward(characterData, reward):
        adjustResource(characterData, reward.resource,reward.amount)
    def adjustResource(characterData, resource, amount):
        characterData.resources[resource] += amount
        renpy.say(None, resource.name + " changed by " + str(amount))
    def tryChallenge(characterData, skill, difficulty):
        result = characterData.skills[skill] + renpy.random.randint(0, DICETYPE)
        return result >= difficulty
    opportunityList = []
    dangerList = []
    loadCards()

label start:
    python:
        opportunity = drawFromList(opportunityList)
        danger = drawFromList(dangerList)
        mainCharacter = CharacterData({})
    call runOpportunity(opportunity, mainCharacter)
    call runDanger(danger, mainCharacter)
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
            gainReward(characterData, opportunity.reward)  
    return

