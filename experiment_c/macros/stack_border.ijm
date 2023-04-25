// stack_border.ijm
// B.Alvial 24/Apr/2023
// This macro takes the full grayscale 64-bit stack
// and obtains a stack with the moving border.

macros_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_c/macros/";
results_dir = "/Users/benjaminalvial/Desktop/Nucleus/cell-jamming/experiment_c/results/";
original_stack_name = "100xFRET_CFP_Ratio.stk";
border_stack_name = "final_border.stk";
i_initial = 1;
i_final = 80;

for (i=i_initial; i<i_final+1; i++) {
	
  i_string = "" + i;
  
  selectWindow(original_stack_name);
  
  run("Make Substack...", "slices="+i_string);
  selectWindow("Substack ("+i_string+")");
  rename("Frame_" + i);
  
  setMinAndMax(0, 293);
  setAutoThreshold("Default dark no-reset");
  setThreshold(80, 65535, "raw");
  setOption("BlackBackground", true);
  run("Convert to Mask");
  
  runMacro(macros_dir + "get_edge.ijm");
  runMacro(macros_dir + "smooth_edge.ijm");
  rename("Edge_" + i);
  
  selectWindow("Frame_" + i);
  close();
  
}

selectWindow(original_stack_name);
close();

run("Concatenate...", "all_open title="+border_stack_name+" open");
saveAs("Tiff", results_dir+"final_border.tif");