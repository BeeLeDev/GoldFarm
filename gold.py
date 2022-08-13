from wizAPI import *
import time
import math
player = wizAPI().register_window()

""" loading screen, needs fix when page loads too fast"""
def await_finished_loading(self):
    print('loading')
    while player.is_GH_loading():
        player.wait(.2)
    print('done')
    while not player.is_idle():
        player.wait(.5)


def print_separator(*args):
    sides = '+'*16
    _str = " ".join([sides, " ".join(args), sides])
    l = len(_str)
    print('='*l)
    print(_str)
    print('='*l)


def print_time(timer):
    minutes = math.floor(timer/60)
    seconds = math.floor(timer % 60)
    print('Round lasted {} minutes and {} seconds.'.format(minutes, seconds))

#where the bot starts
ROUND_COUNT = 0
while True:
    ROUND_COUNT += 1
    START_TIME = time.time()
    print_separator('ROUND', str(ROUND_COUNT))

    """ Attempt to enter the dungeon """

    player.press_key('x')

    #wait for dungeon to load
    player.wait(14)

    #if we are still in loading screen, wait
    #is_idle based on pink pet icon
    #pink pet icon wouldnt be there if on loading screen
    while not player.is_idle():
        player.wait(1)

    #go into battle after loading is done
    #i assume loading takes longer than 14 seconds, is.idle returns false which skips this, then waits for turn before going into battle
    while player.is_idle():
        print('moving')
        player.hold_key('w', 2)
        print('should now be in battle')

    print('waiting for turn to play')
    player.wait_for_turn_to_play()
    print('is turn to play')
    

    inFight = not player.is_idle()
    while inFight:
        if player.enchant('dk', 'epic') or player.find_spell('dk-enchanted') or player.find_spell('dk-enchanted2'):
            player.cast_spell('dk-enchanted') or player.cast_spell('dk-enchanted2')
        #else if player.enchant('khru', 'epic') or player.find_spell('khru-enchanted'):
        #    player.cast_spell('khru-enchanted'):
        else:
            #dk dot should kill in 2 turns if crit didnt work
            player.pass_turn()

        player.wait_for_end_of_round()

        #determines whether fight is over
        if player.is_idle():
            inFight = False

    print_time(time.time() - START_TIME)
    #in case game gests dumb and tries to move before fight is over
    player.wait(1)
    #get out of the dungeon
    player.hold_key('a', .55)
    player.hold_key('w', 2) 

    #apparently when the game loads too fast this doesnt work
    #await_finished_loading(player)
    player.wait(4.5)

    #waiut for animation after finish loading
    #player.wait(.75)



    #go to the exit, by going to where the arrow is pointed and going forward