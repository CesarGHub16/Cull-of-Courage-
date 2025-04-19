from components.ai import HostileEnemy
from components.fighter import Fighter
from entity import Actor


# PLAYER #
player = Actor(
    char=chr(0x263B),
    color=(242, 242, 242),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=100, armor=30, magicresist=27, attackdamage=50, attackpower=0),
)

# ENEMIES #)
swordman = Actor(
    char=chr(0x53),
    color=(59, 120, 255),
    name="Swordman",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=75, armor=24, magicresist=22, attackdamage=42, attackpower=0),
)
ranger = Actor(
    char=chr(0x52),
    color=(22, 198, 12),
    name="Ranger",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=55, armor=24, magicresist=24, attackdamage=44, attackpower=0),
)