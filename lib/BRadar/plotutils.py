from matplotlib.colors import BoundaryNorm
from matplotlib.colorbar import ColorbarBase
import numpy as np		# using .ma for Masked Arrays, also for .isnan()
import matplotlib.pyplot as plt
import ctables		# for color table for reflectivities
from datetime import datetime
from collections import OrderedDict
from matplotlib.animation import FuncAnimation
from BRadar.io import LoadRastRadar

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


class RadarAnim(FuncAnimation) :
    def __init__(self, fig, files, load_func=None, **kwargs) :
        self._rd = files
        self._loadfunc = load_func if load_func is not None else LoadRastRadar
        self._im = None
        FuncAnimation.__init__(self, fig, self.nextframe, frames=len(files),
                                     **kwargs)

    def nextframe(self, index, *args) :
        data = self._loadfunc(self._rd[index])
        if self._im is None :
            self._im = MakeReflectPPI(data['vals'][0],
                                      data['lats'], data['lons'], meth='pcmesh',
                                      axis_labels=False, zorder=0, mask=False)
        else :
            self._im.set_array(data['vals'][0, :-1, :-1].flatten())

        return self._im,
        

class RadarDisplay(object) :
    def __init__(self, ax, radarData, xs=None, ys=None) :
        """
        Create a display for radar data.
        """
        self.ax = ax
        self.radarData = radarData
        self._im = None
        self._title = None
        self.frameIndex = 0
        data = self.radarData.curr()
        self.xs = xs if xs is not None else data['lons']
        self.ys = ys if ys is not None else data['lats']
        self.refresh_display()

    def next(self) :
        if ((self.frameIndex + 1) <= (len(self.radarData) - 1)) :
            self.radarData.next()
            self.frameIndex += 1
            self.refresh_display()
        
    def prev(self) :
        if (0 <= (self.frameIndex - 1)) :
            self.radarData.prev()
            self.frameIndex -= 1
            self.refresh_display()

    def refresh_display(self) :
        """
        Draw the display using the current value of *self.radarData*.
        """
        data = self.radarData.curr()

        # Display current frame's radar image
        if self._im is None :
            self._im = MakeReflectPPI(data['vals'][0], self.ys, self.xs,
                                      meth='pcmesh', ax=self.ax,
                                      colorbar=False, axis_labels=False,
                                      zorder=0, mask=False)
        else :
            self._im.set_array(data['vals'][0, :-1, :-1].flatten())


        theDateTime = datetime.utcfromtimestamp(data['scan_time']).strftime(
                                                        "%Y-%m-%d %H:%M:%S")

        # Update axis title label
        if self._title is None :
            self._title = self.ax.set_title(theDateTime)
        else :
            self._title.set_text(theDateTime)

class BaseControlSys(object) :
    def __init__(self, fig, rd) :
        """
        Create a control system for paging radar frames.

        *fig*
            The matplotlib figure object.

        *rd*
            The RadarDisplay object
        """
        self.fig = fig
        self.rd = rd

        fig.canvas.mpl_connect('key_press_event', self.process_key)
        #fig.canvas.mpl_connect('button_release_event',
        #                       self.process_click)


        self.keymap = OrderedDict()
        self.keymap['left'] = {'func': self.step_back,
                               'help': "Step back display by one frame"}
        self.keymap['right'] = {'func': self.step_forward,
                                'help': 'Step forward display by one frame'}

        self._clean_mplkeymap()


    def _clean_mplkeymap(self) :
        from matplotlib import rcParams
        # TODO: Generalize this
        # Need to remove some keys...
        rcParams['keymap.fullscreen'] = []
        rcParams['keymap.zoom'] = []
        rcParams['keymap.save'] = []
        for keymap in ('keymap.home', 'keymap.back', 'keymap.forward') :
            for key in self.keymap :
                if key in rcParams[keymap] :
                    rcParams[keymap].remove(key)

    def process_key(self, event) :
        """
        Key-press handler
        """
        if event.key in self.keymap :
            self.keymap[event.key]['func']()
            self.fig.canvas.draw_idle()

    def step_back(self) :
        self.rd.prev()

    def step_forward(self) :
        self.rd.next()


