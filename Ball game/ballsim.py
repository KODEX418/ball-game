from tkinter import *
from tkinter import messagebox
import math as m
import matplotlib.pyplot as plt
from sympy import *

def main():
    def graphic_y():
        g = 10
        height = float(height_ent.get())
        angle = float(angle_ent.get())
        velocity = float(velocity_ent.get())
        vy0 = round(m.sin(m.radians(angle)), 5) * velocity
        t = symbols('t')
        if height != 0:
            tend = (vy0 + m.sqrt(vy0 ** 2 + 2 * g * height)) / g
        else:
            tend = (2 * vy0) / g
        plot(height + vy0 * t - ((g * t ** 2) / 2),
             (t, 0, tend),
             title='График координаты по оси Y',
             xlabel='t(c)',
             ylabel='y(м)',
             line_color='green')

    def graphic_x():
        g = 10
        height = float(height_ent.get())
        angle = float(angle_ent.get())
        velocity = float(velocity_ent.get())
        vy0 = round(m.sin(m.radians(angle)), 5) * velocity
        vx = round(m.cos(m.radians(angle)), 5) * velocity
        t = symbols('t')
        if height != 0:
            tend = (vy0 + m.sqrt(vy0 ** 2 + 2 * g * height)) / g
        else:
            tend = (2 * vy0) / g
        plot(vx * t,
             (t, 0, tend),
             title='График координаты по оси X',
             xlabel='t(c)',
             ylabel='x(м)',
             line_color='green')

    def scatter_xy():
        g = 10
        height = float(height_ent.get())
        angle = float(angle_ent.get())
        velocity = float(velocity_ent.get())
        vy0 = round(m.sin(m.radians(angle)), 5) * velocity
        vx = round(m.cos(m.radians(angle)), 5) * velocity
        if height != 0:
            tend = (vy0 + m.sqrt(vy0 ** 2 + 2 * g * height)) / g
        else:
            tend = (2 * vy0) / g
        t = 0
        step_t = tend / 500
        x, y = [], []
        while t <= tend:
            t += step_t
            x.append(vx * t)
            y.append(height + vy0 * t - ((g * t ** 2) / 2))
        plt.title("f(x)")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.scatter(x, y, s=0.25)
        plt.show()

    def graphic_xy():
        g = 10
        height = float(height_ent.get())
        angle = float(angle_ent.get())
        velocity = float(velocity_ent.get())
        vy0 = round(m.sin(m.radians(angle)), 5) * velocity
        vx = round(m.cos(m.radians(angle)), 5) * velocity
        x = symbols('x')
        if height != 0:
            tend = (vy0 + m.sqrt(vy0 ** 2 + 2 * g * height)) / g
        else:
            tend = (2 * vy0) / g
        xend = vx * tend
        plot(height + vy0 * x / vx - g / 2 * (x / vx) ** 2,
             (x, 0, xend),
             title='График координаты',
             xlabel='x(м)',
             ylabel='y(м)',
             line_color='green')

    def inf_main():
        g = 10
        height = float(height_ent.get())
        angle = float(angle_ent.get())
        velocity = float(velocity_ent.get())
        vy0 = round(m.sin(m.radians(angle)), 5) * velocity
        vx = round(m.cos(m.radians(angle)), 5) * velocity
        tpeak = vy0 / g
        ypeak = height + (vy0 * tpeak) - ((g * tpeak ** 2) / 2)
        xpeak = tpeak * vx
        if height != 0:
            tend = (vy0 + m.sqrt(vy0 ** 2 + 2 * g * height)) / g
        else:
            tend = (2 * vy0) / g
        vend = m.hypot(vx, abs(vy0 - g * tend))
        xend = vx * tend
        ms1 = f'''\nОбъект приземлится через {round(tend, 3)} секунд после запуска
    Максимальная высота = {ypeak} м \nВремя достижения = {tpeak} с \nКоордината X = {xpeak} м
    Дистанция до старта по оси X = {round(xend, 3)} м
    Максимальная скорость = {round(vend, 3)} м/с (прямо перед касанием)
    '''
        messagebox.showinfo('Info', ms1)

    win1 = Tk()
    win1.title('Баллистический калькулятор')
    win1.geometry('800x600')
    frame = Frame(
        win1,
        padx=100,
        pady=100
    )

    frame.pack(expand=True)
    main_label = Label(
        frame,
        text='''Баллистический калькулятор тела,
    брошенного под углом к горизонту
        '''
    )
    main_label.grid(row=1, column=2)

    height_label = Label(
        frame,
        text='Начальная высота(м)'
    )
    height_label.grid(row=4, column=1)

    angle_label = Label(
        frame,
        text='Угол(°)'
    )
    angle_label.grid(row=5, column=1)

    velocity_label = Label(
        frame,
        text='Начальная скорость(м/с)'
    )
    velocity_label.grid(row=6, column=1)

    height_ent = Entry(
        frame,
    )
    height_ent.grid(row=4, column=3, pady=5)
    angle_ent = Entry(
        frame,
    )

    angle_ent.grid(row=5, column=3, pady=5)
    velocity_ent = Entry(
        frame
    )

    velocity_ent.grid(row=6, column=3, pady=5)

    main_button = Button(
        frame,
        text='Рассчитать',
        command=inf_main
    )
    main_button.grid(row=7, column=2, pady=5)

    graphic_y_button = Button(
        frame,
        text='Показать график y(t)',
        command=graphic_y
    )
    graphic_y_button.grid(row=8, column=2, pady=5)

    graphic_x_button = Button(
        frame,
        text='Показать график x(t)',
        command=graphic_x
    )
    graphic_x_button.grid(row=9, column=2, pady=5)

    graphic_xy_button = Button(
        frame,
        text='Показать график y(x)',
        command=graphic_xy
    )
    graphic_xy_button.grid(row=10, column=2, pady=5)

    win1.mainloop()
#main()