# Chapter 12, Problem 1 — LCR (Left Center Right) Game Simulation

import random

class Die:

    def __init__(self):
        self.value = ""

    def roll(self):
        number = random.randint(1, 6)
        if number == 1:
            self.value = "L"
        elif number == 2:
            self.value = "R"
        elif number == 3:
            self.value = "C"
        else:
            self.value = "."
        return self.value


class Player:

    def __init__(self, name):
        self.name = name
        self.chips = 3

    def hasChips(self):
        return self.chips > 0

    def removeChip(self):
        self.chips = self.chips - 1

    def addChip(self):
        self.chips = self.chips + 1


class Pot:

    def __init__(self):
        self.chips = 0

    def addChip(self):
        self.chips = self.chips + 1


class Game:

    def __init__(self, playerNames):
        self.players = []
        i = 0
        while i < len(playerNames):
            self.players.append(Player(playerNames[i]))
            i = i + 1
        self.pot = Pot()
        self.die = Die()

    def playersWithChips(self):
        count = 0
        i = 0
        while i < len(self.players):
            if self.players[i].hasChips():
                count = count + 1
            i = i + 1
        return count

    def playTurn(self, playerIndex):
        player = self.players[playerIndex]
        numDice = player.chips
        if numDice > 3:
            numDice = 3

        print()
        print(player.name, "has", player.chips, "chip(s) and rolls", numDice, "die/dice.")

        rollNum = 0
        while rollNum < numDice:
            result = self.die.roll()
            if result == "L":
                player.removeChip()
                leftIndex = (playerIndex + 1) % len(self.players)
                self.players[leftIndex].addChip()
                print("  Rolled L -- gives a chip to", self.players[leftIndex].name)
            elif result == "R":
                player.removeChip()
                rightIndex = (playerIndex - 1) % len(self.players)
                self.players[rightIndex].addChip()
                print("  Rolled R -- gives a chip to", self.players[rightIndex].name)
            elif result == "C":
                player.removeChip()
                self.pot.addChip()
                print("  Rolled C -- puts a chip in the pot.")
            else:
                print("  Rolled a dot -- no chip moves.")
            rollNum = rollNum + 1

    def playGame(self):
        print("Starting LCR with", len(self.players), "players, 3 chips each.")

        currentIndex = 0
        while self.playersWithChips() > 1:
            if self.players[currentIndex].hasChips():
                self.playTurn(currentIndex)
            currentIndex = (currentIndex + 1) % len(self.players)

        winner = None
        i = 0
        while i < len(self.players):
            if self.players[i].hasChips():
                winner = self.players[i]
            i = i + 1

        print()
        print(winner.name, "wins the game and takes the pot of", self.pot.chips, "chip(s)!")


def main():
    numPlayers = int(input("Enter the number of players (3 or more): "))

    playerNames = []
    i = 0
    while i < numPlayers:
        name = input("Enter name for player " + str(i + 1) + ": ")
        playerNames.append(name)
        i = i + 1

    game = Game(playerNames)
    game.playGame()

main()
