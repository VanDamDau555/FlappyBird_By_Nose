import pygame as pg
import random
import sys
import cv2
import PIL.Image
import PIL.ImageTk

pg.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)                 #De tich hop sound tot hon cho pygame
pg.init()
#Set khung hinh
screen_width = 432
screen_height = 768
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Flappy Bird")
#Cac hinh anh su dung
bg_img = pg.transform.scale2x(pg.image.load('D:\Anaconda\python1\FlappyBird\Img_FB\Bg_night.png'))
gr_img = pg.transform.scale2x(pg.image.load('D:\Anaconda\python1\FlappyBird\Img_FB\ground.png'))
bird_img = pg.transform.scale2x(pg.image.load('D:\Anaconda\python1\FlappyBird\Img_FB\yellowbird_midflap.png').convert_alpha())
birdUp_img = pg.transform.scale2x(pg.image.load('D:\Anaconda\python1\FlappyBird\Img_FB\yellowbird_upflap.png').convert_alpha())
birdDown_img = pg.transform.scale2x(pg.image.load('D:\Anaconda\python1\FlappyBird\Img_FB\yellowbird_downflap.png').convert_alpha())
pipe_img = pg.transform.scale2x(pg.image.load('D:\Anaconda\python1\FlappyBird\Img_FB\pipe_green.png'))
gameover_img = pg.transform.scale2x(pg.image.load('D:\Anaconda\python1\FlappyBird\Img_FB\message.png'))
#Cac am thanh duoc su dung
flap_sound = pg.mixer.Sound('D:\Anaconda\python1\FlappyBird\Sound_FB\FB_sfx_wing.wav')
hit_sound = pg.mixer.Sound('D:\Anaconda\python1\FlappyBird\Sound_FB\FB_sfx_hit.wav')
score_sound = pg.mixer.Sound('D:\Anaconda\python1\FlappyBird\Sound_FB\FB_sfx_point.wav')
##Dieu chinh vi tri
#Cua groud va background
bg_pos_x = 0
gr_pos_x = 0

#Cua Bird
gravity = 0.25
bird_movement = 0
birdList = [birdDown_img, bird_img, birdUp_img]         #index 0, 1, 2
bird_index = 0
bird = birdList[bird_index]
bird_rect = bird.get_rect(center = ((screen_width/2)-100,screen_height/2))
#Tao timer cho Bird
bird_flap = pg.USEREVENT + 1                  #Tuong tu Timer cho pipe
pg.time.set_timer(bird_flap, 200)
##Cua ong
pipeList = []
pipe_height = [200, 225, 250, 275, 300, 350, 400, 450]
#Tao timer
#USEREVENT la ham su kien nguoi dung de set = set_timer ben duoi    (kha giong ngat mem)
spawn_pipe = pg.USEREVENT
pg.time.set_timer(spawn_pipe, 1200)         #Thoi gian tinh theo ms
#He so FPS cua game
clock = pg.time.Clock()  
font_Game = pg.font.SysFont('Time new roman', 40, bold=True)
#Bien score
score = 0
high_score = 0
score_time_for_sound = 120

def creat_pipe():
    rd_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_img.get_rect(midtop = (screen_width+32, rd_pipe_pos)) 
    top_pipe = pipe_img.get_rect(midtop = (screen_width+32, rd_pipe_pos-650)) 
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= screen_height/2:
            screen.blit(pipe_img, pipe)
        else:
            flip_pipe = pg.transform.flip(pipe_img, False, True)
            screen.blit(flip_pipe, pipe)

def draw_background():
    #Can 2 background de dao vi tri
    screen.blit(bg_img,(bg_pos_x,0))
    screen.blit(bg_img,(bg_pos_x+screen_width,0))
def draw_ground():
    #Can 2 ground de dao vi tri
    screen.blit(gr_img,(gr_pos_x,screen_height-70))
    screen.blit(gr_img,(gr_pos_x+screen_width,screen_height-70))   

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <=-75 or bird_rect.bottom >= screen_height-150:        #-150 theo ground
        return False
    return True

def gameOver():
    gameOver_rect = gameover_img.get_rect(center = (screen_width/2, screen_height/2))
    screen.blit(gameover_img, gameOver_rect)

#Cho bird nghieng theo huong roi
def rotate_Bird(r_bird):
    #rotozoom de quay goc theo cau truc (Imaga, angle, ti le-scale)
    animation_Bird = pg.transform.rotozoom(r_bird, -bird_movement*2.5, 1)          #-bird_movement vi nguoc huong trong luc
    return animation_Bird
#Cho hoat anh cua bird luon thay doi
def animation_Bird():
    a_bird = birdList[bird_index]
    a_bird_rect = a_bird.get_rect(center = ((screen_width/2)-100, bird_rect.centery))
    return a_bird, a_bird_rect

def scoreGame(gameRun):
    if gameRun:
        score_display = font_Game.render('Score: '+str(int(score)), True, (255, 0, 0))
        score_rect = score_display.get_rect(center = (screen_width/2, 120))
        screen.blit(score_display, score_rect)
    else:
        score_display = font_Game.render('Score: '+str(int(score)), True, (255, 0, 0))
        score_rect = score_display.get_rect(center = (screen_width/2, 120))
        screen.blit(score_display, score_rect)
        #High score chi hien thi ghi game ket thuc
        highScore_display = font_Game.render('High Score: '+str(int(high_score)), True, (255, 0, 0))
        highScore_rect = highScore_display.get_rect(center = (screen_width/2, 630))
        screen.blit(highScore_display, highScore_rect)

def scoreUpdate(score, high_score):
    if score >= high_score:
        high_score = score
    return high_score

class FaceDetect():
    pass

active = True
while True:
    ##Hien thi background, ground, bird
    draw_background()
    if active:
        bg_pos_x-=1
        gr_pos_x-=1    
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotateBird = rotate_Bird(bird)              #Bird se luon bi nghieng
        screen.blit(rotateBird, bird_rect)        
        pipeList = move_pipe(pipeList)
        draw_pipe(pipeList)
        active = check_collision(pipeList)
        #Can chinh de khi qua mot pipe + 1 score
        score += 0.01                           #Dang test nen chua chinh dung
        scoreGame(gameRun=True)
        score_time_for_sound -= 1
        if score_time_for_sound <= 0:
            score_sound.play()
            score_time_for_sound = 120
    else:
        gameOver()
        high_score = scoreUpdate(score, high_score)
        scoreGame(gameRun=False)
    draw_ground() 
    #Khi ground 1 chay xong --> ground 2 --> ground 1 di chuyen ra sau
    if gr_pos_x <= -screen_width:
        gr_pos_x = 0
    #Tuong tu voi background
    if bg_pos_x <= -screen_width:
        bg_pos_x = 0
    #Thoat chuong trinh
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and active:                
                bird_movement = 0
                bird_movement =- 8
                flap_sound.play()
            if event.key == pg.K_SPACE and active == False:
                active = True
                #Cac thuoc tinh duoc reset khi game bat dau lai 1. List pipe; 2. Bird: position; 3. Score = 0
                pipeList.clear()
                bird_rect.center = ((screen_width/2)-100,(screen_height/2))
                bird_movement = 0
                score = 0
            if event.key == pg.K_q:
                pg.quit()
                sys.exit()
        if event.type == spawn_pipe:
            #Extend trong list de chen nhieu phan tu mot luc
            pipeList.extend(creat_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = animation_Bird()
        #pg.mouse.get _pos se tra ve vi tri hien tai qua chuot
        #Dang nghi cach de no di chuyen theo khuon mat
        #if event.type == pg.MOUSEMOTION:
        #    bird_rect = bird.get_rect(center = pg.mouse.get_pos())
            

    pg.display.update()

    #FPS = 90
    FPS = 120
    clock.tick(FPS)              