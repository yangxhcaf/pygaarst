# coding: utf-8
"""
pygaarst.hyperionutils

Utility functions for processing Hyperion datasets

Created by Chris Waigl on 2014-04-25.
"""

from __future__ import division, print_function
from distutils.version import LooseVersion
import os
import numpy as np


def gethyperionbands():
    """
    Load Hyperion spectral band values into Numpy structured array.
    Source: http://eo1.usgs.gov/sensors/hyperioncoverage
    """
    this_dir, _ = os.path.split(__file__)
    tabfile = os.path.join(this_dir, 'data', 'Hyperion_Spectral_coverage.tab')
    kwargs = {
        'delimiter': '\t',
        'skip_header': 1,
        'names': True,
    }
    if LooseVersion(np.__version__) > LooseVersion('1.14'):
        kwargs['encoding'] = 'bytes'
        converter = lambda x: x.decode('utf-8').replace('B', 'band')
    else:
        converter = lambda x: x.replace('B', 'band')
    kwargs['converters'] = {0: converter}
    return np.recfromtxt(tabfile, **kwargs)


def gethyperionirradiance():
    """Load Hyperion spectral irradiance into Numpy array"""
    this_dir, _ = os.path.split(__file__)
    tabfile = os.path.join(
        this_dir, 'data', 'Hyperion_Spectral_Irradiance.txt')
    converter = lambda x: x.replace('b', '')
    return np.recfromtxt(
        tabfile,
        delimiter='\t',
        skip_header=1,
        names=True,
        converters={0: converter}
    )


def getesun(band):
    irradiances = gethyperionirradiance()
    return irradiances[
        irradiances['Hyperion_band'] == band]['Spectral_irradiance_Wm2mu'][0]

def find_nearest_hyp(wavelength):
    """
    Returns index and wavelength of Hyperion band closest to input wavelength

    Arguments:
      wavelength (float): wavelength in nm

    Returns:
      idx (int): band index of closest band, starting at 0
      band (str): band name of closest band, starting at 'band1'
      bandwavelength (float): closest band wavelength in nm
    """
    bands = gethyperionbands().Hyperion_Band
    wavs = gethyperionbands().Average_Wavelength_nm
    idx = (np.abs(wavs - wavelength)).argmin()
    return idx, bands[idx], wavs[idx]
