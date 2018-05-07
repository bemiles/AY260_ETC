import numpy as n
import matplotlib.pyplot as plt
from astropy.io import fits
import etc_routines
import etc_data
from photutils import aperture_photometry, CircularAperture

####Constants########

kb = 1.38064852e-23  #[m^2 kg s^-2 K^-1]
c = 2.998e8          #[m/s]
h = 6.62607004e-34   #[m^2 kg /s]
q_e = 1.60217662e-19 #[Coloubs] charge of electron
microns2m = 1e-6

#Telescope Optics + Seeing 
################################
image_scale = 1e3 / 16.5   #[microns/arcsecond]  #SDSS
aperture = 2.5/2           #[meters]

# image_scale =  0.727  * 1e3  #[microns/arcsecond]  #Keck
# aperture = 10./2             #[meters] 

seeing = .7               #[arcsecond]

####################
#detector characteristics
x_pix = 4112
y_pix = 4096
detector = n.zeros((y_pix, x_pix)) # detector
read_noise = 3             #[e-]
dark_current = 3 / 60 / 60 #[e-/pix/s]
saturation = 200000        #[e-/pixel]
pix_size = 15.             #[microns]
pix_scale = pix_size / image_scale  #[arcsec/pix]

#detector quantum efficiency
detector_qe = etc_data.e2v_detector_qe()

####################

#observation parameters
exp_time = 600 #10 ** n.arange(.25,10,.1) #600 #[seconds]
print('exposure time (seconds) :', exp_time)
print('-------------------------------')


#filter
g_sdss_filter = etc_data.g_sdss_filter()
filter_t, filter_lam = g_sdss_filter

####################
#target parameters
rescale_target_mag = 26

data = fits.getdata('calspec_standards/hd205905_stis_004.fits')
target_flux = data['FLUX']   #[erg s^-1 cm-^2 Ang^-1]
target_lam = data['WAVELENGTH']# Angstroms

target_flux *= (1./1e-10)          #[erg s^-1 cm-^2 m^-1]
target_flux *= ((target_lam * 1e-10) **2)/c  #[erg s^-1 cm-^2 Hz^-1]

target_g_flux = etc_routines.get_flux_in_filter(target_flux, target_lam, g_sdss_filter, detector_qe )
target_mag = -2.5 * n.log10(target_g_flux) - 48.6
print('target mag: ', target_mag)


if rescale_target_mag != False:
    
    expo = ((rescale_target_mag + 48.6)/-2.5)

    scale_factor = (10**(expo))/target_g_flux
    
    target_flux *= scale_factor

    target_g_flux = etc_routines.get_flux_in_filter(target_flux, target_lam, g_sdss_filter, detector_qe )
    target_mag = -2.5 * n.log10(target_g_flux) - 48.6
    print('target mag rescaled: ', target_mag)


#upload the sky and convert the flux to the units of the target
sky_flux, sky_lam = etc_data.opt_sky_emission() #phot/s/nm/arcsec^2/m^2, #angstroms
#sky_flux *= (pix_scale)**2                      #phot/s/nm/m^2 
sky_flux *= (1./100)**2 #*(m/cm)**2             #phot/s/nm/cm^2
sky_flux *= (1./1e-9)     #*(nm/m)              #phot/s/m/cm^2
sky_flux *= (h*c / (sky_lam * 1e-10))           #joules/s/m/cm^2
sky_flux *= 1e7                                 #erg/s/m/cm^2

sky_flux *= ((sky_lam * 1e-10)**2)/c            #erg/s/cm^2/Hz/arcsec^2

sky_g_flux = etc_routines.get_flux_in_filter(sky_flux, sky_lam, g_sdss_filter, detector_qe )
sky_mag = -2.5 * n.log10(sky_g_flux) - 48.6
print('sky mag / arcsec^2: ', sky_mag)
print('-------------------------------')


############################################################################################################
#make calculations of SNR

#pass the spectra through the filters
target_flux_out, target_lam_out = etc_routines.pass_through_transmission(target_flux, target_lam, g_sdss_filter)  #[erg s^-1 cm-^2 Hz^-1]
sky_flux_out, sky_lam_out = etc_routines.pass_through_transmission(sky_flux, sky_lam, g_sdss_filter) #erg/s/cm^2/Hz/arcsec^2

#pass the spectra through the detector qe
target_flux_out, target_lam_out = etc_routines.pass_through_transmission(target_flux_out, target_lam_out, detector_qe) #[erg s^-1 cm-^2 Hz^-1]
sky_flux_out, sky_lam_out = etc_routines.pass_through_transmission(sky_flux_out, sky_lam_out, detector_qe)  #erg/s/cm^2/Hz/arcsec^2

#get total number of photons

#account for aperture
target_flux_out *= n.pi * (aperture**2) #[erg s^-1 Hz^-1]

sky_flux_out *= n.pi * (aperture**2)    #[erg s^-1 Hz^-1 arcsec^-2]
sky_flux_out *= pix_scale**2            #[erg s^-1 Hz^-1] sky per pixel

#convert to photons/s
target_flux_out /= (1e7 * h * c/ ( target_lam_out * 1e-10 ))    #[phtons s^-1 Hz^-1] 
sky_flux_out /= (1e7 * h * c/ ( sky_lam_out * 1e-10 ))          #[phtons s^-1 Hz^-1] sky per pixel


# plt.figure('target photons')
# plt.plot(sky_lam_out, sky_flux_out, label = 'Sky')
# plt.plot(target_lam_out, target_flux_out, label = 'Target')
# plt.xlabel('Wavelength (Angstroms)')
# plt.ylabel('photons/s/Hz')
# #plt.xscale('log')
# plt.yscale('log')
# plt.legend()
# plt.show()


y = target_flux_out
x = c/(target_lam_out * 1e-10)
order = n.argsort(x)
y = y[order]
x = x[order]

target_photons = n.trapz( y,x ) * exp_time  #[phtons]

print('target photons:', target_photons)


y = sky_flux_out
x = c/(sky_lam_out * 1e-10)
order = n.argsort(x)
y = y[order]
x = x[order]

sky_photons = n.trapz( y,x ) * exp_time  #[phtons]

print('sky photons:', sky_photons)


###################################
#SNR estimation

#size of the star on detector
seeing_disk_size = int(seeing/pix_scale)
x0, y0 = 2500, 2000  #star position
ydim = n.arange(y_pix)
xdim = n.arange(x_pix)
xgrid, ygrid = n.meshgrid(xdim,ydim)
disk_inds = etc_routines.seeing_disk(x0,y0,xgrid, ygrid, seeing_disk_size)
npix_total = len(disk_inds[0])

dark_current_total = dark_current * exp_time * npix_total
read_noise_total = read_noise**2 * npix_total
sky_noise_total = sky_photons * npix_total

total_counts = target_photons + sky_noise_total + dark_current_total + read_noise_total
print('total photons (target + noise):', total_counts)
#calculting it using the SNR equation
SNR = target_photons / n.sqrt(total_counts )
print('SNR :', SNR)

SNR_background_limit = target_photons / n.sqrt(sky_noise_total)

# plt.figure('SNR')
# plt.plot(exp_time, SNR, label = 'SNR real')
# plt.plot(exp_time, SNR_background_limit, label = 'SNR background only')
# plt.legend(loc = 'best')
# plt.ylabel('SNR')
# plt.xlabel('exposure time (seconds)')
# plt.yscale('log')
# plt.xscale('log')
# plt.show()


############################################################################################################
#making a detector image
detector[disk_inds] = target_photons/npix_total #n.random.poisson( lam = target_photons/npix_total, size = n.shape(detector[disk_inds]))

sky = n.random.poisson( lam = sky_photons, size = n.shape(detector))
detector += sky
detector += dark_current * exp_time
detector += read_noise**2


detector_subset = detector[1950:2050,  2450: 2550]

# plt.figure('snr test')
# plt.plot(exp_time, SNR)
# plt.xscale('log')
# plt.yscale('log')
# plt.show()

plt.figure('detector')
plt.subplot(121)
plt.title('detector all')
plt.imshow(detector, origin = 'lower')

plt.subplot(122)
plt.title('detector subset')
plt.imshow(detector_subset, origin = 'lower')
plt.show()


background = n.median(detector)
im_skysub = detector - background

positions = (n.array([x0,y0]), n.array([100,100]))
apertures = CircularAperture(positions, r=seeing_disk_size)
phot_table = aperture_photometry(im_skysub, apertures)

target_apt = phot_table['aperture_sum'][0]
noise_apt = phot_table['aperture_sum'][1]

SNR_est = target_apt/noise_apt
print('SNR aperture photometry :', SNR_est)

