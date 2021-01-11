"""
Contains skilling-related functions.

"""

import logging as log
import startup
import vision
import misc
import behaviour
import input    

def cut(trees, wood):
    """
    A woodcutting function.

    Args:
        trees (list): A list containing an arbitrary number of 2-tuples.
                       Each tuple must contain two filepaths:
                       The first filepath must be a needle of the
                       tree in its "full" state. The second filepath
                       must be a needle of the same tree in its "empty"
                       state.
        wood (file): Filepath to a needle of the item icon of the wood
                    being mined, as it appears in the player's
                    inventory.
    """
    # Make sure inventory is selected.
    
    behaviour.open_side_stone('inventory')

    for tries in range(100):

        # Confirm player is in the correct tree spot. This is also
        #   used to re-adjust the player if a mis-click moves the player
        #   out of position.

        for tree_needle in trees:
            # Unpack each tuple in the rocks[] list to obtain the "full"
            #   and "empty" versions of each ore.
            (full_tree_needle, empty_tree_needle) = tree_needle

            log.debug('Searching for tree %s...', tries)

            # If current tree is full, begin cutting it.
            # Move the mouse away from the tree so it doesn't interfere with matching the needle.
            tree_full = vision.Vision(ltwh=vision.game_screen, loop_num=1, needle=full_tree_needle, conf=0.8) \
                .click_image(sleep_range=(0, 100, 0, 100,), move_duration_range=(0, 500), move_away=True)
            if tree_full is True:
                log.info('Waiting for wooductting to startup.')

                # Small chance to do nothing for a short while.
                misc.wait_rand(chance=100, wait_min=10000, wait_max=40000)

                # Once the tree has been clicked on, wait for woodcutting to startup by monitoring chat.
                woodcutting_started = vision.Vision(ltwh=vision.chat_menu_recent, loop_num=5, conf=0.9,
                                            needle='./needles/chat-menu/woodcutting-started.png',
                                            loop_sleep_range=(100, 200)).wait_for_image()

                # If wooductting hasn't started after looping has finished, check to see if the inventory is full.
                if woodcutting_started is False:
                    log.debug('Timed out waiting for woodcutting to startup.')

                    inv_full = vision.Vision(ltwh=vision.chat_menu, loop_num=1,
                                          needle='./needles/chat-menu/woodcutting-inventory-full.png').wait_for_image()

                    # If the inventory is full, empty the ore and
                    #   return.
                    if inv_full is True:
                        log.info('Inventory is full.')
                        wood_dropped = behaviour.drop_item(item=wood)
                        if wood_dropped is False:
                            behaviour.logout()
                            # This runtime error will occur if the
                            #   player's inventory is full, but they
                            #   don't have any ore to drop.
                            raise RuntimeError("Could not find ore to drop!")

                        # Iterate through the other items that could
                        #   be dropped. If any of them is true, drop that item.
                        # The for loop is iterating over a tuple of tuples.
                        # for item in (drop_sapphire, drop_emerald, drop_ruby,
                        #              drop_diamond, drop_clue_geode):
                        # Unpack the tuple
                        (drop_item, path) = item
                        if drop_item is True:
                            behaviour.drop_item(item=str(path), track=False)

                        elapsed_time = misc.run_duration(human_readable=True)
                        log.info('Script has been running for %s (HH:MM:SS)',
                                 elapsed_time)
                        return
                    return

                log.info('Woodcutting started.')

                # Wait until the rock is empty by waiting for the "empty" version of the rock_needle tuple.
                tree_empty = vision.Vision(ltwh=vision.game_screen, loop_num=35,
                                        conf=0.85, needle=empty_tree_needle,
                                        loop_sleep_range=(100, 200)).wait_for_image()
                                        # loop_sleep_range=(300, 400)).wait_for_image()

                if tree_empty is True:
                    log.info('Tree is empty.')
                    log.debug('%s empty.', tree_needle)
                    behaviour.human_behavior_rand(chance=100)
                else:
                    log.info('Timed out waiting for woodcutting to finish.')
    return True

def fdrop_wood(wood):
    """
    Drops ore and optionally gems in inventory.

    Returns:

    """
    # Iterate through the other items that could be dropped. If any of them is true, drop that item.
    # The for loop is iterating over a tuple of tuples.
    wood_dropped = behaviour.drop_item(item=wood)
    
    # Iterate through the other items that could be dropped. If any of them is true, drop that item.
    # The for loop is iterating over a tuple of tuples.
    for item in (drop_sapphire, drop_emerald, drop_ruby,
                 drop_diamond, drop_clue_geode):
        # Unpack the tuple
        (drop_item, path) = item
        if drop_item is True:
            behaviour.drop_item(item=str(path), track=False)
            return True

def woocutter(scenario):
    """
    Script for mining in a variety of locations, based on preset
    "scenarios".

    Supported scenarios:

        'varrock-east-trees-regular' = Cuts normal trees near Varrock East Bank.

        'varrock-east-oak' = Cuts normal trees near Varrock East Bank.

        See "/docs/client-configuration/" for the required client
        configuration settings for each scenario.

    Args:
        scenario (str): The scenario to use. See above for supported
                        scenario types.

    Raises:
        Raises an exception if an unsupported scenario is passed.

    """
    while True:
        # Ensure the client is logged in.
        client_status = vision.orient()
        if client_status[0] == 'logged_out':
            behaviour.login_full()

        if scenario == 'varrock-east-trees-regular':
            skills.cut(trees=[('./needles/game-screen/varrock-east-trees/east-regular-full.png',
                                './needles/game-screen/varrock-east-trees/east-regular-empty.png'),
                               ('./needles/game-screen/varrock-east-trees/south-regular-full.png',
                                './needles/game-screen/varrock-east-trees/south-regular-empty.png')],
                        wood='./needles/items/normal-log.png')

        elif scenario == 'varrock-east-trees-oak':
            skills.cut(trees=[('./needles/game-screen/varrock-east-trees/east-oak-full.png',
                                './needles/game-screen/varrock-east-trees/east-oak-empty.png'),
                               ('./needles/game-screen/varrock-east-trees/west-oak-full.png',
                                './needles/game-screen/varrock-east-trees/west-oak-empty.png')],
                        wood='./needles/items/oak-log.png')

        else:
            raise Exception('Scenario not supported!')

        # Roll for randomized actions when the script returns.
        behaviour.logout_break_range()

def mine(rocks, ore, ore_type, drop_ore):
    """
    A mining function.

    This function alternates mining among the rocks that were provided
    (it can mine one rock, two rocks, or many rocks at once).
    All rocks must be of the same ore type. All mined ore, gems, and
    clue geodes are dropped by default when the inventory is full.

    Args:
        rocks (list): A list containing an arbitrary number of 2-tuples.
                       Each tuple must contain two filepaths:
                       The first filepath must be a needle of the
                       rock in its "full" state. The second filepath
                       must be a needle of the same rock in its "empty"
                       state.
        ore (file): Filepath to a needle of the item icon of the ore
                    being mined, as it appears in the player's
                    inventory.
        ore_type (str): The type of ore being mined, used for generating
                        stats. Available options are: "copper", "iron"
        drop_ore (bool): Whether to drop the ore or bank it. Setting
                         this to 'False' only works for Varrock East
                         bank.

    Raises:
        Raises a runtime error if the player's inventory is full but
        the function can't find any ore in the player's inventory to
        drop.

    """
    gems = ['./needles/items/uncut-sapphire.png',
            './needles/items/uncut-emerald.png',
            './needles/items/uncut-ruby.png',
            './needles/items/uncut-diamond.png',
            './needles/items/clue-geode.png']

    # Vision objects have to be imported within functions because the
    #   init_vision() function has to run before the objects get valid
    #   values.

    # TODO: count the number of items in the inventory to make sure
    #   the function never receives an "inventory is already full" message

    # TODO: refactor a mine_rock() function out of this one.

    # Make sure inventory is selected.
    behaviour.open_side_stone('inventory')

    for tries in range(100):

        # Confirm player is in the correct mining spot. This is also
        #   used to re-adjust the player if a mis-click moves the player
        #   out of position.
        # Applies to Varrock East mine only.
        behaviour.travel([((240, 399), 1, (4, 4), (5, 10))], './haystacks/varrock-east-mine.png')

        for rock_needle in rocks:
            # Unpack each tuple in the rocks[] list to obtain the "full"
            #   and "empty" versions of each ore.
            (full_rock_needle, empty_rock_needle) = rock_needle

            log.debug('Searching for ore %s...', tries)

            # If current rock is full, begin mining it.
            # Move the mouse away from the rock so it doesn't
            #   interfere with matching the needle.
            rock_full = vision.Vision(ltwh=vision.game_screen, loop_num=1, needle=full_rock_needle, conf=0.8) \
                .click_image(sleep_range=(0, 100, 0, 100,), move_duration_range=(0, 500), move_away=True)
            if rock_full is True:
                log.info('Waiting for mining to startup.')

                # Small chance to do nothing for a short while.
                misc.wait_rand(chance=100, wait_min=10000, wait_max=60000)

                # Once the rock has been clicked on, wait for mining to
                #   startup by monitoring chat.
                mining_started = vision.Vision(ltwh=vision.chat_menu_recent, loop_num=5, conf=0.9,
                                            needle='./needles/chat-menu/mining-started.png',
                                            loop_sleep_range=(100, 200)).wait_for_image()

                # If mining hasn't started after looping has finished,
                #   check to see if the inventory is full.
                if mining_started is False:
                    log.debug('Timed out waiting for mining to startup.')

                    inv_full = vision.Vision(ltwh=vision.chat_menu, loop_num=1,
                                          needle='./needles/chat-menu/'
                                                 'mining-inventory-full.png').wait_for_image()

                    # If the inventory is full, empty the ore and
                    #   return.
                    if inv_full is True:
                        log.info('Inventory is full.')
                        if drop_ore is True:
                            fdrop_ore(ore)
                        else:
                            behaviour.open_side_stone('inventory')
                            # Bank from mining spot.
                            behaviour.travel([((253, 181), 5, (35, 35), (1, 6)),
                                            ((112, 158), 5, (20, 20), (1, 6)),
                                            ((108, 194), 1, (10, 4), (3, 8))],
                                            './haystacks/varrock-east-mine.png')
                            behaviour.open_bank('south')
                            vision.Vision(ltwh=vision.inv, needle=ore).click_image()
                            for gem in gems:
                                vision.Vision(ltwh=vision.inv, needle=gem, loop_num=1).click_image()
                            misc.sleep_rand(500, 3000)
                            # Mining spot from bank.
                            behaviour.travel([((240, 161), 5, (35, 35), (1, 6)),
                                            ((262, 365), 5, (25, 25), (1, 6)),
                                            ((240, 399), 1, (4, 4), (3, 8))],
                                            './haystacks/varrock-east-mine.png')
                            misc.sleep_rand(300, 800)
                        elapsed_time = misc.session_duration(human_readable=True)
                        log.info('Script has been running for %s (HH:MM:SS)',
                                 elapsed_time)
                        return True
                    return True

                log.info('Mining started.')

                # Wait until the rock is empty by waiting for the
                #   "empty" version of the rock_needle tuple.
                rock_empty = vision.Vision(ltwh=vision.game_screen, loop_num=35,
                                        conf=0.85, needle=empty_rock_needle,
                                        loop_sleep_range=(100, 200)).wait_for_image()

                if rock_empty is True:
                    log.info('Rock is empty.')
                    log.debug('%s empty.', rock_needle)
                    behaviour.human_behavior_rand(chance=100)
                else:
                    log.info('Timed out waiting for mining to finish.')
    return True

def fdrop_ore(ore):
    """
    Drops ore and optionally gems in inventory.

    Returns:

    """

    # Create tuples of whether or not to drop the item and the item's path.
    drop_sapphire = (startup.config.get('mining', 'drop_sapphire'), './needles/items/uncut-sapphire.png')
    drop_emerald = (startup.config.get('mining', 'drop_emerald'), './needles/items/uncut-emerald.png')
    drop_ruby = (startup.config.get('mining', 'drop_ruby'), './needles/items/uncut-ruby.png')
    drop_diamond = (startup.config.get('mining', 'drop_diamond'), './needles/items/uncut-diamond.png')
    drop_clue_geode = (startup.config.get('mining', 'drop_clue_geode'), './needles/items/clue-geode.png')
    ore_dropped = behaviour.drop_item(item=ore)
    if ore_dropped is False:
        behaviour.logout()
        # This runtime error will occur if the
        #   player's inventory is full, but they
        #   don't have any ore to drop.
        raise RuntimeError("Could not find ore to drop!")

    # Iterate through the other items that could
    #   be dropped. If any of them is true, drop that item.
    # The for loop is iterating over a tuple of tuples.
    for item in (drop_sapphire, drop_emerald, drop_ruby,
                 drop_diamond, drop_clue_geode):
        # Unpack the tuple
        (drop_item, path) = item
        if drop_item is True:
            behaviour.drop_item(item=str(path), track=False)
            return True