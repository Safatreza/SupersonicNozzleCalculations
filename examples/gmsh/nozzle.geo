// Nozzle geometry definition for Gmsh
// Parameters
throat_radius = 0.005;  // 5mm
exit_radius = 0.01;     // 10mm
length = 0.1;           // 100mm
mesh_size = 0.001;      // 1mm

// Points
Point(1) = {0, 0, 0, mesh_size};                    // Inlet center
Point(2) = {0, throat_radius, 0, mesh_size};        // Inlet wall
Point(3) = {length/2, throat_radius, 0, mesh_size}; // Throat
Point(4) = {length, exit_radius, 0, mesh_size};     // Exit wall
Point(5) = {length, 0, 0, mesh_size};               // Exit center

// Lines
Line(1) = {1, 2};  // Inlet
Line(2) = {2, 3};  // Convergent section
Line(3) = {3, 4};  // Divergent section
Line(4) = {4, 5};  // Exit
Line(5) = {5, 1};  // Centerline

// Curves
Curve Loop(1) = {1, 2, 3, 4, 5};

// Surface
Plane Surface(1) = {1};

// Physical groups
Physical Curve("inlet") = {1};
Physical Curve("wall") = {2, 3};
Physical Curve("outlet") = {4};
Physical Curve("axis") = {5};
Physical Surface("fluid") = {1};

// Mesh refinement
Field[1] = Distance;
Field[1].EdgesList = {2, 3};
Field[2] = Threshold;
Field[2].InField = 1;
Field[2].SizeMin = mesh_size/10;
Field[2].SizeMax = mesh_size;
Field[2].DistMin = 0;
Field[2].DistMax = 0.01;
Background Field = 2; 