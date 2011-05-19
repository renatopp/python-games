# -*- coding: utf-8 -*-

import sys
import os
import cocos
import pyglet
from cocos import actions
from pyglet import image

PLAYER_1 = 1
PLAYER_2 = 2

pyglet.resource.path = [os.path.join(os.path.dirname(__file__), 'resources')]
pyglet.resource.reindex()

class Game(object):
    def __init__(self):
        self.values = [0]*9
        self.lastTurn = PLAYER_2
        self.turn = PLAYER_1

    def play(self, index):
        if self.values[index] != 0:
            return False

        self.values[index] = self.turn
        self.turn, self.lastTurn = (self.lastTurn, self.turn)
        
        return True

    def isWinner(self):
        values = self.values
        if values[0] == values[1] == values[2] != 0 or \
           values[3] == values[4] == values[5] != 0 or \
           values[6] == values[7] == values[8] != 0 or \
           values[0] == values[3] == values[6] != 0 or \
           values[1] == values[4] == values[7] != 0 or \
           values[2] == values[5] == values[8] != 0 or \
           values[0] == values[4] == values[8] != 0 or \
           values[2] == values[4] == values[6] != 0:
            return True
        
        return False
        
    def isTie(self):
        if all(self.values):
            return True
        return False


class GameLayer(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self, ):
        super(GameLayer, self).__init__()
        self.sprites = [None]*9
        self.game = None
        self.ableToPlay = True

        self.imageEmpty = image.load('resources/cell.png')
        self.imageX = image.load('resources/cell-x.png')
        self.imageO = image.load('resources/cell-o.png')
        
        self.background = cocos.sprite.Sprite('background.png', (150, 150))
        self.add(self.background)

        self.newGame()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if x < 5 or 95 < x < 105 or 195 < x < 205 or 295 < x or \
           y < 5 or 95 < y < 105 or 195 < y < 205 or 295 < y:
            return
        
        if not self.ableToPlay:
            return

        index = 3*(y/100) + (x/100)
        self.play(index)

    def newGame(self):
        self.unschedule(self.newGame)
        self.game = Game()
        for i in xrange(9):
            if self.sprites[i] is None:
                x = i%3*100+50
                y = i/3*100+50
                cell = cocos.sprite.Sprite(self.imageEmpty, (x, y))
                self.add(cell)
                self.sprites[i] = cell
            else:
                self.sprites[i].image = self.imageEmpty
                self.sprites[i].opacity = 255
        
        self.ableToPlay = True
                

    def play(self, index):
        if self.game.play(index):
            cell = self.sprites[index]
            value = self.game.values[index]
            if value == 1:
                cell.image = self.imageX
            elif value == 2:
                cell.image = self.imageO

            if self.game.isWinner():
                self.__onWin()

            elif self.game.isTie():
                self.__onTie()

    def __onWin(self):
        self.ableToPlay = False
        blink = actions.Blink(10, 2)
        fade = actions.FadeOut(1)

        for i in xrange(9):
            if self.game.values[i] == self.game.lastTurn:
                self.sprites[i].do(blink)
            else:
                self.sprites[i].do(fade)

        self.do(actions.Delay(2) + actions.CallFunc(self.newGame))

    def __onTie(self):
        self.ableToPlay = False
        fade = actions.FadeOut(1)

        for i in xrange(9):
            self.sprites[i].do(fade)

        self.do(actions.Delay(1) + actions.CallFunc(self.newGame))


if __name__ == "__main__":
    cocos.director.director.init(width=300, height=300)

    gameLayer = GameLayer()
    mainScene = cocos.scene.Scene(gameLayer)
    cocos.director.director.run(mainScene)