import tkinter as tk


class Option(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.selection = ('Pomodoro', 'Short Break', 'Long Break')
        self.selected = self.selection[0]

        self.pomodoro_btn = tk.Button(self, text=self.selection[0], state='active', pady=5, command=self.select_pomodoro)
        self.short_break_btn = tk.Button(self, text=self.selection[1], pady=5, command=self.select_short_break)
        self.long_break_btn = tk.Button(self, text=self.selection[2], pady=5, command=self.select_long_break)

        self.pomodoro_btn.grid(row=0, column=0)
        self.short_break_btn.grid(row=0, column=1)
        self.long_break_btn.grid(row=0, column=2)

    def select_pomodoro(self):
        self.pomodoro_btn.config(state='active')
        self.short_break_btn.config(state='normal')
        self.long_break_btn.config(state='normal')
        self.selected = self.selection[0]

    def select_short_break(self):
        self.pomodoro_btn.config(state='normal')
        self.short_break_btn.config(state='active')
        self.long_break_btn.config(state='normal')
        self.selected = self.selection[1]

    def select_long_break(self):
        self.pomodoro_btn.config(state='normal')
        self.short_break_btn.config(state='normal')
        self.long_break_btn.config(state='active')
        self.selected = self.selection[2]

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
        self.timer.config(text=self.display_time(self.time))


class Tracker(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.counter = 1
        self.tracker = ('Pomodoro', 'Break')
        self.tracker_val = 0
        self.curr_tracker = self.tracker[self.tracker_val]

        self.details = tk.Label(self, text=self.display_details())

        self.details.grid(row=0)
    
    def display_details(self):
        return f'#{self.counter} {self.curr_tracker}'
    
    def inc_counter(self):
        self.counter += 1
        self.details.config(text=self.display_details())
    
    def update_curr_tracker(self):
        self.tracker_val = not self.tracker_val
        self.curr_tracker = self.tracker[self.tracker_val]
        self.details.config(text=self.display_details())


class Controller(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        self.started = False

        self.start_btn = tk.Button(self, text='Start', pady=5, command=self.start_timer)
        self.pause_btn = tk.Button(self, text='Pause', state='disabled', pady=5, command=self.pause_timer)

        self.start_btn.grid(row=0, column=0)
        self.pause_btn.grid(row=0, column=2)

    def start_timer(self):
        self.started = True
        self.start_btn.config(state='disabled')
        self.pause_btn.config(state='normal')

    def pause_timer(self):
        self.started = False
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled')

    def get_started(self):
        return self.started


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.setup()
        self.opened = False

        self.option = Option(self)
        self.timer = Timer(self)
        self.tracker = Tracker(self)
        self.controller = Controller(self)
        
        self.option.grid(row=0, column=0)
        self.timer.grid(row=1, column=0)
        self.tracker.grid(row=2, column=0)
        self.controller.grid(row=3, column=0)

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
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=2)
    
    # def create_warning(self, opened):
    #     if not opened:
    #         window = tk.Toplevel(self)

    def update_app(self):
        timer_option = self.option.get_selected()
        started = self.controller.get_started()
        if timer_option == 'Pomodoro':
            self.timer.set_time(25*60000)
        elif timer_option == 'Short Break':
            self.timer.set_time(5*60000)
        elif timer_option == 'Long Break':
            self.timer.set_time(15*60000)
        self.after(100, self.update_app)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()

