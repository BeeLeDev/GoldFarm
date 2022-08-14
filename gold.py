from wizAPI import *
import time
import math
player = wizAPI().register_window()

""" loading screen, needs fix when page loads too fast"""
def await_finished_loading(self):
    print('loading')
    while player.is_GH_loading():
        player.wait(.2)
    while not player.is_idle():
        player.wait(.5)
    print("finished loading")

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
    print("entering dungeon")
    player.press_key('x')

    #temporary timer for loading screen when exiting dungeon, in place of await_finished_loading()
    #player.wait(14)

    #dungeon timer start
    print("timer start")
    #extra 1 second added as i am taking walking time to spot position into consideration
    player.wait(11)
    await_finished_loading(player)

    #player randomly skipped the moving after loading, placing a timer to see if it was due to the bot working too quickly
    player.wait(1)

    #if we are still in loading screen, wait
    #is_idle based on pink pet icon
    #pink pet icon wouldn't be there if you are on the loading screen
    while not player.is_idle():
        print("waiting to move")
        player.wait(1)

    #go into battle after loading is done
    while player.is_idle():
        print('moving')
        player.hold_key('w', 3)
        print('should now be in battle')

    #wait for turn once in battle
    print("waiting for turn")
    player.wait_for_turn_to_play()
    print("player turn")

    #enchants and select card
    #AOE cards only, bot doesn't pick a target
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

    #in case game gets dumb and tries to move before fight is over
    #this is usually where a bug happens as when the battle is over, is_idle can see the pink pet icon and returns that you are idle, it will then try to move... the problem is even when the pink pet icon appears, it does not mean you can move exactly yet, so a timer is placed to 'hopefully' fix that issue
    player.wait(2.5)
    #get out of the dungeon
    print('exiting dungeon')

    #temporary rotation in place of face_arrow()
    #player.hold_key('a', .55)
    player.face_arrow()
    player.hold_key('w', 3) 
    player.wait(1.5)
    print("dungeon exited")

    await_finished_loading(player)

    #temporary timer for loading screen when exiting dungeon, in place of await_finished_loading()
    #player.wait(4.5)