// get_final_overlay.ijm
// B.Alvial 05/May/2023
// This macro takes the full grayscale 64-bit stack
// and obtains a gif with the moving border.

macros_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/macros/";
results_images_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/results/images_final_overlay/";
results_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/results/";
original_stack_name = "Substack (1-185).tif";

i_initial = 1;
i_final = 185;
range_string = "" + i_initial + "_" + i_final;

final_gif_name = "final_overlay_" + range_string + ".gif";

for (i=i_initial; i<i_final+1; i++) {
	
  selectWindow(original_stack_name);
  png_image_name = "final_overlay_" + range_string + "__" + i + ".png";
  
  // Three types of windows:
  frame_i = "Frame_" + i; // Frame_i has the original nuclei image.
  edge_i = "Edge_" + i; // Edge_i has the white-on-black border.
  frame_copy_i = "Frame_copy_" + i; // Frame_copy_i has a copy of the original nuclei image.
  
  // First copy of original image, border will be extracted from here.
  run("Make Substack...", "slices="+i);
  selectWindow("Substack ("+i+")");
  rename(frame_i);
  
  // Second copy of original image, border will be pasted here.
  run("Make Substack...", "slices=1");
  selectWindow("Substack (1)");
  rename(frame_copy_i);
  
  // Find the edge.
  selectWindow(frame_i);
  setMinAndMax(0, 293);
  setAutoThreshold("Default dark no-reset");
  setThreshold(80, 65535, "raw");
  setOption("BlackBackground", true);
  run("Convert to Mask");
  runMacro(macros_dir + "get_edge.ijm");
  runMacro(macros_dir + "smooth_edge.ijm");
  rename(edge_i);
  
  // Prune short branches and paste result as overlay.
  run("Geodesic Diameter", "label=" + edge_i + " distances=[Chessknight (5,7,11)] show image=" + frame_copy_i);
  selectWindow(frame_copy_i);
  run("Overlay Options...", "stroke=red width=10 fill=red set apply");
  run("Overlay Options...", "stroke=red width=5 fill=red set apply");
  
  selectWindow(frame_i);
  close();
  
  selectWindow(edge_i);
  close();
  
  selectWindow(frame_copy_i);
  saveAs("Png", results_images_dir + png_image_name);
  close();
  
}

selectWindow(original_stack_name);
close();

// Concatenate all the png images into one gif.
for (i=i_initial; i<i_final+1; i++) {
  png_image_name = "final_overlay_" + range_string + "__" + i + ".png";
  open(results_images_dir + png_image_name);
  selectWindow(png_image_name);
}

run("Concatenate...", "all_open title=" + final_gif_name + " open");
saveAs("Gif", results_dir + final_gif_name);
