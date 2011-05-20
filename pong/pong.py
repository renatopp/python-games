# -*- coding:utf-8 -*-

u"""
Jogo Pong
=========

Controles:

- Jogador 1: ``A`` para cima e ``Z`` para baixo.
- Jogador 2: ``K`` para cima e ``M`` para baixo.
"""

import os
import itertools
import cocos
import pyglet
import random
from pyglet.window import key as keys
from vectors import Vector
V = Vector

# Registrando o diretório de imagens para o cocos/pyglet
pyglet.resource.path = [os.path.join(os.path.dirname(__file__), 'resources')]
pyglet.resource.reindex()

class Entity(object):
    u"""
    Um objeto do jogo.

    Representa as barrinhas dos jogadores e a bola.
    """
    def __init__(self, image, position, velocity=(0, 0), direction=(0, 0), acceleration=(0, 0)):
        self.position = V(position)
        self.velocity = V(velocity)
        self.direction = V(direction)
        self.acceleration = V(acceleration)

        self.sprite = cocos.sprite.Sprite(image, position)
    
    def move(self, value):
        u"""
        Movimenta o objeto adicionando o vetor ``value`` à posição atual
        """
        self.position += value
        self.sprite.position = self.position

    def collision_y(self, minLimit, maxLimit):
        u"""
        Verifica a colisão no eixo y. Se a direção do objeto está apontada para
        cima, então a posição é comparada com o ``maxLimit``, no contrário, se
        a direção está apontada para baixo, então a posição é comparada com o
        ``minLimit``. É considerado o tamanho da imagem do sprite.
        """
        anchor = self.sprite.image_anchor[1]

        if self.direction[1] > 0:
            return self.position[1]+anchor >= maxLimit
        elif self.direction[1] < 0:
            return self.position[1]-anchor <= minLimit

        return False
        
    def collision_x(self, minLimit, maxLimit):
        u"""
        Verifica a colisão no eixo x. Se a direção do objeto está apontada para
        direita, então a posição é comparada com o ``maxLimit``, no contrário, 
        se a direção está apontada para esquerda, então a posição é comparada 
        com o ``minLimit``. É considerado o tamanho da imagem do sprite.
        """
        anchor = self.sprite.image_anchor[0]

        if self.direction[0] > 0:
            return self.position[0]+anchor >= maxLimit
        elif self.direction[0] < 0:
            return self.position[0]-anchor <= minLimit

        return False

    def collision(self, entity):
        u"""
        Verifica a colisão entre dois objetos, considerando o tamanho da imagem
        dos sprites.
        """
        myAnchor = self.sprite.image_anchor
        entAnchor = entity.sprite.image_anchor
        myX = self.position[0]-myAnchor[0]-entAnchor[0]/2, self.position[0]+myAnchor[0]+entAnchor[0]/2
        myY = self.position[1]-myAnchor[1]-entAnchor[1], self.position[1]+myAnchor[1]+entAnchor[1]

        return myX[0] <= entity.position[0] <= myX[1] and myY[0] <= entity.position[1] <= myY[1]


class GameLayer(cocos.layer.ColorLayer):
    u"""
    Layer responsável por desenhar os elementosm, controlar o jogo e receber os
    eventos do usuário via teclado.
    """
    is_event_handler = True

    def __init__(self, screenLimits):
        super(GameLayer, self).__init__(255, 255, 255, 255)

        self.screenLimits = screenLimits
        self.points1 = 0
        self.points2 = 0

        self.player1 = Entity('bar.png', (50, 300), (500, 500))
        self.player2 = Entity('bar.png', (750, 300), (500, 500))
        self.ball = Entity('ball.png', (400, 300), (500, 500), (0.7682, 0.6401), (0.1, 0.1))
        self.add(self.player1.sprite)
        self.add(self.player2.sprite)
        self.add(self.ball.sprite)

        self.lblPoints1 = cocos.text.Label('0', font_size=40, color=(0, 0, 0, 255), x=100, y=self.screenLimits[1]-50, anchor_x='center', anchor_y='center')
        self.lblPoints2 = cocos.text.Label('0', font_size=40, color=(0, 0, 0, 255), x=self.screenLimits[0]-100, y=self.screenLimits[1]-50, anchor_x='center', anchor_y='center')
        self.add(self.lblPoints1)
        self.add(self.lblPoints2)

        self.schedule_interval(self.update, 0.02)

    def on_key_press (self, key, modifiers):
        u"""
        Quando uma tecla é pressionada a direção das barrinhas é setada
        """
        if key == keys.K:
            self.player2.direction = V(0, 1)
        elif key == keys.M:
            self.player2.direction = V(0, -1)
        
        if key == keys.A:
            self.player1.direction = V(0, 1)
        elif key == keys.Z:
            self.player1.direction = V(0, -1)
    
    def on_key_release (self, key, modifiers):
        u"""
        Quando uma tecla é solta a direção das barrinhas é nula
        """
        if key == keys.K and self.player2.direction == [0, 1]:
            self.player2.direction = V(0, 0)
        elif key == keys.M and self.player2.direction == [0, -1]:
            self.player2.direction = V(0, 0)

        if key == keys.A and self.player1.direction == [0, 1]:
            self.player1.direction = V(0, 0)
        elif key == keys.Z and self.player1.direction == [0, -1]:
            self.player1.direction = V(0, 0)

    def _restartBallProperties(self, position):
        u"""
        Reinicia a posição, velocidade e direção da bola, chamado quando alguém
        faz um ponto.
        """
        self.ball.position = position
        self.ball.velocity = V(400, 400)
        self.ball.direction = V(0.7682, random.choice([0.6401, -0.6401]))    
        self.ball.sprite.position = self.ball.position

    def _changeBallDirection(self, player):
        u"""
        Muda a direção da bolinha na colisão, a direção depende de onde acontece
        a colisão entre a bola e a barrinha do ``player``.
        """
        anchor = player.sprite.image_anchor[1]*0.8
        # Se pegar no topo da barrinha
        if self.ball.position[1] > player.position[1]+anchor:
            if self.ball.direction[1] > 0:
                self.ball.direction[1] -= random.random()
                self.ball.direction.norm()
            else:
                self.ball.direction[1] += random.random()
                self.ball.direction.norm()
                self.ball.direction[1] *= -1

        # Se pegar no parte de baixo da barrinha
        elif self.ball.position[1] < player.position[1]-anchor:
            if self.ball.direction[1] < 0:
                self.ball.direction[1] += random.random()
                self.ball.direction.norm()
            else:
                self.ball.direction[1] -= random.random()
                self.ball.direction.norm()
                self.ball.direction[1] *= -1

        # Se pegar no meio da barrinha
        else:
            self.ball.direction[1] -= random.random()/2
            self.ball.direction.norm()

        if self.ball.direction[1] > 0.8:
            self.ball.direction[1] = 0.8
            self.ball.direction.norm()
        self.ball.direction[0] *= -1

    def update(self, tick):
        u"""
        Atualização das posições dos objetos, verificações das colisões e 
        verificação da pontuação.
        """
        # Player 1 bar vertical collision
        if not self.player1.collision_y(0, self.screenLimits[1]):
            self.player1.move(self.player1.velocity*tick*self.player1.direction)

        # Player 2 bar vertical collision
        if not self.player2.collision_y(0, self.screenLimits[1]):
            self.player2.move(self.player2.velocity*tick*self.player2.direction)

        # Point verification
        if self.ball.collision_x(0, self.screenLimits[0]):
            if self.ball.direction[0] > 0:
                self.points1 += 1
                self.lblPoints1.element.text = str(self.points1)
                self._restartBallProperties(V(self.screenLimits[0]-100, 300))
                self.ball.direction[0] *= -1
            else:
                self.points2 += 1
                self.lblPoints2.element.text = str(self.points2)
                self._restartBallProperties(V(100, 300))
            

        # Ball and Player 1 bar collision
        if self.ball.direction[0] < 0 and self.player1.collision(self.ball):
            self._changeBallDirection(self.player1)

        # Ball and Player 2 bar collision
        if self.ball.direction[0] > 0 and self.player2.collision(self.ball):
            self._changeBallDirection(self.player2)

        # Ball vertical collision
        if not self.ball.collision_y(0, self.screenLimits[1]):
            self.ball.move(self.ball.velocity*tick*self.ball.direction)
        else:
            self.ball.direction[1] *= -1

        self.ball.velocity += self.ball.acceleration


if __name__ == '__main__':
    width, height = 800, 600
    screenLimits = width, height
    cocos.director.director.init(width, height, u'Pong!')

    gameLayer = GameLayer(screenLimits)
    mainScene = cocos.scene.Scene(gameLayer)
    cocos.director.director.run(mainScene)