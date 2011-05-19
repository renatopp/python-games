import sys
import os
import cocos
import pyglet
from pyglet import image

pyglet.resource.path = [os.path.join(os.path.dirname(__file__), 'resources')]
pyglet.resource.reindex()

class Game(object):
    def __init__(self):
        self.values = [0]*9
        self.turn = 0

    def play(self, index):
        if self.values[index] != 0:
            return False

        value = self.turn%2 + 1
        self.values[index] = value
        self.turn += 1

        if self._isWinner():
            v =  'Player ' + str(value) + ' won'
            raise Exception(v)

        if self._isTie():
            raise Exception('Tie')
        
        return True

    def _isWinner(self):
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
        
    def _isTie(self):
        if all(self.values):
            return True
        return False

class GameLayer(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self, ):
        super(GameLayer, self).__init__()
        self.cells = [None]*9
        self.game = None

        self.imageCell = image.load('resources/cell.png')
        self.imageX = image.load('resources/cell-x.png')
        self.imageO = image.load('resources/cell-o.png')
        
        self.background = cocos.sprite.Sprite('background.png', (150, 150))
        self.add(self.background)

        self.newGame()

    def newGame(self):
        self.game = Game()
        for i in xrange(9):
            if self.cells[i] is None:
                x = i%3*100+50
                y = i/3*100+50
                cell = cocos.sprite.Sprite(self.imageCell, (x, y))
                self.add(cell)
                self.cells[i] = cell
            else:
                self.cells[i].image = self.imageCell

    def on_mouse_press(self, x, y, buttons, modifiers):
        if x < 5 or 95 < x < 105 or 195 < x < 205 or 295 < x or \
           y < 5 or 95 < y < 105 or 195 < y < 205 or 295 < y:
            return

        index = 3*(y/100) + (x/100)
        if self.game.play(index):
            cell = self.cells[index]
            value = self.game.values[index]
            if value == 1:
                cell.image = self.imageX
            elif value == 2:
                cell.image = self.imageO


if __name__ == "__main__":
    cocos.director.director.init(width=300, height=300)

    gameLayer = GameLayer()
    mainScene = cocos.scene.Scene(gameLayer)
    cocos.director.director.run(mainScene)