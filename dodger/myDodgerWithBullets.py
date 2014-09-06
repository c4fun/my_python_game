import pygame, sys, random;
from pygame.locals import *;

# set up constants
WINDOWWIDTH = 600;
WINDOWHEIGHT = 600;
FPS = 60;

PLAYERMOVESPEED = 5;

BADGUYMINSPEED = 1;
BADGUYMAXSPEED = 6;
BADGUYMINSIZE = 10;
BADGUYMAXSIZE = 40;
ADDNEWBADGUYRATE = 6;
ADDBULLETRATE = 18;
DEFAULTBULLETSPEED = -5 * BADGUYMAXSPEED;

# set up color
WHITE = (255, 255, 255);
BLACK = (0,0,0);
TEXTCOLOR = WHITE;
BACKGROUNDCOLOR = BLACK;

def terminate():
    pygame.quit();
    sys.exit();

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate();
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate();
                # 注意这个return是无返回值的，即void
                pygame.mouse.set_visible(False);
                return;
    
# This function is used to draw a text on a surface
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR);
    textrect = textobj.get_rect();
    textrect.topleft = (x, y);
    surface.blit(textobj, textrect);

def playerHadHitBadguy(playerRect, badguy):
    for b in badguy:
        if playerRect.colliderect(b['rect']):
            return True;
    return False;

def bulletHasHitBadguy(bulletRect, badguy):
    for b in badguy:
        if bulletRect.colliderect(b['rect']):
            return True;
    return False;

def main():
    # set up pygame, the window, and the mouse cursor
    pygame.init();
    mainClock = pygame.time.Clock();
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),pygame.FULLSCREEN);
    pygame.display.set_caption('dodger');
    pygame.mouse.set_visible(False);
    fullScreen = True;

    # set up the fonts
    font = pygame.font.SysFont(None, 48);

    # set up sounds
    gameOverSound = pygame.mixer.Sound('gameover.wav');
    pygame.mixer.music.load('background.mid');
    bulletShootingSound = pygame.mixer.Sound('Skorpion.wav');

    # set up images
    playerImage = pygame.image.load('whiteplaneblackWithExtraCannon40by40.png');
    playerRect = playerImage.get_rect();
    badguyImage = pygame.image.load('badguy.png');
    bulletImage = pygame.image.load('bullet.png');

    # show the "Start" screen
    drawText('Dodger', font, windowSurface, (WINDOWWIDTH/3), (WINDOWHEIGHT/3));
    drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH/3) -30, (WINDOWHEIGHT/3) + 50);
    pygame.display.update();
    waitForPlayerToPressKey();
    
    topScore = 0;
    while True:
        # set up the start of the game;
        badguy = [];
        score = 0;
        playerRect.topleft = (WINDOWWIDTH /2, WINDOWHEIGHT - 50);
        moveLeft = moveRight = moveUp = moveDown = False;
        reverseCheat = slowCheat = False;
        badguyAddCounter = 0;

        bullets = [];
        bulletAddCounter = 0;
        pygame.mixer.music.play(-1, 0.0);
        while True:
            score += 1;

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate();
                if event.type == KEYDOWN:
                    # change the direction when the key is pressed down
                    if event.key == ord('z'):
                        reverseCheat = True;
                    if event.key == ord('x'):
                        slowCheat = True;
                    if event.key == K_LEFT or event.key == ord('a'):
                        moveRight = False;
                        moveLeft = True;
                    elif event.key == K_RIGHT or event.key == ord('d'):
                        moveRight = True;
                        moveLeft = False;
                    if event.key == K_UP or event.key == ord('w'):
                        moveUp = True;
                        moveDown = False;
                    elif event.key == K_DOWN or event.key == ord('s'):
                        moveUp = False;
                        moveDown = True;
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        terminate();
                    if event.key == K_LEFT or event.key == ord('a'):
                        moveLeft = False;
                    elif event.key == K_RIGHT or event.key == ord('d'):
                        moveRight = False;
                    if event.key == K_UP or event.key == ord('w'):
                        moveUp = False;
                    elif event.key == K_DOWN or event.key == ord('s'):
                        moveDown = False;
                    if event.key == ord('z'):
                        reverseCheat = False;
                        score = 0;
                    elif event.key == ord('x'):
                        slowCheat = False;
                        score = 0;
                    if event.key == ord('f'):
                        if fullScreen:
                            windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT));
                            fullScreen = not fullScreen;
                        else:
                            windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),pygame.FULLSCREEN);
                            fullScreen = not fullScreen;
                        
                if event.type == MOUSEMOTION:
                    playerRect.move_ip(event.pos[0] - playerRect.centerx,
                                       event.pos[1] - playerRect.centery);

            if not (reverseCheat or slowCheat):
                badguyAddCounter += 1;
                bulletAddCounter += 1;
            if badguyAddCounter == ADDNEWBADGUYRATE:
                badguyAddCounter = 0;
                badguySize = random.randint(BADGUYMINSIZE, BADGUYMAXSIZE);
                #这里每个badguy都自己有一个surface是什么意思？就是说每一个badguy因为大小不同，所以都定义有相应的surface吧？yes
                newBadguy = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH- badguySize), 0 - badguySize, badguySize, badguySize),
                             'speed': random.randint(BADGUYMINSPEED, BADGUYMAXSPEED),
                             'surface': pygame.transform.scale(badguyImage, (badguySize, badguySize))}
                badguy.append(newBadguy);
            # Add a bullet when there are three bad guys
            if bulletAddCounter == ADDBULLETRATE:
                bulletAddCounter = 0;
                newBullet = {'rect': pygame.Rect(playerRect.left+15, playerRect.top-30, 10, 30),
                             'speed': DEFAULTBULLETSPEED,
                             'surface': pygame.transform.scale(bulletImage, (10, 30))}
                bullets.append(newBullet);
                # TODO Add bullet shooting sound
                bulletShootingSound.set_volume(0.5);
                bulletShootingSound.play();
                

            # Move the player around
            if moveLeft and playerRect.left > 0:
##                playerRect.left -= MOVESPEED;
                playerRect.move_ip(-1* PLAYERMOVESPEED, 0);
            elif moveRight and playerRect.right < WINDOWWIDTH:
                playerRect.move_ip(PLAYERMOVESPEED, 0);
            if moveDown and playerRect.bottom < WINDOWHEIGHT:
                playerRect.move_ip(0, PLAYERMOVESPEED);
            elif moveUp and playerRect.top > 0:
                playerRect.move_ip(0, -1 * PLAYERMOVESPEED);

            # Move the mouse cursor to match the player.
            # The reason we want the mouse cursor to match the location of the player's character is to avoid sudden jumps.
            pygame.mouse.set_pos(playerRect.centerx, playerRect.centery);

            # move the badguy down
            for b in badguy:
                if not reverseCheat and not slowCheat:
                    b['rect'].move_ip(0, b['speed']);
                elif reverseCheat:
                    b['rect'].move_ip(0, -5);
                elif slowCheat:
                    b['rect'].move_ip(0, 1);

            # delete the badguy that have fallen past the bottom
            for b in badguy[:]:
                if b['rect'].top > WINDOWHEIGHT:
                    badguy.remove(b);


            # move the bullet up
            for b in bullets:
                b['rect'].move_ip(0, b['speed']);

            # delete the bullet that have gone past the top
            for bul in bullets[:]:
                if bul['rect'].bottom < 0:
                    bullets.remove(bul);
                    continue;

            # delete the bullet and the badguy if they collide
            for bul in bullets[:]:
                bulletRect = bul['rect'];
                bulletHitBadguy = False;
                for b in badguy[:]:
                    if bulletRect.colliderect(b['rect']):
                        badguy.remove(b);
                        bulletHitBadguy = True;
                if bulletHitBadguy:
                    bullets.remove(bul);

                        # TODO Add boom effect (video)
                        # TODO Add boom effect (sound)

                

            # Draw the game world on the window
            windowSurface.fill(BACKGROUNDCOLOR);

            # Draw the score and top score
            drawText('Score: %s' % (score), font, windowSurface, 10, 0);
            drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40);

            # Draw the player's rectangle
            windowSurface.blit(playerImage, playerRect);

            # Draw each badguy
            for b in badguy:
                windowSurface.blit(b['surface'], b['rect']);

            # Draw each bullet
            for b in bullets:
                windowSurface.blit(b['surface'], b['rect']);

            # Check if any badguy have hit the player
            if playerHadHitBadguy(playerRect, badguy):
                if score > topScore:
                    topScore = score # set new top score
                break;

            pygame.display.update();
            mainClock.tick(FPS);


        # Stop the game and show "Game Over" screen.
        pygame.mixer.music.stop();
        gameOverSound.play();

        drawText('GAME OVER', font, windowSurface,(WINDOWWIDTH / 3), (WINDOWHEIGHT /3));
        drawText('Press a key to play again.', font, windowSurface,
                 (WINDOWWIDTH /3 ) - 80, (WINDOWHEIGHT/3) + 50);
        pygame.mouse.set_visible(True);
        pygame.display.update();
        waitForPlayerToPressKey();

        gameOverSound.stop();
   

main();

#BUG 1: 由于FPS速度有限（而每次边界检测都发生在FPS中），而鼠标速度可以很快，所以鼠标当鼠标移动很快时，可以穿越某些badguy。
#改进方法：把边界检测的频率单独提高一些。
#习题2：将人物变成飞机，并且能够打子弹消灭badguy （DONE）
#习题2.1：将人物变为飞机（DONE）
#习题2.2：将子弹发射加上声音(done, 不过加上的是scorpio枪的声音)
#习题2.3：将子弹与坏人碰撞加上爆炸效果
