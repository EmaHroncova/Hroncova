from tkinter import Tk, Canvas, BOTH, ALL
from tkinter.ttk import Frame
import colorsys
 
 
BAR_WIDTH = 60
BAR_HEIGHT = 1
BAR_INIT_X = 170
BAR_Y = 250
 
BOTTOM_EDGE = 270
RIGHT_EDGE = 400
 
BALL_SIZE = 3
NEAR_BAR_Y = BAR_Y - BALL_SIZE - BAR_HEIGHT
BALL_INIT_X = 200
BALL_INIT_Y = 150
 
INIT_DELAY = 800
DELAY = 30
 
class Example(Frame):
 
    def __init__(self, parent):
        Frame.__init__(self, parent)
 
        self.parent = parent
 
        self.initVariables()
        self.initBoard()
        self.after(INIT_DELAY, self.onTimer)
 
 
    def initVariables(self):
 
        self.bricks = []
        self.ballvx = self.ballvy = 3
        self.ball_x = BALL_INIT_X
        self.ball_y = BALL_INIT_Y
        self.inGame = True
 
        self.bar_x = BAR_INIT_X
        self.bar_y = BAR_Y
 
        self.lives = 3
 
 
    def initBoard(self):
 
        self.parent.title("Breakout")
        self.pack(fill=BOTH, expand=True)
 
        self.parent.config(cursor="none")
 
        self.canvas = Canvas(self, width=400, height=300,
                             background="black")
        self.canvas.bind("<Motion>", self.onMotion)
 
        self.bar = self.canvas.create_line(self.bar_x, self.bar_y,
                       self.bar_x+BAR_WIDTH, self.bar_y,
                       fill="blue")
 
        self.lives_item = self.canvas.create_text(15, 270,
                                  text=self.lives, fill="white")
 
        k = 0.0
        for j in range(10):
            for i in range(10):
 
                c =  colorsys.hsv_to_rgb(k, 0.5, 0.4)
                d = hex(int(c[0]*256)<<16 | int(c[1]*256)<<8
                    | int(c[2]*256))
                d = "#"+d[2:len(d)]
                k += 0.01
 
                brick = self.canvas.create_rectangle(40*i,
                    (j*10)+20, 40+(40*i), 30+(j*10), fill=d)
                self.bricks.append(brick)
 
        self.ball = self.canvas.create_oval(self.ball_x-BALL_SIZE,
            self.ball_y-BALL_SIZE, self.ball_x+BALL_SIZE,
            self.ball_y+BALL_SIZE, fill="#cccccc")
 
        self.canvas.pack(fill=BOTH, expand=True)
 
 
    def onMotion(self, e):
 
        if (e.x + BAR_WIDTH <= RIGHT_EDGE):
            self.bar_x = e.x
 
 
    def onTimer(self):
 
        if self.inGame:
            self.doCycle()
            self.checkCollisions()
            self.after(DELAY, self.onTimer)
        else:
            self.gameOver()
 
 
    def doCycle(self):
 
        self.ball_x += self.ballvx
        self.ball_y += self.ballvy
 
        self.canvas.coords(self.ball, self.ball_x - BALL_SIZE,
            self.ball_y - BALL_SIZE, self.ball_x + BALL_SIZE,
            self.ball_y + BALL_SIZE)
 
        self.canvas.coords(self.bar, self.bar_x, self.bar_y,
            self.bar_x+BAR_WIDTH, self.bar_y)
 
        if (len(self.bricks) == 0):
            self.msg = "Game won"
            self.inGame = False
 
 
    def checkCollisions(self):
 
        if (self.ball_x >= RIGHT_EDGE or self.ball_x <= 0):
            self.ballvx *= -1
 
        if (self.ball_y <= 0):
            self.ballvy *= -1
 
        for brick in self.bricks:
 
            hit = 0
            co = self.canvas.coords(brick)
 
            if (self.ball_x > co[0] and self.ball_x < co[2]
                and self.ball_y + self.ballvy > co[1]
                and self.ball_y + self.ballvy < co[3]):
 
                hit = 1
                self.ballvy *= -1
 
            if (self.ball_x + self.ballvx > co[0]
                and self.ball_x + self.ballvx < co[2]
                and self.ball_y > co[1]
                and self.ball_y < co[3]):
 
                hit = 1
                self.ballvx *= -1
 
            if (hit == 1):
 
                self.bricks.remove(brick)
                self.canvas.delete(brick)
 
        if ((self.ball_y == NEAR_BAR_Y and self.ball_y < self.bar_y)
            and (self.ball_x > self.bar_x
                 and self.ball_x < self.bar_x + BAR_WIDTH)):
 
            self.ballvy *= -1
 
        if (self.ball_y == NEAR_BAR_Y
            and self.ball_x < self.bar_x + BAR_WIDTH/2
            and self.ball_x > self.bar_x
            and self.ballvx > 0):
 
            self.ballvx *= -1
 
        if (self.ball_y == NEAR_BAR_Y
            and self.ball_x > self.bar_x + BAR_WIDTH/2
            and self.ball_x < self.bar_x + BAR_WIDTH
            and self.ballvx < 0):
 
            self.ballvx *= -1
 
        if (self.ball_y > BOTTOM_EDGE):
 
            self.lives -= 1
            self.canvas.delete(self.lives_item)
            self.lives_item = self.canvas.create_text(15, 270,
                                      text=self.lives, fill="white")
 
            if self.lives == 0:
 
                self.inGame = False
                self.msg = "Game lost"
            else:
 
                self.ball_x = BALL_INIT_X
                self.ball_y = BALL_INIT_Y
 
 
    def gameOver(self):
 
        self.canvas.delete(ALL)
        self.canvas.create_text(self.winfo_width()/2,
            self.winfo_height()/2, text=self.msg, fill="white")
 
 
def main():
 
    root = Tk()
    ex = Example(root)
    root.geometry("+300+300")
    root.mainloop()
 
 
if __name__ == '__main__':
    main()
