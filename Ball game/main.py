from time import sleep
from tkinter import *
from tkinter import messagebox, font
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
s_y, s_x = 0, 0
x1, y1 = 0, 0
angle = 60
correct_coords = []
trajectory_ready = False
player_lose = False
traj_state = NORMAL
player_entry_str = StringVar()
errmsg = StringVar()
start_brick_pos, fin_brick_pos = (-100, -100), (-100, -100)
question_text1 = f'''C какой скоростью V(м/с) должен двигаться объект чтобы достигнуть звездочки?\n'''
star_count = 0

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
    global trajectory, trajectory_ready, star_count
    if is_valid(player_entry_str.get()):
        if trajectory_ready:
            canvas.delete(trajectory)
        print(canvas.coords(win_star))
        x_0, h = x1, y1
        v = int(get_user_data())
        a = angle
        t = 10
        coords = calculate_trajectory(h, a, v, x_0, t)
        for k in coords:
            if 0 <= k[0] <= n - 32 and k[1] <= m - 32:
                canvas.moveto(player, *k)
                canvas.update()
                k_prev = coords[coords.index(k) - 1]
            else:
                canvas.moveto(player, x_0, h)
                messagebox.showwarning(message='Вы проиграли!')
                break
            if abs(canvas.coords(player)[0] - canvas.coords(win_star)[0]) < grid_size / 2 and abs(canvas.coords(player)[1] - canvas.coords(win_star)[1]) < grid_size / 2:
                canvas.moveto(player, canvas.coords(win_star)[0] - 54, canvas.coords(win_star)[1] - 54)
                canvas.moveto(win_star, -50, -50)
                star_count += 1
                messagebox.showinfo(message='Вы победили!')
                break
            canvas.update()
            sleep(0.01 ** 2)
    print(canvas.coords(player))
    #trajectory_ready = True


def buttons_state():
    if start_ready:
        main_button.configure(state=NORMAL)
    else:
        main_button.configure(state=DISABLED)


def get_user_data():
    return entry1.get()


def calculate_trajectory(height, angle, velocity, x_0, t_0):
    global player_lose, trajectory
    correct_coords = []
    t = 0
    vx = round(mh.cos(mh.radians(angle)), 5) * velocity
    vy0 = round(mh.sin(mh.radians(angle)), 5) * velocity
    g = 10
    tend = 2*t_0
    while t <= tend:
        t += 0.01
        x = x_0 + vx * t
        y = height - vy0 * t + ((g * t ** 2) / 2)
        correct_coords.append((x, y))
    return correct_coords


def create_level():
    global start_brick_pos, fin_brick_pos, win_star_pos
    start_brick_pos = (
        randrange(0, n // 2 - 2 * grid_size, grid_size) - 1, randrange(m // 2, m - grid_size, grid_size) - 8)
    canvas.moveto(start_brick, *start_brick_pos)
    fin_brick_pos = (
        randrange(n // 2, n - 3 * grid_size, grid_size) + 4,
        randrange(2 * grid_size, m // 2 - grid_size, grid_size) - 1)
    canvas.moveto(fin_brick, *fin_brick_pos)
    win_star_pos = (fin_brick_pos[0] + grid_size, fin_brick_pos[1] - 2 * grid_size)
    canvas.moveto(win_star, *win_star_pos)


def start_sequence():
    global x_axis, y_axis
    global start_ready, player
    global s_y, s_x, x1, y1
    canvas.delete(x_axis)
    canvas.delete(y_axis)
    start_ready = True
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
    text1.configure(state='normal')
    text1.delete('1.0', END)
    s_y = y1 + 40 - (win_star_pos[1] + 32)
    s_x = win_star_pos[0] + 32 - (x1 + 50)
    text1.insert('1.0', question_text1 + f'H = {s_y}м, L = {s_x}, угол = 60гр., t = 10с')
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
player = canvas.create_image(10, 10, image=player_png, anchor=CENTER)
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
