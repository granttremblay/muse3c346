import pyfits
import numpy
import pylab

def gal_extinct(wave,A_V,Rv=3.1):
  '''Milky Way extinction correction'''
  m=wave/10000.0
  x=1/m
  y=(x-1.82)
  ax=1+(0.17699*y)-(0.50447*y**2)-(0.02427*y**3)+(0.72085*y**4)+(0.01979*y**5)-(0.77530*y**6)+(0.32999*y**7)
  bx=(1.41338*y)+(2.28305*y**2)+(1.07233*y**3)-(5.38434*y**4)-(0.62251*y**5)+(5.30260*y**6)-(2.09002*y**7)
    
  Arat=ax+(bx/Rv)
  Alambda=Arat*A_V
  return Alambda

def correct_cube(incube,outcube,sky_region,A_V,star_position=[],offset=(0,0),binning=True):
  hdu = pyfits.open(incube)
  data = hdu[1].data
  header = hdu[1].header
  hdu.close()
 
  dim = data.shape
  wave = numpy.arange(dim[0])*header['CD3_3'] + header['CRVAL3']
  if binning:
	dim_out = (dim[0],(dim[1]-offset[1])//2,(dim[2]-offset[0])//2)
  	cube = numpy.zeros(dim_out,dtype=numpy.float32)
  	for x in range(dim_out[2]):
    		for y in range(dim_out[1]):
      			cube[:,y,x] = numpy.sum(numpy.sum(data[:,2*y+offset[1]:2*(y+1)+1+offset[1],2*x+offset[0]:2*(x+1)+offset[0]],axis=1),axis=1)/1e4
      
 	error = numpy.std(cube[:,sky_region[2]//2:sky_region[3]//2,sky_region[0]//2:sky_region[1]//2].reshape(dim_out[0],(sky_region[3]//2-sky_region[2]//2)*(sky_region[1]//2-sky_region[0]//2)),axis=1)
  else:
	error = numpy.std(data[:,sky_region[2]:sky_region[3],sky_region[0]:sky_region[1]].reshape(dim[0],(sky_region[3]-sky_region[2])*(sky_region[1]-sky_region[0])),axis=1)

	cube = data
  nan = numpy.isnan(cube)
  cube[nan] = 0.0

  if len(star_position)>0:
    if binning:
	    star_spec = numpy.sum(numpy.sum(cube[:,star_position[1]//2-2:star_position[1]//2+2,star_position[0]//2-2:star_position[0]//2+2],1),1)
    else:
	star_spec = numpy.sum(numpy.sum(cube[:,star_position[1]-4:star_position[1]+4,star_position[0]-4:star_position[0]+4],1),1)
    telluric = [[6800,6950],[7130,7220],[7550,7700],[8150,8300],[9000,9280]]
    clean_star = numpy.array(star_spec)
    for i in range(len(telluric)):
      blue = telluric[i][0]
      red = telluric[i][1]
      select_blue=(wave>blue-10) & (wave<blue+10)
      select_red=(wave>red-10) & (wave<red+10)
      select_telluric=(wave>blue) & (wave<red)
      flux_blue = numpy.median(star_spec[select_blue])
      flux_red = numpy.median(star_spec[select_red])
      m = (flux_red-flux_blue)/(red-blue)
      z = flux_blue-m*blue
      clean_star[select_telluric]=wave[select_telluric]*m+z
    ratio = clean_star/star_spec  
    cube = cube*ratio[:,numpy.newaxis,numpy.newaxis]
    error = error * ratio
    
  cube = cube/10**(gal_extinct(wave,A_V)[:,numpy.newaxis,numpy.newaxis]/-2.5)
  error = error/10**(gal_extinct(wave,A_V)/-2.5)
  hdus = []
  hdus.append(pyfits.PrimaryHDU(cube.astype(numpy.float32)))
  hdus.append(pyfits.ImageHDU(error.astype(numpy.float32),name='ERRSPEC'))
  hdu = pyfits.HDUList(hdus)
  header['EXTEND'] = False
  header['CRPIX1'] = (float(header['CRPIX1'])-offset[0])/2.0
  header['CRPIX2'] = (float(header['CRPIX2'])-offset[1])/2.0
  header['CD1_1'] = float(header['CD1_1'])*2.0
  header['CD2_2'] = float(header['CD2_2'])*2.0
  header['CDELT3'] = header['CD3_3']
  header['BUNIT'] = '10**(-16)*erg/s/cm**2/Angstrom'
  header['EXTINCT'] = (A_V,'V-band Galactic extinction')
  hdu[0].header = header
  hdu.verify('silentfix')
  hdu.writeto(outcube,clobber=True)


infile = "DATACUBE_FINAL.fits"
outfile = "DATACUBE_ANALYZE_ME.fits"


# A_V for 3C 346 is 0.186 (NED)
corrected_cube = correct_cube(infile,outfile,[211,280,65,128],0.186,binning=True)