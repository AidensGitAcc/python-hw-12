# Chapter 12, Problem 2 — LCR With Textual and Graphical Interfaces

import random
from graphics import *

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


class TextInterface:

    def getNumPlayers(self):
        return int(input("Enter the number of players (3 or more): "))

    def getPlayerName(self, index):
        return input("Enter name for player " + str(index + 1) + ": ")

    def showMessage(self, text):
        print(text)

    def showChipCounts(self, players, potChips):
        print()
        i = 0
        while i < len(players):
            print(" ", players[i].name, "-", players[i].chips, "chip(s)")
            i = i + 1
        print("  Pot -", potChips, "chip(s)")

    def showWinner(self, name, potChips):
        print()
        print(name, "wins the game and takes the pot of", potChips, "chip(s)!")


class GraphicalInterface:

    def __init__(self):
        self.win = None
        self.texts = []

    def getNumPlayers(self):
        return int(input("Enter the number of players (3 or more): "))

    def getPlayerName(self, index):
        return input("Enter name for player " + str(index + 1) + ": ")

    def setupWindow(self, players):
        numPlayers = len(players)
        self.win = GraphWin("LCR", 500, 80 + numPlayers * 40)
        self.win.setBackground("lightyellow")

        heading = Text(Point(250, 30), "LCR -- click anywhere to advance each turn")
        heading.draw(self.win)

        self.texts = []
        i = 0
        while i < numPlayers:
            label = Text(Point(250, 70 + i * 40), players[i].name + ": " + str(players[i].chips) + " chip(s)")
            label.setSize(14)
            label.draw(self.win)
            self.texts.append(label)
            i = i + 1

        self.potText = Text(Point(250, 70 + numPlayers * 40), "Pot: 0 chip(s)")
        self.potText.setSize(14)
        self.potText.draw(self.win)

    def showMessage(self, text):
        print(text)

    def showChipCounts(self, players, potChips):
        i = 0
        while i < len(players):
            self.texts[i].setText(players[i].name + ": " + str(players[i].chips) + " chip(s)")
            i = i + 1
        self.potText.setText("Pot: " + str(potChips) + " chip(s)")
        self.win.getMouse()

    def showWinner(self, name, potChips):
        result = Text(Point(250, 40), name + " wins the pot of " + str(potChips) + " chip(s)! Click to exit.")
        result.setSize(14)
        result.setTextColor("darkgreen")
        result.draw(self.win)
        self.win.getMouse()
        self.win.close()


class Game:

    def __init__(self, interface):
        self.interface = interface
        numPlayers = interface.getNumPlayers()

        self.players = []
        i = 0
        while i < numPlayers:
            name = interface.getPlayerName(i)
            self.players.append(Player(name))
            i = i + 1

        self.pot = Pot()
        self.die = Die()

        if hasattr(interface, "setupWindow"):
            interface.setupWindow(self.players)

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

        self.interface.showMessage("")
        self.interface.showMessage(player.name + " has " + str(player.chips) + " chip(s) and rolls " + str(numDice) + " die/dice.")

        rollNum = 0
        while rollNum < numDice:
            result = self.die.roll()
            if result == "L":
                player.removeChip()
                leftIndex = (playerIndex + 1) % len(self.players)
                self.players[leftIndex].addChip()
                self.interface.showMessage("  Rolled L -- gives a chip to " + self.players[leftIndex].name)
            elif result == "R":
                player.removeChip()
                rightIndex = (playerIndex - 1) % len(self.players)
                self.players[rightIndex].addChip()
                self.interface.showMessage("  Rolled R -- gives a chip to " + self.players[rightIndex].name)
            elif result == "C":
                player.removeChip()
                self.pot.addChip()
                self.interface.showMessage("  Rolled C -- puts a chip in the pot.")
            else:
                self.interface.showMessage("  Rolled a dot -- no chip moves.")
            rollNum = rollNum + 1

        self.interface.showChipCounts(self.players, self.pot.chips)

    def playGame(self):
        self.interface.showMessage("Starting LCR with " + str(len(self.players)) + " players, 3 chips each.")

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

        self.interface.showWinner(winner.name, self.pot.chips)


def main():
    choice = input("Play with a (t)ext or (g)raphical interface? ")

    if choice.lower().startswith("g"):
        interface = GraphicalInterface()
    else:
        interface = TextInterface()

    game = Game(interface)
    game.playGame()

main()
