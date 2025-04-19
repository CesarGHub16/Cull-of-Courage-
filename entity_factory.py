from entity import Entity

# PLAYER #
player = Entity(char=chr(0x40), color=(242, 242, 242), name="Player", block_movement=True)

# ENEMIES #
swordmen = Entity(char=chr(0x263B), color=(197, 15, 31), name="Swordmen", block_movement=True)
cultist = Entity(char=chr(0x263A), color=(136, 23, 152), name="Cultist", block_movement=True)