# Auteur : JM-1000


import pygame,random

size=25
wid=800
H=600
txt_color=255,255,255

class Egg:
    def __init__(self,win):
        self.win=win
        self.block=pygame.image.load('./resource/egg.jpg').convert()
        self.x=size*5
        self.y=size

    def draw(self):
        self.win.blit(self.block,(self.x,self.y))

    def change(self):
         self.x=random.randint(0,wid//size-1)*size
         self.y=random.randint(0,H//size-1)*size


class Snake:
    def __init__(self,win):
        self.len=1
        self.win=win
        self.block=pygame.image.load('./resource/snake.jpg').convert()
        self.x=[size]
        self.y=[size]
        self.to='R'

    def increase(self):
         self.len+=1
         self.x.append(-1)
         self.y.append(-1)
    
    def draw(self):
        for i in range(self.len):
            self.win.blit(self.block,(self.x[i],self.y[i]))

    def setTo(self,to):
         self.to=to
       
    def move(self):
        for i in range(self.len-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.to=='L':
            self.x[0] -=size
        elif self.to=='R':
            self.x[0] +=size
        elif self.to=='U':
            self.y[0] -=size
        elif self.to=='D':
            self.y[0] +=size
        self.draw()    
              
     
class Jeu:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.surface=pygame.display.set_mode((wid,H))
        self.snake=Snake(self.surface)
        self.snake.draw()
        self.egg=Egg(self.surface)
        self.egg.draw()
        self.sound('bg',True)

        self.paused=False
        
        
    def collisions(self,x1,y1,x2,y2):
        if x1>=x2 and x1<x2+size:
            if y1>=y2 and y1<y2+size:
                self.egg.change()
                return True
              
    def mur_collisions(self):
        if self.snake.x[0]<0 or self.snake.x[0]>wid-size or self.snake.y[0]<0 or self.snake.y[0]>H-size:
            self.sound("crash")
            pygame.mixer.music.pause()
            self.display_over()

    
    def sound(self,file,bg=False):
        file="./resource/{}.mp3".format(file)
        if bg:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(100)
            pygame.mixer.music.set_volume(0.2)
            
        else:
            s=pygame.mixer.Sound(file)
            pygame.mixer.Sound.play(s)
            pygame.mixer.Sound.set_volume(s,0.25)
     
    
    def background(self):
        bg = pygame.image.load('./resource/bg.jpg')
        self.surface.blit(bg,(0,0))


    def display_score(self):
         font=pygame.font.SysFont('arial',25)
         score=font.render(f"Score :   {self.snake.len}",True,(txt_color))
         self.surface.blit(score,(650,10))
         score=font.render(f"Niveau : {niveau}",True,(txt_color))
         self.surface.blit(score,(650,40))


    def display_over(self):
        self.background()
        font=pygame.font.SysFont('arial',25)
        score=font.render(f"Tu a perdu! Ton score : {self.snake.len}",True,(txt_color))
        self.surface.blit(score,(wid/4,H/2.5))
        score=font.render(f"Appuyer Enter pour recommencer le jeu...",True,(txt_color))
        self.surface.blit(score,(wid/4,H/2.5+40))
        self.paused=True


    def restart(self):
        pygame.mixer.music.unpause()
        self.snake=Snake(self.surface)
        self.apple=Egg(self.surface)
        self.paused=False


    def play(self):
        self.background()
        self.snake.move()
        self.egg.draw()
        self.display_score()

        self.mur_collisions()

        if self.collisions(self.snake.x[0],self.snake.y[0],self.egg.x,self.egg.y): 
            self.sound("eat")
            self.snake.increase()
        
        for i in range(2,self.snake.len):
            if self.collisions(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.sound("crash")
                pygame.mixer.music.pause()
                self.display_over()    
        
        
    def run(self):
        global niveau
        clock=pygame.time.Clock()
        delay,ancien_len,niveau=40,1,1

        while True:
            if ancien_len!=self.snake.len and self.snake.len%10==0:
                delay-=3
                niveau+=1
                ancien_len=self.snake.len 
                  
            
            pygame.time.delay(delay)
            clock.tick(50)
            for E in pygame.event.get():
                if E.type==pygame.QUIT:
                    pygame.quit()

                keys=pygame.key.get_pressed()
                for key in keys:
                    if keys[pygame.K_LEFT] or keys[113]:
                        self.snake.setTo('L')
                    elif keys[pygame.K_RIGHT] or keys[100]:
                        self.snake.setTo('R')
                    elif keys[pygame.K_UP] or keys[122]:
                        self.snake.setTo('U')
                    elif keys[pygame.K_DOWN] or keys[119]:
                        self.snake.setTo('D')
                    elif self.paused and keys[pygame.K_RETURN]:
                        self.restart()
                        delay,niveau=40,1
                            
            if not self.paused: self.play()
            pygame.display.update()
            

if __name__=='__main__': Jeu().run()