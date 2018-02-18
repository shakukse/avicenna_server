from copy import copy, deepcopy

import numpy as np


class DummySegmentation:

    def create_segmetns(self, picture):

        masks = np.zeros((5,10))
        segmented_image = picture
        segmentation_info = {"cell_n": 5, "num_bad_cells": 3}
        print(segmented_image)
        return masks, segmented_image, segmentation_info


