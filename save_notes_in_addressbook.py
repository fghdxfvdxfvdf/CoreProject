# Для збереження нотаток з текстовою інформацією в класі AddressBook в файлі classes.py,
# додаємо новий атрибут, який буде зберігати нотатки.
# Також, можна розширити функціональність для додавання та відображення нотаток.
# Наприклад, це можна зробити:

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def get_notes(self):
        return self.notes

    
