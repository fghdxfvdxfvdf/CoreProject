# To add in Class AddressBook (classes.py)

class AddressBook(UserDict):
    # ...
    def search_notes(self, query):
        matching_notes = []
        for note in self.notes:
            if query.lower() in note.title.lower() or query.lower() in note.text.lower():
                matching_notes.append(note)
        return matching_notes



# To add in func.py

# Add a new method to the COMMANDS dictionary

def search_notes(*args):
    query = args[1].lower()
    matching_notes = phonebook.search_notes(query)
    if not matching_notes:
        return 'No notes matching the query were found.'
    result = '\n\n'.join(f"Title: {note.title}\nText: {note.text}\nCreated at: {note.created_at}" for note in matching_notes)
    return result