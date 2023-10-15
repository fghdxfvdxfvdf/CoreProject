import re
import shutil
import sys
from pathlib import Path


def normalize(name):

    UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюяы'
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t","u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja", "y")
    TRANS = {}
    for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
        TRANS[ord(key)] = value
        TRANS[ord(key.upper())] = value.upper()
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)

    return f"{new_name}.{'.'.join(extension)}"


def scan_folders(folder):
    groups_files = {
        'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
        'video': ['AVI', 'MP4', 'MOV', 'MKV'],
        'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
        'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
        'archives': ['ZIP', 'GZ', 'TAR']
    }
    ignored_folders = ['archives', 'images', 'video', 'documents', 'audio']

    result = {'images': [], 'video': [], 'documents': [], 'audio': [], 'archives': [], 'others': [], 'unknown': [],
              'extentions': []}

    for item in folder.iterdir():
        if item.is_dir():

            if item.name in ignored_folders:
                continue
            else:
                live_result = scan_folders(item)
                result.update((key, result[key] + live_result[key]) for key in result)
        if item.is_file():
            extension = item.suffix.upper().lstrip('.')
            if extension in groups_files['images']:
                result['images'].append(item)
                result['extentions'].append(extension)
            elif extension in groups_files['video']:
                result['video'].append(item)
                result['extentions'].append(extension)
            elif extension in groups_files['documents']:
                result['documents'].append(item)
                result['extentions'].append(extension)
            elif extension in groups_files['audio']:
                result['audio'].append(item)
                result['extentions'].append(extension)
            elif extension in groups_files['archives']:
                result['archives'].append(item)
                result['extentions'].append(extension)
            else:
                result['others'].append(item)
                result['unknown'].append(extension)
    result['extentions'] = list(set(result['extentions']))
    result['unknown'] = list(set(result['unknown']))

    return result


def translation(folder):
    for item in folder.iterdir():
        if item.is_dir():
            translation(item)
        new_name = normalize(item.name).rstrip('.')
        item.rename(folder / new_name)


def moving_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    distinction = target_folder / path.name
    shutil.move(path, distinction)


def moving_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    if not target_folder.exists():
        target_folder.mkdir()
    new_name = path.name.replace(path.suffix, '')
    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)
    try:
        shutil.unpack_archive(path, archive_folder)
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(folder_path):
    for item in folder_path.iterdir():
        if item.is_dir():
            if not any(item.iterdir()):
                item.rmdir()
                remove_empty_folders(folder_path)
            else:
                remove_empty_folders(item)


def sorted_files(path):
    folder_path = Path(path)
    print(path)
    folder_path = folder_path.rename(folder_path.parent / normalize(folder_path.name).rstrip('.'))
    translation(folder_path)
    lists_files = scan_folders(folder_path)
    for key, val in lists_files.items():
        print(f'{key} : {val}')
    for key, value in lists_files.items():
        if key == 'extentions' or key == 'unknown':
            continue
        if key == 'archives':
            for file in value:
                moving_archive(file, folder_path, key)
        else:
            for file in value:
                moving_file(file, folder_path, key)

    remove_empty_folders(folder_path)
    return f'{folder_path.name} успішно відсортовонно'


def main():
    # folder_path = Path(sys.argv[1])
    folder_path = Path('L:/Projects/Мотлох')
    sorted_files(folder_path)


if __name__ == '__main__':
    main()