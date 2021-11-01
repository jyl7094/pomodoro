import tkinter as tk


class OptionFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.option = 'p'
        self.clicked = False
        self.create_widgets()

    def create_widgets(self):
        self.p_btn = tk.Button(self, text='Pomodoro', state='active', pady=5, command=lambda: self.combined('p'))
        self.sb_btn = tk.Button(self, text='Short Break', pady=5, command=lambda: self.combined('sb'))
        self.lb_btn = tk.Button(self, text='Long Break', pady=5, command=lambda: self.combined('lb'))
        
        self.p_btn.grid(row=0, column=0)
        self.sb_btn.grid(row=0, column=1)
        self.lb_btn.grid(row=0, column=2)

    def select_option(self, option):
        if option == 'p':
            self.p_btn.config(state='active')
            self.sb_btn.config(state='normal')
            self.lb_btn.config(state='normal')
            self.option = 'p'
        elif option == 'sb':
            self.p_btn.config(state='normal')
            self.sb_btn.config(state='active')
            self.lb_btn.config(state='normal')
            self.option = 'sb'
        elif option == 'lb':
            self.p_btn.config(state='normal')
            self.sb_btn.config(state='normal')
            self.lb_btn.config(state='active')
            self.option = 'lb'
    
    def toggle_options(self, val:str):
        if val == 'enable':
                self.select_option(self.option)
        elif val == 'disable':
            self.p_btn.config(state='disabled')
            self.sb_btn.config(state='disabled')
            self.lb_btn.config(state='disabled')

    def combined(self, option):
        self.select_option(option)
        self.set_clicked(True)

    def get_option(self):
        return self.option
    
    def set_option(self, val:str=''):
        self.option = val

    def get_clicked(self):
        return self.clicked

    def set_clicked(self, val:bool):
        self.clicked = val


class TimerFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.MINUTE = 60000
        self.time = 25 * self.MINUTE
        self.create_widgets()

    def create_widgets(self):
        self.timer = tk.Label(self, text=self.time_to_string(self.time), font=('Helvetica', 120))

        self.timer.grid(row=0)

    def time_to_string(self, time): # ms -> mm:ss
        minutes, seconds = divmod(time/1000, 60)
        return '{:02}:{:02}'.format(int(minutes), int(seconds))
    
    def set_time(self, time):
        self.time = time * self.MINUTE
        self.timer.config(text=self.time_to_string(self.time))

    def countdown(self):
        self.time -= 1000
        self.timer.config(text=self.time_to_string(self.time))

    def get_time(self):
        return self.time



# class InfoFrame(tk.Frame):
#     def __init__(self, container):
#         super().__init__(container)
#         self.cycle = 1
#         self.event = 'Pomodoro'
#         self.create_widgets()

#     def create_widgets(self):
#         self.details = tk.Label(self, text=f'Cycle {self.cycle} - {self.event}')

#         self.details.grid(row=0)
    
#     def inc_cycle(self):
#         self.cycle += 1
#         self.details.config(text=f'Cycle {self.cycle} - {self.event}')
    
#     def set_event(self, event):
#         self.event = event
#         self.details.config(text=f'Cycle {self.cycle} - {self.event}')


class ControllerFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)       
        self.started = ''
        self.create_widgets()

    def create_widgets(self):
        self.start_btn = tk.Button(self, text='Start', pady=5, command=lambda: self.toggle_timer('start'))
        self.pause_btn = tk.Button(self, text='Pause', state='disabled', pady=5, command=lambda: self.toggle_timer('pause'))

        self.start_btn.grid(row=0, column=0)
        self.pause_btn.grid(row=0, column=2)

    def toggle_timer(self, val:str):
        if val == 'start':
            self.started = 'start'
            self.start_btn.config(state='disabled')
            self.pause_btn.config(state='normal')
        elif val == 'pause':
            self.started = 'pause'
            self.start_btn.config(state='normal')
            self.pause_btn.config(state='disabled')
    
    def set_started(self, val=''):
        self.started = val

    def get_started(self):
        return self.started
    

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.setup()
        self.create_widgets()
        self.after_id = None
        self.running = False
        self.update()

    def update(self):
        started = self.controller.get_started()
        if self.timer.get_time() <= 0 and self.after_id != None:
            self.after_cancel(self.after_id)
        if started == 'start':
            self.running = True
            self.option.toggle_options('disable')
            self.after_id = self.after(1000, self.countdown)
            self.controller.set_started()
        elif started == 'pause':
            if self.after_id != None:
                self.running = False
                self.option.toggle_options('enable')
                self.after_cancel(self.after_id)

        if not self.running:
            option = self.option.get_option()
            self.timer.set_time(self.timer.get_time()/60000)
            if option == 'p' and self.option.get_clicked():
                self.timer.set_time(25)
            elif option == 'sb' and self.option.get_clicked():
                self.timer.set_time(5)
            elif option == 'lb' and self.option.get_clicked():
                self.timer.set_time(15)
        self.option.set_clicked(False)
        
        self.after(100, self.update)

    def countdown(self):
        self.timer.countdown()
        self.after_id = self.after(1000, self.countdown)

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
    
    def create_widgets(self):
        self.option = OptionFrame(self)
        self.timer = TimerFrame(self)
        self.info = InfoFrame(self)
        self.controller = ControllerFrame(self)
        
        self.option.grid(row=0, column=0)
        self.timer.grid(row=1, column=0)
        self.info.grid(row=2, column=0)
        self.controller.grid(row=3, column=0)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()

