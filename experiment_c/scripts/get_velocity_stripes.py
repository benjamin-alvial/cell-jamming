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

    results_plots_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_c/results/plots_velocity/velocity_delta_" + str(delta_frames)

    df_general = pd.read_csv(os.path.join(data_delta_dir, new_csv_name))

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

        average_speed_stripes = [0] * stripe_amount # 1/N * sum(|vect vj|)
        average_module_y_vel = [0] * stripe_amount # 1/N * sum(|vect vyj|)
        average_module_x_vel = [0] * stripe_amount # 1/N * sum(|vect vxj|)
        module_average_velocity_stripes = [0] * stripe_amount # | 1/N * sum(vect j)|

        csv_mask_name = 'final_mask_1_80__' + str(t) + '.csv'
        mask_array = np.loadtxt(os.path.join(results_masks_dir,csv_mask_name), delimiter=',')

        
        for j in range(0, len(df_for_frame)):
            x, y = round(df_for_frame['POS_X'][j]), round(df_for_frame['POS_Y'][j])
            vx, vy = df_for_frame['VEL_X'][j], df_for_frame['VEL_Y'][j]

            # Find the stripe
            stripe_idx = int(mask_array[y][x])
            if stripe_idx < 0:
                continue

            n_spots_stripes[stripe_idx] += 1
            vel_x_stripes[stripe_idx] += vx
            vel_y_stripes[stripe_idx] += vy
            average_module_x_vel[stripe_idx] += abs(vx)
            average_module_y_vel[stripe_idx] += abs(vy)
            average_speed_stripes[stripe_idx] += math.sqrt(vx**2+vy**2)

        for k in range(0, len(n_spots_stripes)):
            n_spots = n_spots_stripes[k]
            if n_spots != 0:
                average_module_x_vel[k] = average_module_x_vel[k] / n_spots
                average_module_y_vel[k] = average_module_y_vel[k] / n_spots
                average_speed_stripes[k] = average_speed_stripes[k] / n_spots
                module_average_velocity_stripes[k] = math.sqrt(vel_x_stripes[k]**2 + vel_y_stripes[k]**2) / n_spots

        # Create the figure and axis objects
        fig, ax1 = plt.subplots()

        # Plot the first four series on the left axis
        ax1.plot(average_speed_stripes, 'r-', label='Average speed')
        ax1.plot(average_module_x_vel, 'g-', label='Average module of x velocity')
        ax1.plot(average_module_y_vel, 'b-', label='Average module of y velocity')
        ax1.plot(module_average_velocity_stripes, 'm-', label='Module of average velocity')
        ax1.set_xlabel('Index')
        ax1.set_ylabel(r'Speed ($\mu$m/h)')
        ax1.legend(loc='upper left')

        # Create a second y-axis
        ax2 = ax1.twinx()

        # Plot the fourth series on the right axis
        ax2.plot(n_spots_stripes, 'y-', label='Number of spots')
        ax2.set_ylabel('Amount')

        # Show the legend for the right axis
        ax2.legend(loc='upper right')

        plt.title('frame '+str(t))

        # Save the figure as a PNG image
        plt.savefig(os.path.join(results_plots_dir,"plot_"+str(t)))        

for option in [12]:
    get_velocity_stripes(delta_frames=option, stripe_amount = 10)

