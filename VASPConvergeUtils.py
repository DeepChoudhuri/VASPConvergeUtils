# -*- coding: utf-8 -*-
"""
Module name : VASPConvergeUtils.py

Motivation :
Density functional theory (DFT) based calculations often requires one (e.g. a dilligent grad student / postdoc) to 
perform convergence calculations on a supercell, prior to examining a research problem . Such calculations typically 
involve identifying several parameters  like the cut-off energy (to incorporate all the necessary plane wave basis sets), 
k-spacing (required for integration over the Brilloiun zone), smearing width, etc. These calculations, while important, 
are extremely tedious, and expensive softwares can happily do them for you.

Purpose:
This python module attempts to automate the aforementioned rocess by using already available robust and extensive, open-source python libraries e.g numpy, matplotlib etc. 
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
sufficiently general so that they can be extended to other types of packages (if a dilligent grad student / postdoc wishes to). Presently, the module will assist in the evaluation of ONLY cut-off energy and k-spacing. Since this is a priliminary version, I cannot guarantee that this code could be used as a drop-in substitute and 
the user probably have to "tweak" it to suite their needs.

IMPORTANT :  VASP is not included :)

Author: Deep Choudhuri, PhD
Date: 7th July 2015
"""
import os
import shutil
import math
import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt

# 1. Class for loading and extracting data from files
class FileLoader(object):
    """
    Class for loading and extracting data from files like POSCAR, KPOINTS and any file containing the converged data sets
    INPUT = name of the file
    OUTPUTS = file content and/or  plot of the converged data
    """
    
    def __init__(self, fileName):
        self.fileName = fileName
        
    def setFileName(self,fname):
        """
        change the file name if it has changed during the process
        """
        self.fileName = fname # End Method
        
    def getFileName(self):
        """
        Self descriptive
        """
        return self.fileName # End Method
    
    def getFileListData(self):
        """
        Get the data inside the file as a LIST
        """
        fp = open(self.fileName)
        lineData = [line.strip() for line in fp]
        fp.close()
        return lineData # End Method
        
    def getProcessedData(self):
        """
        Get data inside the file as a text which can be latter imported in excel, or any other plotting program like this one
        """
        data = np.loadtxt(self.fileName)
        return data # End Method
        
    def plotConvData(self,lowYLim = -0.01, highYLim = 0.01):
        """
        Plots the data present in a file.
        Allows you to set the upper and lower limits in the vertical Y axis
        """
        data = FileLoader(self.fileName).getProcessedData()
        print data
        x = data[:,0]
        y = data[:,1]
        ydiff = ndarray(len(y),float)
        for i in range(len(y)): # Calcuating Energy differnece
            if i == 0:
                ydiff[0] = y[0] - y[0]
            elif i > 0:
                ydiff[i] = y[i] - y[i-1]
        
        plt.close('all')       
        f, axarr = plt.subplots(2, sharex = True)
        axarr[0].plot(x,y,'-ro')
        axarr[0].set_ylabel('Energy of the cell, eV')
        axarr[1].plot(x,ydiff,'ro')
        axarr[1].set_ylabel('Energy differenece, eV')
        axarr[1].set_ylim(lowYLim,highYLim)
        plt.xlabel('Cut off energy, eV')
        plt.show()    # End Method 
        


# 2. Class for setting up a directory tree
class SetupDirectoryStructure(object):
    """
    Create a directory structure, where the folder names and their quantity (number of folders) is based on the upper and lower limit of the values provided and the scannign step
    """
    
    def __init__(self, lowLimit, highLimit, step):
        self.lowLimit = lowLimit    
        self.highLimit = highLimit
        self.step = step   
        
    def createDirs(self, filePath):
       dirNum = np.linspace(self.lowLimit, self.highLimit, self.step)
       for i in dirNum:
           os.mkdir(filePath + '%0.2f'%i) # End Method
           
 
# 3. Class for manipulating lattice vectors
class VectorMath(object):
    """
    Does priliminary vector maths
    INPUT : Two vectors
    OUTPUT : Dot or Cross products of the two vectors
    """
    
    def __init__(self, latticeVec1, latticeVec2): # 1D vector
        self.A = latticeVec1
        self.B = latticeVec2
    
    def getDotProduct(self,):
        """
        Self descriptive, if the seems unfamiliar please refer to any calculus book with vector algebra
        """
        A1 = self.A
        A2 = self.B        
        dotProd = A1[0]*A2[0] + A1[1]*A2[1] + A1[2]*A2[2]
        return dotProd # End Method
    
    def getCrossProduct(self):
        """
        Self descriptive
        """
        A1 = self.A
        A2 = self.B        
        c1 = A1[1]*A2[2] - A2[1]*A1[2]
        c2 = A1[0]*A2[2] - A2[0]*A1[2]
        c3 = A1[0]*A2[1] - A2[0]*A1[1]        
        crossProd = ([c1, -c2, c3])
        return crossProd # End Method
    
       
# 4. Class for creating a directory structure to perform cut-off energy converngence calculations    
class EcutConvSetup(object):
    """
    This class create the directory/folder structure required for cut-off energy calculations
    INPUT : Lower and upper limits of the cut-off energies to be scanned and the scanning step
    OUTPUT : folder name after the each step e.g. lowLimit = 100, upperlImit =120 and step= 2, the folders with names 100, 100 and 120 will be created
    """
    
    def __init__(self, ecutStart = 0, ecutStop = 10, estep = 5, parentFolder = 'Ecut_Convergence'):
        self.ecutStart = ecutStart
        self.ecutStop = ecutStop
        self.estep = estep
        self.parentFolder = parentFolder

        
    def locateSubstringPos(self,targetList, subString):
        """
        Locate a specific sub-strin inside a give string.
        """
        for i, s in enumerate(targetList):
            if subString in s:
              return i
        return -1  # End Method
               
    def setINCARValue(self, ecutVal):
        """
        Sets the energy value inside the INCAR file
        """
        tempList = FileLoader('INCAR').getFileListData()
        pos = self.locateSubstringPos(tempList,'ENCUT')
        tempList[pos] = 'ENCUT = '+ '%0.0f'%ecutVal
        return tempList # End Method
        
        
    def getINCARFiles(self, path):
       """
        Creates and copies INCAR files (with differing cut-off energy values ) to previously existing folders
       """
       eVals = np.linspace(self.ecutStart, self.ecutStop, self.estep)
       for i in eVals:
           tempINCAR = self.setINCARValue(i)
           fp = open('INCAR_temp','w')
           for item in tempINCAR:
               fp.write("%s\n"%item)
           fp.close();
           shutil.copy('INCAR_temp',path+'%0.2f'%i+'/INCAR') # End Method
                          
                    
    def setupEcutDirs(self):
        """
        Work horse method , that actually creates the directory structure and copies all the relevant files to that structure
        """
        os.mkdir(self.parentFolder)
        path = self.parentFolder+'/'
        SetupDirectoryStructure(self.ecutStart,self.ecutStop, self.estep).createDirs(path)
        self.getINCARFiles(path)        
        dirList = os.listdir(path)
        for i in dirList:  # Copy rest of the files
            shutil.copy('KPOINTS',path+i)
            shutil.copy('POSCAR',path+i)
            shutil.copy('POTCAR',path+i)
            shutil.copy('VASP.qsub',path+i)
        
        shutil.copy('1-runvasploop.sh',path)
        shutil.copy('2-extractData.sh',path)
        print "Completed INCAR directory structure creation ......" # End Method           
            
 

# 5. Class for creating a directory structure to perform KPOINT converngence calculations     
class KPOINTSSetup(object):
    """
    This class create the directory/folder structure required for k-spacing  calculations
    INPUT : Lower and upper limits of the k-spacings to be scanned and the scanning step
    OUTPUT : folder name after the each step e.g. lowLimit = 0.1, upperlImit = 0.2and step= 2, the folders with names 0.10, and 0.20 will be created
    """
    
    def __init__(self, kStart = 0.05, kStop = 0.40, kStep = 20, kParentFolder = 'KPoint_Convergence'):
        print " Usage , 0 = Gamma , 1 = Monkhorst-Pack"
        self.kStart = kStart
        self.kStop = kStop
        self.kStep = kStep
        self.kParentFolder = kParentFolder
    
    def getLatticeVectors(self):
        """
        Extracts lattice vectors of the supercell formt he POSCAR file
        """
        tempPOSCAR = FileLoader('POSCAR').getFileListData()
        vecS1 = tempPOSCAR[2].split()
        vecS2 = tempPOSCAR[3].split()
        vecS3 = tempPOSCAR[4].split()
        latticeVectorMatrix = np.ndarray(shape = (3,3), dtype = float)        
        for i in range(3):
            latticeVectorMatrix[0,i] = float(vecS1[i])
            latticeVectorMatrix[1,i] = float(vecS2[i])
            latticeVectorMatrix[2,i] = float(vecS3[i])            
        return latticeVectorMatrix # End Method
                            
    def getKMesh(self, kSpacing = 0.10, gamma = 1):
        """
        Generates K mesh depending on the k-spacing value and the selection of gamma centered or Monkhorst-Pack Brillouin zone integration scheme
        """
        basis = self.getLatticeVectors()
        A1 = basis[0,:]
        A2 = basis[1,:]
        A3 = basis[2,:]    
        
        b1cross = VectorMath(A2,A3).getCrossProduct()  
        b1denom = VectorMath(A1,b1cross).getDotProduct()          
        b1 = np.multiply(2.0*math.pi/b1denom,b1cross)
        
        b2cross = VectorMath(A3,A1).getCrossProduct()  
        b2denom = VectorMath(A2,b2cross).getDotProduct()          
        b2 = np.multiply(2.0*math.pi/b2denom,b2cross)
        
        b3cross = VectorMath(A1,A2).getCrossProduct()  
        b3denom = VectorMath(A3,b3cross).getDotProduct()          
        b3 = np.multiply(2.0*math.pi/b3denom,b3cross)
        
        b1mag2 = VectorMath(b1,b1).getDotProduct()
        b2mag2 = VectorMath(b2,b2).getDotProduct()
        b3mag2 = VectorMath(b3,b3).getDotProduct()
        
        if gamma == 0:
            print "Gamma Centered meshing"
            M1 = ((math.sqrt(b1mag2)) / kSpacing) + 0.5
            M2 = ((math.sqrt(b2mag2)) / kSpacing) + 0.5
            M3 = ((math.sqrt(b3mag2)) / kSpacing) + 0.5
        elif gamma == 1:
            print "Monkhorst-Pack meshing"
            M1 = ((math.sqrt(b1mag2)) / kSpacing)
            M2 = ((math.sqrt(b2mag2)) / kSpacing)
            M3 = ((math.sqrt(b3mag2)) / kSpacing)
            
        if (M1 - int(M1)) >= 0.5:
             M1new = int(round(M1))
        elif (M1 - int(M1)) < 0.5:
             M1new = int(M1)
        if (M2 - int(M2)) >= 0.5:
             M2new = int(round(M2))
        elif (M2 - int(M2)) < 0.5:
             M2new = int(M2)
        if (M3 - int(M3)) >= 0.5:
             M3new = int(round(M3))
        elif (M3 - int(M3)) < 0.5:
             M3new = int(M3)
        
        M = ([M1new,M2new,M3new])
        #print M
        #M = ([M1,M2,M3])
        #M = ([int(round(M1)),int(round(M2)),int(round(M3))])
        
        return M # End method
    
    
    def setupKmeshDirs(self, gamma = 1):
        """
        Work horse method , that actually creates the directory structure and copies all the relevant files to that structure
        """
        os.mkdir(self.kParentFolder)
        path = self.kParentFolder+'/'
        SetupDirectoryStructure(self.kStart,self.kStop,self.kStep).createDirs(path)
        tempList = FileLoader('KPOINTS').getFileListData()
        for i in np.linspace(self.kStart,self.kStop,self.kStep):
            tempKmesh = self.getKMesh(i,gamma)
            meshString = str(tempKmesh[0])+ '  ' + str(tempKmesh[1])+ '  ' + str(tempKmesh[2])
            print meshString
            tempList[3] = meshString            
            fp = open('KPOINTS_temp','w')            
            for item in tempList:
               fp.write("%s\n"%item)
            fp.close();
            shutil.copy('KPOINTS_temp',path+'%0.2f'%i+'/KPOINTS')
            shutil.copy('INCAR',path+'%0.2f'%i)
            shutil.copy('POSCAR',path+'%0.2f'%i)
            shutil.copy('POTCAR',path+'%0.2f'%i)
            shutil.copy('VASP.qsub',path+'%0.2f'%i)
        
        shutil.copy('1-runvasploop.sh',path)
        shutil.copy('2-extractData.sh',path)
        print "Completed KPOINT directory structure creation ......"
