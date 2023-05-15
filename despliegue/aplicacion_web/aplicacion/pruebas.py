import os
import ccbhash
import views

hashes = {}
for (dir_path, dir_names, file_names) in os.walk('/'):
    if 'Downloads' in dir_path or 'Desktop' in dir_path:
        continue
    files = []
    for file in file_names:
        if file.endswith('.exe'):
            files.append(file)
    if len(files) > 0:
        for file in files:
            file_hash = ccbhash.calculate_ccbhash(f'{dir_path}/{file}')
            hashes[f'{dir_path}/{file}'] = file_hash
            print(f'{dir_path}/{file}: Hash calculated')
            mascot_2={
                "name": {file},
                "ccbhash" : {file_hash}
            }
            views.collection.insert_one(mascot_2)
