# Given the dataframe with the calculated velocities,
# finds the stripe each spot is in to plot
# velocity_x/velocity_y/speed/number_spots vs. the index.

import pandas as pd
import numpy as np
import os
import math
import matplotlib.pyplot as plt

results_masks_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_c/results/csvs_final_mask/"

def get_velocity_stripes(delta_frames, stripe_amount):

    data_delta_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_c/data_extracted/velocity_delta/"
    new_csv_name = "velocities_delta_"+str(delta_frames)+".csv"

    results_plots_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_c/results/plots_velocity/velocity_delta_/" + str(delta_frames)

    df_general = pd.read_csv(os.path.join(results_data_delta_dir, new_csv_name))

    # Iterate over the frames and generate their dataframe.
    for t in df_general.FRAME.unique():

        t = int(t+1)

        df_for_frame = df_general[df_general['FRAME'] == t]
        df_for_frame = df_for_frame.reset_index(drop=True)

        csv_mask_name = 'final_mask_1_80__' + str(t) + '.csv'

        # Velocity will only be calculated for the given amount of stripes.
        n_spots_stripes = [0] * stripe_amount
        vel_x_stripes = [0] * stripe_amount
        vel_y_stripes = [0] * stripe_amount
        speed_stripes = [0] * stripe_amount

        csv_mask_name = 'final_mask_1_80__' + str(t) + '.csv'
        mask_array = np.loadtxt(os.path.join(results_masks_dir,csv_mask_name), delimiter=',')

        for j in range(0, len(df_for_frame)):
            x, y = round(df_for_frame['POS_X'][j]), round(df_for_frame['POS_Y'][j])
            vx, vy = df_for_frame['VEL_X'][j], df_for_frame['VEL_Y'][j]

            # Find the stripe
            stripe_idx = int(mask_array[y][x])
            if stripe_idx < 0 or stripe_idx >= 10: # WIP: get real injection near borders.
                continue

            n_spots_stripes[stripe_idx] += 1
            vel_x_stripes[stripe_idx] += vx
            vel_y_stripes[stripe_idx] += vy
            speed_stripes[stripe_idx] += math.sqrt(vx**2+vy**2)

        for k in range(0, len(n_spots_stripes)):
            n_spots = n_spots_stripes[k]
            if n_spots != 0:
                vel_x_stripes[k] = vel_x_stripes[k] / n_spots
                vel_y_stripes[k] = vel_y_stripes[k] / n_spots
                speed_stripes[k] = speed_stripes[k] / n_spots

        #plt.plot(n_spots_stripes, label='Number of spots')
        #plt.plot(vel_x_stripes, label='Velocity in x')
        #plt.plot(vel_y_stripes, label='Velocity in y')
        if t < 10:
            plt.plot(speed_stripes, label='Speed')
            plt.xlabel('Index')
            plt.ylabel('Value')
            plt.title('frame '+str(t))
            plt.savefig(os.path.join(results_data_delta_dir,"plot_"+str(t)))
            plt.show()

for option in [12]:
    get_velocity_stripes(delta_frames=option, stripe_amount = 10)

