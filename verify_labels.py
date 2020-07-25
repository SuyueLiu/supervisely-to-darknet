import random

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.patches as patches


def get_classes(path):
    """The path to the meta file generated by supervise.ly"""
    classes = []
    data_folder_name = path.split('/')[-1]
    meta_path = os.path.join(path, 'meta.json')
    with open(meta_path, 'rb') as f:
        contents = json.load(f)
    for content in contents['classes']:
        classes.append(content['title'])

    return classes, data_folder_name


def verify_boxes(img_path, label_path, meta_path):
    camp = plt.get_cmap('tab20b')
    colors = [camp(i) for i in np.linspace(0, 1, 20)]

    print("Image: '%s'" % img_path)
    img = np.array(Image.open(img_path))
    fig, ax = plt.subplots(1)
    ax.imshow(img)

    with open(label_path, 'r') as f:
        objects = f.readlines()

    for obj_idx in range(len(objects)):
        n_boxes = len(objects)
        bbox_color = random.sample(colors, n_boxes)

        box_info = []

        for coor_idx in range(len(objects[obj_idx].split(' '))):
            box_info.append(float(objects[obj_idx].split(' ')[coor_idx]))

        x1 = (box_info[1] - box_info[3] / 2) * img.shape[1]  # * width
        y1 = (box_info[2] - box_info[4] / 2) * img.shape[0]  # * height
        x2 = (box_info[1] + box_info[3] / 2) * img.shape[1]
        y2 = (box_info[2] + box_info[4] / 2) * img.shape[0]

        box_w = x2 - x1
        box_h = y2 - y1

        color = bbox_color[int(obj_idx)]
        bbox = patches.Rectangle((x1, y1), box_w, box_h, linewidth=2, edgecolor=color, facecolor='none')
        ax.add_patch(bbox)

        classes, _ = get_classes(meta_path)

        plt.text(
            x1, y1,
            s=classes[int(box_info[0])],
            color='white',
            verticalalignment='top',
            bbox={'color': color, 'pad': 0},
        )

    plt.axis('off')
    plt.show()



# example:
# verify_boxes('../data/hands6/images/train/0000000361.jpg', '../data/test_data_dir/labels/0000000361.txt', './meta.json')

