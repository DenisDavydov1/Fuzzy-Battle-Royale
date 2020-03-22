"""
from tkinter import *
import mamdani
import random

# GLOBAL VARIABLES
# global field size
WIDTH = 600
HEIGHT = 600

# pad size
PAD_W = 10
PAD_H = 100

class Ball:
    # ball radius
    ball_radius = 10

    def __init__(self, canvas):
        self.BALL = canvas.create_oval(WIDTH / 2 - self.ball_radius / 2,
                                       HEIGHT / 2 - self.ball_radius / 2,
                                       WIDTH / 2 + self.ball_radius / 2,
                                       HEIGHT / 2 + self.ball_radius / 2,
                                       fill="white")

    # ball velocity growth
    ball_speed_up = 1.05
    ball_max_speed = 40
    ball_x_speed = random.choice([-8,-7,-6,-5,-4,-3,3,4,5,6,7,8])
    ball_y_speed = random.choice([-8,-7,-6,-5,-4,-3,3,4,5,6,7,8])

    # ball movement function
    def move_ball(self):
        # find ball sides and center coordinates
        ball_left, ball_top, ball_right, ball_bot = c.coords(self.BALL)
        ball_center = (ball_top + ball_bot) / 2

        # vertical bounce
        # if ball is far from vertical lines
        if ball_right + self.ball_x_speed < right_line_distance and \
                ball_left + self.ball_x_speed > PAD_W:
            c.move(self.BALL, self.ball_x_speed, self.ball_y_speed)

        # if ball touches field boarder with its left or right sides
        elif ball_right == right_line_distance or ball_left == PAD_W:
            if ball_right > WIDTH / 2:
                if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                    self.bounce(("strike", RIGHT_PAD_SPEED))
                else:
                    update_score("right")
                    self.spawn_ball()
            else:
                if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                    self.bounce(("strike", LEFT_PAD_SPEED))
                else:
                    update_score("left")
                    self.spawn_ball()
        # if the ball goes out of game field
        else:
            if ball_right > WIDTH / 2:
                c.move(self.BALL, right_line_distance - ball_right, self.ball_y_speed)
            else:
                c.move(self.BALL, -ball_left + PAD_W, self.ball_y_speed)
        # horizontal bounce
        if ball_top + self.ball_y_speed < 0 or ball_bot + self.ball_y_speed > HEIGHT:
            self.bounce(("ricochet"))

    # ball initial speed after respawn
    initial_speed = 5

    # ball respawn function
    def spawn_ball(self):
        #global BALL_X_SPEED
        # set ball on center
        c.coords(self.BALL,
                 WIDTH / 2 - self.ball_radius / 2,
                 HEIGHT / 2 - self.ball_radius / 2,
                 WIDTH / 2 + self.ball_radius / 2,
                 HEIGHT / 2 + self.ball_radius / 2)
        # set ball movement direction to loser with initial speed
        self.ball_x_speed = -(self.ball_x_speed * -self.initial_speed) / abs(self.ball_x_speed)
        self.ball_y_speed = random.randrange(-10, 10)

    # get ball center coords
    def ball_center(self):
        ball_left, ball_top, ball_right, ball_bot = c.coords(self.BALL)
        return (ball_top + ball_bot) / 2, (ball_left + ball_right) / 2

    # ball bounce function
    def bounce(self, action):
        # global BALL_X_SPEED, BALL_Y_SPEED
        # pad hit
        if action[0] == "strike":
            # BALL_Y_SPEED = random.randrange(-10, 10)
            if abs(self.ball_x_speed) < self.ball_max_speed:
                self.ball_x_speed *= -self.ball_speed_up
                self.ball_y_speed += action[1] * 0.05
            else:
                self.ball_x_speed = -self.ball_x_speed
        else:
            self.ball_y_speed = -self.ball_y_speed

    # get ball center coordinates
    def ball_coords(self, pad):
        x, y = self.ball_center()
        # print(x, y)
        # print(c.coords(LEFT_PAD)[3] - PAD_H/2)
        # print(x - c.coords(LEFT_PAD)[3] + (PAD_H/2))
        return (x - c.coords(pad)[3] + (PAD_H / 2)), y


# WINDOW SETTINGS
# set window
root = Tk()
root.title("Cyka Blyat")

# animation area
c = Canvas(root, width=WIDTH, height=HEIGHT, background="black")
c.pack()

# GAME ELEMENTS
# left line
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
# right line
c.create_line(WIDTH-PAD_W, 0, WIDTH-PAD_W, HEIGHT, fill="white")
# central line
c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="white")


# create left pad
LEFT_PAD = c.create_line(PAD_W/2, 0, PAD_W/2, PAD_H,
                         width=PAD_W, fill="#1E90FF")
# create right pad
RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2,
                          PAD_H, width=PAD_W, fill="yellow")


BALL = Ball(c)
BALL1 = Ball(c)


# PADS MOVE GLOBALS
PAD_SPEED = 20
LEFT_PAD_SPEED = 0
RIGHT_PAD_SPEED = 0


def move_pads():
    PADS = {LEFT_PAD: LEFT_PAD_SPEED,
            RIGHT_PAD: RIGHT_PAD_SPEED}
    for pad in PADS:
        c.move(pad, 0, PADS[pad])
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])

def main():
    BALL.move_ball()
    BALL1.move_ball()
    mamdani_move()
    move_pads()
    root.after(30, main)


# set focus on canvas for keyboard reaction
c.focus_set()


# MAMDANI
mamdani_x = mamdani.Variable("X",
                             {"Left": (-600,-599,-50,0), "Center": (-50,0,50), "Right": (0,50,599,600)},
                             (-600, 600))
mamdani_y = mamdani.Variable("Y",
                             {"Close": (0,1,100,110), "Far": (100,110,299,300)},
                             (0, 300))

mamdani_rules = mamdani.Rule()
mamdani_rules.add_rule(("Left", "Far"), -10)
mamdani_rules.add_rule(("Left", "Close"), -15)
mamdani_rules.add_rule(("Right", "Far"), 10)
mamdani_rules.add_rule(("Right", "Close"), 15)
mamdani_rules.add_rule(("Center", "Far"), 0)
mamdani_rules.add_rule(("Center", "Close"), 0)


def mamdani_move():
    global LEFT_PAD_SPEED
    coords = BALL.ball_coords(LEFT_PAD)
    coords1 = BALL1.ball_coords(LEFT_PAD)
    if coords[1] < coords1[1]:
        LEFT_PAD_SPEED = mamdani_rules.defuzzification(mamdani.get_conditions({mamdani_x: coords[0], mamdani_y: coords[1]}, "max"))
    else:
        LEFT_PAD_SPEED = mamdani_rules.defuzzification(mamdani.get_conditions({mamdani_x: coords1[0], mamdani_y: coords1[1]}, "max"))


# keyboard press handle
def movement_handler(event):
    global RIGHT_PAD_SPEED
    if event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED


# reaction on button release
def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in ("w", "s"):
        LEFT_PAD_SPEED = 0
    elif event.keysym in ("Up", "Down"):
        RIGHT_PAD_SPEED = 0


# bind keyboard control
c.bind("<KeyPress>", movement_handler)
c.bind("<KeyRelease>", stop_pad)

# GAME PROCESS GLOBALS

# distance to right game field boarder
right_line_distance = WIDTH - PAD_W




# GAME SCORING
PLAYER_1_SCORE = 0
MAMDANI_SCORE = 0

# print players scores
p_1_text = c.create_text(WIDTH-WIDTH/6, PAD_H/4,
                         text=PLAYER_1_SCORE,
                         font="Arial 20",
                         fill="white")
mamdani_name = c.create_text(55, PAD_H/4,
                             text="Mamdani",
                             font="Arial 10",
                             fill="#1E90FF")
mamdani_text = c.create_text(WIDTH / 6, PAD_H / 4,
                             text=MAMDANI_SCORE,
                             font="Arial 20",
                             fill="white")

# scores update function
def update_score(player):
    global PLAYER_1_SCORE, MAMDANI_SCORE
    if player == "right":
        PLAYER_1_SCORE -= 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        MAMDANI_SCORE -= 1
        c.itemconfig(mamdani_text, text=MAMDANI_SCORE)






# enable movement
main()

# enable window
root.mainloop()
"""
"""
class Block:
    def __init__(self, master):
        self.e = Entry(master, width=20)
        self.b = Button(master, text="Convert")
        self.l = Label(master, bg='black', fg='white', width=20)
        self.e.pack()
        self.b.pack()
        self.l.pack()

    def setFunc(self, func):
        self.b['command'] = eval('self.' + func)

    def strToSortList(self):
        s = self.e.get()
        s = s.split()
        s.sort()
        self.l['text'] = ' '.join(s)

    def strReverse(self):
        s = self.e.get()
        s = s.split()
        s.reverse()
        self.l['text'] = ' '.join(s)

root = Tk()
first_block = Block(root)
first_block.setFunc('strToSortList')
second_block = Block(root)
second_block.setFunc('strReverse')
root.mainloop()
"""


