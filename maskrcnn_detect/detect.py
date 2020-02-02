#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: face.py
Description: Detection function for running the ML model on new image.
"""
import skimage

from .utils import get_ax
from .visualize import display_instances


def detect(image_file, model, class_names):
    """Detect object and draw mask + bboxes

    Args:
    image_file : str with file name
    model : ML model loaded in to memory
    class_names : array of class names

    Returns:
    dict with detection drawn on image and number of detections

    """
    # Run model detection and generate the color splash effect
    print("Running on {}".format(image_file))
    # Read image
    image = skimage.io.imread(image_file)
    # Detect objects from 3 channel image (removing alpha channel as needed)
    r = model.detect([image[:,:,:3]], verbose=1)[0]

    # # Display results
    ax = get_ax(1)
    image_file = display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                                class_names, r['scores'], ax=ax,
                                title="Predictions", show=False)

    return {'image_file': image_file, 'num_objects': len(r['rois'])}


