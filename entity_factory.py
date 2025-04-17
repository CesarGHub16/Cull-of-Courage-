from entity import Entity

player = Entity(char="@", color=(255, 255, 255), name="Player", block_movement=True)

# ENEMIES #
pikeman = Entity(char="P", color=(36, 119, 135), name="Pikemen", block_movement=True)
longsword = Entity(char="L", color=(219, 136, 120), name="Longsword", block_movement=True)