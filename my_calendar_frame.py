from tkinter import *
import calendar
import customtkinter
from datetime import datetime, timedelta


class MyCalendar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.days = []
        self.now = datetime.now()
        self.year = self.now.year
        self.month = self.now.month

        self.back_button = customtkinter.CTkButton(self, text='<', command=self.back, width=30, height=25, fg_color='black',
                                                   text_color='yellow', hover_color='purple', font=('Arial bold', 18))
        self.back_button.grid(row=0, column=0, sticky='nsew')
        self.next_button = customtkinter.CTkButton(self, text='>', command=self.next, width=30, height=25, text_color='yellow',
                                                   fg_color='black', hover_color='purple', font=('Arial bold', 18))
        self.next_button.grid(row=0, column=6, sticky='nsew')
        self.info_lable = customtkinter.CTkLabel(self, text='0', font=('Arial bold', 18), text_color='yellow',
                                                 fg_color='black')
        self.info_lable.grid(row=0, column=1, columnspan=5, sticky='nsew')

        for n in range(7):
            lbl = customtkinter.CTkLabel(self, text=calendar.day_abbr[n], font=('Arial bold', 13), text_color='yellow',
                                         fg_color='black', width=30, height=25)
            lbl.grid(row=1, column=n, sticky='nsew')

        for row in range(6):
            for col in range(7):
                lbl = customtkinter.CTkLabel(self, text='0', font=('Arial bold', 18), height=30)
                lbl.grid(row=row + 2, column=col, sticky='nsew')
                self.days.append(lbl)

        self.fill()

    def back(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.fill()

    def next(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.fill()

    def fill(self):
        self.info_lable.configure(text=calendar.month_name[self.month] + ', ' + str(self.year))
        month_days = calendar.monthrange(self.year, self.month)[1]

        if self.month == 1:
            back_month_days = calendar.monthrange(self.year-1, 12)[1]
        else:
            back_month_days = calendar.monthrange(self.year, self.month-1)[1]
        week_day = calendar.monthrange(self.year, self.month)[0]

        for n in range(month_days):
            self.days[n + week_day].configure(text=n + 1, text_color='black')
            if self.year == self.now.year and self.month == self.now.month and n+1 == self.now.day:
                self.days[n + week_day].configure(fg_color='green', text_color='beige')
            # elif datetime(year, month, n+1).date() in current_days_month:
            #     days[n + week_day].configure(fg_color='light green', text_color='beige')
            # elif datetime(year, month, n+1).date() in current_nights_month:
            #     days[n + week_day].configure(fg_color='light blue', text_color='beige')
            else:
                self.days[n + week_day].configure(fg_color='beige')

        for n in range(week_day):
            self.days[week_day - n - 1].configure(text=back_month_days - n, text_color='beige', fg_color='grey')

        for n in range(6 * 7 - month_days - week_day):
            self.days[week_day + month_days + n].configure(text=n + 1, text_color='beige', fg_color='grey')


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('Календар')
        self.calendar_frame = MyCalendar(self)
        self.calendar_frame.grid(row=0, column=0)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()