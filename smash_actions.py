"""

smash_actions.py

The file for defining different actions and interactions.

"""

from enum import Enum

# Classifies messages into different types
class ActionType(Enum):
    ATTACK = 1
    SHIELD = 3
    GRAB = 2


class Action:
    """
    A general class for player actions
    """

    def __init__(self, text: str, action_type: ActionType, cost: int,
                gain: int, bonus: int, loss: int,
                damage: int, crit: int, thresh: int) -> None:
        self.text = text
        self.action_type = action_type
        self.cost = cost
        self.gain = gain
        self.bonus = bonus
        self.loss = loss
        self.damage = damage
        self.crit_damage = crit
        self.kill_threshold = thresh


class Attack(Action):
    """
    A class used to represent standard attack actions
    """

    def __init__(self):
        self.text = "attacked"
        self.action_type = ActionType.ATTACK
        self.cost = 0
        self.gain = 2
        self.bonus = 3
        self.loss = 1
        self.damage = 15
        self.crit_damage = 25
        self.kill_threshold = 120


class Smash(Action):
    """
    A class used to represent Smash Attack actions
    """

    def __init__(self):
        self.text = "Smash Attacked"
        self.action_type = ActionType.ATTACK
        self.cost = 3
        self.gain = 4
        self.bonus = 5
        self.loss = 1
        self.damage = 30
        self.crit_damage = 40
        self.kill_threshold = 80


class Shield(Action):
    """
    A class used to represent shield actions
    """

    def __init__(self):
        self.text = "put up their shield"
        self.action_type = ActionType.SHIELD
        self.cost = 0
        self.gain = 0
        self.bonus = 4
        self.loss = 0
        self.damage = 0
        self.crit_damage = 0
        self.kill_threshold = 1000


class Parry(Action):
    """
    A class used to represent parry actions
    """

    def __init__(self):
        self.text = "is parrying"
        self.action_type = ActionType.SHIELD
        self.cost = 3
        self.gain = 0
        self.bonus = 7
        self.loss = 0
        self.damage = 0
        self.crit_damage = 0
        self.kill_threshold = 1000


class Grab(Action):
    """
    A class used to represent grab actions
    """

    def __init__(self):
        self.text = "grabbed"
        self.action_type = ActionType.GRAB
        self.cost = 0
        self.gain = 4
        self.bonus = 6
        self.loss = 3
        self.damage = 5
        self.crit_damage = 10
        self.kill_threshold = 1000


class Throw(Action):
    """
    A class used to represent throw actions
    """

    def __init__(self):
        self.text = "threw"
        self.action_type = ActionType.GRAB
        self.cost = 3
        self.gain = 7
        self.bonus = 11
        self.loss = 3
        self.damage = 5
        self.crit_damage = 10
        self.kill_threshold = 100

