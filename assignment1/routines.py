import numpy as n
from astropy.stats import sigma_clip
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

#constants
kb = 1.38064852e-23 #[m^2 kg s^-2 K^-1]
c = 2.998e8         #[m/s]
h = 6.62607004e-34  #[m^2 kg /s]
microns2m = 1e-6
