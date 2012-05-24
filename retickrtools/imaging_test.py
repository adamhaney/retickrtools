"""
imaging_test.py demonstrates the capabilaties of the imaging module.

@author: Cory Walker
@organization: Retickr
@contact: cory.walker@retickr.com

"""

from imaging import round_corners

# These could also be StringIO instances instead of files
image_f = open('imaging_example.png', 'r')
save_f = open('imaging_example_icon.png', 'w')
round_corners(image_f, save_f)
