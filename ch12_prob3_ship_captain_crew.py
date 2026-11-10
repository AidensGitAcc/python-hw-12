# Chapter 12, Problem 3 — Ship, Captain, and Crew Dice Game

import random

class Die:

    def __init__(self):
        self.value = 0
        self.held = False

    def roll(self):
        if not self.held:
            self.value = random.randint(1, 6)
        return self.value

    def hold(self):
        self.held = True

    def isHeld(self):
        return self.held

    def reset(self):
        self.value = 0
        self.held = False


class DiceHand:

    def __init__(self, numDice):
        self.dice = []
        i = 0
        while i < numDice:
            self.dice.append(Die())
            i = i + 1

    def rollAll(self):
        i = 0
        while i < len(self.dice):
            self.dice[i].roll()
            i = i + 1

    def resetAll(self):
        i = 0
        while i < len(self.dice):
            self.dice[i].reset()
            i = i + 1

    def getValues(self):
        values = []
        i = 0
        while i < len(self.dice):
            values.append(self.dice[i].value)
            i = i + 1
        return values


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = DiceHand(5)
        self.hasShip = False
        self.hasCaptain = False
        self.hasCrew = False
        self.score = 0

    def resetForTurn(self):
        self.hand.resetAll()
        self.hasShip = False
        self.hasCaptain = False
        self.hasCrew = False
        self.score = 0

    def holdMatches(self, targetValue):
        dice = self.hand.dice
        i = 0
        found = False
        while i < len(dice) and not found:
            if not dice[i].isHeld() and dice[i].value == targetValue:
                dice[i].hold()
                found = True
            i = i + 1
        return found

    def processRoll(self):
        if not self.hasShip:
            if self.holdMatches(6):
                self.hasShip = True
        if self.hasShip and not self.hasCaptain:
            if self.holdMatches(5):
                self.hasCaptain = True
        if self.hasCaptain and not self.hasCrew:
            if self.holdMatches(4):
                self.hasCrew = True

    def cargoScore(self):
        total = 0
        dice = self.hand.dice
        i = 0
        while i < len(dice):
            if not dice[i].isHeld():
                total = total + dice[i].value
            i = i + 1
        return total

    def takeTurn(self):
        self.resetForTurn()

        rollNum = 1
        while rollNum <= 3:
            self.hand.rollAll()
            print("  Roll", rollNum, ":", self.hand.getValues())
            self.processRoll()

            if self.hasShip and self.hasCaptain and self.hasCrew:
                self.score = self.cargoScore()
                print("  Ship, captain, and crew complete -- cargo score is", self.score)

            rollNum = rollNum + 1

        if not (self.hasShip and self.hasCaptain and self.hasCrew):
            self.score = 0
            print("  Did not roll a ship, captain, and crew in 3 rolls -- score is 0")


class Game:

    def __init__(self, playerNames):
        self.players = []
        i = 0
        while i < len(playerNames):
            self.players.append(Player(playerNames[i]))
            i = i + 1

    def playRound(self, contenders):
        i = 0
        while i < len(contenders):
            print()
            print(contenders[i].name, "is rolling...")
            contenders[i].takeTurn()
            print(contenders[i].name, "scores", contenders[i].score)
            i = i + 1

    def playGame(self):
        print("Starting Ship, Captain, and Crew with", len(self.players), "players.")

        contenders = self.players
        winner = None

        while winner is None:
            self.playRound(contenders)

            highScore = -1
            i = 0
            while i < len(contenders):
                if contenders[i].score > highScore:
                    highScore = contenders[i].score
                i = i + 1

            tied = []
            i = 0
            while i < len(contenders):
                if contenders[i].score == highScore:
                    tied.append(contenders[i])
                i = i + 1

            if len(tied) == 1:
                winner = tied[0]
            else:
                names = ""
                i = 0
                while i < len(tied):
                    names = names + tied[i].name
                    if i < len(tied) - 1:
                        names = names + ", "
                    i = i + 1
                print()
                print("Tie at", highScore, "points between:", names, "-- rolling again.")
                contenders = tied

        print()
        print(winner.name, "wins the game with a score of", winner.score, "!")


def main():
    numPlayers = int(input("Enter the number of players (2 or more): "))

    playerNames = []
    i = 0
    while i < numPlayers:
        name = input("Enter name for player " + str(i + 1) + ": ")
        playerNames.append(name)
        i = i + 1

    game = Game(playerNames)
    game.playGame()

main()
