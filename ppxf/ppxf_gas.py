# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 15:43:08 2024

@author: cammy
"""
from astropy.io import fits
from os import path
import matplotlib.pyplot as plt
import numpy as np
import h5py


from os import path



   
from plotbin import display_pixels
from plotbin.display_pixels import display_pixels
from plotbin.display_bins import display_bins


from ppxf.ppxf import ppxf
import ppxf.ppxf_util as util
import ppxf.sps_util as lib
from os import path
from time import perf_counter as clock
from urllib import request


##############################################################################



import os


c = 299792.458

dir_path='C:/Users/cammy/OneDrive/Documents/astronomy/ppxf/E-MILES'

res = []

# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        res.append(path)
check=0
for i in range(len(res)):
    if res[i]=='spectra_e-miles_1.3.npz':
        check=1

check=1
from os import path
if check != 1:
    print('creating file')
    hdul=fits.open(dir_path+'/'+res[68])
    data=hdul[0].data
    nlam=hdul[0].header['NAXIS1']
    lam_start=hdul[0].header['CRVAL1']
    lam_delt=hdul[0].header['CDELT1']
    lam=lam_start+(np.arange(nlam)*lam_delt)
    temp=np.zeros([nlam,len(res)])

    temp_m=np.zeros_like(res)

    temp_z=np.zeros_like(res)
    temp_a=np.zeros_like(res)
    
    print(res[1],res[0][3:7],res[0][9:13],res[0][14:21])
    
    for i in range(len(res)):
    #print(float(res[i][3:7]),res[i][8],res[i][9:13],float(res[i][14:20]))
        temp_m[i]=float(res[i][3:7])
        if res[i][8]=='m':
            temp_z[i]=-1*float(res[i][9:13])
        else:
            temp_z[i]=float(res[i][9:13])
        temp_a[i]=float(res[i][14:21])
        #print(float(res[i][14:21]),res[i][14:21])
        hdul=fits.open(dir_path+'/'+res[i])
    
        temp[:,i]=hdul[0].data
        
    metals=np.unique(temp_z)
    ages=np.unique(temp_a)
    print(temp_a)
    masses=np.zeros([len(ages),len(metals)])
    print(ages,metals)
    masses=np.full(masses.shape,1.3)
    print(masses)
    templates=np.zeros([nlam,len(ages),len(metals)])
    print(temp.shape,metals.size,ages.size)
    for i in range(len(metals)):
        for j in range(len(ages)):
            templates[:,j,i]
            templates[:,j,i]=temp[:,len(ages)*i+j]

    FWHM=np.zeros(lam.shape)


    fwhm_3060=3
    fwhm_3541=5
    fwhm_8950=2.51
    fwhm_50000=c*lam_delt/lam

    for i in range(len(lam)):
    #print(i)
        if lam[i]<=3060.8:
            FWHM[i]=fwhm_3060
        elif lam[i]>3060 and lam[i]<=3541:
            FWHM[i]=fwhm_3541
        elif lam[i]>3541 and lam[i]<=8950:
            FWHM[i]=fwhm_8950
        else:
            FWHM[i]=fwhm_50000[i]
        
        np.savez_compressed('spectra_e-miles_1.3.npz', templates=templates, masses=masses, 
                                lam=lam, ages=ages, metals=metals, fwhm=FWHM)


  # SAURON has an instrumental resolution FWHM of 4.2A.
ppxf_dir = path.dirname(path.realpath(util.__file__))

    # Read a galaxy spectrum and define the wavelength range
    #
hf = h5py.File('C:/Users/cammy/OneDrive/Documents/astronomy/ppxf/binned_spectra_NGC4694.h5','r')
binNum=hf.get('binNum')
x_bar=hf.get('x_bar')
y_bar=hf.get('y_bar')
logLam1=hf.get('logLam1')
lamGal=hf.get('lamGal')
velscale=hf.get('velscale')
log_gal=hf.get('log_gal')
log_var=hf.get('log_var')


binNum=np.array(binNum)
x_bar=np.array(x_bar)
y_bar=np.array(y_bar)
logLam1=np.array(logLam1)
lamGal=np.array(lamGal)
velscale=np.array(velscale)
log_gal=np.array(log_gal)
log_var=np.array(log_var)



velscale=velscale.item()


nbins=max(binNum)+1
redshift_0=0.00
redshift=0.003869
fwhm_gal=2.65

tie_balmer=False
limit_doublets=False


#trunc,=np.where(log_gal[:,499]>0)#np.where((lamGal>0) & (lamGal<100000))
#trunc_lamGal=np.array(lamGal[trunc])
#trunc_loglam=np.array(logLam1[trunc])
#trunc_log_gal=np.array(log_gal[trunc,:])
#trunc_log_var=np.array(log_var[trunc,:])







lam_range_temp = [lamGal[0]/1.02, lamGal[-1]*1.02]
lam_range_gal = np.array([np.min(lamGal), np.max(lamGal)])/(1 + redshift)

    # Read SPS models file from my GitHub if not already in the ppxf package dir.
    # The SPS model files are also available here https://github.com/micappe/ppxf_data
#basename = f"spectra_{sps_name}_9.0.npz"
#filename = path.join(ppxf_dir, 'sps_models', basename)


sps_name='emiles'


basename = f"spectra_{sps_name}_9.0.npz"
filename = path.join(ppxf_dir, 'sps_models', basename)
if not path.isfile(filename):
    url = "https://raw.githubusercontent.com/micappe/ppxf_data/main/" + basename
    request.urlretrieve(url, filename)
#pathname = '/fred/oz059/cammy/data_processing/MAUVE-project/ppxf/E-Miles/spectra_e-miles_1.3.npz'


sps = lib.sps_lib(filename, velscale, fwhm_gal, wave_range=lam_range_temp)
#templates=sps.templates
print(templates.shape)
    # Compute a mask for gas emission lines
#goodPixels = util.determine_goodpixels(logLam1, lam_range_temp, redshift)
stars_templates = sps.templates.reshape(sps.templates.shape[0], -1)

gas_templates, gas_names, line_wave = util.emission_lines(
    sps.ln_lam_temp, lam_range_gal, fwhm_gal, tie_balmer=tie_balmer,
    limit_doublets=limit_doublets)
    # Here the actual fit starts. The best fit is plotted on the screen. Gas
    # emission lines are excluded from the pPXF fit using the GOODPIXELS
    # keyword.

templates = np.column_stack([stars_templates, gas_templates])

#print(templates)

n_temps = stars_templates.shape[1]
n_forbidden = np.sum(["[" in a for a in gas_names])  # forbidden lines contain "[*]"
n_balmer = len(gas_names) - n_forbidden

    # Assign component=0 to the stellar templates, component=1 to the Balmer
    # gas emission lines templates and component=2 to the forbidden lines.
component = [0]*n_temps + [1]*n_balmer + [2]*n_forbidden
gas_component = np.array(component) > 0  # gas_component=True for gas templates

gas_reddening = 0 if tie_balmer else None

    # Fit (V, sig, h3, h4) moments=4 for the stars
    # and (V, sig) moments=2 for the two gas kinematic components
moments = np.array([4, 2, 2])

    # Adopt the same starting value for the stars and the two gas components



vel = c*np.log(1 + redshift)   # eq.(8) of Cappellari (2017, MNRAS)
start = [vel, 200.]  # (km/s), starting guess for [V, sigma]
start = np.array([start, start, start])
print(len(start[1]),moments[1])
t = clock()
summed_spec=np.nansum(log_gal,axis=1)
summed_var=np.nansum(log_var,axis=1)

pp = ppxf(templates, summed_spec, np.sqrt(summed_var), velscale, start, plot=True, lam=np.exp(logLam1),
          lam_temp=sps.lam_temp, degree=4,component=component,
          gas_component=gas_component, gas_names=gas_names,
          gas_reddening=gas_reddening,moments=moments)

#print(np.array(np.where(pp.weights.reshape(sps.n_ages,sps.n_metals)>0)).T)
#print(pp.weights[:pp.weights.shape[0]-len(gas_names)])

weights=np.array(pp.weights)
#temp_temp=np.zeros([sps.lam_temp.size,sps.n_ages,sps.n_metals])
#for i in range(sps.n_ages):
#    for j in range(sps.n_metals):
#        if weights[i,j]>0:
#            temp_temp[:,i,j]=templates[:,i,j]
temp_temp2=templates[:,np.where(weights>0)[0]]
print(temp_temp2.shape)
#print(temp_temp[55,:,:])
x=3100
masked_pixels=np.full(log_gal.shape,True)
#plt.plot(logLam1,log_var[:,x])
bestfits=np.zeros(log_gal.shape)
V,rms,h3,h4,eV,erms,eh3,eh4,chi2,redshift_fit,redshift_err = np.zeros(nbins),np.zeros(nbins),np.zeros(nbins),np.zeros(nbins),np.zeros(nbins),np.zeros(nbins),np.zeros(nbins),np.zeros(nbins),np.zeros(nbins),np.zeros(nbins),np.zeros(nbins)
Vhb,Vo3,rmshb,rmso3=np.zeros(nbins),np.zeros(nbins),np.zeros(nbins),np.zeros(nbins)

#weights= np.zeros([nbins,sps.n_ages*sps.n_metals])

weights= np.zeros([nbins,temp_temp2[0].shape[0]])
#print(sps.lam_temp[0],sps.lam_temp[-1],lamGal[0],lamGal[-1])


print('-------------------------------------------')

n_temps = temp_temp2.shape[1]-len(gas_names)
n_forbidden = np.sum(["[" in a for a in gas_names])  # forbidden lines contain "[*]"
n_balmer = len(gas_names) - n_forbidden

    # Assign component=0 to the stellar templates, component=1 to the Balmer
    # gas emission lines templates and component=2 to the forbidden lines.
component = [0]*n_temps + [1]*n_balmer + [2]*n_forbidden
gas_component = np.array(component) > 0  # gas_component=True for gas templates

gas_reddening = 0 if tie_balmer else None

print('-------------------------------------------')

for i in range(x-1,x+1):
    pp = ppxf(temp_temp2, log_gal[:,i], np.sqrt(log_var[:,i]), velscale, start, plot=True, lam=np.exp(logLam1),
              lam_temp=sps.lam_temp, degree=4,component=component,
              gas_component=gas_component, gas_names=gas_names,
              gas_reddening=gas_reddening,moments=moments)
    V[i],rms[i],h3[i],h4[i]=pp.sol[0]
    Vhb[i],rmshb[i]=pp.sol[1]
    Vo3[i],rmso3[i]=pp.sol[2]
    eV[i],erms[i],eh3[i],eh4[i]=pp.error[0]*np.sqrt(pp.chi2)
    chi2[i]=pp.chi2
    goodpixels=pp.goodpixels
    #print(pp.weights.reshape(25,6))
    weights[i]=pp.weights
    redshift_fit[i] = (1 + redshift_0)*np.exp(V[i]/c) - 1  # eq. (5c) C22
    redshift_err[i] = (1 + redshift_fit[i])*eV[i]/c    
    bestfits[:,i]=pp.bestfit
    
    for j in range(len(logLam1)):
   ##print(np.any(logLam1[goodpixels]==logLam1[i]))
       if np.any(logLam1[goodpixels]==logLam1[j])==True:
           masked_pixels[j,i]=False
   
    print(redshift_fit[i])
    print('Elapsed time in pPXF: %.2f s' % (clock() - t))
    plt.pause(2)
    #plt.savefig('ppxf_check.png')
#values = np.arange(2*2*4).reshape(4, 2, 2)

print(len(x_bar),log_gal[0,:].size,log_gal.shape)

f = h5py.File('C:/Users/cammy/OneDrive/Documents/astronomy/ppxf/ppxf_out_NGC4694.h5','w')

f.create_dataset("x_bar", data=x_bar)
f.create_dataset("y_bar", data=y_bar)


f.create_dataset("Vhb", data=Vhb)
f.create_dataset("rmshb", data=rmshb)

f.create_dataset("Vo3", data=Vo3)
f.create_dataset("rmso3", data=rmso3)

f.create_dataset("V", data=V)
f.create_dataset("rms", data=rms)

f.create_dataset("h3", data=h3)
f.create_dataset("h4", data=h4)

f.create_dataset("eV", data=eV)
f.create_dataset("erms", data=erms)

f.create_dataset("eh3", data=eh3)
f.create_dataset("eh4", data=eh4)

f.create_dataset("redshift", data=redshift_fit)
f.create_dataset("eredshift", data=redshift_err)

f.create_dataset("chi2", data=chi2)
f.create_dataset("spectra", data=log_gal)

f.create_dataset("variance", data=log_var)
f.create_dataset("bestfits", data=bestfits)

f.create_dataset("binNum", data=binNum)
f.create_dataset("masked_pixels", data=masked_pixels)

f.create_dataset("weights", data=weights)
f.create_dataset("lamGal", data=lamGal)
f.create_dataset("logLam1", data=logLam1)


hf.close()












