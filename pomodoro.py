import tkinter as tk
import time

class Option(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.selected = 'Pomodoro'

        self.pomodoro_button = tk.Button(self, text='Pomodoro', state='active', command=self.set_pomodoro)
        self.short_break_button = tk.Button(self, text='Short Break', command=self.set_short_break)
        self.long_break_button = tk.Button(self, text='Long Break', command=self.set_long_break)

        self.pomodoro_button.grid(row=0, column=0)
        self.short_break_button.grid(row=0, column=1)
        self.long_break_button.grid(row=0, column=2)

    def set_pomodoro(self):
        self.pomodoro_button.config(state='active')
        self.short_break_button.config(state='normal')
        self.long_break_button.config(state='normal')
        self.selected = 'Pomodoro'

    def set_short_break(self):
        self.pomodoro_button.config(state='normal')
        self.short_break_button.config(state='active')
        self.long_break_button.config(state='normal')
        self.selected = 'Short Break'

    def set_long_break(self):
        self.pomodoro_button.config(state='normal')
        self.short_break_button.config(state='normal')
        self.long_break_button.config(state='active')
        self.selected = 'Long Break'

    def get_selected(self):
        return self.selected


class Timer(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.time = 25*60000

        self.timer = tk.Label(self, text=self.display_time(self.time), font=('Helvetica', 120))

        self.timer.grid(row=0)

    def display_time(self, time): # ms -> mm:ss
        minutes, seconds = divmod(time / 1000, 60)
        return '{:02}:{:02}'.format(int(minutes), int(seconds))

    def update_time(self):
        self.time -= 1000
        self.timer.config(text=self.display_time(self.time))
    
    def set_time(self, time):
        self.time = time
        self.update_time()


class Controller(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        self.started = False

        self.start_button = tk.Button(self, text='Start', command=self.start_timer)
        self.pause_button = tk.Button(self, text='Pause', state='disabled', command=self.pause_timer)

        self.start_button.grid(row=0, column=0)
        self.pause_button.grid(row=0, column=2)

    def start_timer(self):
        self.started = True
        self.start_button.config(state='disabled')
        self.pause_button.config(state='normal')

    def pause_timer(self):
        self.started = False
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled')

    def get_started(self):
        return self.started


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.setup()

        self.option = Option(self)
        self.timer = Timer(self)
        self.controller = Controller(self)
        
        self.option.grid(row=0, column=0)
        self.timer.grid(row=1, column=0)
        self.controller.grid(row=2, column=0)


        self.after(100, self.update_app)

    def setup(self):
        self.title('Pomodoro Timer')

        self.resizable(False, False)

        self.screen_width = self.winfo_screenwidth() # width of the screen
        self.screen_height = self.winfo_screenheight() # height of the screen

        self.width = 425 if self.screen_width > 425 else self.screen_width
        self.height = 450 if self.screen_height > 450 else self.screen_height

        # calculate x and y coordinates for the Tk root window
        self.x_position = (self.screen_width/2) - (self.width/2)
        self.y_position = (self.screen_height/2) - (self.height/2)

        # set dimension of screen and new x and y location to open from
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x_position, self.y_position))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)

    def update_app(self):
        if self.controller.get_started():
            print('Hello')
        self.after(100, self.update_app)


def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()

