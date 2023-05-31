# Given an original skeletonized version of the white border
# on black background, generates and saves the
# 1. binarized version (image)
# 2. mapping version (image)
# 3. mask array (csv)

# In this context, a mapping is an image where EVERY pixel
# in the y dimension (each row) has ONE AND ONLY one white border
# pixel (column) associated in that row.

from PIL import Image
import numpy as np
import os
import pandas as pd
import generate_mask

results_border_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_c/results/images_final_border/"
results_binarized_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_c/results/images_final_binarized/"
results_injection_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_c/results/images_final_injection/"
results_masks_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_c/results/csvs_final_mask/"

offset = 20
delta_x = 100

for i in range(1, 81):
    img_border_name = 'final_border_1_80__' + str(i) + '.png'
    img_binarized_name = 'final_binarized_1_80__' + str(i) + '.png'
    img_injection_name = 'final_injection_1_80__' + str(i) + '.png'
    csv_mask_name = 'final_mask_1_80__' + str(i) + '.csv'

    image = Image.open(os.path.join(results_border_dir, img_border_name)).convert('L')

    # Binarize the image
    binarized_image = image.point(lambda x: 255 if x > 0 else 0, '1')
    binarized_image.save(os.path.join(results_binarized_dir, img_binarized_name))

    binarized_array = np.array(binarized_image)

    # Iterate over each row of the image
    for row in range(binarized_array.shape[0]):
        found_white_pixel = False

        # Iterate over each pixel in the row
        for col in range(binarized_array.shape[1]):

            if found_white_pixel:
                if binarized_array[row, col] == True:
                    binarized_array[row, col] = 0
                
            else:
                if binarized_array[row, col] == True:
                    found_white_pixel = True

    injection_image = Image.fromarray(binarized_array)
    injection_image.save(os.path.join(results_injection_dir, img_injection_name))

    mask_array = generate_mask.get_mask(injection_image, offset, delta_x)
    np.savetxt(os.path.join(results_masks_dir,csv_mask_name), mask_array, delimiter=',')
    #generate_mask.visualize_mask(mask_array)
