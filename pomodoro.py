import tkinter as tk


class OptionFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        pomodoro_button = tk.Button(self, text='Pomodoro')
        short_break_button = tk.Button(self, text='Short Break')
        long_break_button = tk.Button(self, text='Long Break')

        pomodoro_button.grid(row=0, column=0)
        short_break_button.grid(row=0, column=1)
        long_break_button.grid(row=0, column=2)


class TimerFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        timer = tk.Label(self, text='%s:%s' % ('25', '00'), font=('Helvetica', 120))

        timer.grid(row=1)


class ControllerFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        start_button = tk.Button(container, text='Start')
        pause_button = tk.Button(container, text='Pause')

        start_button.grid(row=0, column=0)
        pause_button.grid(row=0, column=2)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.setup()

        option_frame = OptionFrame(self)
        timer_frame = TimerFrame(self)
        controller_frame = ControllerFrame(self)
        
        option_frame.grid(row=0, column=0)
        timer_frame.grid(row=1, column=0)
        controller_frame.grid(row=2, column=0)

    
    def setup(self):
        self.title('Pomodoro Timer')

        self.screen_width = self.winfo_screenwidth() # width of the screen
        self.screen_height = self.winfo_screenheight() # height of the screen

        self.width = 800 if self.screen_width > 800 else self.screen_width
        self.height = 450 if self.screen_height > 450 else self.screen_height

        # calculate x and y coordinates for the Tk root window
        self.x_position = (self.screen_width/2) - (self.width/2)
        self.y_position = (self.screen_height/2) - (self.height/2)

        # set dimension of screen and new x and y location to open from
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x_position, self.y_position))

        self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)


def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()

    