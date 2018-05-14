from ...kerasmodels import split
import json
import os
import ast
import shutil
import csv

dict_path = 'mergeparams.json'
root = 'D:\\PycharmProjects\\Lobster\\data\\logs\\rendering_debug_logs\\test_run_bbox\\ten_set_model_format_SUN_back_2018-05-05_00_21_25'
images_path = os.path.join(root, 'images')
train_path = os.path.join(images_path, 'train')
val_path = os.path.join(images_path, 'validation')
annot_file = os.path.join(root, 'mergeparams_dump.json')
validation_percentage = 0.2

def get_annotations(filename):
    with open(annot_file) as json_data:
        annot = json.load(json_data)

    annot = annot['all_bboxes']
    annot = ast.literal_eval(annot)
    return annot

def split_annotations(annotations):
    val_annotations = {}
    for class_key in annotations:
        val_annotations[class_key] = {}
    for val_filename in val_filenames:
        class_key = os.path.basename(os.path.dirname(val_filename))
        image_key = os.path.basename(val_filename)
        val_annotations[class_key][image_key] = annotations[class_key].pop(image_key, None)
    return val_annotations

def prepare_csv(annotations, image_root):
    csv_name = os.path.join(image_root, 'annotations.csv')
    with open(csv_name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for class_key in annotations:
            class_annotations = annotations[class_key]
            for image in class_annotations:
                full_path = os.path.join(image_root, class_key, image)
                bbox = class_annotations[image]
                writer.writerow((full_path, bbox[0][0], bbox[1][0], bbox[0][1], bbox[1][1], class_key))
    return csv_name

def make_class_csv(annotations, root):
    csv_name = os.path.join(root, 'classes.csv')
    class_keys = list(annotations.keys())
    class_keys.sort()
    with open(csv_name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i, class_key in enumerate(class_keys):
            writer.writerow((class_key, i))
    return csv_name

if not os.path.exists(train_path):
    os.makedirs(train_path)
    for c in os.listdir(images_path):
        if c == 'train':
            continue
        shutil.move(os.path.join(images_path, c), os.path.join(train_path, c))

annotations = get_annotations(annot_file)
val_filenames = split.split_train_to_validation(images_path, validation_percentage)
val_annotations = split_annotations(annotations)
train_csv = prepare_csv(annotations, train_path)
val_csv = prepare_csv(val_annotations, val_path)
class_csv = make_class_csv(val_annotations, images_path)

print(train_csv)
print(val_csv)
print(class_csv)