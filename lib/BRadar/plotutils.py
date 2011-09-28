from matplotlib.colors import BoundaryNorm
from matplotlib.colorbar import ColorbarBase
import numpy as np		# using .ma for Masked Arrays, also for .isnan()
import matplotlib.pyplot as plt
import ctables		# for color table for reflectivities


def MakePPI(x, y, vals, norm, ref_table, ax=None, mask=None, 
            rasterized=False, meth='pcmesh', **kwargs):
    """
    Make a PPI plot at coordinates of *x*, *y* using *vals*.
    Colors are determined by the *norm* and *ref_table*.

    The function will automatically convert the *vals* array
    into a masked_array if there are NaNs and no *mask* is
    provided.

    *meth*      ['pc'|'pcmesh'|'im']
        Plotting method to use (pcolor, pcolormesh, imshow).
        pcolor() ('pc') works for the most generic case of arbitrary
        coordinates, but can be inefficient for regular domains.
        pcolormesh() ('pcmesh') can be more efficient, but assumes regular
        domains.
        imshow() ('im') is very efficient for rectilinear domains.

    Additional kwargs are passed to the plotting function.

    Returns the plotted object.

    """
    # It would be best if x and y were parallel arrays to vals.
    # I haven't tried to see what would happen if they were just 1-D arrays each...
    if ax is None :
        ax = plt.gca()

    if mask is None :
        mask = np.isnan(vals)

    # If vals is already a masked array, then the
    # final mask is the or'd of *mask* and the array's
    # existing mask.
    maskedVals = np.ma.masked_array(vals, mask=mask)
    
    #print(x.ndim, y.ndim)
    if meth == 'pc' :
        thePlot = ax.pcolor(x, y, maskedVals,
                        cmap=ref_table, norm=norm, **kwargs)
    elif meth == 'pcmesh' :
        thePlot = ax.pcolormesh(x, y, maskedVals,
                        cmap=ref_table, norm=norm, **kwargs)
    elif meth == 'im' :
        extent=(x.min(), x.max(), y.min(), y.max())
        thePlot = ax.imshow(maskedVals,
                        cmap=ref_table, norm=norm,
                        interpolation='none', origin='lower',
                        extent=extent,
                        **kwargs)
    else :
        raise ValueError("Invalid method for MakePPI: %s" % meth)

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


def MakeReflectPPI(vals, lats, lons,
                   ax=None, cax=None,
                   axis_labels=True, colorbar=True, **kwargs) :
    # The Lats and Lons should be parallel arrays to vals.
    if ax is None :
       ax = plt.gca()

    thePlot = MakePPI(lons, lats, vals,
                      NWS_Reflect['norm'], NWS_Reflect['ref_table'],
                      ax=ax, **kwargs)

    # I am still not quite sure if this is the best place for this...
    if axis_labels : 
       ax.set_xlabel("Longitude [deg]")
       ax.set_ylabel("Latitude [deg]")

    if colorbar and cax is not None:
        MakeReflectColorbar(cax)

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


def TightBounds(lons, lats, vals) :
    badVals = np.isnan(vals)
    lats_masked = np.ma.masked_array(lats, mask=badVals)
    lons_masked = np.ma.masked_array(lons, mask=badVals)
    minLat = lats_masked.min()
    maxLat = lats_masked.max()
    minLon = lons_masked.min()
    maxLon = lons_masked.max()
    return {'minLat': minLat, 'minLon': minLon, 'maxLat': maxLat, 'maxLon': maxLon}

