// smooth_edge.ijm
// B.Alvial 24/Apr/2023
// This macro smoothes out the noise from the edge.

//radius_input = getNumber("Radio:", 20);
//radius_string = "" + radius_input;

radius_string = "20";

run("Maximum...", "radius="+radius_string);
setOption("BlackBackground", true);
run("Skeletonize");
