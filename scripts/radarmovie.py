from BRadar.plotutils import RadarAnim
from BRadar.io import LoadRastRadar, LoadLevel2, LoadPAR_lipn, LoadPAR_wdssii
import matplotlib.pyplot as plt
import numpy as np



def load_wrapper(fname, loadfunc) :
    radData = loadfunc(fname)
    az = np.radians(radData['azimuth'])
    r = radData['range_gate']/1000.0

    return dict(vals=radData['vals'][None, :, :], lons=az, lats=r)

_load_funcs = dict(rast_nc=LoadRastRadar,
                   lev2_nc=lambda fname: load_wrapper(fname, LoadLevel2),
                   lip_nc=lambda fname: load_wrapper(fname, LoadPAR_lipn),
                   wdssii=lambda fname: load_wrapper(fname, LoadPAR_wdssii))

_projections = dict(rast_nc=None,
                    lev2_nc='polar',
                    lip_nc='polar',
                    wdssii='polar')


def main(args) :
    fig = plt.figure()
    proj = _projections[args.loadfunc]
    ax = fig.gca(projection=proj)

    if proj == 'polar' :
        ax.set_theta_zero_location('N')
        ax.set_theta_direction('clockwise')

    anim = RadarAnim(fig, args.radarfiles, load_func=_load_funcs[args.loadfunc])
    anim.add_axes(ax)


    if args.savefile is not None :
        anim.save(args.savefile)

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
                        help="Select the data loader for your files."
                             " Choices: %(choices)s. Default: %(default)s",
                        metavar="LOADER", default='rast_nc')
    parser.add_argument("--save", dest="savefile", type=str,
                        help="Save the movie as OUTPUT",
                        metavar="OUTPUT", default=None)
    parser.add_argument("--noshow", dest="doShow", action='store_false',
                        help="Do not display the animation to the screen")


    args = parser.parse_args()

    main(args)
