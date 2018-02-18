import numpy as np
from PIL import Image
import numpy as np
import model as modellib
from CellsDataset import CellsConfig, CellsDataset
import visualize as visualize

import sys
sys.path.insert(0, '/home/pony/Models/Data_Science_Bowl_2018_Mask_RCNN/src/')

# Create model object in inference mode.
model_inf = modellib.MaskRCNN(mode="inference", model_dir='/home/pony/Models/Data_Science_Bowl_2018_Mask_RCNN/src/', config=config)

# Load weights trained on MS-COCO
model_inf.load_weights('/home/pony/Models/Data_Science_Bowl_2018_Mask_RCNN/src/model_weights3.h5', by_name=True)



model_inf = modellib.MaskRCNN(mode="inference", model_dir='/home/pony/', config=config)


class DummySegmentation:

    #def create_segments(self, picture):

        #masks = np.zeros((5,10))
        #segmented_image = picture
        #segmentation_info = {"cell_n": 5, "num_bad_cells": 3}
        #print(segmented_image)
        #return masks, segmented_image, segmentation_info


    create_segments(self, picture, output):
        img = Image.open(picture)
        oldwidth, oldheight = img.size
        newsize = (250, 250)
        img.thumbnail(newsize, Image.ANTIALIAS)
        image = np.array(img)[:,:,:3]

        r = model_inf.detect([image], verbose=0)[0]
        visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                                ['nucleus', 'nucleus'], r['scores'], output=output)
        return len(r['class_ids'])
