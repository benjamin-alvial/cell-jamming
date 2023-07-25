# Given the dataframe with the calculated velocities,
# finds the stripe each spot is in to plot
# velocities vs. the index.

import pandas as pd
import numpy as np
import os
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

results_masks_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/results/csvs_final_mask/"

def exponential_func(x, a, b, c):
    return a * np.exp(-b * x) + c

def fit_exponential(data, start_index):
    x = np.arange(len(data))
    y = data[start_index:]
    popt, _ = curve_fit(exponential_func, x[start_index:], y, p0=[17,0.3,14], maxfev=5000)
    return popt

def get_velocity_stripes(delta_frames, stripe_amount):

    data_delta_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/data_extracted/velocity_delta/"
    new_csv_name = "velocities_delta_"+str(delta_frames)+".csv"

    results_plots_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/results/plots_velocity/velocity_delta_" + str(delta_frames)
    expfit_plots_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/results/plots_expfit/expfit_delta_" + str(delta_frames)
    stripesobs_plots_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/results/plots_stripesobs/stripesobs_delta_" + str(delta_frames)
    stdev_plots_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/results/plots_stdev/stdev_delta_" + str(delta_frames)

    df_general = pd.read_csv(os.path.join(data_delta_dir, new_csv_name))

    frame_list = []
    b_matrix = []

    # Each element of the following lists is a list [O0, O1, ..., Oi]
    # where Oj is the observable O measured in stripe of index j
    average_module_x_vel_in_time = []
    average_module_y_vel_in_time = []
    average_speed_stripes_in_time = []
    module_average_velocity_stripes_in_time = []

    # Iterate over the frames and generate their dataframe.
    for t in df_general.FRAME.unique():

        t = int(t+1)

        df_for_frame = df_general[df_general['FRAME'] - t < 0.001]
        df_for_frame = df_for_frame.reset_index(drop=True)

        csv_mask_name = 'final_mask_1_185__' + str(t) + '.csv'

        # Velocity will only be calculated for the given amount of stripes.
        n_spots_stripes = [0] * stripe_amount
        vel_x_stripes = [0] * stripe_amount
        vel_y_stripes = [0] * stripe_amount
        vel_x_normalized_stripes = [0] * stripe_amount
        vel_y_normalized_stripes = [0] * stripe_amount

        average_speed_stripes = [0] * stripe_amount # 1/N * sum(|vect vj|)
        average_module_y_vel = [0] * stripe_amount # 1/N * sum(|vect vyj|)
        average_module_x_vel = [0] * stripe_amount # 1/N * sum(|vect vxj|)
        module_average_velocity_stripes = [0] * stripe_amount # | 1/N * sum((vect j)/|vect j|) |
        average_speed_squares_stripes = [0] * stripe_amount
        stdev_stripes = [0] * stripe_amount

        csv_mask_name = 'final_mask_1_185__' + str(t) + '.csv'
        mask_array = np.loadtxt(os.path.join(results_masks_dir,csv_mask_name), delimiter=',')
        
        for j in range(0, len(df_for_frame)):
            x, y = round(df_for_frame['POS_X'][j]), round(df_for_frame['POS_Y'][j])
            vx, vy = df_for_frame['VEL_X'][j], df_for_frame['VEL_Y'][j]

            # Find the stripe
            if y == 648: 
                continue

            stripe_idx = int(mask_array[y][x])
            if stripe_idx < 0 or stripe_idx >= stripe_amount:
                continue

            if math.sqrt(vx**2+vy**2) == 0:
                continue

            n_spots_stripes[stripe_idx] += 1
            vel_x_stripes[stripe_idx] += vx
            vel_y_stripes[stripe_idx] += vy
            vel_x_normalized_stripes[stripe_idx] += vx / math.sqrt(vx**2+vy**2)
            vel_y_normalized_stripes[stripe_idx] += vy / math.sqrt(vx**2+vy**2)
            average_module_x_vel[stripe_idx] += abs(vx)
            average_module_y_vel[stripe_idx] += abs(vy)
            average_speed_stripes[stripe_idx] += math.sqrt(vx**2+vy**2)
            average_speed_squares_stripes[stripe_idx] += vx**2+vy**2

        for k in range(0, len(n_spots_stripes)):
            n_spots = n_spots_stripes[k]
            if n_spots != 0:
                average_module_x_vel[k] = average_module_x_vel[k] / n_spots
                average_module_y_vel[k] = average_module_y_vel[k] / n_spots
                average_speed_stripes[k] = average_speed_stripes[k] / n_spots
                module_average_velocity_stripes[k] = math.sqrt(vel_x_normalized_stripes[k]**2 + vel_y_normalized_stripes[k]**2) / n_spots
                average_speed_squares_stripes[k] = average_speed_squares_stripes[k] / n_spots
                stdev_stripes[k] = math.sqrt(average_speed_squares_stripes[k]-(average_speed_stripes[k])**2)

        average_module_x_vel_in_time.append(average_module_x_vel)
        average_module_y_vel_in_time.append(average_module_y_vel)
        average_speed_stripes_in_time.append(average_speed_stripes)
        module_average_velocity_stripes_in_time.append(module_average_velocity_stripes)

        # Create the figure and axis objects
        fig, ax1 = plt.subplots()

        # Plot the first four series on the left axis
        ax1.plot(average_speed_stripes, 'r-', label='Average speed')
        ax1.plot(average_module_x_vel, 'g-', label='Average module of x velocity')
        ax1.plot(average_module_y_vel, 'b-', label='Average module of y velocity')
        #ax1.plot(module_average_velocity_stripes, 'm-', label='Module of average normalized velocity')
        ax1.set_ylim(0, 45)
        ax1.set_xlabel('Index')
        ax1.set_ylabel(r'Speed ($\mu$m/h)')
        ax1.legend(loc='upper left')

        # Create a second y-axis
        ax2 = ax1.twinx()

        # Plot the fourth series on the right axis
        #ax2.plot(n_spots_stripes, 'y-', label='Number of spots')
        ax2.plot(module_average_velocity_stripes, 'm-', label='Module of average normalized velocity') #####
        ax2.set_ylim(0, 1)
        ax2.set_ylabel('Module of average normalized velocity')

        # Show the legend for the right axis
        ax2.legend(loc='upper right')

        plt.title('frame '+str(t))

        # Save the figure as a PNG image
        plt.savefig(os.path.join(results_plots_dir,"plot_"+str(t)))
        plt.close()

        # ======== Plotting speed standard deviation ========
        # Create the figure and axis objects
        fig, ax = plt.subplots()

        # Plot the first four series on the left axis
        ax.plot(stdev_stripes, label='Standard deviation of speed')
        #ax1.plot(module_average_velocity_stripes, 'm-', label='Module of average normalized velocity')
        ax.set_ylim(0, 20)
        ax.set_xlabel('Index')
        ax.set_ylabel(r'Standard deviation ($\mu$m/h)')
        ax.legend(loc='upper left')

        plt.title('frame '+str(t))

        # Save the figure as a PNG image
        plt.savefig(os.path.join(stdev_plots_dir,"plot_"+str(t)))
        plt.close()

        # ======== Fit exponential to speed ========
        
        fig, ax = plt.subplots()

        y = average_speed_stripes
        x = []
        for index, value in enumerate(y):
            x.append(float(index))
        x = np.array(x)

        # Fit the exponential function to the data
        params = []
        b_list = []
        for i in range(5):
            popt = fit_exponential(y, i)
            params.append(popt)

            # Extract the optimized parameters
            a_fit, b_fit, c_fit = popt
            b_list.append(b_fit)

            # Create points for the fitted curve
            x_fit = np.linspace(0, max(x), 100)
            y_fit = exponential_func(x_fit, a_fit, b_fit, c_fit)

            # Plot the data and the fit
            ax.scatter(x, y, c='red')
            ax.plot(x_fit, y_fit, label=f'expfit: a={a_fit:.2f}, b={b_fit:.2f}, c={c_fit:.2f}')

        ax.set_ylim(0, 45)
        ax.set_xlabel('Index')
        ax.set_ylabel(r'Speed ($\mu$m/h)')
        ax.legend()

        plt.title('frame '+str(t))
        plt.savefig(os.path.join(expfit_plots_dir,"expfit_"+str(t)))
        plt.close()
        

        # ======== Save parameters for lambda vs. frame plot ========
        b_matrix.append(b_list)
        frame_list.append(t) 
    
    b_matrix = np.array(b_matrix)
    b_matrix = np.transpose(b_matrix)
    fig, ax = plt.subplots()

    for i in range(5):
    	b_list = b_matrix[i,:]
    	lambda_list = [1/x for x in b_list]
    	ax.scatter(frame_list, lambda_list, label='lambda=1/b starting from '+str(i))

    ax.set_ylim(0, 20)
    ax.set_xlabel('Frame')
    ax.set_ylabel('Parameter lambda=1/b')
    ax.legend(loc='upper left')

    plt.title('Exponential parameter for a*e^(-bR)')

    plt.savefig(os.path.join(expfit_plots_dir,"parameters"))
    plt.close()
    

    # ======== Plotting observables by stripe ========
    
    average_module_x_vel_in_time = np.array(average_module_x_vel_in_time)
    average_module_y_vel_in_time = np.array(average_module_y_vel_in_time)
    average_speed_stripes_in_time = np.array(average_speed_stripes_in_time)
    module_average_velocity_stripes_in_time = np.array(module_average_velocity_stripes_in_time)

    for stripe_idx in range(0, stripe_amount):
        x = frame_list
        y1 = average_module_x_vel_in_time[:, stripe_idx]
        y2 = average_module_y_vel_in_time[:, stripe_idx]
        y3 = average_speed_stripes_in_time[:, stripe_idx]
        y4 = module_average_velocity_stripes_in_time[:, stripe_idx]

        fig, ax1 = plt.subplots()

        ax1.scatter(frame_list, y1, c='green', label='Average module of x velocity')
        ax1.scatter(frame_list, y2, c='blue', label='Average module of y velocity')
        ax1.scatter(frame_list, y3, c='red', label='Average speed')
          
        ax1.set_ylim(0, 45)
        ax1.set_xlabel('Frame')
        ax1.set_ylabel(r'Speed ($\mu$m/h)')
        ax1.legend(loc='upper left')

        ax2 = ax1.twinx()
        ax2.scatter(frame_list, y4, c='magenta', label='Module of average normalized velocity')
        ax2.set_ylim(0, 1)
        ax2.set_ylabel('Module of average normalized velocity')
        ax2.legend(loc='upper right')

        plt.title('stripe index ' + str(stripe_idx))

        plt.savefig(os.path.join(stripesobs_plots_dir,"stripesobs_"+str(stripe_idx)))
        plt.close()
    


for option in [4, 6, 8, 10, 12]:
    print('Plotting for delta_frames=' + str(option))
    get_velocity_stripes(delta_frames=option, stripe_amount = 40)
    print('Plotting successful')

