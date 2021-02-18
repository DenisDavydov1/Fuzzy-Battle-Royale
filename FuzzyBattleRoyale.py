from tkinter import *
import base
import Mamdani
import Tsukamoto
import Larsen
import Sugeno
import random
import math

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
        ball_center_v = (ball_top + ball_bot) / 2
        ball_center_h = (ball_left + ball_right) / 2
        # if ball is far from vertical lines
        if ball_left + self.ball_x_speed > PAD_W and \
                ball_right + self.ball_x_speed < WIDTH - PAD_W and \
                ball_top + self.ball_y_speed > PAD_W and \
                ball_bot + self.ball_y_speed < HEIGHT - PAD_W:
            c.move(self.BALL, self.ball_x_speed, self.ball_y_speed)

        # if ball touches field boarder with its left or right sides
        elif ball_left - 15 <= PAD_W and ball_top - 10 > PAD_W and ball_bot + 10 < HEIGHT-PAD_W:
            if c.coords(LEFT_PAD)[1] < ball_center_v < c.coords(LEFT_PAD)[3]:
                self.bounce(("strike", LEFT_PAD_SPEED), 'v')
            else:
                update_score("left")
                self.spawn_ball()
        elif ball_right + 15 >= WIDTH - PAD_W and ball_top - 10 > PAD_W and ball_bot + 10 < HEIGHT-PAD_W:
            if c.coords(RIGHT_PAD)[1] < ball_center_v < c.coords(RIGHT_PAD)[3]:
                self.bounce(("strike", RIGHT_PAD_SPEED), 'v')
            else:
                update_score("right")
                self.spawn_ball()
        # if ball touches field boarder with its top or bottom sides # HERE: condition for TOP
        elif ball_bot + 15 >= HEIGHT-PAD_W and ball_left - 10 > PAD_W and ball_right + 10 < WIDTH-PAD_W:
            if c.coords(BOTTOM_PAD)[0] < ball_center_h < c.coords(BOTTOM_PAD)[2]:
                self.bounce(("strike", BOTTOM_PAD_SPEED), 'h')
            else:
                update_score("bottom")
                self.spawn_ball()
        elif ball_top - 15 <= PAD_W and ball_left - 10 > PAD_W and ball_right + 10 < WIDTH-PAD_W:
            if c.coords(TOP_PAD)[0] < ball_center_h < c.coords(TOP_PAD)[2]:
                self.bounce(("strike", TOP_PAD_SPEED), 'h')
            else:
                update_score("top")
                self.spawn_ball()
        else:
            self.spawn_ball()

    # ball initial speed after respawn
    initial_speed = 5

    # ball respawn function
    def spawn_ball(self):
        # set ball on center
        c.coords(self.BALL,
                 WIDTH / 2 - self.ball_radius / 2,
                 HEIGHT / 2 - self.ball_radius / 2,
                 WIDTH / 2 + self.ball_radius / 2,
                 HEIGHT / 2 + self.ball_radius / 2)
        # set ball movement direction to loser with initial speed
        self.ball_x_speed = random.choice([-5,-4,-3,3,4,5])
        self.ball_y_speed = random.choice([-5,-4,-3,3,4,5])

    # ball bounce function
    def bounce(self, action, side):
        # pad hit
        if action[0] == "strike" and side == 'v':
            if abs(self.ball_x_speed) < self.ball_max_speed:
                self.ball_x_speed *= -self.ball_speed_up
                self.ball_y_speed += action[1] * 0.05
            else:
                self.ball_x_speed = -self.ball_x_speed
        elif action[0] == "strike" and side == 'h':
            if abs(self.ball_y_speed) < self.ball_max_speed:
                self.ball_y_speed *= -self.ball_speed_up
                self.ball_x_speed += action[1] * 0.05
            else:
                self.ball_y_speed = -self.ball_y_speed
        else:
            self.ball_y_speed = -self.ball_y_speed

    # get ball center coords
    def ball_center(self):
        ball_left, ball_top, ball_right, ball_bot = c.coords(self.BALL)
        return (ball_top + ball_bot) / 2, (ball_left + ball_right) / 2

    # get ball center coordinates
    def ball_coords(self, pad, side):
        x, y = self.ball_center()
        if side == 'l':
            return x - c.coords(pad)[3] + (PAD_H / 2), y
        elif side == 'r':
            return x - c.coords(pad)[3] + (PAD_H / 2), WIDTH-y
        elif side == 't':
            return y - c.coords(pad)[0] - (PAD_H/2), x
        elif side == 'b':
            return y - c.coords(pad)[0] - (PAD_H/2), HEIGHT - x


# WINDOW SETTINGS
# set window
root = Tk()
root.title("Fuzzy Battle Royale")

# animation area
c = Canvas(root, width=WIDTH, height=HEIGHT, background="black")
c.pack()


# GAME ELEMENTS

# field border
c.create_rectangle(PAD_W, PAD_W, WIDTH-PAD_W, HEIGHT-PAD_W, outline="white")
# central lines
c.create_line(WIDTH/2, PAD_W, WIDTH/2, HEIGHT-PAD_W, fill="white")
c.create_line(PAD_W, WIDTH/2, HEIGHT-PAD_W, WIDTH/2, fill="white")

# create balls
BALL = Ball(c)
BALL1 = Ball(c)

# PADS

# create left pad (Sugeno)
LEFT_PAD = c.create_line(PAD_W/2, HEIGHT/2-PAD_H/2,
                         PAD_W/2, HEIGHT/2+PAD_H/2,
                         width=PAD_W, fill="#1E90FF")
# create right pad (Tsukamoto)
RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, HEIGHT/2-PAD_H/2,
                          WIDTH-PAD_W/2, HEIGHT/2+PAD_H/2,
                          width=PAD_W, fill="yellow")
# create top pad (Mamdani)
TOP_PAD = c.create_line(WIDTH/2-PAD_H/2, PAD_W/2,
                        WIDTH/2+PAD_H/2, PAD_W/2,
                        width=PAD_W, fill="red")
# create bottom pad (Larsen)
BOTTOM_PAD = c.create_line(WIDTH/2-PAD_H/2, HEIGHT-PAD_W/2,
                           WIDTH/2+PAD_H/2, HEIGHT-PAD_W/2,
                           width=PAD_W, fill="green")

# PADS MOVE GLOBALS
PAD_SPEED = 20
LEFT_PAD_SPEED = 0
RIGHT_PAD_SPEED = 0
TOP_PAD_SPEED = 0
BOTTOM_PAD_SPEED = 0


def move_pads():
    # Vertical pads
    c.move(LEFT_PAD, 0, LEFT_PAD_SPEED)
    c.move(RIGHT_PAD, 0, RIGHT_PAD_SPEED)
    PADS = [LEFT_PAD, RIGHT_PAD]
    for pad in PADS:
        if c.coords(pad)[1] < PAD_W:
            c.move(pad, 0, -c.coords(pad)[1] + PAD_W)
        elif c.coords(pad)[3] > HEIGHT-PAD_W:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3] - PAD_W)
    # Horizontal pads
    c.move(TOP_PAD, TOP_PAD_SPEED, 0)
    c.move(BOTTOM_PAD, BOTTOM_PAD_SPEED, 0)
    PADS = [TOP_PAD, BOTTOM_PAD]
    for pad in PADS:
        if c.coords(pad)[0] < PAD_W:
            c.move(pad, -c.coords(pad)[0] + PAD_W, 0)
        elif c.coords(pad)[2] > WIDTH-PAD_W:
            c.move(pad, WIDTH - c.coords(pad)[2] - PAD_W, 0)


def main():
    BALL.move_ball()
    BALL1.move_ball()
    tsukamoto_move()
    larsen_move()
    mamdani_move()
    sugeno_move()
    move_pads()
    root.after(10, main)


# Set focus on canvas for keyboard reaction
c.focus_set()


########################### DEFINE FUZZY CONTROLLER VARIABLES AND RULES ###########################

class FuzzyController:
    def __init__(self, controller):
        self.var_x = controller.Variable("X",
                                         {"LeftFar": (-600,-599,-250,-200), "Left": (-300,-200,-50,0),
                                          "Center": (0,10),
                                          "Right": (0,50,200,300), "RightFar":(200,250,599,600)},
                                         (-600, 600))
        self.var_y = controller.Variable("Y",
                                         {"Close": (0,1,100,150), "Far": (100,160,599,600)},
                                         (0, 600))
        self.var_out = controller.Variable("Out",
                                           {"LeftSprint": (-30,-29,-20), "LeftFast": (-30,-20,-15),
                                            "LeftNormal": (-20,-15,-10), "LeftSlow": (-15,-10,0),
                                            "StopFar": (-10,-5,5,10), "StopClose": (-10,-5,5,10),
                                            "RightSlow": (0,10,15), "RightNormal": (10,15,20),
                                            "RightFast": (15,20,30), "RightSprint": (20,29,30)},
                                           (-30, 30))
        self.contr_rules = controller.Rule()
        self.contr_rules.add_rule(("LeftFar", "and", "Close"), "LeftSprint")
        self.contr_rules.add_rule(("LeftFar", "and", "Far"), "LeftFast")
        self.contr_rules.add_rule(("Left", "and", "Close"), "LeftNormal")
        self.contr_rules.add_rule(("Left", "and", "Far"), "LeftSlow")
        self.contr_rules.add_rule(("Center", "and", "Far"), "StopFar")
        self.contr_rules.add_rule(("Center", "and", "Close"), "StopClose")
        self.contr_rules.add_rule(("Right", "and", "Far"), "RightSlow")
        self.contr_rules.add_rule(("Right", "and", "Close"), "RightNormal")
        self.contr_rules.add_rule(("RightFar", "and", "Far"), "RightFast")
        self.contr_rules.add_rule(("RightFar", "and", "Close"), "RightSprint")


#################################### CREATE FUZZY CONTROLLERS #####################################

# MAMDANI (top)
mamdani = FuzzyController(Mamdani)


def mamdani_move():
    global TOP_PAD_SPEED
    coords = BALL.ball_coords(TOP_PAD, 't')
    coords1 = BALL1.ball_coords(TOP_PAD, 't')

    def get_speed(coords):
        curr_fuzzy = Mamdani.FuzzyMethods()
        curr_fuzzy.fuzzification({mamdani.var_x: coords[0], mamdani.var_y: coords[1]})
        curr_fuzzy.aggregation(mamdani.contr_rules.rules)
        return curr_fuzzy.defuzzification(mamdani.var_out)

    if BALL.ball_y_speed < 0 and math.sqrt(coords[1]**2 + coords[0]**2) < \
            math.sqrt(coords1[1]**2 + coords1[0]**2):
        TOP_PAD_SPEED = get_speed(coords)
    elif BALL1.ball_y_speed < 0 and math.sqrt(coords[1]**2 + coords[0]**2) > \
        math.sqrt(coords1[1]**2 + coords1[0]**2):
        TOP_PAD_SPEED = get_speed(coords1)
    elif BALL.ball_y_speed < 0 and coords[1] < coords1[1]:
        TOP_PAD_SPEED = get_speed(coords)
    else:
        TOP_PAD_SPEED = get_speed(coords1)


###################################################################################################

# TSUKAMOTO (right)
tsukamoto = FuzzyController(Tsukamoto)


def tsukamoto_move():
    global RIGHT_PAD_SPEED
    coords = BALL.ball_coords(RIGHT_PAD, 'r')
    coords1 = BALL1.ball_coords(RIGHT_PAD, 'r')

    def get_speed(coords):
        curr_fuzzy = Tsukamoto.FuzzyMethods()
        curr_fuzzy.fuzzification({tsukamoto.var_x: coords[0], tsukamoto.var_y: coords[1]})
        curr_fuzzy.aggregation(tsukamoto.contr_rules.rules)
        curr_fuzzy.activation(tsukamoto.var_out)
        return curr_fuzzy.defuzzification()

    if BALL.ball_x_speed > 0 and math.sqrt(coords[1] ** 2 + coords[0] ** 2) < \
            math.sqrt(coords1[1] ** 2 + coords1[0] ** 2):
        RIGHT_PAD_SPEED = get_speed(coords)
    elif BALL1.ball_x_speed > 0 and math.sqrt(coords[1] ** 2 + coords[0] ** 2) > math.sqrt(
            coords1[1] ** 2 + coords1[0] ** 2):
        RIGHT_PAD_SPEED = get_speed(coords1)
    elif BALL.ball_x_speed > 0 and coords[0] < coords1[0]:
        RIGHT_PAD_SPEED = get_speed(coords)
    else:
        RIGHT_PAD_SPEED = get_speed(coords1)


###################################################################################################

# LARSEN (bottom)
larsen = FuzzyController(Larsen)


def larsen_move():
    global BOTTOM_PAD_SPEED
    coords = BALL.ball_coords(BOTTOM_PAD, 'b')
    coords1 = BALL1.ball_coords(BOTTOM_PAD, 'b')

    def get_speed(coords):
        curr_fuzzy = Larsen.FuzzyMethods()
        curr_fuzzy.fuzzification({larsen.var_x: coords[0], larsen.var_y: coords[1]})
        curr_fuzzy.aggregation(larsen.contr_rules.rules)
        return curr_fuzzy.defuzzification(larsen.var_out)

    if BALL.ball_y_speed > 0 and math.sqrt(coords[1] ** 2 + coords[0] ** 2) < \
            math.sqrt(coords1[1] ** 2 + coords1[0] ** 2):
        BOTTOM_PAD_SPEED = get_speed(coords)
    elif BALL1.ball_y_speed > 0 and math.sqrt(coords[1] ** 2 + coords[0] ** 2) > math.sqrt(
            coords1[1] ** 2 + coords1[0] ** 2):
        BOTTOM_PAD_SPEED = get_speed(coords1)
    elif BALL.ball_y_speed > 0 and coords[1] < coords1[1]:
        BOTTOM_PAD_SPEED = get_speed(coords)
    else:
        BOTTOM_PAD_SPEED = get_speed(coords1)


###################################################################################################

# SUGENO (left)
sugeno = FuzzyController(Sugeno)


def sugeno_move():
    global LEFT_PAD_SPEED
    coords = BALL.ball_coords(LEFT_PAD, 'l')
    coords1 = BALL1.ball_coords(LEFT_PAD, 'l')

    def get_speed(coords):
        curr_fuzzy = Sugeno.FuzzyMethods()
        curr_fuzzy.fuzzification({sugeno.var_x: coords[0], sugeno.var_y: coords[1]})
        curr_fuzzy.aggregation(sugeno.contr_rules.rules)
        curr_fuzzy.activation(coords[0], coords[1], sugeno.var_out)
        return curr_fuzzy.defuzzification()

    if BALL.ball_x_speed < 0 and math.sqrt(coords[1] ** 2 + coords[0] ** 2) < \
            math.sqrt(coords1[1] ** 2 + coords1[0] ** 2):
        LEFT_PAD_SPEED = get_speed(coords)
    elif BALL1.ball_x_speed < 0 and math.sqrt(coords[1] ** 2 + coords[0] ** 2) > math.sqrt(
            coords1[1] ** 2 + coords1[0] ** 2):
        LEFT_PAD_SPEED = get_speed(coords1)
    elif BALL.ball_x_speed < 0 and coords[0] < coords1[0]:
        LEFT_PAD_SPEED = get_speed(coords)
    else:
        LEFT_PAD_SPEED = get_speed(coords1)

###################################################################################################


# GAME PROCESS GLOBALS

# GAME SCORING
TSUKAMOTO_SCORE = 0
SUGENO_SCORE = 0
LARSEN_SCORE = 0
MAMDANI_SCORE = 0

# print players scores
sugeno_name = c.create_text(55, 25,
                          text="Sugeno",
                          font="Arial 10",
                          fill="#1E90FF")
sugeno_text = c.create_text(100, 25,
                          text=SUGENO_SCORE,
                          font="Arial 20",
                          fill="white")
larsen_name = c.create_text(55, 575,
                            text="Larsen",
                            font="Arial 10",
                            fill="green")
larsen_text = c.create_text(100, 575,
                            text=LARSEN_SCORE,
                            font="Arial 20",
                            fill="white")
mamdani_name = c.create_text(545, 25,
                             text="Mamdani",
                             font="Arial 10",
                             fill="red")
mamdani_text = c.create_text(500, 25,
                             text=MAMDANI_SCORE,
                             font="Arial 20",
                             fill="white")
tsukamoto_name = c.create_text(545, 575,
                               text="Tsukamoto",
                               font="Arial 10",
                               fill="yellow")
tsukamoto_text = c.create_text(500, 575,
                               text=TSUKAMOTO_SCORE,
                               font="Arial 20",
                               fill="white")


# scores update function
def update_score(player):
    global TSUKAMOTO_SCORE, SUGENO_SCORE, LARSEN_SCORE, MAMDANI_SCORE
    if player == "right":
        TSUKAMOTO_SCORE -= 1
        c.itemconfig(tsukamoto_text, text=TSUKAMOTO_SCORE)
    elif player == "left":
        SUGENO_SCORE -= 1
        c.itemconfig(sugeno_text, text=SUGENO_SCORE)
    elif player == "top":
        MAMDANI_SCORE -= 1
        c.itemconfig(mamdani_text, text=MAMDANI_SCORE)
    elif player == "bottom":
        LARSEN_SCORE -= 1
        c.itemconfig(larsen_text, text=LARSEN_SCORE)


#if __name__ == "main":
# enable movement
main()
# enable window
root.mainloop()
