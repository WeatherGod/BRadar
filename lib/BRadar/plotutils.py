from matplotlib.colors import BoundaryNorm
from matplotlib.colorbar import ColorbarBase
import numpy as np		# using .ma for Masked Arrays, also for .isnan()
import matplotlib.pyplot as plt
import ctables		# for color table for reflectivities


def MakePPI(x, y, vals, norm, ref_table, axis=None, mask=None, 
            rasterized=False, **kwargs):
    # It would be best if x and y were parallel arrays to vals.
    # I haven't tried to see what would happen if they were just 1-D arrays each...
    if axis is None :
        axis = plt.gca()

    if mask is None :
        mask = np.isnan(vals)
    
    thePlot = axis.pcolor(x, y,
                        np.ma.masked_array(vals, mask=mask),
                        cmap=ref_table, norm=norm, **kwargs)
    thePlot.set_rasterized(rasterized)

    return thePlot



#--------------------------------------
#     Reflectivity
#--------------------------------------
# lut=-1 sets up discretized colormap, rather than smoothly changing colormap 
reflect_cmap = ctables.get_cmap("NWSRef", lut=-1)
reflect_cmap.set_over('0.25')
reflect_cmap.set_under('0.75')

NWS_Reflect = {'ref_table': reflect_cmap,
	           'norm': BoundaryNorm(np.arange(0, 80, 5),
               reflect_cmap.N, clip=False)}


def MakeReflectPPI(vals, lats, lons, axis=None, axis_labels=True, colorbar=True, **kwargs) :
    # The Lats and Lons should be parallel arrays to vals.
    if axis is None :
       axis = plt.gca()

    thePlot = MakePPI(lons, lats, vals, NWS_Reflect['norm'], NWS_Reflect['ref_table'],
                      axis=axis, **kwargs)

    # I am still not quite sure if this is the best place for this, but oh well...
    if axis_labels : 
       axis.set_xlabel("Longitude [deg]")
       axis.set_ylabel("Latitude [deg]")

    if colorbar :
        MakeReflectColorbar(axis)

    return thePlot



def MakeReflectColorbar(ax=None, colorbarLabel="Reflectivity [dBZ]", **kwargs) :
    # Probably need a smarter way to allow fine-grained control of properties
    # like fontsize and such...
    if ax is None :
        ax = plt.gca()

    cbar = ColorbarBase(ax, cmap=NWS_Reflect['ref_table'],
                        norm=NWS_Reflect['norm'], **kwargs)
    cbar.set_label(colorbarLabel)
    return cbar


# Maybe this should go into MapUtils?
def TightBounds(lons, lats, vals) :
    badVals = np.isnan(vals)
    lats_masked = np.ma.masked_array(lats, mask=badVals)
    lons_masked = np.ma.masked_array(lons, mask=badVals)
    minLat = min(lats_masked)
    maxLat = max(lats_masked)
    minLon = min(lons_masked)
    maxLon = max(lons_masked)
    return {'minLat': minLat, 'minLon': minLon, 'maxLat': maxLat, 'maxLon': maxLon}

