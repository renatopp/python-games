# -*- coding: utf-8 -*-
u"""
Jogo da Velha
=============

Esse é um jogo da velha usando Cocos2D. Essa versão está limitada somente a dois
jogadores, ou seja, não há opção para jogar contra o computador.
"""
import sys
import os
import cocos
import pyglet
from cocos import actions
from pyglet import image

# Definições das constantes para respresentação dos jogadores
PLAYER_1 = 'X'
PLAYER_2 = 'O'

# Registrando o diretório de imagens para o cocos/pyglet
pyglet.resource.path = [os.path.join(os.path.dirname(__file__), 'resources')]
pyglet.resource.reindex()


class Game(object):
    u"""
    Classe contendo as regras do jogo 
    """

    def __init__(self):
        u"""
        Método construtor, inicia as variables de estado do jogo:

        - values: é a lista com as jogadas que estão no "tabuleiro".
        - lastTurn: o último jogador que fez o movimento, usado para não ter que
          fazer comparações mais tarde.
        - turn: o jogador que fará o movimento na próxima jogada.
        """
        self.values = [0]*9
        self.lastTurn = PLAYER_2
        self.turn = PLAYER_1

    def play(self, index):
        u"""
        Método para fazer uma jogada. O parâmetro ``index`` indica a posição que
        o jogador quer marcar. O jogador que fará o movimento é o que está no
        ``self.turn``.
        """

        # Verifica se a posição está livre, se não estiver o método é parado
        if self.values[index] != 0:
            return False

        # O valor da posição jogada é o contido na variavel self.turn (jogador
        # da vez)
        self.values[index] = self.turn

        # Muda o jogador do próximo turno e atualiza o último jogador que fez a
        # movimentação
        self.turn, self.lastTurn = (self.lastTurn, self.turn)
        
        return True

    def isWinner(self):
        u"""
        Verifica se alguém ganhou o jogo, independente do jogador.
        """
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
        u"""
        Verifica se houve empate. 
        """
        # Se todas as posições foram marcadas, então houve empate
        if all(self.values):
            return True
        
        return False


class GameLayer(cocos.layer.Layer):
    u"""
    Layer responsável por desenhar os elementos do jogo e receber os eventos
    do usuário via mouse.
    """
    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()

        # Lista de sprites (X's e O's)
        self.sprites = [None]*9

        # Intância do jogo
        self.game = None

        # Variavel para verificar se o usuário está habilitado à jogador. A 
        # variável estará falsa somente no caso de alguém ganhar ou o jogo 
        # empatar, esperando a finalização dos efeitos para habilitar o jogo 
        # novamente
        self.ableToPlay = True

        # Lista de imagens do jogo, elas são definidas separadamente para não
        # fiarem duplicadas em vários sprites.
        self.imageEmpty = image.load('resources/cell.png')
        self.imageX = image.load('resources/cell-x.png')
        self.imageO = image.load('resources/cell-o.png')
        
        # Imagem de fundo
        self.background = cocos.sprite.Sprite('background.png', (150, 150))
        self.add(self.background)

        # Inicia um novo jogo
        self.newGame()

    def on_mouse_press(self, x, y, buttons, modifiers):
        u"""
        Evento chamado automáticamente quando o usuário fizer algum clique com o
        mouse. Esse método é responsável por verificar se o jogo está parado 
        para a execução dos efeitos, não deixando fazer nenhuma movimentação.
        """

        # Verifica se o usuário clicou nas "bordas", não deixando fazer o 
        # movimento
        if x < 5 or 95 < x < 105 or 195 < x < 205 or 295 < x or \
           y < 5 or 95 < y < 105 or 195 < y < 205 or 295 < y:
            return
        
        # Verifica se o jogo está parado para os efeitos
        if not self.ableToPlay:
            return

        # Converte as coodenadas do clique para a posição de jogada. 
        index = 3*(y/100) + (x/100)

        self.play(index)

    def newGame(self):
        u"""
        Inicia um novo jogo.
        """
        self.game = Game()

        # Inicia ou reseta os sprites
        for i in xrange(9):
            if self.sprites[i] is None:
                x = i%3*100+50
                y = i/3*100+50
                cell = cocos.sprite.Sprite(self.imageEmpty, (x, y))
                self.add(cell)
                self.sprites[i] = cell
            else:
                self.sprites[i].image = self.imageEmpty

                # A ação FadeOut baixou a opacidade para 0, resetando pra 255
                self.sprites[i].opacity = 255 
        
        self.ableToPlay = True
                

    def play(self, index):
        u"""
        Método responsável por fazer uma jogada.
        """
        if self.game.play(index):
            # Se o movimento foi executado, então é atualizado o sprite e 
            # verifica-se se o jogador ganhou ou se houve empate

            cell = self.sprites[index]
            value = self.game.values[index]
            if value == PLAYER_1:
                cell.image = self.imageX
            elif value == PLAYER_2:
                cell.image = self.imageO

            if self.game.isWinner():
                self.__onWin()

            elif self.game.isTie():
                self.__onTie()

    def __onWin(self):
        u"""
        Execução dos efeitos quando alguém ganhar
        """
        # Para o jogo para execução dos efeitos
        self.ableToPlay = False

        # Definição dos efeitos
        blink = actions.Blink(10, 1.5)
        fade = actions.FadeOut(1)

        for i in xrange(9):
            if self.game.values[i] == self.game.lastTurn:
                # Se o sprite é do jogador vencedor então fazer ele piscar
                self.sprites[i].do(blink)
            else:
                # Se o sprite é do jogador perdedor então fazer ele desaparecer
                self.sprites[i].do(fade)

        # Define um atraso de 2 segundos pro jogo reiniciar
        self.do(actions.Delay(1.5) + actions.CallFunc(self.newGame))

    def __onTie(self):
        u"""
        Execução dos efeitos quando houver empate
        """
        # Para o jogo para execução dos efeitos
        self.ableToPlay = False

        # Definição dos efeitos
        fade = actions.FadeOut(1)

        for i in xrange(9):
            # Faz todos sprites desaparecerem
            self.sprites[i].do(fade)

        # Define um atraso de 1 segundo pro jogo reiniciar
        self.do(actions.Delay(1) + actions.CallFunc(self.newGame))


if __name__ == "__main__":
    cocos.director.director.init(width=300, height=300)

    gameLayer = GameLayer()
    mainScene = cocos.scene.Scene(gameLayer)
    cocos.director.director.run(mainScene)