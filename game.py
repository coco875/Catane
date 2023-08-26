"""Module principal du jeu. Gère l'affichage et les évènements."""
# pylint: disable=no-member
import socketio
import pygame
from plateau import Plateau
from outils import (
    # class
    Bouton,

    # fonctions
    rectangle, affiche_texte,

    # dimensions
    LARGEUR, MARGES, FPS,
    LARGEUR_IMAGE_BOUTON_MESSAGES, LARGEUR_IMAGE_GRAND_JOUEUR, HAUTEUR_IMAGE_GRAND_JOUEUR,
    HAUTEUR_TITRE, HAUTEUR_IMAGE_ADRESSE_IP, LARGEUR_IMAGE_ADRESSE_IP,
    LARGEUR_IMAGE_ADRESSE_IP_PETITE,
    X_PLATEAU, Y_PLATEAU,

    # instances
    SCREEN,
    IMAGE_BOUTON_QUITTER, IMAGE_GRAND_JOUEUR,
    IMAGE_FOND_EAU
)
from input import InputTextBox
# from const import *

sio = socketio.Client()

LOGIN = 'login'
CONDITIONS_INIT_JEU = 'conditionsInitJeu'
LISTE_JOUEURS = 'listeJoueurs'
SAUVEGARDE = 'sauvegarde'

EVT_ACTION = 'action'
EVT_GET_EVENT = 'event'

PARAM_PSEUDO = 'pseudo'
PARAM_TYPE = 'type'
PARAM_CONTENU = 'contenu'
PARAM_INFO = 'info'
PARAM_ID = 'id'

STATE_CHOOSING_PSEUDO = 'choosing_pseudo'
STATE_SELECT_IP = 'select_ip'
STATE_WAITING_PLAYERS = 'waiting_players'

sio = socketio.Client()

class Game:
    """Classe principale du jeu. Gère l'affichage et les évènements."""
    state:str = STATE_CHOOSING_PSEUDO
    boutonQuitter = Bouton(LARGEUR - MARGES - LARGEUR_IMAGE_BOUTON_MESSAGES, MARGES,
                           'sauvegarde', image=IMAGE_BOUTON_QUITTER)

    pseudo: str = None
    ip: str = None
    _input: InputTextBox = InputTextBox('Pseudo')
    _input.display_icon= lambda self_=_input : SCREEN.blit(IMAGE_GRAND_JOUEUR, (
                            int((LARGEUR - LARGEUR_IMAGE_GRAND_JOUEUR) / 2),
                            self_.y - HAUTEUR_IMAGE_GRAND_JOUEUR - 15 + 9
                            ))

    plateau = Plateau(X_PLATEAU, Y_PLATEAU)

    def __init__(self):
        pass

    def main(self):
        self.events = pygame.event.get()
        x_mouse, y_mouse = pygame.mouse.get_pos()

        if self.state == STATE_SELECT_IP or self.state == STATE_CHOOSING_PSEUDO:
            self.main_menu()

        if self.state == STATE_CHOOSING_PSEUDO:
            self.choosing_pseudo()
        elif self.state == STATE_SELECT_IP:
            self.choosing_ip()

        if any([event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONUP and self.boutonQuitter.clic(x_mouse,y_mouse)) for event in self.events]):
            pygame.quit()
            exit(0)

        self.boutonQuitter.affiche()
        pygame.display.update()
        pygame.time.Clock().tick(FPS)
    
    def main_menu(self):
        SCREEN.blit(IMAGE_FOND_EAU, (0, 0))
        rectangle(MARGES, MARGES, LARGEUR - 2 * MARGES, HAUTEUR_TITRE)
        affiche_texte('CATANE', LARGEUR / 2 - MARGES, HAUTEUR_TITRE / 2 - 3, None, 130, GRIS_FONCE, centrer=True)
    
    def choosing_pseudo(self):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                self.pseudo = self._input.input_text(event)
                if self.pseudo != None:
                    self.init_menu_ip()
            if event.type == pygame.MOUSEBUTTONUP:
                self.pseudo = self._input.clic(x_mouse, y_mouse)
                if self.pseudo != None:
                    self.init_menu_ip()
        
        self._input.display()
    
    def init_menu_ip(self):
        self.state = STATE_SELECT_IP
        self._input = None
        self._input = InputTextBox('Adresse IP')
        self._input.retry = False
        self._input.display_icon = lambda self=self._input : (
            affiche_texte("La connection avec le serveur", LARGEUR / 2, self.y - 85, None, 34, ROUGE, centrer=True),
            affiche_texte("n'a pas pu être effectuée.", LARGEUR / 2, self.y - 56, None, 34, ROUGE, centrer=True),
            affiche_texte("Veuillez réessayer :", LARGEUR / 2, self.y - 23, None, 34, ROUGE, centrer=True),
            SCREEN.blit(IMAGE_ADRESSE_IP_PETITE, (
                int((LARGEUR - LARGEUR_IMAGE_ADRESSE_IP_PETITE) / 2), self.y - HAUTEUR_IMAGE_ADRESSE_IP - 15 + 9))
        ) if self.retry else SCREEN.blit(IMAGE_ADRESSE_IP,
                (int((LARGEUR - LARGEUR_IMAGE_ADRESSE_IP) / 2), self.y - HAUTEUR_IMAGE_ADRESSE_IP - 15 + 9))

    def choosing_ip(self):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                self.ip = self._input.input_text(event)
                if self.ip != None:
                    self.init_connection()
            if event.type == pygame.MOUSEBUTTONUP:
                self.ip = self._input.clic(x_mouse, y_mouse)
                if self.ip != None:
                    self.init_connection()

        
        self._input.display()

    def init_connection(self):
        try:
            sio.connect(f'http://{self.ip}:{DEFAULT_PORT}')
        except socketio.exceptions.ConnectionError:
            self._input.retry = True
            return
        sio.emit(LOGIN, {PARAM_PSEUDO: self.pseudo})
        self.state = None
