from __future__ import print_function
import numpy as np
from matplotlib.nxutils import points_inside_poly
from maputils import sph2latlon, latlon2pix, makerefmat

from multiprocessing import Pool

def Rastify(statLat, statLon, origData, azimuths, 
            rangeGates, elevAngle, deltaAz, deltaR,
            cellSize=None, lonAxis=None, latAxis=None,
            mask=False) :
    """
    RASTIFY    Covert data in spherical domain into rectilinear
                lat/lon domain

    Rastify(...) takes the vector or matrix of data points and places
    the points into a 2-D matrix organized by latitudes and longitudes.
    The original data has a parallel vector or matrix of azimuths (in
    degrees North) and rangeGates (in meters) as well as a scalar elevAngle
    (in degrees). The origin of the spherical coordinates is given by
    the statLat (in degrees North) and statLon (in degrees East). deltaAz
    denotes the width of the beam in degrees while the deltaR scalar
    denotes the width the of range gate in meters.

    For the final grid, the user can specify the latitude and/or longitude
    axes with the *lonAxis* and *latAxis* kwargs. For which ever axis not
    specified, the user can specify a resultion (in degrees) with the
    *cellSize* kwarg, and the axis will be automatically determined by
    the limits of the supplied inputs.

    Author: Benjamin Root
    """
    if (latAxis is None or lonAxis is None) and cellSize is None :
        raise ValueError("Must specify *cellSize* if *latAxis* and/or"
                         "*lonAxis* is not given")

    goodVals = (~np.isnan(origData) | ~mask)
    origData = origData[goodVals]
    azimuths = azimuths[goodVals]
    rangeGates = rangeGates[goodVals]
 
    # These arrays are for creating the verticies of the resolution volume
    # in 2-D.
    deltaAzMult = np.array([-1, -1, 1, 1])
    deltaRMult = np.array([-1, 1, 1, -1])
    
    # Getting the lat/lon locations of all the verticies.
    tmpLat, tmpLon = sph2latlon(statLat, statLon, 
                                (azimuths[:, np.newaxis] +
                                 (deltaAzMult[np.newaxis, :] * deltaAz)),
                                (rangeGates[:, np.newaxis] +
                                 (deltaRMult[np.newaxis, :] * deltaR)),
                                elevAngle)

    # Automatically determine the domain,
    # note that this isn't friendly to crossing the prime-meridian.
    if latAxis is None :
        latlim = (tmpLat.min(), tmpLat.max())
        latAxis = np.arange(latlim[0], latlim[1] + cellSize, cellSize)
    else :
        latlim = (latAxis.min(), latAxis.max())

    latRes = np.abs(np.median(np.diff(latAxis)))

    if lonAxis is None :
        lonlim = (tmpLon.min(), tmpLon.max())
        lonAxis = np.arange(lonlim[0], lonlim[1] + cellSize, cellSize)
    else :
        lonlim = (lonAxis.min(), lonAxis.max())

    lonRes = np.abs(np.median(np.diff(lonAxis)))

    # Automatically determine the grid size from the calculated axes.
    gridShape = (len(latAxis), len(lonAxis))
    
    # Reference matrix is used to perform the affine transformation from
    # lat/lon to the x-y coordinates that we need.
    # This can be adjusted later to allow for the user to specify a
    # different resolution for x direction from the resolution in the y
    # direction.
    R = makerefmat(lonlim[0], latlim[0], lonRes, latRes)
    
    # Getting the x and y locations for each and every verticies.
    (tmpys, tmpxs) = latlon2pix(R, tmpLat, tmpLon)
    
    # I wonder if it is computationally significant to get the min/max's of
    # each polygon's coordinates in one shot.  What about storage
    # requirements?
    
    # Initializing the data matrix.
    rastData = np.empty(gridShape)
    rastData[:] = np.nan

    #p = Pool(6)
    #
    #results = [p.apply_async(_raster_points,
    #                         (tmpx,tmpy,gridShape)) for
    #           tmpx, tmpy in zip(tmpxs, tmpys)]

    #p.close()
    #p.join()

    # Take the original data value, and assign it to each rasterized
    # gridpoint that fall within its voxel.
    #for tmpx, tmpy, val in zip(tmpxs, tmpys, origData) :
    for tmpx, tmpy, val in zip(tmpxs, tmpys, origData) :
        pts = _raster_points(tmpx, tmpy, gridShape)
        #pts = res.get()
	    # Assign values to the appropriate locations (the grid points that
        # were inside the polygon), given that the data value that might
        # already be there is less-than the value to-be-assigned, or if
        # there hasn't been a data-value assigned yet (NAN).
        # This method corresponds with the method used by NEXRAD.
        for containedPoint in zip(*pts) :
            if (np.isnan(rastData[containedPoint])
                or (rastData[containedPoint] < val)) :
                rastData[containedPoint] = val

    return (rastData, latAxis, lonAxis)

def _raster_points(tmpx, tmpy, gridShape) :
    """
    Find the raster grid points that lie within the voxel
    """
    if (max(tmpx) < 0 or max(tmpy) < 0 or
        min(tmpx) >= gridShape[1] or min(tmpy) >= gridShape[0]) :
        # points lie outside the rasterization grid
        # so, none of them are good.
        return ([], [])

    resVol = zip(tmpx[[0, 1, 2, 3, 0]],
                 tmpy[[0, 1, 2, 3, 0]])

    # Getting all of the points that the polygon has, and then some.
    # This meshed grid is bounded by the domain.
    bbox = ((int(max(np.floor(min(tmpy)), 0)),
             int(min(np.ceil(max(tmpy)), gridShape[0] - 1))),
            (int(max(np.floor(min(tmpx)), 0)),
             int(min(np.ceil(max(tmpx)), gridShape[1] - 1))))
    (ygrid, xgrid) = np.meshgrid(np.arange(bbox[0][0], bbox[0][1] + 1),
                                 np.arange(bbox[1][0], bbox[1][1] + 1))
    gridPoints = zip(xgrid.flat, ygrid.flat)

    if len(gridPoints) == 0 :
        print("Bad situation...:", bbox, gridShape, min(tmpy), max(tmpy), \
                                                    min(tmpx), max(tmpx))
        gridPoints = np.zeros((0, 2), dtype='i')

    # Determines which points fall within the resolution volume.  These
    # points will be the ones that will be assigned the value of the
    # original data point that the resolution volume represents.
    goodPoints = points_inside_poly(gridPoints, resVol)

    return (ygrid.flat[goodPoints], xgrid.flat[goodPoints])


def point_inside_polygon(pnts, poly):
    n = len(poly)
    pnts = np.asanyarray(pnts)
    inside = np.zeros(pnts.shape[0], dtype=bool)

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]

        locs = ((pnts[:, 1] > min(p1y,p2y)) &
                (pnts[:, 1] <= max(p1y, p2y)) &
                (pnts[:, 0] <= max(p1x, p2x)) &
                ((p1x == p2x) | (pnts[:, 0] <= ((pnts[:, 1] - p1y)*(p2x-p1x)/(p2y-p1y)+p1x))))
        inside[locs] = ~inside[locs]
        p1x,p1y = p2x,p2y
    return inside

