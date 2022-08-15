from wizAPI import *
import time
import math
player = wizAPI().register_window()

while True:
    if player.low_mana():
        print('using potion')
        player.click(170, 300, delay=.2)
    player.wait(.2)