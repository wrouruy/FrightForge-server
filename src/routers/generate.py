import random

adjective_ideas = ['scary', 'terrible', 'ugly', 'sleeping', 'evil', 'furios', 'angry', 'sinister', 'mad']
creature_ideas  = ['hedgehog', 'wolf', 'scarecrow', 'crow', 'witch', 'bat', 'spider', 'pie']
accessory_ideas = ['broomstick', 'earring', 'ring', 'mask','wings', 'hat' ]

async def generate():
    return {
        "adjective": random.choice(adjective_ideas),
        "creature": random.choice(creature_ideas),
        "accessory": random.choice(accessory_ideas)
    }