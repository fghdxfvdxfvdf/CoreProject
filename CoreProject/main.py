from CoreProject.func import *
import customtkinter
import my_calendar_frame
from CoreProject import sorted_files


def change_theme_menu(new_appearance):
    customtkinter.set_appearance_mode(new_appearance)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_default_color_theme('green')
        self.geometry('1200x850')
        self.title('My phonebook')
        # self.resizable(False, False)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.first_frame = customtkinter.CTkFrame(self)
        self.first_frame.grid(row=0, column=1, padx=(20, 20), pady=(10, 10), sticky='ew')
        self.tablo_lbl = customtkinter.CTkLabel(self.first_frame, text='Тут могла бути ваша реклама', font=('Arial bold', 30),
                                                text_color=('black', 'beige'))
        # self.tablo_lbl.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky='w')
        self.lbl = customtkinter.CTkLabel(self.first_frame, text='Hello', font=('Arial bold', 30),
                                          text_color=('black', 'beige'))
        self.lbl.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky='w')
        self.entry_input = customtkinter.CTkEntry(self.first_frame, width=880, height=50, font=('Arial bold', 20))
        self.entry_input.grid(row=2, column=0, padx=(20, 20), sticky='ew')
        self.lbl_count = customtkinter.CTkLabel(self.first_frame, text=f'{len(phonebook)} контактів', font=('Arial bold', 16),
                                                text_color=('black', 'beige'))
        self.lbl_count.grid(row=3, column=0, pady=(10, 10), sticky='nsew')

        self.btn_frame = customtkinter.CTkFrame(self)
        self.btn_frame.grid(row=0, column=0, rowspan=2, pady=(20, 20))
        self.btn_add = customtkinter.CTkButton(self.btn_frame, text='Додати', text_color='yellow',
                                               fg_color=('green', 'black'), hover_color='purple', font=('Arial bold', 16),
                                               command=self.added)
        self.btn_add.grid(row=0, column=0, padx=(25, 25), pady=(15, 15), sticky='ew')
        self.btn_remove = customtkinter.CTkButton(self.btn_frame, text='Видалити', text_color='yellow',
                                                  fg_color=('green', 'black'), hover_color='purple', font=('Arial bold', 16),
                                                  command=self.delete_app)
        self.btn_remove.grid(row=1, column=0, padx=(25, 25), pady=(15, 15), sticky='ew')
        self.btn_change = customtkinter.CTkButton(self.btn_frame, text='Змінити', text_color='yellow',
                                                  fg_color=('green', 'black'), hover_color='purple', font=('Arial bold', 16),
                                                  command=self.change_app)
        self.btn_change.grid(row=2, column=0, padx=(25, 25), pady=(15, 15), sticky='ew')
        self.btn_find = customtkinter.CTkButton(self.btn_frame, text='Знайти', text_color='yellow',
                                                fg_color=('green', 'black'), hover_color='purple', font=('Arial bold', 16),
                                                command=self.show_app)
        self.btn_find.grid(row=3, column=0, padx=(25, 25), pady=(15, 15), sticky='ew')
        self.btn_find = customtkinter.CTkButton(self.btn_frame, text='Показати всі', text_color='yellow',
                                                fg_color=('green', 'black'), hover_color='purple',
                                                font=('Arial bold', 16), command=self.show_all_app)
        self.btn_find.grid(row=4, column=0, padx=(25, 25), pady=(15, 15), sticky='ew')
        self.btn_sorted_files = customtkinter.CTkButton(self.btn_frame, text='Сортувати файли', text_color='yellow',
                                                        fg_color=('green', 'black'), hover_color='purple',
                                                        font=('Arial bold', 16), command=self.sort_files_app)
        self.btn_sorted_files.grid(row=5, column=0, padx=(25, 25), pady=(15, 15), sticky='ew')
        self.btn_ok = customtkinter.CTkButton(self.btn_frame, text='Дні народження на тижні', text_color='yellow',
                                              fg_color=('green', 'black'), hover_color='purple', font=('Arial bold', 16))
        self.btn_ok.grid(row=6, column=0, padx=(25, 25), pady=(15, 15), sticky='ew')

        self.out_frame = customtkinter.CTkFrame(self)
        self.out_frame.grid(row=1, column=1, padx=(20, 20), pady=(10, 10), sticky='nsew', rowspan=3)
        self.out_text = customtkinter.CTkTextbox(self.out_frame, font=('Arial bold', 20), width=880, height=450)
        self.out_text.grid(row=0, column=0, padx=(20, 20), pady=(10, 10), sticky='nsew')

        self.menu_frame = customtkinter.CTkFrame(self, border_color='black')
        self.menu_frame.grid(row=2, column=0, padx=(0, 20), pady=(0, 20))
        self.appearance_menu = customtkinter.CTkOptionMenu(self.menu_frame, values=['Light', 'Dark', 'System'],
                                                           command=change_theme_menu, fg_color=('green', 'black'),
                                                           text_color='yellow', font=('Arial bold', 16))
        self.appearance_menu.grid(row=0, column=0)
        self.appearance_menu.set('System')

        self.calendar_frame = my_calendar_frame.MyCalendar(self)
        self.calendar_frame.grid(row=3, column=0, padx=(20, 0), pady=(0, 20))

    def added(self):
        self.entry_input.focus()
        self.out_text.delete('1.0', 'end')
        value = self.entry_input.get()
        list_value = value.split()
        self.lbl.configure(text=add('add', *list_value))
        self.entry_input.delete('0', 'end')
        self.lbl_count.configure(text=f'{len(phonebook)} контактів')

    def change_app(self):
        self.entry_input.focus()
        self.out_text.delete('1.0', 'end')
        value = self.entry_input.get()
        list_value = value.split()
        if len(list_value) < 3:
            self.lbl.configure(text="Введіть через пробіл ім'я, старий номер та новий номер")
        else:
            self.lbl.configure(text=change('change', *list_value))
        self.entry_input.delete('0', 'end')

    def show_app(self):
        self.entry_input.focus()
        self.lbl.configure(text="")
        self.out_text.delete('1.0', 'end')
        value = self.entry_input.get()
        if not value:
            self.out_text.insert('1.0', 'Нічого не знайдено')
            self.lbl.configure(text="Введіть ім'я або номер або дату народження")
        else:
            self.out_text.insert('1.0', phonebook.find_match(value))
        self.entry_input.delete('0', 'end')

    def delete_app(self):
        self.entry_input.focus()
        self.lbl.configure(text="Для видалення контакту введіть ім'я.\nДля видалення номеру введіть ім'я та номер")
        self.out_text.delete('1.0', 'end')
        value = self.entry_input.get()
        list_value = value.split()
        if len(list_value) == 1:
            self.lbl.configure(text=delete('delete', *list_value))
        elif len(list_value) == 2:
            self.lbl.configure(text=remove('remove', *list_value))
        self.entry_input.delete('0', 'end')
        self.lbl_count.configure(text=f'{len(phonebook)} контактів')

    def show_all_app(self):
        self.entry_input.delete('0', 'end')
        self.out_text.delete('1.0', 'end')
        value = self.entry_input.get()
        list_value = value.split()
        self.lbl.configure(text="")
        self.out_text.insert('1.0', show_all('show all', *list_value))

    def sort_files_app(self):
        self.entry_input.focus()
        self.out_text.delete('1.0', 'end')
        value = self.entry_input.get()
        if len(value) == 0:
            self.lbl.configure(text="Введіть повний шлях до папки")
        else:
            try:
                self.lbl.configure(text=sorted_files.sorted_files(value))
            except FileNotFoundError:
                self.lbl.configure(text="Такої папки не існує або не вірний шлях")
        self.entry_input.delete('0', 'end')


def main():
    app = App()
    app.mainloop()
    with open('book.bin', 'wb') as fh:
        pickle.dump(phonebook, fh)


if __name__ == '__main__':
    main()