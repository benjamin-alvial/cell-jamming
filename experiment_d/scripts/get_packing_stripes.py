# Reads the png images one by one.
# For each image, iterates over the pixels,
# finding their parent stripe, and calculating packing fraction for each stripe.

import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

images_original_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/data_extracted/images_original_tif/"
results_masks_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/results/csvs_final_mask/"
results_plots_packing_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/results/plots_packing/"

def read_tiff(path):
    img = Image.open(path)
    images = []
    for i in range(img.n_frames):
        img.seek(i)
        images.append(np.array(img))
    return np.array(images)

def get_packing_stripes(stripe_amount):

    for t in range(1,186):

        img_name = 'frame_' + str(t).zfill(3) + '.tif'
        img = Image.open(os.path.join(images_original_dir, img_name))
        grayscale_image = img.convert("L")
        pixel_data = grayscale_image.load()

        total_pixels_stripes = [0] * stripe_amount
        black_pixels_stripes = [0] * stripe_amount
        non_black_pixels_stripes = [0] * stripe_amount
        packing_fraction_stripes = [0] * stripe_amount

        csv_mask_name = 'final_mask_1_185__' + str(t) + '.csv'
        mask_array = np.loadtxt(os.path.join(results_masks_dir,csv_mask_name), delimiter=',')

        # Iterate over the pixels
        width, height = grayscale_image.size
        for x in range(width):
            for y in range(height):
                # Get the pixel value at the current position
                pixel_value = pixel_data[x, y]
                stripe_idx = int(mask_array[y][x])

                if stripe_idx < 0 or stripe_idx >= 10: # WIP: get real injection near borders.
                    continue

                # Check if the pixel is black (0) or non-black (any other value)
                if pixel_value == 0:
                    black_pixels_stripes[stripe_idx] += 1
                else:
                    non_black_pixels_stripes[stripe_idx] += 1

                total_pixels_stripes[stripe_idx] += 1


        for k in range(0, len(total_pixels_stripes)):
            total_pixels = total_pixels_stripes[k]
            packing_fraction_stripes[k] = non_black_pixels_stripes[k] / total_pixels

        fig, ax = plt.subplots()

        plt.plot(packing_fraction_stripes)

        ax.set_ylim(0.3, 0.6)
        ax.set_xlabel('Index')
        ax.set_ylabel('Packing fraction')
        plt.title('frame '+str(t))

        plt.savefig(os.path.join(results_plots_packing_dir,"packing_"+str(t)))
        #plt.show()
        plt.close()   

get_packing_stripes(stripe_amount = 10)