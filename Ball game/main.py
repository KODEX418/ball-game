from time import sleep
from tkinter import *
from tkinter import ttk, messagebox, font
from random import *
import math as mh
import ballsim

master = Tk()
master.title('Ball Game')
master.geometry('600x900')
master.configure(bg='#99d9ea')
master.resizable(width=False, height=False)
player_png = PhotoImage(file='idle1.png')
star_png = PhotoImage(file='star.png')
m = 675
n = 530
grid_size = 30

correct_coords = []
trajectory_ready = False
player_lose = False
traj_state = HIDDEN
player_entry_str = StringVar()
errmsg = StringVar()
start_brick_pos, fin_brick_pos = -100, -100
question_text1 = f'''C какой скоростью V(м/с) должен двигаться объект чтобы достигнуть звездочки?\n'''


def calc_menu():
    ballsim.main()


def is_valid(s):
    result = s.isdigit()
    if not result:
        errmsg.set("Введите правильное значение")
    else:
        errmsg.set("")
    return result


def jump_command():
    if is_valid(player_entry_str.get()):
        for k in correct_coords:
            canvas.moveto(player, *k)
            canvas.update()
            sleep(0.01 ** 2)


def buttons_state():
    if trajectory_ready:
        main_button.configure(state=NORMAL)
    else:
        main_button.configure(state=DISABLED)


def get_user_data():
    return entry1.get()


def calculate_trajectory(height, angle, velocity):
    global player_lose, trajectory
    correct_coords = []
    t = 0
    vx = round(mh.cos(mh.radians(angle)), 5) * velocity
    vy0 = round(mh.sin(mh.radians(angle)), 5) * velocity
    g = 10
    tend = (vy0 + mh.sqrt(vy0 ** 2 + 2 * g * height)) / g
    while t <= tend:
        t += 0.01
        x = vx * t
        y = height - vy0 * t + ((g * t ** 2) / 2)
        if 0 <= x <= n - grid_size * 0.5 and y <= m - grid_size * 0.5:
            correct_coords.append((x, y))
        else:
            correct_coords.append((x, y))
            player_lose = True
            break
    trajectory = canvas.create_line([(h[0] + grid_size / 2, h[1] + grid_size / 2) for h in correct_coords],
                                    fill='red',
                                    width=2,
                                    smooth=True,
                                    state=traj_state)
    return correct_coords


def create_level():
    global start_brick_pos, fin_brick_pos, win_star_pos
    start_brick_pos = (
        randrange(0, n // 2 - 2 * grid_size, grid_size) - 1, randrange(m // 2, m - grid_size, grid_size) - 8)
    canvas.moveto(start_brick, *start_brick_pos)
    fin_brick_pos = (
        randrange(n // 2, n - 3 * grid_size, grid_size) + 4, randrange(2*grid_size, m // 2 - grid_size, grid_size) - 1)
    canvas.moveto(fin_brick, *fin_brick_pos)
    win_star_pos = (fin_brick_pos[0] + grid_size, fin_brick_pos[1] - 2 * grid_size)
    canvas.moveto(win_star, *win_star_pos)


def start_sequence():
    global x_axis, y_axis
    global trajectory_ready, player
    canvas.delete(x_axis)
    canvas.delete(y_axis)
    trajectory_ready = True
    buttons_state()
    create_level()
    x1, y1 = start_brick_pos
    x1 += + randrange(0, 3 * grid_size - 80, 80)
    y1 += -80
    x_axis = canvas.create_line(x1 + 50, y1 + 40, win_star_pos[0] + 32, y1 + 40,
                                width=2,
                                arrow='last',
                                )
    y_axis = canvas.create_line(x1 + 50, y1 + 40, x1 + 50, win_star_pos[1] + 32,
                                width=2,
                                arrow='last',
                                )
    canvas.moveto(player, x1, y1)
    canvas.lift(player)
    text1.delete('1.0', END)
    text1.insert('1.0', question_text1)
    text1.configure(state='disabled')


canvas = Canvas(
    bg='#b8f3be',
    height=m,
    width=n,
    border=1,
    bd=0,
    highlightthickness=3,
    highlightbackground="black",
    relief=SUNKEN
)
canvas.pack(anchor=N, pady=10)

x_axis, y_axis = canvas.create_line(-10, -10, -1, -1), canvas.create_line(-10, -10, -1, -1)
for x in range(0, n, grid_size):
    canvas.create_line(x, 0, x, m + 10,
                       width=1,
                       )
for y in range(0, m, grid_size):
    canvas.create_line(0, y, n + 10, y,
                       width=1,
                       )

# player = canvas.create_oval(0, 0, grid_size, grid_size, fill='ORANGE')
player = canvas.create_image(10, 10, image=player_png)
canvas.moveto(player, -100, -100)
start_brick = canvas.create_rectangle(0, 0, 4 * grid_size, grid_size, fill='#bf6d40')
canvas.moveto(start_brick, -100, -100)
fin_brick = canvas.create_rectangle(0, 0, 4 * grid_size, grid_size, fill='#bf6d40')
canvas.moveto(fin_brick, -100, -100)
win_star = canvas.create_image(10, 10, image=star_png)
canvas.moveto(win_star, -50, -50)
text1 = Text(
    bg='#b8f3be',
    height=4,
    width=40,
    font=('Copperplate Gothic', 18),
    padx=7,
    pady=7,
    wrap='word'
)

text1.pack()

entry1 = Entry(
    bg='#b8f3be',
    width=12,
    font=font.Font(family="Arial", size=22, weight="normal", slant="roman"),
    textvariable=player_entry_str,
)
entry1.place(x=32, y=833)

error_label = Label(bg='#99d9ea', foreground="red", textvariable=errmsg, wraplength=250)
error_label.place(x=30, y=873)

main_button = Button(
    width=19,
    bg='#0df2b1',
    text='ПРЫЖОК',
    font=font.Font(family="Arial", size=12, weight="bold", slant="roman"),
    pady=3,
    padx=3,
    command=jump_command,
    state=DISABLED
)
main_button.place(x=242, y=833)

start_button = Button(
    bg='#0af5ec',
    width=2,
    text='🔄',
    font=font.Font(family="Arial", size=14, weight="bold", slant="roman"),
    pady=0,
    padx=0,
    command=start_sequence,
)
start_button.place(x=538, y=832)

faq_button = Button(
    bg='#b8f3be',
    width=2,
    text='❔',
    font=font.Font(family="Arial", size=14, weight="normal", slant="roman"),
    pady=0,
    padx=0
)
faq_button.place(x=462, y=832)

config_button = Button(
    bg='#b8f3be',
    width=2,
    text='⚙️',
    font=font.Font(family="Arial", size=14, weight="bold", slant="roman"),
    pady=0,
    padx=0,
    command=calc_menu
)
config_button.place(x=500, y=832)

canvas.mainloop()
