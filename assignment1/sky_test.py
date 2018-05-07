import numpy as n
import matplotlib.pyplot as plt
from astropy.io import fits
import etc_routines
import etc_data

####Constants########

kb = 1.38064852e-23  #[m^2 kg s^-2 K^-1]
c = 2.998e8          #[m/s]
h = 6.62607004e-34   #[m^2 kg /s]
q_e = 1.60217662e-19 #[Coloubs] charge of electron
microns2m = 1e-6

####################
#detector characteristics
x_pix = 4112
y_pix = 4096
detector = n.zeros((y_pix, x_pix))

read_noise = 3             #[e-]
dark_current = 3 / 60 / 60 #[e-/pix/s]
saturation = 200000        #[e-/pixel]
aperture = 2.5/2           #[meters] radius goddamit
pix_size = 15.             #[microns]
image_scale = 1e3 / 16.5   #[microns/arcsecond]
sensitivty = 7e-6          #[V/e-]
pix_scale = pix_size / image_scale  #[arcsec/pix]
seeing = .7               #[arcsecond]

#detector qe
detector_qe = etc_data.e2v_detector_qe()


#observation parameters
exp_time = 600 #[seconds]

#filter
g_sdss_filter = etc_data.g_sdss_filter()
filter_t, filter_lam = g_sdss_filter

#upload the sky and convert the flux to the units of the target
sky_flux, sky_lam = etc_data.opt_sky_emission() #phot/s/nm/arcsec^2/m^2, #angstroms
#sky_flux *= (pix_scale)**2                      #phot/s/nm/m^2 
sky_flux *= (1./100)**2 #*(m/cm)**2             #phot/s/nm/cm^2
sky_flux *= (1./1e-9)     #*(nm/m)              #phot/s/m/cm^2
sky_flux *= (h*c / (sky_lam * 1e-10))           #joules/s/m/cm^2
sky_flux *= 1e7                                 #erg/s/m/cm^2

sky_flux *= ((sky_lam * 1e-10)**2)/c            #erg/s/cm^2/Hz   #arcsec^2

sky_g_flux = etc_routines.get_flux_in_filter(sky_flux, sky_lam, g_sdss_filter, detector_qe )
sky_mag = -2.5 * n.log10(sky_g_flux) - 48.6
print('sky mag / arcsec^2: ', sky_mag)
#sky_mag = -2.5 * n.log10(sky_g_flux/g0_flux)
