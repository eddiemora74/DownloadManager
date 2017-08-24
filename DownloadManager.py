import requests
import csv
from random import randint
import shutil
import os
from time import sleep
from PIL import Image


def s():
    return randint(1, 10000)


def space():
    print("")


def clear():
    os.system('cls')


current_csv_files = []

directory = 'C:\pythonFiles\DownloadManager\\'
directory_dump = 'C:\pythonFiles\DownloadManager\dump\\'


def downloader():
    cf = 0

    size = 0, 0

    if len(current_csv_files) == 1:
        print('Using ' + current_csv_files[cf] + '...')
        sleep(1)
    else:
        for x in current_csv_files:
            print(str(current_csv_files.index(x)) + ": " + x)

        space()
        cf = int(input("Select file: "))

    ccf = current_csv_files[cf]

    space()

    folder_name = input("Press ENTER to use CSV name for folder, or enter a custom name: ")

    if folder_name == "":
        folder_name = ccf[:-4]

    space()

    resize_images = input("Resize images? [y/n] ")
    if resize_images == 'y':
        space()
        size_pref = int(input("Enter max width or height: "))
        size = size_pref, size_pref
    else:
        space()
        pass

    directory_folder_name = directory_dump + folder_name

    os.makedirs(directory_folder_name)

    with open(ccf, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            url = row[0]
            # head, tail = os.path.split(url)
            fname, ext = os.path.splitext(url)
            name = row[1] + ext  # + '_' + tail

            filename = directory_folder_name + '\\' + name

            req = ''

            while req == '':
                try:
                    print("Downloading " + name + "...")
                    req = requests.get(url)
                except:
                    print("Connection timeout.")
                    sleep(1)
                    print("Retrying in 5 seconds")
                    sleep(5)
                else:
                    x = open(filename, 'wb')
                    x.write(req.content)
                    x.close()

                    if resize_images == 'y' and ((ext == '.jpg' or ext == '.JPG' or ext == '.jpeg' or ext == '.JPEG') or
                                                     (ext == '.png' or ext == '.PNG') or
                                                     (ext == '.bmp' or ext == '.BMP') or
                                                     (ext == '.TIF')):

                        c = Image.open(filename)

                        if c.height > size_pref or c.width > size_pref:
                            print("Resizing image...")
                            c.thumbnail(size, Image.ANTIALIAS)
                            c.save(filename)
                            c.close()
                        else:
                            c.close()
                            pass

                    else:
                        pass

    print("Compressing folder...")
    shutil.make_archive(folder_name, 'zip', directory_folder_name)

    print("Deleting uncompressed folder...")
    shutil.rmtree(directory_folder_name)

    sleep(1)

    print("All Done!")

    sleep(1)

    space()


for file in os.listdir(directory):
    if file.endswith('.csv'):
        current_csv_files.append(file)

clear()

if len(current_csv_files) == 0:
    print("No CSV files found!")
    sleep(1)
    space()
    print("Please save your CSV file to " + directory)
    space()
    print("Exiting in 5 seconds...")
    sleep(5)
else:
    downloader()
