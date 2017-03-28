# importo alcune librerie standard di python
# prova di pull
import os
import sys

# importo la libreria aggiuntiva PyGame
import pygame

# definisco una classe per i colori
class Colori():
    """Raccoglie i colori base"""
    nero   = [  0,  0,  0]
    bianco = [255,255,255]
    blu    = [  0,  0,255]
    verde  = [  0,255,  0]
    rosso  = [255,  0,  0]

# definisco una classe per lo schermo
class Schermo():
    """Gestisce le dimensioni dello schermo"""
    def __init__( self, larghezza, altezza ):
        self.larghezza = larghezza
        self.altezza = altezza

    def Dimensione( self ):
        return [self.larghezza, self.altezza]
    
class Percorsi():
    # ricavo il percorso del modulo corrente
    percorso_corrente = sys.path[0]

    # setto due variabili con le cartelle delle risorse
    cartella_immagini = 'img'
    cartella_suoni = 'snd'

    def Musica( self, nome_file ):
        return os.path.join( self.percorso_corrente, self.cartella_suoni, nome_file )
    
    def Immagine( self, nome_file ):
        return os.path.join( self.percorso_corrente, self.cartella_immagini, nome_file )
    
class Block(pygame.sprite.Sprite):
    """Questa rappresenta gli oggetti mobili del gioco.\nDeriva dalla classe "Sprite" di Pygame"""
    def __init__(self, color, width, height, image):
        """Costruttore: i parametri sono il colore del blocco, le coordinate e l'immagine"""
        # Chiamata al costruttore della classe base
        pygame.sprite.Sprite.__init__(self)
        # Crea una superfice grafica
        self.image = pygame.Surface([width, height])
        # La riempie del colore di sfondo
        self.image.fill(color)
        # Ci carica dentro l'immagine convertita
        self.image = pygame.image.load(image).convert()
        # Setta il colore della trasparenza
        self.image.set_colorkey(color)
        # Si setta il rettangono elaborato per l'imamgine
        self.rect = self.image.get_rect()

