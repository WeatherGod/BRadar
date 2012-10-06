from BRadar.plotutils import RadarAnim, MakeReflectPPI
from BRadar.io import LoadRastRadar, LoadLevel2, LoadPAR_lipn, LoadPAR_wdssii
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation
from itertools import cycle
from datetime import datetime

#from mpl_toolkits.axes_grid1 import AxesGrid

#plt.rcParams['animation.writer'] = 'ffmpeg_file'
#plt.rcParams['animation.codec'] = 'mpeg1video'
#plt.rcParams['animation.ffmpeg_args'] = ['-sameq']

def load_wrapper(fname, loadfunc) :
    radData = loadfunc(fname)
    az = np.radians(radData.pop('azimuth'))
    r = radData.pop('range_gate')/1000.0

    return dict(vals=radData['vals'][None, :, :], lons=az, lats=r, **radData)

_load_funcs = dict(rast_nc=LoadRastRadar,
                   lev2_nc=lambda fname: load_wrapper(fname, LoadLevel2),
                   lip_nc=lambda fname: load_wrapper(fname, LoadPAR_lipn),
                   wdssii=lambda fname: load_wrapper(fname, LoadPAR_wdssii))

_projections = dict(rast_nc=None,
                    lev2_nc='polar',
                    lip_nc='polar',
                    wdssii='polar')


def _update_title(anim, ax) :
    if anim.curr_time is not None :
        currTitle = ax.title
        titlestr = anim.curr_time.strftime("%Y-%m-%d %H:%M:%S UTC")
        currTitle.set_text(titlestr)


class TitleAnim(FuncAnimation) :
    def __init__(self, radanim, ax, **kwargs) :
        self._radanim = radanim
        self._ax = ax

        FuncAnimation.__init__(self, radanim._fig, self.update_title,
                                    blit=False, **kwargs)

    def update_title(self, *args) :
        currTime = self._radanim.curr_time
        if currTime is not None :
            currTitle = self._ax.title
            titleStr = currTime.strftime("%Y-%m-%d %H:%M:%S UTC")
            currTitle.set_text(titleStr)


class SyncedRadar(FuncAnimation) :
    def __init__(self, fig, grid, filelists,
                       load_funcs=None, robusts=False, **kwargs) :

        self._filelists = [cycle(files) for files in filelists]
        self._loadfunc = load_func if load_func is not None else LoadRastRadar
        self._curr_times = [None] * len(filelists)
        self._ims = [None] * len(filelists)
        self._datas = [None] * len(filelists)
        #self.im_kwargs = [None] * len(filelists)
        self._has_looped = [False] * len(filelists)
        self._grid = grid
        self.robust = robust

        FuncAnimation.__init__(self, fig, self.nexttick, blit=False,
                                          init_func=self.firsttick, **kwargs)

    @staticmethod
    def _get_time(data) :
        currTime = data.get('scan_time', None)
        if (currTime is not None and
            not isinstance(currTime, datetime)) :
            currTime = datetime.utcfromtimestamp(currTime)

        return currTime

    def _advance_anim(self, index) :
        data = self._loadfunc(next(self._filelists[index]))
        self._datas[index] = data
        self._curr_times[index] = self._get_time(data)

        if self._ims[index] is not None and not self.robust :
            self._ims[index].set_array(data['vals'][0, :-1, :-1].flatten())
        else :
            self._ims[index] = MakeReflectPPI(data['vals'][0],
                                              data['lats'], data['lons'],
                                              meth='pcmesh',
                                              axis_labels=False,
                                              mask=False,
                                              ax=self._grid[index])


    def firsttick(self, *args) :
        for index in range(len(self._curr_times)) :
            if self._curr_times[index] is None :
                self._advance_anim(index)

    def nexttick(self, *args) :
        latestTime = max(self._curr_times)

        force_advance = all([currTime == latestTime for
                             currTime in self._curr_times])

        for index in range(len(self._curr_times)) :
            # Only advance the animation if the current frame is older
            # than the newest frame overall, and if the filelist hasn't
            # cycled yet.  The cycle indicator is reset when all anims
            # have cycled.
            if force_advance or (latestTime > self._curr_times[index] and 
                                 not self._has_looped[index]) :
                prevTime = self._curr_times[index]
                self._advance_anim(index)

                if prevTime > self._curr_times[index] :
                    self._has_looped[index]

        if all(self._has_looped) :
            self._has_looped = [False] * len(self._has_looped)
 

def main(args) :

    if args.layout is None :
        args.layout = (1, len(args.others) + 1)

    if args.figsize is None :
        args.figsize = plt.figaspect(float(args.layout[0]) / args.layout[1])

    proj = _projections[args.loadfunc]
    """
    fig = plt.figure(figsize=args.figsize)


    if proj is None :
        if args.shareall:
            grid = AxesGrid(fig, 111, nrows_ncols=args.layout, aspect=False,
                            share_all=True)
        else:
            grid = [fig.add_subplot(args.layout[0], args.layout[1],
                                    index + 1) for index in
                    range(np.prod(args.layout))]
    elif proj == 'polar' :
        # Currently can't make an AxesGrid of PolarAxes
        grid = [fig.add_subplot(args.layout[0], args.layout[1],
                                index + 1, polar=True) for index in
                range(np.prod(args.layout))]

        for ax in grid :
            ax.set_theta_zero_location('N')
            ax.set_theta_direction('clockwise')
    """
    fig, grid = plt.subplots(args.layout[0], args.layout[1],
                             sharex=args.shareall, sharey=args.shareall,
                             squeeze=False,
                             subplot_kw=dict(projection=proj,axisbg='0.78'),
                             figsize=args.figsize)

    if proj == 'polar':
        for ax in grid.flat:
            ax.set_theta_zero_location('N')
            ax.set_theta_direction('clockwise')

    filelists = [args.radarfiles] + args.others

    anims = []
    event_source = None
    time_markers = None
    
    for index, (radarFiles, ax) in enumerate(zip(filelists, grid.flat)) :
        anim = RadarAnim(fig, radarFiles, robust=args.robust,
                         load_func=_load_funcs[args.loadfunc], sps=600.0,
                         event_source=event_source, time_markers=time_markers,
                         blit=False)
        anim.add_axes(ax)
        anims.append(anim)

        event_source = anim.event_source
        time_markers = anim.time_markers
    
        # Remember, Python is late-binding.  If I had just
        # simply passed ax and anim to the lambda function, _update_title()
        # would have been called only with the last axes and animation objects.
        #anim.event_source.add_callback(lambda i : _update_title(anims[i],
        #                                                        grid[i]),
        #                               index)
    

    #anim = SyncedRadar(fig, grid, filelists, robust=args.robust,
    #                   load_func=_load_funcs[args.loadfunc])
    text_anims = []

    for anim, ax in zip(anims, grid.flat) :
        text_anims.append(TitleAnim(anim, ax,
                                    event_source=anim.event_source,
                                    frames=len(time_markers)))



    if args.savefile is not None :
        anims[0].save(args.savefile, extra_anim=text_anims + anims[1:])

    if args.doShow :
        plt.show()


if __name__ == '__main__' :
    import argparse

    parser = argparse.ArgumentParser(description='View/Save an animation'
                                     ' of radar reflectivities.')

    parser.add_argument("radarfiles", nargs='+', type=str,
                        help="FILEs of the radar data",
                        metavar="FILE")
    parser.add_argument("--loader", dest="loadfunc",
                        choices=['rast_nc', 'lev2_nc', 'lip_nc', 'wdssii'],
                        action='append',
                        help="Select the data loader for your files."
                             " Choices: %(choices)s. Default: %(default)s",
                        metavar="LOADER", default='rast_nc')
    parser.add_argument("--save", dest="savefile", type=str,
                        help="Save the movie as OUTPUT",
                        metavar="OUTPUT", default=None)
    parser.add_argument("--noshow", dest="doShow", action='store_false',
                        help="Do not display the animation to the screen")
    parser.add_argument("--robust", dest="robust", action='store_true',
                        help="Force the animation to not assume a consistant"
                             " data size/shape and consistant domain."
                             " Use this option if you are getting 'weird'"
                             " rendering results.")

    parser.add_argument("-i", "--inputs", dest="others", type=str,
                        action="append", nargs="+",
                        help="Add another display of radar animation."
                             " Currently assumes to use the same loader.",
                        metavar="FILE", default=[])

    parser.add_argument("-l", "--layout", dest="layout", type=int, nargs=2,
                        help="Specify the layout (row x col) of the animation."
                             " Default: auto",
                        metavar='N', default=None)
    parser.add_argument("-f", "--figsize", dest="figsize", type=float, nargs=2,
                        help="Specify the figure size (height x width)"
                             " in inches. Default: auto.",
                        metavar="X", default=None)
    parser.add_argument("--shareall", action='store_true', default=False,
                        help="Have the subplots share the same domain")


    args = parser.parse_args()

    main(args)
