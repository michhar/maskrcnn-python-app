#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: face.py
Description: Face section of the Cognitive Face API.
"""
import skimage

from . import util
from .util import get_ax
from .visualize import display_instances


def detect(image_file, model, class_names):
    """Detect car damage

    Args:

    Returns:

    """
    # Run model detection and generate the color splash effect
    print("Running on {}".format(image_file))
    # Read image
    image = skimage.io.imread(image_file)
    # Detect objects
    r = model.detect([image], verbose=1)[0]

    # # Display results
    ax = get_ax(1)
    image_file = display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                                class_names, r['scores'], ax=ax,
                                title="Predictions", show=False)

    return {'image_file': image_file, 'num_objects': len(r['rois'])}

def detect_service(image, face_id=True, landmarks=False, attributes=''):
    """Detect human faces in an image and returns face locations, and
    optionally with `face_id`s, landmarks, and attributes.

    Args:
        image: A URL or a file path or a file-like object represents an image.
        face_id: [Optional] Return faceIds of the detected faces or not. The
            default value is true.
        landmarks: [Optional] Return face landmarks of the detected faces or
            not. The default value is false.
        attributes: [Optional] Analyze and return the one or more specified
            face attributes in the comma-separated string like
            "age,gender". Supported face attributes include age, gender,
            headPose, smile, facialHair, glasses, emotion, makeup, accessories,
            occlusion, blur, exposure, noise. Note that each face attribute
            analysis has additional computational and time cost.

    Returns:
        An array of face entries ranked by face rectangle size in descending
        order. An empty response indicates no faces detected. A face entry may
        contain the corresponding values depending on input parameters.
    """
    url = 'detect'
    headers, data, json = util.parse_image(image)
    params = {
        'returnFaceId': face_id and 'true' or 'false',
        'returnFaceLandmarks': landmarks and 'true' or 'false',
        'returnFaceAttributes': attributes,
    }

    return util.request(
        'POST', url, headers=headers, params=params, json=json, data=data)

