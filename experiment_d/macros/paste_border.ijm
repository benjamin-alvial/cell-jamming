// paste_border.ijm
// B.Alvial 24/Apr/2023
// This pastes the given frame of the result into the desired image.

frame_input = getNumber("Frame:", 1);
frame_string = "" + frame_input;

results_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/results/";
open(results_dir+"/final_border.tif");
selectWindow("final_border.tif");
run("Make Substack...", "slices="+frame_string);

origin_image = "Substack ("+frame_string+")";
target_image = "Substack (1-185).tif";
image_width = 1512;

selectWindow(origin_image);
run("Create Selection");
run("Select Bounding Box");
getSelectionBounds(x, y, width, height);

x_translate = x - (image_width/2 - width/2);
x_translate_string = "" + x_translate;

run("Create Selection");
run("Copy");

selectWindow(target_image);
run("Paste");
run("Translate... ", "x="+x_translate_string+" y=0");
