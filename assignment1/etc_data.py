import numpy as n
import matplotlib.pyplot as plt

#Telescope DATA

def g_sdss_filter():
    
    g_data = n.genfromtxt('sdss_data/filters/g.dat')
    g_lam = g_data[:,0] #Angstroms
    g_t = g_data[:,1] #1.3 airmasses point source

    return g_t, g_lam

def u_sdss_filter():
    
    u_data = n.genfromtxt('sdss_data/filters/u.dat')
    u_lam = u_data[:,0] #Angstroms
    u_t = u_data[:,1] #1.3 airmasses point source

    return u_t, u_lam

def r_sdss_filter():

    r_data = n.genfromtxt('sdss_data/filters/r.dat')
    r_lam = r_data[:,0] #Angstroms
    r_t = r_data[:,1] #1.3 airmasses point source

    return r_t, r_lam

def i_sdss_filter():

    i_data = n.genfromtxt('sdss_data/filters/i.dat')
    i_lam = i_data[:,0] #Angstroms
    i_t = i_data[:,1] #1.3 airmasses point source

    return i_t, i_lam

def z_sdss_filter():
    
    z_data = n.genfromtxt('sdss_data/filters/z.dat')
    z_lam = z_data[:,0] #Angstroms
    z_t = z_data[:,1] #1.3 airmasses point source

    return z_t, z_lam

def e2v_detector_qe():

    detector_data = n.genfromtxt('detector_data/e2vhirhomulti.txt')

    qe_lam = detector_data[:,0] * 10000 #[Angstroms]
    qe_t = detector_data[:,1] / 100     #[percentage]

    return qe_t, qe_lam 

# plt.figure('filter')
# plt.plot(g_lam, g_t, '-g')
# plt.plot(u_lam, u_t, '-m')
# plt.plot(r_lam, r_t, '-r')
# plt.plot(i_lam, i_t, '-b')
# plt.plot(z_lam, z_t, '-k')
# plt.show()



#SKY DATA
def opt_sky_emission():

    opt_sky_data = n.genfromtxt('sky_data/mauna_kea_skybg_50_10.dat', skip_header = 14)

    opt_sky_lam = opt_sky_data[:,0]*10. #angstroms
    opt_sky_flux = opt_sky_data[:,1] #phot/s/nm/arcsec^2/m^2

    return opt_sky_flux, opt_sky_lam

# plt.figure('h')
# plt.plot(opt_sky_lam, opt_flux_lam)
# plt.show()




    
    
