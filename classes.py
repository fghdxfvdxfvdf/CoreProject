import re
from collections import UserDict
from datetime import datetime, date


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)


class Name(Field):
    @Field.value.setter
    def value(self, value):
        if 2 < len(value) < 15:
            self._value = value
        else:
            raise ValueError("Ім'я повинно бути від 3 до 15 символів")


class Phone(Field):

    @Field.value.setter
    def value(self, value):
        if value is None:
            self._value = value
        elif len(value) == 10 and value.isdigit():
            self._value = value
        else:
            raise ValueError('Номер телефону має бути: код_оператора ХХХХХХ\nКод оператора: 067, 050, 068, 096, 097,'
                             '098, 063, 093, 099, 095')


class Birthday(Field):

    @Field.value.setter
    def value(self, value: str):
        if value is None:
            self._value = value
        else:
            date_pattern = r'\d{2}\.\d{2}\.\d{4}'  # Регулярка формату дати "dd.mm.yyyy"
            if re.match(date_pattern, value):
                day, month, year = map(int, value.split('.'))
                # Валідація значень дня, місяця та року
                if month in [1, 3, 5, 7, 8, 10, 12]:
                    max_day = 31
                elif month in [4, 6, 9, 11]:
                    max_day = 30
                elif month == 2:
                    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                        max_day = 29  # Високосний рік
                    else:
                        max_day = 28
                else:
                    raise ValueError('Невірний місяць')

                if 1 <= day <= max_day:
                    self._value = datetime(year, month, day).date()
                else:
                    raise ValueError(f"В {month} місяці від 1 до {max_day} днів")
            else:
                raise ValueError('Невірний формат дати. Введіть у форматі dd.mm.yyyy')

    def __str__(self):
        return f"{self._value.strftime('%d.%m.%Y')}"


class Record:
    def __init__(self, name, birthday=None, email=None, address=None):
        self.name = Name(name)  # застосування асоціації під назваю композиція. Об'єкт Name існує поки є об'єкт Record
        self.birthday = Birthday(birthday)
        self.phones = []

    def add_phone(self, number):
        if number is None:
            return
        elif number in map(lambda num: num.value, self.phones):
            return 'вже є у контакта'  # Якщо такий номер вже є у контакта
        else:
            self.phones.append(Phone(number))
            return 'додано до контакту'

    def remove_phone(self, phone: str = None):
        if self.phones == []:
            return None        
        for phone in self.phones:
            if phone.value == phone:
                self.phones.remove(phone) 
                return f'Номер {self.name.value} видалено'
        return f'{self.name.value} такого номеру не знайдено'
    
    def edit_phone(self, old_phone: str, new_phone: str):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError('Такого номеру немає у контакта')
    
    def find_phone(self, phone: str = None):
        if len(self.phones) == 0:
            return None
        for phone in self.phones:
            if phone.value == phone:
                return phone

    def add_birthday(self, birthday):
        if self.birthday.value is None:
            self.birthday = Birthday(birthday)
            return 'додано'
        else:
            return 'вже є'

    def days_to_birthday(self):
        today = date.today()
        current_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()
        if current_birthday < today:
            current_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()
        delta = current_birthday - today
        return delta.days

    def __str__(self):
        if self.birthday.value is not None:
            return (f"{self.name.value}:\n\tPhone: {'; '.join(p.value for p in self.phones)} "
                    f"\n\tbirthday: {self.birthday}, days to birthday: {self.days_to_birthday()}\n")
        return f"{self.name.value}:\n\tPhone: {'; '.join(p.value for p in self.phones)}\n"


class AddressBook(UserDict):
    def add_record(self, user: Record):  # асоціація під назвою агригація
        self.data[user.name.value] = user

    def find(self, name: str):
        for char in self.data:
            if char == name:
                return self.data[char]
        return None 

    def find_birthday_boy(self, days):
        boys = []
        result = ''
        for record in self.data.values():
            if record.birthday.value is None:
                continue
            if record.days_to_birthday() <= int(days):
                boys.append(record)
                # result += f'{record}\n'
        if len(boys) == 0:
            result += f"Найближчі {days} днів іменинників немає"
        else:
            sorted_boys = sorted(boys, key=lambda record: record.days_to_birthday())
            for record in sorted_boys:
                result += f'{record}'
        return result

    def delete(self, name: str):
        result = self.data.pop(name, None)
        return result is not None
    
    def iterator(self, page_size):
        print(self.data)
        keys = list(self.data.keys())
        total_pages = (len(keys) + page_size - 1) // page_size
        keys.sort()

        for page_number in range(total_pages):
            start = page_number * page_size
            end = (page_number + 1) * page_size
            page = {k: self.data[k] for k in keys[start:end]}
            yield page

    def find_match(self, string):
        if not self.data:
            return f'Немає жодного контакту'  # Якщо немає контактів
        result = ''
        for record in self.data.values():
            if string.lower() in record.name.value.lower():
                result += f'{record}\n'

            for number in record.phones:
                if number.value is not None and string in number.value:
                    result += f'{record}\n'

            if record.birthday.value is not None and string in str(record.birthday.value):
                result += f'{record}\n'
        if len(result) == 0:
            result += 'Нічого не знайдено'
        return result
