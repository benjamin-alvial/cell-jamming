// get_edge.ijm
// B.Alvial 24/Apr/2023
// This macro generates the edge of tissue from a binary image.

macros_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_d/macros/";
fill_macro_dir = "Fill_Border_Holes.ijm"

run("Dilate");
runMacro(macros_dir+fill_macro_dir);
run("Dilate");
runMacro(macros_dir+fill_macro_dir);
run("Dilate");
runMacro(macros_dir+fill_macro_dir);
run("Dilate");
runMacro(macros_dir+fill_macro_dir);
run("Keep Largest Region");
run("Find Edges");
