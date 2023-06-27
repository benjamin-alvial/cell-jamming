# Given the dataframe extracted from FIJI,
# calculates velocities with a given frame interval,
# and saves it in a dedicated folder for that given time interval.

import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd

results_masks_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/results/csvs_final_mask/"
csv_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/data_extracted/"
csv_name = "half185.csv"

time_resolution = 3/60 # 3 minutes between frames, to hours
space_resolution = 1.5 # 1,5 microns per pixel

# Define delta_frames to calculate velocity between frames. 
# Example: if original is f1 f2 f3 f4 f5 f6 f7 f8 and delta_frames = 3,
# velocity will be calculated between f1 f4 f7
# resulting in a total of 2 velocities located in frames f1 and f4
def get_velocity_data(delta_frames):
    
    results_data_delta_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/data_extracted/velocity_delta/"
    new_csv_name = "velocities_delta_"+str(delta_frames)+".csv"

    df_original = pd.read_csv(os.path.join(csv_dir, csv_name), skiprows=[1, 2, 3])
    df = df_original.copy()
    df = df.sort_values(by=['TRACK_ID', 'FRAME'], ascending=True)
    df = df.reset_index(drop=True)
    df_general = pd.DataFrame(columns=['FRAME','POS_X','POS_Y','VEL_X','VEL_Y','DIFF_T','TRACK_ID'])

    # Iterate over the tracks and generate their dataframe.
    for i in range(0, len(df.TRACK_ID.unique())):
        df_filtered = df[df['TRACK_ID'] == i]
        df_filtered = df_filtered.reset_index(drop=True)
        
        if len(df_filtered) <= delta_frames:
            continue # Do not calculate because it is impossible.

        else:

            # Iterate over the frames (except the last, velocities are undefined here) in the track.
            for j in range(0, len(df_filtered)-delta_frames, delta_frames): # Velocity will be calculated for every frame possible.

                frame = df_filtered['FRAME'][j]
                
                if frame != j:
                    continue

                pos_x = df_filtered['POSITION_X'][j]
                pos_y = df_filtered['POSITION_Y'][j]
                vel_x = (space_resolution/time_resolution) * (1/delta_frames) * (df_filtered['POSITION_X'][j + delta_frames] - df_filtered['POSITION_X'][j])
                vel_y = - (space_resolution/time_resolution) * (1/delta_frames) * (df_filtered['POSITION_Y'][j + delta_frames] - df_filtered['POSITION_Y'][j]) # Fiji inverts y-axis
                diff_t = df_filtered['FRAME'][j + delta_frames] - df_filtered['FRAME'][j]
                track_id = df_filtered['TRACK_ID'][j]

                # Define a tuple to be added to the DataFrame
                new_tuple = (frame, pos_x, pos_y, vel_x, vel_y, diff_t, track_id)
                # Add the tuple to the DataFrame
                df_general.loc[len(df_general)] = new_tuple

    df_general.to_csv(os.path.join(results_data_delta_dir, new_csv_name), index=False)

    print("Dataframe created and saved in "+os.path.join(results_data_delta_dir, new_csv_name))
    print(df_general)

for option in [12, 10, 8, 6, 4]:
    get_velocity_data(delta_frames=option)