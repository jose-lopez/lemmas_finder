from time import sleep
from progress.bar import IncrementalBar as Bar

files = 10

with Bar(f'Files on process: {int(files)}') as bar_files:

    for i in range(int(files)):

        sleep(0.02)

        with Bar(f'File on process: {i}', color="white") as bar_file:

            sleep(0.01)
