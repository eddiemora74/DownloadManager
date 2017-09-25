import requests
import csv
import shutil
import os
from time import sleep
from PIL import Image
from Helpers.osi import space, clear

# List created to hold all CSV files in current directory
current_csv_files = []


# Set the directory variables where to read and write
directory = os.getcwd() + '\\'
directory_dump = os.getcwd() + '\dump\\'

def downloader():
    # Instantiate variable that will be used for user to select file.
    cf = 0

    # Instantiate variable that will hold the max size of height or width.
    size = 0, 0

    # Create a list that will hold URLs that couldn't be downloaded.
    error_list = []

    # If there is only one CSV file, just use that.
    # Else, list out the files and have the user select which one.
    if len(current_csv_files) == 1:
        print('Using ' + current_csv_files[cf] + '...')
        sleep(1)
    else:
        for x in current_csv_files:
            print(str(current_csv_files.index(x)) + ": " + x)

        space()
        cf = int(input("Select file: "))

    # Match the selection to the file.
    ccf = current_csv_files[cf]

    space()

    # This will be the name of the zipped folder.
    # If left blank, it will use the name of the CSV file.
    folder_name = input("Press ENTER to use CSV name for folder, or enter a custom name: ")

    if folder_name == "":
        folder_name = ccf[:-4]

    space()

    # This asks the user if they want to resize any images that may be downloaded.
    # If so, then the user will be prompted to enter the max width or height.
    resize_images = input("Resize images? [y/n] ")
    if resize_images == 'y':
        space()
        size_pref = int(input("Enter max width or height: "))
        size = size_pref, size_pref
    else:
        space()
        pass

    # This creates the dump folder to download unzipped files.
    directory_folder_name = directory_dump + folder_name
    os.makedirs(directory_folder_name)

    # Open the CSV file, and skip the header.
    # It will establish the URL that will be used in request, and creates the name of the file.
    with open(ccf, newline='') as csvfile:
        tries = 0
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            url = row[0]
            fname, ext = os.path.splitext(url)
            name = row[1] + ext

            # Gets the path of the file to be created
            filename = directory_folder_name + '\\' + name

            # Creates a variable to hold the request
            req = ''

            # As long as the request is blank, it will attempt to download the file.
            while req == '':
                if tries < 3:
                    try:
                        print("Downloading " + name + "...")
                        req = requests.get(url)
                    except:
                        # If the download fails, it will timeout for 5 seconds to let it rest, then try again.
                        print("Connection timeout.")
                        sleep(1)
                        print("Retrying in 5 seconds")
                        tries += 1
                        sleep(5)
                    else:
                        # Open the file that was created and write the content from the request to the file.
                        x = open(filename, 'wb')
                        x.write(req.content)
                        x.close()

                        # If an image and user chose to resize it, then apply the adjustment.
                        if resize_images == 'y' and (
                                            (ext == '.jpg' or ext == '.JPG' or ext == '.jpeg' or ext == '.JPEG') or
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
                        # if no resize, then skip it.
                        else:
                            pass
                # If requests failed to the download file 3 times, then skip it and append it to error list.
                else:
                    print(f"Error downloading {url}. Skipping...")
                    error_list.append(url)
                    sleep(1)

    # Make a zipped version of the folder with all the files.
    print("Compressing folder...")
    shutil.make_archive(folder_name, 'zip', directory_folder_name)

    # Delete the unzipped version.
    print("Deleting uncompressed folder...")
    shutil.rmtree(directory_folder_name)

    sleep(1)

    # If there were any URLs that failed, then list them.
    # Else, it is done.
    if len(error_list) > 0:
        print("URLs that could not be downloaded...")
        for url in error_list:
            print(url)
        space()
    else:
        print("All Done!")

    sleep(1)

    space()


# Takes all CSV files from the directory and appends them to a list
for file in os.listdir(directory):
    if file.endswith('.csv'):
        current_csv_files.append(file)

clear()

# Checks to make sure there are files available to use.
# If there is, it will start the program.
# If not, it will exit the program.
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
