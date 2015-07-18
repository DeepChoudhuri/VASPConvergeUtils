Motivation :
------------
Density functional theory (DFT) based calculations often requires one (e.g. a dilligent grad student / postdoc) to 
perform convergence calculations on a supercell, prior to examining a research problem . Such calculations typically 
involve identifying several parameters  like the cut-off energy (to incorporate all the necessary plane wave basis sets), 
k-spacing (required for integration over the Brilloiun zone), smearing width, etc. These calculations, while important, 
are extremely tedious, and expensive softwares can happily do them for you.

As a practitioner of  DFT calculations, and a python-aficionado, I took it as an
opportunity to solve this pertinent problem (atleast to me).  

Limitations of the Code:
------------------------
The code is written using python 2.7 with SPYDER IDE, and is tested on OSX (Yosemite) ONLY. Potential users are reccomended
to test this module on their respective platforms. The current version is specifically written for VASP. Furthermore, I 
cannot guarantee that this code could be used "AS IS" and the user may be required "tweak" it to suite their needs.  
