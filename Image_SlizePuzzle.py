import pygame as pg
import os.path
import random
import sys
from pygame import mixer 

mixer.init() 
mixer.music.load("pop.mp3") 
mixer.music.set_volume(0.7) 

  
class Slideimagepuzzle():
   def __init__(self):
      
      window_width = 600
      window_height = 650
      
      self.tile_width = 150
      self.tile_height = 150

      self.coloumn = 4
      self.rows = 4
      icon=pg.image.load('icon.png')
      pg.display.set_icon(icon)
      self.img_list = [0,"1.png","5.png","msit.png","3.jpg","4.jpg","5.jpg","6.jpg",
                       "7.jpg","8.jpg","image7.jpg","image8.jpg",
                       "image9.jpg","image10.jpg"]

      self.empty_tile = (3,3)
      global emptyc,emptyr
      emptyc,emptyr = 3,3
      
      self.color = (255,130,130)
      white = (125,125,125)
      self.black = (0,0,0)

      self.tiles = {}

      pg.init()
      self.gameWindow = pg.display.set_mode((window_width,window_height))
      pg.display.set_caption("Sliding Image Puzzle")
      self.gameWindow.fill(white)
      pg.display.update()

      if(os.path.isfile('level.txt')):
            lfile=open('level.txt','r')
            #print(storefile)
            self.level=int(lfile.read())
            #print(self.highscore)
            lfile.close()
      else:
            self.level=1

      self.intro()
   
   def message(self,v1,u1,text):
      rect_w = 50
      rect_h = 50
      
      font = pg.font.SysFont('Arial',45)
      TextSurf = font.render(text,True,self.black)
      TextRect = TextSurf.get_rect()
      TextRect.center = ((v1*rect_w+((rect_w-3)/2)),(u1*rect_h+(rect_h/2)))
      
      self.gameWindow.blit(TextSurf,TextRect)
      pg.display.update()

   def buttons(self,text):
    
      rect_w = 50
      rect_h = 50
      color = self.color

      mouse_pos = pg.mouse.get_pos()
      click = pg.mouse.get_pressed()

      if (self.v*rect_w+rect_w-3 > mouse_pos[0] > self.v*rect_w
          and self.u*rect_h+rect_h-3 > mouse_pos[1] > self.u*rect_h):
         if int(text) <= self.level:
            color = (255,30,30)
            if click[0] == 1:
               self.start(int(text))
                
         else:
            pass

      pg.draw.rect(self.gameWindow,color,[self.v*rect_w,self.u*rect_h,rect_w-3,rect_h-3])
      self.message(self.v,self.u,text)
      #self.message(text)
      pg.display.update()

   def intro(self):

      while True:
         
         self.v = 4
         self.u = 5
         
         for event in pg.event.get():
            
            if event.type == pg.QUIT:
               pg.quit()
               sys.exit()
               
         for rec in range(1,11):
               
            self.buttons(str(rec))
            #self.message(self.v,self.u,str(rec))
              
            self.v += 1
         
            if self.v == 8:
               self.v = 4
               self.u += 1
               
#############################################################################

   def labels(self,v1,u1,text,color,size=20):
      font = pg.font.SysFont('comicsansms',size)
      TextSurf = font.render(text,True,color)
      TextRect = TextSurf.get_rect()
      #print(TextRect)
      TextRect.center = (v1,u1)
      
      self.gameWindow.blit(TextSurf,TextRect)
      pg.display.update()
      
   def check(self):

      global game_over
   
      j,k = 0,0
      tag_list = []
      
      for i in range(1,17):
         #print("checking ",i,tiles[(j,k)])
      
         tag = "tag"+str(i)
         #print(tag,j,k)
      
         if self.tiles[(j,k)][1] == tag:
            tag_list.append(tag)
            j += 1
            if j > 3:
               k += 1
               j = 0

         else:
            break

      if i == 16:
         print("GAME FINISHED")
         game_over = True

   def shift (self,c, r) :
       global emptyc, emptyr
       mixer.music.play()
       rect_color = (55,55,55)
       self.gameWindow.blit(
           self.tiles[(c, r)][0],
           (emptyc*self.tile_width, emptyr*self.tile_height))

       '''pg.draw.rect(gameWindow,black,[c*tile_width,r*tile_height,
                                   tile_width-1,tile_height-1])'''
    
       self.gameWindow.blit(
           self.tiles[self.empty_tile][0],
           (c*self.tile_width, r*self.tile_height))

       #state[(emptyc, emptyr)] = state[(c, r)]
       #state[(c, r)] = empty_tile
       
       temp = self.tiles[(c,r)]
       #print(temp,c,r)
    
       self.tiles[(c,r)] = self.tiles[(emptyc,emptyr)]
       self.tiles[(emptyc,emptyr)] = temp
       
       emptyc, emptyr = c, r

       #tiles[(emptyc, emptyr)].fill(black)
       pg.draw.rect(self.gameWindow,rect_color,[c*self.tile_width,r*self.tile_height,
                                      self.tile_width-1,self.tile_height-1])
    
       self.empty_tile = (emptyc, emptyr)
    
       #empty_tile.fill(0,0,0)
       pg.display.flip()

   def shuffle(self) :
      global emptyc, emptyr
      # keep track of last shuffling direction to avoid "undo" shuffle moves
      last_r = 0 
      for i in range(100):
         # slow down shuffling for visual effect
         pg.time.delay(40)
         while True:
            # pick a random direction and make a shuffling move
            # if that is possible in that direction
            r = random.randint(1, 4)
            if (last_r + r == 5):
               # don't undo the last shuffling move
               continue
            if r == 1 and (emptyc > 0):
               self.shift(emptyc - 1, emptyr) # shift left
            elif r == 4 and (emptyc < self.coloumn - 1):
               self.shift(emptyc + 1, emptyr) # shift right
            elif r == 2 and (emptyr > 0):
               self.shift(emptyc, emptyr - 1) # shift up
            elif r == 3 and (emptyr < self.rows - 1):
               self.shift(emptyc, emptyr + 1) # shift down
            else:
               # the random shuffle move didn't fit in that direction  
               continue
            last_r=r
            break # a shuffling move was made

   def start(self,l):
      f=1
      global level,game_over
      game_over = False
      level = l
      img = self.img_list[level]
      self.image = pg.image.load("./Res/"+img)

      self.gameWindow.fill((190,190,190))
      for r in range (self.coloumn):
      
         for c in range (self.rows):

            tag = "tag"+str(f)
         
            tile = self.image.subsurface(c*self.tile_width,r*self.tile_height,
                              self.tile_width-1,self.tile_height-1)
            f += 1
            self.tiles [(c, r)] = (tile,tag)
         
            if(c,r) == self.empty_tile:
               pg.draw.rect(self.gameWindow,(255,255,255),
                            [c*self.tile_width,r*self.tile_height,
                             self.tile_width-1,self.tile_height-1])
               break
            
            self.gameWindow.blit(tile,(c*self.tile_width,r*self.tile_height))
            pg.display.update()
            #print(tile)
          
      #print(tiles)
      text = "Level "+str(level)
      self.labels(75,625,text,(0,0,0))
      self.labels(300,625,"Click to start Game",(0,0,0))
         
      pg.display.update()

      self.gameloop()

   def gameloop(self):
   
      started = False
      show_sol = False

      global level
      #self.gameWindow.fill((190,190,190),(150,610,300,40))
   
      while True:

         if game_over:
            self.labels(300,300,"Good job well played",(0,0,0),50)
            #self.labels(300,625,"Click to next Level",(0,0,255))
      
         for event in pg.event.get():
         
            #print(event)
            if event.type == pg.QUIT:
               pg.quit()
               sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
               #print(event.type)
               #print(event.dict)
               #shuffle()
            
               if not started:
                  self.shuffle()
                  self.gameWindow.fill((190,190,190),(150,610,300,40))
                  self.labels(300,625,"Right click to see Solution",(0,0,0))
                  started = True

               if game_over:
                  level += 1
                  #self.labels(300,300,"Good job well played",(255,100,30),50)
                  #self.labels(300,625,"Click to next Level",(0,0,255))
                  if self.level < level:
                     self.level +=1
                     file = open("level.txt","w")
                     file.write(str(self.level))
                     file.close()
                  self.start(level)

               if event.dict['button'] == 1:
                  mouse_pos = pg.mouse.get_pos()
               
                  c = mouse_pos[0] // self.tile_width
                  r = mouse_pos[1] // self.tile_height
               
                  #print("dot posn",emptyc,emptyr)
                  #print("mouse posn",c,r)
               
                  if c == emptyc and r == emptyr:
                     continue
                  elif c == emptyc and (r == emptyr-1 or r == emptyr+1):
                     self.shift(c,r)
                     self.check()
                  elif r == emptyr and (c == emptyc-1 or c == emptyc+1):
                     self.shift(c,r)
                     self.check()
                  #print(c,r)

               elif event.dict['button'] == 3:
                  saved_image = self.gameWindow.copy()
                  #print(saved_image)
                  #gameWindow.fill(255,255,255)
                  self.gameWindow.blit(self.image, (0, 0))
                  pg.display.flip()
                  show_sol= True

            elif show_sol and (event.type == pg.MOUSEBUTTONUP):
               # stop showing the solution
               self.gameWindow.blit (saved_image, (0, 0))
               pg.display.flip()
               show_sol = False

if __name__ == "__main__":
   Slideimagepuzzle()



