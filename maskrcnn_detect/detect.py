#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: face.py
Description: Detection function for running the ML model on new image.
"""
import sys
sys.path.append('.')  # To find local version of the library

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
    # Read image
    image = skimage.io.imread(image_file)
    print(f"Read {image_file}.")

    # Detect objects from 3 channel image (removing alpha channel as needed)
    r = model.detect([image[:,:,:3]], verbose=1)[0]
    print(f"Done running detection on {image_file}.")

    # # Display results
    ax = get_ax(1)
    image_file = display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                                class_names, r['scores'], ax=ax,
                                title="Predictions", show=False)
    print(f"Created instances display.")
    print(f"Number of objects = {len(r['rois'])}")
    
    return {'image_file': image_file, 'num_objects': len(r['rois'])}


async def async_detect(image_file, model, class_names):
    """Detect object and draw mask + bboxes

    Args:
    image_file : str with file name
    model : ML model loaded in to memory
    class_names : array of class names

    Returns:
    dict with detection drawn on image and number of detections

    """
    # Read image
    image = skimage.io.imread(image_file)
    print(f"Read {image_file}.")

    # Detect objects from 3 channel image (removing alpha channel as needed)
    r = model.detect([image[:,:,:3]], verbose=1)[0]
    print(f"Done running detection on {image_file}.")

    # # Display results
    ax = get_ax(1)
    image_file = display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                                class_names, r['scores'], ax=ax,
                                title="Predictions", show=False)
    print(f"Created instances display.")
    print(f"Number of objects = {len(r['rois'])}")
    
    return {'image_file': image_file, 'num_objects': len(r['rois'])}


