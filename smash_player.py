"""

smash_player.py

The file for defining players and their interactions.

"""

from enum import Enum

from smash_actions import Action, ActionType, Attack, Smash, Shield, Parry, Grab, Throw

class PlayerStatus(Enum):
    SHIELDING = 3
    GRABBING = 2
    GRABBED = 1
    NORMAL = 0


class Player:
    """
    A class used to represent a player
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.points = 10
        self.damage = 0
        self.action = None
        self.target = None
        self.status = PlayerStatus.NORMAL
        self.KOs = 0
        self.falls = 0

    def chooseAction(self, action: str, target: str):
        if (action == "attack"):
            self.action = Attack()
            self.target = target
        elif(action == "smash"):
            self.action = Smash()
            self.target = target
        elif(action == "shield"):
            self.action = Shield()
            self.target = self
            self.status = PlayerStatus.SHIELDING
        elif(action == "parry"):
            self.action = Parry()
            self.target = self
            self.status = PlayerStatus.SHIELDING
        elif(action == "grab"):
            self.action = Grab()
            self.target = target
        elif(action == "throw"):
            self.action = Throw()
            self.target = target
        else:
            self.action = None
            self.target = None
            self.status = PlayerStatus.NORMAL

    def increasePoints(self, amount: int) -> None:
        self.points = self.points + amount

    def decreasePoints(self, amount: int) -> None:
        self.points = self.points - amount
        if self.points < 0:
            self.points = 0

    def takeDamage(self, damage: int) -> None:
        self.damage = self.damage + damage

    def KO(self) -> None:
        self.decreasePoints(6)
        self.damage = 0


def resetPlayers(player_list: list[Player]) -> None:
    for player in player_list:
        player.action = None
        player.target = None
        player.status = PlayerStatus.NORMAL


def processAction(player: Player, target: Player) -> None:
    offense = player.action
    defense = target.action

    print(player.name + " " + offense.text + " " + target.name)

    
    if (offense.action_type == ActionType.SHIELD):
        player.status = PlayerStatus.SHIELDING
        player.decreasePoints(offense.cost)
            
    elif (player.status != PlayerStatus.GRABBED):
        player_pts = 0
        target_pts = 0
        target_dmg = 0
        player_sts = "gained"
        target_sts = "lost"

        player.decreasePoints(offense.cost)

        if (offense.action_type == ActionType.ATTACK):
            if (target.status == PlayerStatus.SHIELDING):
                player_sts = "lost"
                player_pts = offense.loss
                target_sts = "gained"
                target_pts = defense.bonus

                print('Attack shielded!')
            
            elif (defense.action_type == ActionType.GRAB and
                  target.status != PlayerStatus.GRABBED):
                player_pts = offense.bonus
                target_dmg = offense.crit_damage
                target_pts = defense.loss

                print("Critical hit!")

            else:
                player_pts = offense.gain
                target_dmg = offense.damage

        elif (offense.action_type == ActionType.GRAB):
            if (target.status != PlayerStatus.GRABBING and
                target.status != PlayerStatus.GRABBED):
                if (defense.action_type == ActionType.ATTACK):
                    player_sts = "lost"
                    player_pts = offense.loss
                    
                    print("Grab repelled!")

                else:                    
                    if (target.status == PlayerStatus.SHIELDING):
                        player_pts = offense.bonus
                        target_dmg = offense.crit_damage
                        target_pts = defense.loss

                        print("Critical grab!")

                    else:
                        player_pts = offense.gain
                        target_dmg = offense.damage
                        target_pts = defense.loss

                    player.status = PlayerStatus.GRABBING
                    target.status = PlayerStatus.GRABBED

            else:
                print("Grab failed!")

        if(player_sts == "lost"):
            player.decreasePoints(player_pts)
        else:
            player.increasePoints(player_pts)

        if(target_sts == "gained"):
            target.increasePoints(target_pts)
        else:
            target.decreasePoints(target_pts)

        target.takeDamage(target_dmg)

        if(offense.action_type != ActionType.SHIELD):
            print(f'{player.name} {player_sts} {player_pts} points')
            print(f'{target.name} {target_sts} {target_pts} points')
            print(f'{target.name} took {target_dmg} damage')

        if (target_dmg > 0 and target.damage >= (offense.kill_threshold + target_dmg)):
            target.KO()
            player.increasePoints(12)
            player.KOs = player.KOs + 1
            target.falls = target.falls + 1
            print(f'{target.name} was KO\'d!')

    else:
        print(f'{player.name} is grabbed! No action')




if __name__ == "__main__":
    import random

    random.seed()

    action_list = [Attack(), Smash(), Shield(), Parry(), Grab(), Throw()]

    player_list = []

    NUM_PLAYERS = 4
    for i in range(NUM_PLAYERS):
        player_list.append(Player("Player " + str(i)))

    action_count = {Attack: 0, Smash: 0, Shield: 0, Parry: 0, Grab: 0, Throw: 0}

    for i in range(30):
        print(f'Turn {i+1}')
        resetPlayers(player_list)

        shield_list = []
        grab_list = []
        attack_list = []

        for player in player_list:
            player.target = player.name
            
            while player.target == player.name:
                player.target = random.choices(player_list, weights=(10, 15, 30, 60), k=1)[0].name
            
            # player.action = action_list[random.randint(0,5)]
            player.action = random.choices(action_list, weights=(50,20,30,10,30,10), k=1)[0]

            if (player.action.action_type == ActionType.SHIELD):
                shield_list.append(player)
            elif (player.action.action_type == ActionType.GRAB):
                grab_list.append(player)
            elif (player.action.action_type == ActionType.ATTACK):
                attack_list.append(player)

            print(f'{player.name} will {player.action.text} {player.target}')

            action_count[type(player.action)] = action_count[type(player.action)] + 1



        print()
        action_queue = shield_list + grab_list + attack_list

        for player in action_queue:
            target = next((target for target in player_list if target.name == player.target), None)
            processAction(player, target)
            print()

        player_list.sort(key=lambda x: x.points)

        for player in player_list:
            print(f'{player.name}: {player.damage}% | {player.points} Pts. | {player.KOs - player.falls}')
        
        print()

    for action in action_count:
        print(action, action_count[action])
