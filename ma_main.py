# -*- coding: utf-8 -*-

# importo la libreria aggiuntiva PyGame
import pygame

# Importo la libreria custom delle utility
from ma_helper import *

# creo un oggetto Percorsi
p = Percorsi()

# costruisco i persorsi dei file grafici
bg_path = p.Immagine( "bg.jpg" )
starship_path = p.Immagine( "starship.jpg" )
asteroid_path = p.Immagine( "asteroid.png" )
bullet_path = p.Immagine( "bullet.png" )

# costruisco i persorsi dei file audio
music_path = p.Musica( "morricone.ogg" )
shot_path = p.Musica( "shotgun.ogg" )
hurt_path = p.Musica( "fireball.ogg" )
hit_path = p.Musica( "hit.ogg" )
laugh_path = p.Musica( "laugh.ogg" )

# Initialize the game engine
pygame.init()

schermo = Schermo( 640, 480 )

# Inizializzo la dimensione della finestra
screen = pygame.display.set_mode( schermo.Dimensione() )

# Setto il titolo della finestra
pygame.display.set_caption( "Z-Game - a Py Game developed by Luca Zomparelli" )

# Nascondo il mouse all'interno della finestra, al suo posto si vedrà la navicella
pygame.mouse.set_visible( False )

# ricavo la classe che mi servirà per gestire la velocità
clock = pygame.time.Clock()

# carico l'immagine di sfondo
background_image = pygame.image.load( bg_path ).convert()

# Mi creo le liste per la gestione delle collisioni
steroid_list = pygame.sprite.RenderPlain()
bullet_list = pygame.sprite.RenderPlain()
all_sprites_list = pygame.sprite.RenderPlain()

# Create a player block
player = Block( Colori.nero, 20, 15, starship_path )
all_sprites_list.add( player )

# Create a steroid block
steroid = Block( Colori.nero, 20, 15, asteroid_path )
all_sprites_list.add( steroid )
steroid_list.add( steroid )

# Seleziono il font da utilizzare. Default font, 25 pt di dimensione
font = pygame.font.Font( None, 25 )

# carico la misica di sottofondo
pygame.mixer.music.load( music_path )

# Carico gli effetti sonori
shot = pygame.mixer.Sound( shot_path )
crush = pygame.mixer.Sound( hurt_path )
hit = pygame.mixer.Sound( hit_path )
laugh = pygame.mixer.Sound( laugh_path )

# faccio partire la musica
pygame.mixer.music.play()

# Inizializzo un po' di variabili
# ...per la gestione dei loop di esecuzione...
esci = False
game_over = False
# ...per la gestione dei punti del gioco...
punteggio = 0
energia = 100
livello = 1
#...e per la gestione del posizionamento degli elementi
rect_change_x = 5
rect_change_y = 5
level_rect_change_x = 5
level_rect_change_y = 5
rect_x = 50
rect_y = 50

# -------- inizio loop principale -----------
while( not(esci or game_over) ):
    # leggo la posizione del mouse...
    posizione_mouse = pygame.mouse.get_pos()
    # ... e posizione l'astronavicella in base alle coordinate ottenute
    player.rect.x = posizione_mouse[0] - 50
    player.rect.y = posizione_mouse[1] - 50
    
    for event in pygame.event.get():# Guardo nella lista degli event
        if event.type == pygame.QUIT: # ...se l'utente ha premuto esci
            esci = True # alzo il flag per l'uscita dal gioco

        # Ho premuto il pulsante del mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            # riproduco il suono dello sparo...
            shot.play()
            # ...e creo un nuovo proiettile...
            bullet = Block( Colori.nero, 50, 40, bullet_path )
            bullet.rect.x = posizione_mouse[0] - 25
            bullet.rect.y = posizione_mouse[1] - 20
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)
            bullet = None

    # Clear the screen and set the screen background
    screen.fill( Colori.nero )

    screen.blit( background_image, [0,0] )

    # Calcolo le velocità e le nuove posizioni in base al livello raggiunto
    level_rect_change_x = rect_change_x * livello
    level_rect_change_y = rect_change_y * livello
    rect_x += level_rect_change_x
    rect_y += level_rect_change_y
    steroid.rect.x = rect_x
    steroid.rect.y = rect_y

    # Scorro la lista dei proiettili in volo
    for bullet in bullet_list:
        bullet.rect.x = bullet.rect.x - 6
        bullet.rect.y = bullet.rect.y + 5
        # se i proiettili sono usciti dallo schermo ...
        if(( bullet.rect.x < 0) or (bullet.rect.y > schermo.altezza)):
            bullet.kill() # ...li elimino

    # Calcolo la posizione e la traiettoria dell'asteroide
    if rect_y > 480-50 or rect_y < 0:
        rect_change_y = rect_change_y * -1
    if rect_x > 640-50 or rect_x < 0:
        rect_change_x = rect_change_x * -1

    # verifico se l'astronave è stata colpita dall'asteroide
    blocks_hit_list = pygame.sprite.spritecollide( player, steroid_list, False )

    # Se ho elementi nella lista vuol dire che l'astronave è stat colpita
    if( blocks_hit_list ):
        # riproduco il suono di collisione...
        crush.play()
        # ...e calo l'energia
        energia -= 1
        if( energia <= 0 ):# se l'energia arriva a zero
            game_over = True
            
    # verifico se l'asteroide è stato colipito dal uno dei proiettili
    blocks_hit_list = pygame.sprite.spritecollide( steroid, bullet_list, True )
    
    # Se ho elementi nella lista vuol dire che l'asteroide è stato colpito
    if( blocks_hit_list ):
        # riproduco il suono di collisione...
        hit.play()
        # ...e aumento i punti
        punteggio += 1

    # disegno tutte le sprite
    all_sprites_list.draw( screen )

    # scivo a monitor lo stato della partita
    livello = int(punteggio / 10) + 1

    text = font.render("Energy: %s" % ("|"*energia), True, Colori.rosso)
    screen.blit(text, [10,10])
    text = font.render("Score: %3d" % (punteggio), True, Colori.verde)
    screen.blit(text, [10,30])
    text = font.render("Level: %3d" % (livello), True, Colori.blu)
    screen.blit(text, [10,50])

    # limito l'esecuzione 24 fps
    clock.tick(24)

    # aggiorniamo lo schermo
    pygame.display.flip()

# Seleziono il font da utilizzare. Default font, 40 pt di dimensione
font = pygame.font.Font( None, 40 )

# Fermo ogni altro suono e riproduco il suono di GAME OVER
crush.stop()
laugh.play()

# se ho già premuto esci in questo loop non ci entra
while (not esci):
    for event in pygame.event.get():# Guardo nella lista degli event
        if event.type == pygame.QUIT: # ...se l'utente ha premuto esci
            esci = True # alzo il flag per l'uscita dal gioco
            
    text = font.render( "GAME OVER", True, Colori.bianco )
    screen.blit( text, [220,200] )

    # Limit to 24 frames per second
    clock.tick(24)

    # aggiorniamo lo schermo
    pygame.display.flip()

# Arresto i suoni
pygame.mixer.music.stop()
pygame.mixer.quit()

# Termino la libreria di PyGame
pygame.quit()
