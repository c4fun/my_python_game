import pygame, sys, random;
from pygame.locals import *

def continuePlaying():
    print('Wanna Continue? (Yes/No)');
    return input().lower().startswith('y');

def haveMovement(pressed):
    return pressed[K_LEFT] or pressed[K_RIGHT] or pressed[K_UP] or pressed[K_DOWN] or pressed[K_a] or pressed[K_d] or pressed[K_w] or pressed[K_s];

# set up the game
pygame.init();
mainClock = pygame.time.Clock();


# set up the window
WINDOWWIDTH = 1200;
WINDOWHEIGHT = 600;
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32);
pygame.display.set_caption('See if you can eat them all');

# set up the color
BLACK = (0, 0, 0);
GREEN = (0, 255, 0);
WHITE = (255, 255, 255);
RED = (255, 0, 0);
BLUE = (0, 0, 255);

# set up the bouncer and food data structures
FPS = 80;
foodCounter = 0;
NEWFOOD = 80;
moveCounter = 0;
CLOCKPERMOVE = 5;
FOODSIZE = 20;
player = pygame.Rect(300, 100, 40, 40);
foods = [];
for i in range(20):
    foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH- FOODSIZE),
                             random.randint(0, WINDOWHEIGHT- FOODSIZE),
                             FOODSIZE, FOODSIZE));

# set up the image
playerImage = pygame.image.load('player.png');
playerStretchedImage = pygame.transform.scale(playerImage, (40, 40));
foodImage = pygame.image.load('cherry.png');

# set up the music
pickUpSound = pygame.mixer.Sound('pickup.wav');
pygame.mixer.music.load('background.mid');
pygame.mixer.music.play(-1, 0.0);
musicPlaying = True;

# set up the movement variables
xMoveSpeed = 0;
yMoveSpeed = 0;

# set up the movement
MAXMOVESPEED = 10;
# 注意 ACCELERATION 必须大于 FRICTIONSPEED, 否则速度加不起来
ACCELERATION = 2;
FRICTIONSPEED = 1;

# run the main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit();
            sys.exit();
        if event.type == KEYDOWN:
            # change the direction when the key is pressed down
            if event.key == K_LEFT or event.key == ord('a'):
                xMoveSpeed -= ACCELERATION;
                if abs(xMoveSpeed) > MAXMOVESPEED:
                    xMoveSpeed = -MAXMOVESPEED;

            elif event.key == K_RIGHT or event.key == ord('d'):
                xMoveSpeed += ACCELERATION;
                if abs(xMoveSpeed) > MAXMOVESPEED:
                    xMoveSpeed = MAXMOVESPEED;

            if event.key == K_UP or event.key == ord('w'):
                yMoveSpeed -= ACCELERATION;
                if abs(yMoveSpeed) > MAXMOVESPEED:
                    yMoveSpeed =-MAXMOVESPEED;

            elif event.key == K_DOWN or event.key == ord('s'):
                yMoveSpeed += ACCELERATION;
                if abs(yMoveSpeed) > MAXMOVESPEED:
                    yMoveSpeed = MAXMOVESPEED;

        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit();
                sys.exit();

            if event.key == ord('x'):
                player.top = random.randint(0, WINDOWHEIGHT - player.height);
                player.left = random.randint(0, WINDOWWIDTH - player.width);

            if event.key == ord('m'):
                if musicPlaying:
                    pygame.mixer.music.stop();
                else:
                    pygame.mixer.music.play(-1, 0.0);
                musicPlaying = not musicPlaying;
                
# 减速逻辑还有一点问题，如果不反方向按键，速度没有减下来。只有按下了相反的按钮之后，速度才会减下来
# 究其原因，是因为KEYUP event只在松开按键时有效。要检测一直按下的键，需要用key_pressed()
##            if event.key != (K_ESCAPE or ord('x')):
##                if xMoveSpeed > 0:
##                    xMoveSpeed -= FRICTIONSPEED;
##                    if xMoveSpeed < 0:
##                        xMoveSpeed = 0;
##                elif xMoveSpeed < 0:
##                    xMoveSpeed += FRICTIONSPEED;
##                    if xMoveSpeed > 0:
##                        xMoveSpeed = 0;
##                        
##                if yMoveSpeed > 0:
##                    yMoveSpeed -= FRICTIONSPEED;
##                    if yMoveSpeed < 0:
##                        yMoveSpeed = 0;
##                elif yMoveSpeed < 0:
##                    yMoveSpeed += FRICTIONSPEED;
##                    if yMoveSpeed > 0:
##                        yMoveSpeed = 0;                

        if event.type == MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0]-FOODSIZE/2, event.pos[1]-FOODSIZE/2, FOODSIZE, FOODSIZE));

    # pygame.key.get_pressed()可以返回现在被按住的键的bool值
    moveCounter += 1;
    if moveCounter == CLOCKPERMOVE:
        moveCounter = 0;
        pressed = pygame.key.get_pressed();
        if pressed[K_LEFT] or pressed[K_a]:
            xMoveSpeed -= ACCELERATION;
            if abs(xMoveSpeed) > MAXMOVESPEED:
                xMoveSpeed = -MAXMOVESPEED;
        elif pressed[K_RIGHT] or pressed[K_d]:
            xMoveSpeed += ACCELERATION;
            if abs(xMoveSpeed) > MAXMOVESPEED:
                xMoveSpeed = MAXMOVESPEED;
        if pressed[K_UP] or pressed[K_w]:
            yMoveSpeed -= ACCELERATION;
            if abs(yMoveSpeed) > MAXMOVESPEED:
                yMoveSpeed =-MAXMOVESPEED;
        elif pressed[K_DOWN] or pressed[K_s]:
            yMoveSpeed += ACCELERATION;
            if abs(yMoveSpeed) > MAXMOVESPEED:
                yMoveSpeed = MAXMOVESPEED;

    ##    if not haveMovement(pressed):
        if xMoveSpeed > 0:
            xMoveSpeed -= FRICTIONSPEED;
            if xMoveSpeed < 0:
                xMoveSpeed = 0;
        elif xMoveSpeed < 0:
            xMoveSpeed += FRICTIONSPEED;
            if xMoveSpeed > 0:
                xMoveSpeed = 0;
                
        if yMoveSpeed > 0:
            yMoveSpeed -= FRICTIONSPEED;
            if yMoveSpeed < 0:
                yMoveSpeed = 0;
        elif yMoveSpeed < 0:
            yMoveSpeed += FRICTIONSPEED;
            if yMoveSpeed > 0:
                yMoveSpeed = 0;                
    

    foodCounter += 1;
    if foodCounter >= NEWFOOD:
        foodCounter = 0;
        foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH- FOODSIZE),
                                 random.randint(0, WINDOWHEIGHT- FOODSIZE),
                                 FOODSIZE, FOODSIZE));

    windowSurface.fill(BLACK);

    # move the player
    if abs(yMoveSpeed) > 0 and yMoveSpeed > 0:
        if player.bottom < WINDOWHEIGHT - yMoveSpeed:
            player.bottom += yMoveSpeed;
        else:
            player.bottom = WINDOWHEIGHT;
            # 注意这一句还挺重要的，这样靠到墙壁了之后该方向的速度能够立马减下来，如果需要反弹的话，也是这里速度改为相反方向的。yMoveSpeed = -yMoveSpeed;
            yMoveSpeed = 0;
    elif abs(yMoveSpeed) > 0 and yMoveSpeed < 0:
        if player.top > abs(yMoveSpeed):
            player.top += yMoveSpeed;
        else:
            player.top = 0;
            yMoveSpeed = 0;
            
    if abs(xMoveSpeed) > 0 and xMoveSpeed < 0:
        if player.left > abs(xMoveSpeed):
            player.left += xMoveSpeed;
        else:
            player.left = 0;
            xMoveSpeed = 0;
    elif abs(xMoveSpeed) > 0 and xMoveSpeed > 0:
        if player.right < WINDOWWIDTH - xMoveSpeed:
            player.right += xMoveSpeed;
        else:
            player.right = WINDOWWIDTH;
            xMoveSpeed = 0;
	

    # draw the player onto the surface
    windowSurface.blit(playerStretchedImage, player);
    
    # check if the bouncer has intersected with any food squares.
    # do not delete from a list while iterating through it
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food);
            player = pygame.Rect(player.left, player.top, player.width+2, player.height+2);
            playerStretchedImage = pygame.transform.scale(playerImage,
                                                          (player.width, player.height));
            if musicPlaying:
                pickUpSound.play();

    # draw the food
    for food in foods:
        windowSurface.blit(foodImage, food);
        
       
    pygame.display.update();
    #下面这句话的意思, 40 is milli-second, right? No. Actually, it's 40 frames/sec
    mainClock.tick(FPS);
    
#习题1： 将player改为圆形的。（注意改完之后，需要自己写检查是否相交的函数。这个要给出有效算法）
#习题2： 增加一个判断吃完的条件，在吃完的时候整蛊选手(DONE)，并且问是否继续(DOING)。
#习题3： 方向上增加加速减速器，即运动具有惯性。（需要把True, false的形式改为数字形式）
    #问题1： 除了keydown和keyup两种状态之外，是不是还有一种是保持按键。我现在的程序如果要加速，需要不断点那个方向的方向键。
    #问题2： 减速逻辑还有一点问题，如果不反方向按键，速度没有减下来。只有按下了相反的按钮之后，速度才会减下来
#习题4： 增加惯性的基础上，增加游戏壁的弹性，即有一定速度的player可以反弹。
