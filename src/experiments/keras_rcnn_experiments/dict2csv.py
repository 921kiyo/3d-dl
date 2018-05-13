import csv
import keras
import keras_rcnn.datasets.shape

"""
utility script to convert data from the keras_rcnn database to keras_retinanet format
"""

training_dictionary, test_dictionary = keras_rcnn.datasets.shape.load_data()

def flatten_dict(the_dict):
    flattened = []
    image_name = the_dict['image']['pathname']
    for object in the_dict['objects']:
        cat = object['category']
        bbox = object['bounding_box']
        x1 = bbox['minimum']['c']
        x2 = bbox['maximum']['c']
        y1 = bbox['minimum']['r']
        y2 = bbox['maximum']['r']
        if(x1==-1 or x2==-1 or y1==-1 or y2==-1):
            print('anomaly detected')
            continue
        flattened.append((image_name, x1, y1, x2, y2, cat))
    return flattened

flattened = []
numrows = 0
for d in test_dictionary:
    numrows += 1
    f = flatten_dict(d)
    flattened.extend(f)
print('Total number of images: ', numrows)

csv_name = 'shapes.csv'
numrows = 0
with open(csv_name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for f in flattened:
            numrows += 1
            writer.writerow(f)

print('Total number of rows: ', numrows)
