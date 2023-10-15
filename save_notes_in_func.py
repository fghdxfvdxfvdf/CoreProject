# Можна додати по роботі з нотатками до func.py

def add_note(*args):
    title = args[1]
    text = args[2]
    created_at = datetime.now()
    note = Note(title, text, created_at)
    phonebook.add_note(note)
    return f'Note "{title}" added successfully.'

def show_notes(*args):
    notes = phonebook.get_notes()
    if not notes:
        return 'No saved notes.'
    result = '\n\n'.join(f"Title: {note.title}\nText: {note.text}\nCreated at: {note.created_at}" for note in notes)
    return result

