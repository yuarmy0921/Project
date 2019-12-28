#建立遊戲素材
import pygame
import random 
import math
import numpy as np
import os, sys
import time
import cv2
from pygame.locals import *
from pygame.compat import geterror
#pygame.image.load()預設得到的type是surface
#pygame.sprite.Group.update：call the update method
def load_image(name, prev, colorkey = None):
    '''
    把圖片載下來
    '''
    fullname = os.path.join('game_material/'+prev+"/", name)
    try:
        #pygame.image.load(圖片檔案路徑)
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image: ', name)
        raise SystemExit(message)
    #把圖片轉換成最適合呈現的樣子
    image = image.convert_alpha()
    if colorkey is not True:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    #get_rect():把rect設定成圖片大小
    return image, image.get_rect()

def load_sound(name):
    #如果沒有成功載入音樂就不撥放
    class NoneSound:
        def play(self): pass
    #pygame.mixer：撥放音樂的module
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('game_material/voice/', name)
    print(fullname)
    try:
        #create a new sound object
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load a sound: ', name)
        raise SystemExit(message)
    return sound

#玩家
class Player(pygame.sprite.Sprite):
    '''
    隨著滑鼠移動，滑鼠要換成圖片!!!!!!
    碰到迷宮邊界則損血
    碰到NPC回血
    不會呼叫外面的參數
    只有玩家用pos，其他都用x y
    rect吃四個參數(左上角x座標, 左上角y座標, 長, 寬)
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.screen = None
        self.dead = False
        #被取代成滑鼠的圖片，已經convert完了
        # 回來改圖片！不要讓你家寶貝變成barrier！他會哭！QQ
        self.image, self.rect = load_image("huahua.png","main_pic")
        self.save_image = self.image
        #self.image, self.rect = pygame.surface.Surface((10, 10)), pygame.Rect((10, 10), (10, 10))
        #把圖片轉成可以快速貼到螢幕上的形式
        self.image = self.image.convert_alpha()
        self.size_half= (self.rect[2]//2, self.rect[3]//2)
        pygame.mouse.set_visible(False)
        #初始位置
        #因為是滑鼠所以要這樣用
        #這個用來記錄滑鼠當前位置
        self.start = (160, 170)
        self.finish = (1240, 740)
        self.pos = (160, 170)
        self.last_pos = (160, 170)
        self.dx, self.dy = None, None
<<<<<<< HEAD
        self.save_rect = None
        pygame.mouse.set_pos([x, y])
        self.rect[0], self.rect[1] = self.pos[0]-self.size_half[0], self.pos[1]-self.size_half[1]


=======
        self.rect[0], self.rect[1] = self.pos[0]-self.size_half[0], self.pos[1]-self.size_half[1]
        pygame.mouse.set_pos([self.pos[0], self.pos[1]])
>>>>>>> 23b15f58981853b5e268da84bb6db7ceb8e2d8d7
        #設定玩家血量，然後顯示血條：調整到難易適中，還要再回來設定!!!!!!!!!
        self.blood = 300
        #長150寬20
        self.blood_surface = pygame.Surface((self.blood, 20))
        self.blood_surface.fill((255,0,0))
        self.empty_surface = pygame.Surface((300, 20))
        self.empty_surface.fill((255, 255, 255))
        #然後玩家的初始設定大概差不多就結束了
        self.scream = load_sound("scream.wav")

    def walk(self):
<<<<<<< HEAD
        self.pos = pygame.mouse.get_pos()
        self.dx, self.dy = self.pos[0]-self.last_pos[0]-self.size_half[0], self.pos[1]-self.last_pos[1]-self.size_half[1]
        self.rect.move_ip(self.dx, self.dy)
=======
        #self.pos = pygame.mouse.get_pos()
        #self.dx, self.dy = self.pos[0]-self.last_pos[0]-self.size_half[0], self.pos[1]-self.last_pos[1]-self.size_half[1]
        #self.rect.move_ip(self.dx, self.dy)
        self.rect[0], self.rect[1] = self.pos[0], self.pos[1]
>>>>>>> 23b15f58981853b5e268da84bb6db7ceb8e2d8d7
        '''
        #計算位置更新前後座標的大小
        #往哪邊移
        #左上
        if self.rect[0] < self.last_pos[0] and self.rect[1] < self.last_pos[1]:
            self.save_rect = pygame.Rect(self.rect[0], self.rect[1], self.rect[2]+abs(self.dx), self.rect[3]+abs(self.dy))
        #左下
        if self.rect[0] < self.last_pos[0] and self.rect[1] > self.last_pos[1]:
            self.save_rect = pygame.Rect(self.rect[0], self.last_pos[1], self.rect[2]+abs(self.dx), self.rect[3]+abs(self.dy))
        #右上
        if self.rect[0] > self.last_pos[0] and self.rect[1] < self.last_pos[1]:
            self.save_rect = pygame.Rect(self.last_pos[0], self.rect[1], self.rect[2]+abs(self.dx), self.rect[3]+abs(self.dy))
        #右下
        if self.rect[0] > self.last_pos[0] and self.rect[1] > self.last_pos[1]:
            self.save_rect = pygame.Rect(self.last_pos[0], self.last_pos[1], self.rect[2]+abs(self.dx), self.rect[3]+abs(self.dy))
        '''

    def stepback(self):
        self.rect.move_ip(self.last_pos[0], self.last_pos[1])
        self.pos = (self.rect[0], self.rect[1])

    def recover(self):
        #調血量!!!!!!!!!!!!
        if self.blood <= 290:
            self.blood += 10
            self.blood_surface = pygame.Surface((self.blood, 20))
            self.blood_surface.fill((255,0,0))
        else:
            self.blood = 300
            self.blood_surface = pygame.Surface((self.blood, 20))
            self.blood_surface.fill((255,0,0))


    def injure(self, times, play):
        '''
        這裡完成了!!!!!!!!!!!!!!!!!!!!!!!!!!!
        '''
        if play:
            self.scream.play()
        #血條減少(一次把兩個surface貼上去)
        #這裡要調整難度!!!!!!!!!!!!!!!!!現在可以被摸15次
        for round in range(times):
            self.blood -= 0
            if self.blood > 0:
                self.blood_surface = pygame.Surface((self.blood, 20))
                self.blood_surface.fill((255,0,0))
<<<<<<< HEAD
=======
                self.screen.blits(((self.empty_surface, (570, 50)), (self.blood_surface, (570, 50))))
                pygame.display.update(self.empty_surface.get_rect())
>>>>>>> 23b15f58981853b5e268da84bb6db7ceb8e2d8d7
                
            else:
                self.dead = True
    def update(self):
        #把所有東西都畫上去
        #人的部分
<<<<<<< HEAD
        self.draw(screen)
        #血條的部分
        screen.blits(((empty_surface, (500, 150)), (blood_surface, (500, 150))))
=======
        self.screen.blit(self.image, self.rect)
        #血條的部分
        self.screen.blits(((self.empty_surface, (570, 50)), (self.blood_surface, (570, 50))))
        pygame.display.update(self.rect)
>>>>>>> 23b15f58981853b5e268da84bb6db7ceb8e2d8d7
    
class BTS(pygame.sprite.Sprite):
    '''
    不用管分別的技能是甚麼，反正只要碰到就損血，另外寫碰到玩家時的行為
    設定進行速度
    把外界參數抓進來用(判斷碰撞)
    移動模式可能要改一下(不是隨機移動，不然會像撞球，從哪邊碰到障礙物也很難判斷)
    '''
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.Surface((10, 10))
        self.image, self.rect = pygame.surface.Surface((10, 10)), pygame.Rect(0, 0, 10, 10)
        self.dx, self.dy = 2, 2
        self.speed = 2
        self.skill = None 
<<<<<<< HEAD
        self.skill_flag = False
        

    def stepback(self):
        self.move_ip(-self.dx, -self.dy)
=======
        #要再建立維持技能的計時器!!!!!!!!
        #貼上特效再受傷!!!!!!!!!!!!!!!!!!
        self.skill_flag = False
        self.skill_flag_pic = False
        self.sound_flag = False
        self.rect.clamp_ip(pygame.Rect(0, 0, 1440, 800))
        

    def stepback(self):
        self.rect.move_ip(-self.dx, -self.dy)
>>>>>>> 23b15f58981853b5e268da84bb6db7ceb8e2d8d7

    def change_dir(self):    
        direction = random.randint(0, 360)
        radian = math.radians(direction)
        self.dx = self.speed*math.cos(radian)
        self.dy = self.speed*math.sin(radian)

    def walk(self):
        self.rect.move_ip(self.dx, self.dy)
        
    def update(self):
<<<<<<< HEAD
        self.draw(screen)
=======
        self.walk()
        self.screen.blit(self.image, self.rect)
        pygame.display.update(self.rect)
>>>>>>> 23b15f58981853b5e268da84bb6db7ceb8e2d8d7



class NPC(pygame.sprite.Sprite):
    '''
    技能都一樣，差別在於對話框不同
    遇到邊界要後退
    遇到玩家或NPC不能疊上去
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.screen = None
        self.image, self.rect = pygame.surface.Surface((10, 10)), pygame.Rect(0, 0, 10, 10)
        self.rect.clamp_ip(pygame.Rect(0, 0, 1440, 800))
        self.save_image = None
        self.size = (self.rect[2], self.rect[3])
        self.speed = 10
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        #上一個按下的按鍵
        self.prev = None
        #對話內容
        talk_font = pygame.font.Font("game_material/font/HanaMin/HanaMinA.ttf", 10)
        self.alltalk = None
        
    def Up(self):
        self.prev = self.up
        self.rect.move_ip(0, -self.speed)
    def Down(self):
        self.prev = self.down
        self.rect.move_ip(0, self.speed)
    def Left(self):
        self.prev = self.left
        self.rect.move_ip(-self.speed, 0)
    def Right(self):
        self.prev = self.right
        self.rect.move_ip(self.speed, 0)

    def stepback(self):    
        '''
        碰到障礙物
        已經寫好啦!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        '''
        if self.prev == self.up:
            self.rect.move_ip(0, 5)
        elif self.prev == self.down:
            self.rect.move_ip(0, -5)
        elif self.prev == self.left:
            self.rect.move_ip(5, 0)
        elif self.prev == self.right:
            self.rect.move_ip(-5, 0)
        else:
            pass
    
    '''
    def trash_talk(self):
        
        碰到玩家
        講一些幹話
        
        class Talk(pygame.sprite.Sprite):
            def __init__(self, talk):
                pygame.sprite.Sprite.__init__(self)
                #從一群對話中隨機選出一句，對話放頭上(名字以上)，決定適當的距離!!!!!!!!!!
                self.talk = talk
                #convert()：建立副本
                self.talk = self.talk.convert()
                #文字框根據對話的長度來決定
                self.talk_bg = pygame.Surface((self.talk.get_width(), self.talk.get_height()))
                self.talk_bg.fill((255, 255, 255))
                self.talk_bg = self.talk_bg.convert()
                self.talk_bg.blit(self.talk, (0, 0))
                self.image, self.rect = self.talk_bg, 
        #建立計時器，維持幾秒
        #先這樣!!!!!!!!!!!!!!!!!!
        random_talk = self.alltalk[random.randint(0, len(self.alltalk)-1)]
        random_talk = pygame.sprite.GroupSingle(Talk(random_talk))
        screen.blit((random_talk.talk_bg, (self.x, self.y + 10)))
        pygame.time.wait(5000)
        #移除對話
<<<<<<< HEAD
'''
    def update(self):
        self.draw(screen)
=======
    '''
    def update(self):
        self.screen.blit(self.image, self.rect)
        pygame.display.update(self.rect)

def Resize(path, unit):
    image = cv2,imread(path)
    image = cv2.resize(image, (unit,unit))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image
>>>>>>> 23b15f58981853b5e268da84bb6db7ceb8e2d8d7

class MazeBarrier(pygame.sprite.Sprite):

    def __init__(self, position, row, col, unit, maze, x,y): # position是傳進行與列
        super().__init__()
        self.position = position
        self.unit = unit

        barrier_image = Resize("./game_material/main_pic/barrier.png",self.unit)
        maze[x*2+row*unit:x*2+row*unit+unit, y+col*unit:y+col*unit+unit, :] = barrier_image
        self.image = pygame.surfarray.make_surface(np.transpose(barrier_image ,(1,0,2)))
        self.rect = pygame.Rect(position, barrier_image.shape[:2])

        fire_image = Resize("./game_material/main_pic/fire.png", self.unit)
        self.fire_image = pygame.surfarray.make_surface(np.transpose(fire_image, (1,0,2)))
        self.fire_rect = self.rect.copy()
    
    def fire(self):
        # 每一個障礙物都會燒起來！
        ori_image = self.image
        quit_flag = False
        clock = pygame.time.Clock()
        while not quit_flag:
            if t > 1:
                quit_flag = True
            clock.tick(30)
            self.image = self.fire_image.subsurface(self.fire_rect)
            t += 1
        self.image = ori_image
     
class Maze(pygame.sprite.Sprite):

    def __init__(self, position, texture):
        super().__init__()
        self.texture = texture
        self.image = pygame.surfarray.make_surface(np.transpose(texture, (1,0,2)))
        self.rect = pygame.Rect(position,self.texture.shape[:2])

<<<<<<< HEAD
<<<<<<< HEAD
# 遊戲最最初始值設定，主程式一定是要先跑這個，阿然後可能還要再call NPC and BTS
=======
>>>>>>> e065b04
class MazeGame(Player, NPC, BTS):
=======
class MazeGame:
>>>>>>> 23b15f58981853b5e268da84bb6db7ceb8e2d8d7

    def __init__(self):
        unit = 15
        width, height = 1440, 800
        maze_width, maze_height = 1140, 650

        # The following attributes will be initialized later
        self.player = Player()
        self.npc1 = NPC()
        self.npc2 = NPC()
        self.bts1 = BTS()
        self.bts2 = BTS()
        self.bts3 = BTS()
        self.bts4 = BTS()
        self.bts5 = BTS()
        self.bts6 = BTS()
        self.bts7 = BTS()
        self.maze = None
        self.barriers = []
        self.exit_point = None
<<<<<<< HEAD
<<<<<<< HEAD

=======
        #self.NPC = NPC()
        #self.BTS = BTS()
>>>>>>> e065b04
=======
>>>>>>> 23b15f58981853b5e268da84bb6db7ceb8e2d8d7
       
        # Build Maze
        with open(("maze.txt"), "r") as f:
            # Reserve space for maze
            lines = f.read().strip("\n").split("\n") # Read the map
            maze = np.zeros((height, width, 3))
            # numpy shape (height, width, depth)
            # cv2.resize(image,(width, height))
            # [height, width,:]

            # resize bg
            bg = cv2.imread("./game_material/main_pic/mars.jpg")
            bg = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
            bg = cv2.resize(bg, (maze_width, maze_height))
            x, y = (height - maze_height)//2, (width - maze_width)//2
            maze[x*2:x*2+maze_height, y:y+maze_width, :] = bg
            # 左上角：(150, 75)

            # Initialize maze row by row
            for row, line in enumerate(lines):
                for col, symbol in enumerate(line):
                    if symbol == '0': # 障礙物
                        # Create barrier
                        barrier = MazeBarrier((col*unit, row*unit),row,col,unit,maze,x,y)
                        self.barriers.append(barrier)
                    elif symbol == '1': # 路，不需要load image，用背景即可
                        pass
                    elif symbol == 'S': # 起點
                        # 設成green
                        maze[x*2+row*unit:x*2+row*unit+unit, y+col*unit:y+col*unit+unit, 1] = 255

                        # Create player
                        #self.player = Player((col*unit, row*unit))
                        # 我想要做的是，是在傳player位置，安捏干丟？？？？
                    elif symbol == 'F': # 終點
                        # 設成blue
                        maze[x*2+row*unit:x*2+row*unit+unit, y+col*unit:y+col*unit+unit, 2] = 255

                        # Record the exit point
                        self.exit_point = (col*unit, row*unit)
                    else:
                        raise Exception("Invalid symbol in maze '%s'" % symbol)
        # Save maze
        self.maze = Maze((0,0), maze.copy())
        
        # Create groups
        self.barrier_group = pygame.sprite.Group(self.barriers)