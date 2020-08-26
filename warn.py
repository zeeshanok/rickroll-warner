import imagehash
from PIL import Image
import sys, os, glob
import cv2

def framize_rickroll():
    
    vidcap = cv2.VideoCapture('base_video/rickroll.mp4')
    
    success, image = vidcap.read()
    i = 0
    c = 0
    slash_progress_list = [
        '\\','\\','\\','\\','\\',
        '|', '|', '|', '|', '|',
        '/', '/', '/', '/', '/',
        '-', '-', '-', '-', '-',
    ]
    while success:
        if c > len(slash_progress_list) - 1:
            c = 0
        cv2.imwrite(f'base_pics/frame-{i}.jpg',image)
        success, image = vidcap.read()
        sys.stdout.write(f"Frames created: {i+1}  {slash_progress_list[c]}\r")
        sys.stdout.flush()
        i += 1
        c += 1

def check_for_base_pics():
    base_pics = 'base_pics'

    if not os.path.exists('base_video') or not len([i for i in os.listdir('base_video')]):
        try:
            os.mkdir('base_video')
        except FileExistsError:
            print('There is no file in "base_video". Put one')
            input()
            sys.exit()
            return
        print('Put a video in "base_video" to compare it with other images')
        input()
        sys.exit()

    if not os.path.exists(base_pics):
        os.mkdir(base_pics)
    if len([i for i in os.listdir(base_pics)]) < 20:
        print(f'There are less than 20 images of rickrolls in "{base_pics}"')
        if input('Do you want to create more pictures? [Y]es or [N]o ').lower() == 'y':
            framize_rickroll()
            print('Files created successfully. Rerun this script to work')

def check_for_rickroll():
    compare_pics = 'compare_pics'
    base_pics = 'base_pics'

    if not os.path.exists(base_pics):
        check_for_base_pics()
        return
    if not os.path.exists(compare_pics):
        os.mkdir(compare_pics)
        print(f'Add your pictres to the folder named {compare_pics} and run this script again')
        return
    compare_pics_list = [i for i in os.listdir(compare_pics)]
    base_pics_list = [i for i in os.listdir(base_pics)]
    for j in compare_pics_list:
        if j.startswith('__'):
            continue
        print(f'\n\n{j}\n')
        hash0 = imagehash.average_hash(Image.open(f'{compare_pics}/{j}'))
        c = 0
        cutoff = 5
        success = False
        for i in base_pics_list:
            hash1 = imagehash.average_hash(Image.open(f'{base_pics}/{i}'))
            if hash0 - hash1 < 5:
                print(f"Warning the file: \"{j}\" has a chance of being a rick roll")
                print(f'It seemed similar to {i}')
                success = True
                break
            else:
                progress = int(((c*20)/len(base_pics_list)))
                sys.stdout.write(
                    f'|{"█"*progress}{"░"*(20-progress)}|  ({int(progress * 100 / 20)}%) ... {i}\r')
                sys.stdout.flush()
                c += 1
                continue
            success = False
        sys.stdout.flush()
        if not success:
            sys.stdout.flush()
            print('\nIt seems that wasnt a rickroll. Lucky you')
        print(f'\nTotal images compared with {j}: {c}')


if __name__ == '__main__':
    check_for_base_pics()
    check_for_rickroll()
    input('\nPress any key to continue...')
