import os
import shutil

dirs = [
    'json',
    'output/buffer/transcripts',
    'output/equations',
    'output/figures',
    'output/tables',
    'output/buffer/content_json',
    'ppts',
    'data'
]

for d in dirs:
    sub_paths = os.listdir(d)
    for p in sub_paths:
        file_path = os.path.join(d, p)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    print(f"deleted files/dirs in {d}")

for file in os.listdir('output'):
    # Check if the file is a JSON file and delete it
    if file.endswith('.json'):
        os.remove(os.path.join('output', file))
        print(f"deleted file {file}")