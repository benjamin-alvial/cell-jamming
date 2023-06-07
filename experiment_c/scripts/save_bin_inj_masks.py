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

    # ONE WHITE PER ROW
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

    # EVERY ROW HAS ONE WHITE
    # Patch upper hole
    found_uppermost_white_pixel = False
    for row in range(binarized_array.shape[0]):
        
        # Iterate over each pixel in the row
        for col in range(binarized_array.shape[1]):

                if binarized_array[row, col] == True:
                    uppermost_white_pixel_col = col
                    uppermost_white_pixel_row = row
                    found_uppermost_white_pixel = True
                    break

        if found_uppermost_white_pixel:
            break

    for row in range(uppermost_white_pixel_row):
        binarized_array[row, uppermost_white_pixel_col] = 1

    # Patch lower hole
    found_lowermost_white_pixel = False
    for row in reversed(range(binarized_array.shape[0])):
        
        # Iterate over each pixel in the row
        for col in range(binarized_array.shape[1]):

                if binarized_array[row, col] == True:
                    lowermost_white_pixel_col = col
                    lowermost_white_pixel_row = row
                    found_lowermost_white_pixel = True
                    break

        if found_lowermost_white_pixel:
            break
            
    for row in reversed(range(lowermost_white_pixel_row, binarized_array.shape[0])):
        binarized_array[row, lowermost_white_pixel_col] = 1

    injection_image = Image.fromarray(binarized_array)
    injection_image.save(os.path.join(results_injection_dir, img_injection_name))

    mask_array = generate_mask.get_mask(injection_image, offset, delta_x)
    np.savetxt(os.path.join(results_masks_dir,csv_mask_name), mask_array, delimiter=',')
    #generate_mask.visualize_mask(mask_array)
