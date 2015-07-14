Motivation :
Density functional theory (DFT) based calculations often requires one (e.g. a dilligent grad student / postdoc) to 
perform convergence calculations on a supercell, prior to examining a research problem . Such calculations typically 
involve identifying several parameters  like the cut-off energy (to incorporate all the necessary plane wave basis sets), 
k-spacing (required for integration over the Brilloiun zone), smearing width, etc. These calculations, while important, 
are extremely tedious, and expensive softwares can happily do them for you.

As a practitioner of  DFT calculations, and a recent python-convert / aficionado / beginner, I took it as an
opportunity to teach myself python while developing a code to solve a pertinent problem (atleast to me).  

Purpose:
This python module attempts to automate the process by using already available robust and extensive, open-source python libraries e.g numpy, matplotlib etc. 
The module provides the user with several tools (in form of classes and methods) to facilitate convergence calculations and analyzes the data.

Code operation:
1. Automatically creates a directory structure for convergence calculations, containing all the required files
   Basic files REQUIRED to create the strucutre : POSCAR, POTCAR, KPOINTS, INCAR, VASP.qsub (or any other job submission script), 1-runvasploop.sh and 2-extractData.sh
    
2. Use the seprately provided shell script,1-runvasploop.sh, to run the calculations by submitting jobs to your favourite cluster uisng VASP.qsub

3. After the calculations are over,a second shell script, 2-extractData.sh (provided separately), will extract the calculated data, and

4. The plotting utility , using Matplotlib,  will plot energies vs. the relavent parameter. This plot can be further used to identify convergence parameters

Limitations of the Code:
The code is written using python 2.7, and has been tested on OSX (Yosemite) only.
The current version only supports VASP (Vienna Ab Inito Simulation Package), however I have tried to keep the classes and methods 
sufficiently general so that they can be extended to other types of packages (if a dilligent grad student / postdoc wiches to). Presently, the module will assist in the evaluation of  
ONLY cut-off energy and k-spacing. Since this is a priliminary version, I cannot guarantee that this code could be used as a drop-in substitute and 
the user probably have to "tweak" it to suite their needs.

IMPORTANT :  VASP is not included :)
