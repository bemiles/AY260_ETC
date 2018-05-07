## Assignment 1

### 1) For a 10-minute exposure, how many total photons are collected in the g-band from a G2V star of g-magnitude 12, 18 and 26?

using the SDSS settings

magnitude, photons

12,       19508.566026175427 

18,       77.66500149355913 

26,      0.04900330220159084

### 2) In all three cases, for that same 10-minute exposure what is the number of counts in pixel that is completly inside the disk "psf"?  Is this pixel saturated?

magnitude, total photons within the seeing disk

12,      19597.400977422603

18,      166.4999527407345

26,      88.88395454937698

The seeing disk takes up about 9 pixels. In all cases the seeing disk is not saturated. 

### 3) How many counts from the sky are collected in that 10-minute exposure in the same aperture in the g-band?

sky counts per pixel in the SDSS image scale: 0.37055013857504265

### 4)  What is the signal to noise for all three observations from parts 1-3?  You should include readnoise and dark current as well as the sky.

magnitude, SNR using the signal to noise equation

12,      139.3561400278323

18,      6.018916211977239

26,      0.005197729361501597

magnitude, SNR attempting aperture photometry (photutils)

12,      9142.516298328814

18,      22.184186795311795

26,      0.8109178011992169

### 5) Suppose instead you system had the same focal plane scale as Keck: 0.727 mm/arcecond.  What is the signal to noise for each obesrvation in a 10 minute exposure? 

using Keck image scale

magnitude, SNR using the signal to noise equation

12,      531.7065783388886

18,      39.04273634763486

26,      0.00434990687932382

magnitude, SNR attempting aperture photometry (photutils)

12,      2152.459180839915

18,      58.46842454252552

26,      0.8984092875554677


### 6) Still with the same Keck focal plane scale, how long would you have to integrate to be sky-noise limited at 26th magnitude? 

