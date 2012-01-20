"""
All of the loading functions will load the data into (theta, r) coordinates
They will also produce coordinate data that will be parallel to the data array.
In other words, you will have three 2-D arrays: data, range gate [Meters], azimuth [DEGREES north]
"""

import numpy as np
import datetime
from scipy.io import netcdf

class WDSSII_Error(Exception) : 
    def __init__(self, typeName) :
        self.badType = typeName

    def __repr__(self) :
        return self.__str__()

    def __str__(self) :
        return "Unknown WDSSII PAR datatype %s" % (self.badType)


def LoadPAR_wdssii(filename) :
    """
    This loader will retreive the radar moments data obtained
    from the wdssii.arrc.nor.ouint computer

    Returns a dictionary with the following keys:
        'vals'
        'azimuth'       [degrees North]
        'range_gate'    [m]
        'elev_angle'    [degrees]
        'stat_lat'
        'stat_lon'
        'scan_time'
        'var_name'
        'gate_length'   [m]
        'beam_width'    [degrees]
    """
    nc = netcdf.netcdf_file(filename, 'r')

    varName = nc.TypeName
    
    azimuths = nc.variables['Azimuth'][:]
    gateWidths = nc.variables['GateWidth'][:]
    beamWidths = nc.variables['BeamWidth'][:]

    missingData = nc.MissingData
    rangeFolded = nc.RangeFolded

    elevAngle = nc.Elevation
    statLat = nc.Latitude
    statLon = nc.Longitude
    scanTime = nc.Time

    parData = None
    aziLen = None
    rangeLen = None

    dataType = nc.DataType

    if (dataType == 'SparseRadialSet') :
        rawParData = nc.variables[varName][:]
        xLoc = nc.variables['pixel_x'][:]
        yLoc = nc.variables['pixel_y'][:]

        aziLen = azimuths.shape[0]
        rangeLen = (yLoc.max() + 1) if len(yLoc) > 0 else 0

        parData = np.empty((aziLen, rangeLen))
        parData.fill(np.nan)
        parData[xLoc, yLoc] = rawParData

    elif (dataType == 'RadialSet') :
        parData = np.array(nc.variables[varName][:])

        (aziLen, rangeLen) = parData.shape

    else :
        raise WDSSII_Error(dataType)

    
    rangeGrid = nc.RangeToFirstGate + (np.arange(rangeLen)[np.newaxis, :] * 
						               gateWidths[:, np.newaxis])
    aziGrid = np.tile(azimuths, (rangeLen, 1)).T

    # TODO: Maybe we should be using masks?
    parData[(parData == missingData) | (parData == rangeFolded)] = np.nan

    nc.close()
    
    return {'vals': parData,
    	    'azimuth': aziGrid, 'range_gate': rangeGrid,
            'elev_angle': elevAngle,
	        'stat_lat': statLat, 'stat_lon': statLon,
	        'scan_time': scanTime, 'var_name': varName,
    	    'gate_length': np.median(gateWidths),
            'beam_width': np.median(beamWidths)}



# TODO: Maybe adjust the code so that a parameterized version of this function can choose
#       which moment(s) to calculate from the data?
def LoadPAR_lipn(filename) :
    """
    This function will load the radar data from a "Level-I Plus" file and produce Reflectivity moments.
    These files were generated by Boon Leng Cheong's program to process PAR data streams.

    Returns a dictionary with the following keys:
        'vals'
        'azimuth'
        'range_gate'
        'elev_angle'
        'stat_lat'
        'stat_lon'
        'scan_time'
        'var_name'
        'gate_length'
        'beam_width'
    """
    nc = netcdf.netcdf_file(filename, 'r')
      
    varName = 'Reflectivity'
    azimuths = nc.variables['Azimuth'][:]
    ranges = nc.variables['Range'][:] * 1000.0    # convert to meters from km

    R0 = nc.variables['R0'][:]
    #R1 = nc.variables['R1_real'][:] + nc.variables['R1_imag'][:] * 1j
    #specWidth = np.sqrt(np.abs(np.log(np.abs(R0./R1)))) 
    #            * np.sign(np.log(np.abs(R0./R1))) 
    #            * (nc.Lambda / (2*np.sqrt(6)*np.pi*nc.PRT))
    noiseThresh = 5.0
    parData = np.where(R0 / nc.NoiseFloor < noiseThresh,
                       np.nan,
                       (10*np.log10(R0 / nc.NoiseFloor) +
                        20*np.log10(ranges[np.newaxis, :] / 1000.0) +
                        nc.SNRdBtodBZ))

    (rangeGrid, aziGrid) = np.meshgrid(ranges, azimuths)

    gateLength = nc.GateSize
      
    elevAngle = nc.Elevation
    statLat = nc.Latitude
    statLon = nc.Longitude
    scanTime = nc.ScanTimeUTC
      
    nc.close()

    return {'vals': parData,
	        'azimuth': aziGrid, 'range_gate': rangeGrid,
            'elev_angle': elevAngle,
	        'stat_lat': statLat, 'stat_lon': statLon,
            'scan_time': scanTime, 'var_name': varName,
	        'gate_length': gateLength,
            'beam_width': 1.0}

def LoadLevel2(filename) :
    """
    This function will load the netcdf export of a Level II radar
    data file.  The netcdf file assumes the "_Coordinates" convention
    with the "ARCHIVE2" format and "RADIAL" cdm_data_type.

    Returns a dictionary with the following keys:
        'vals'
        'azimuth'
        'range_gate'
        'elev_angle'
        'stat_lat'
        'stat_lon'
        'scan_time'
        'var_name'
        'gate_length'
        'beam_width'
    """
    from BRadar.radarsites import ByName

    nc = netcdf.netcdf_file(filename, 'r')

    varName = 'Reflectivity'
    azimuths = nc.variables['azimuthR'][:]      # (scanR, radialR)
    ranges = nc.variables['distanceR'][:]       # (gateR)  already in meters
    elevAngle = nc.variables['elevationR'][:]   # (scanR, radialR)

    # Each scan is a different elevation angle, but elevationR
    # records a higher precision elevation angle for each dwell.
    # We don't need that.
    # elevAngle will be 3-D, (elev, azi, range)
    elevAngle = np.mean(elevAngle, axis=1)[:, np.newaxis, np.newaxis]
    
    aziArgs = np.argsort(azimuths)      # Sort the azimuths for each scan
    # azimuths is 3-D (elev, azi, range)
    azimuths = np.array([azimuths[scan, aziArgs[scan, :]] for
                         scan in range(azimuths.shape[0])])[..., np.newaxis]


    if nc.variables[varName]._Unsigned == 'true' :
        datavals = nc.variables[varName][:].view(dtype=np.uint8)
    else :
        datavals = nc.variables[varName][:]

    varData = ((datavals *
                nc.variables[varName].scale_factor) +
               nc.variables[varName].add_offset)     # (scanR, radialR, gateR)
    #varData = np.where(datavals == nc.variables[varName].missing_value[0]
    #                  |datavals == nc.variables[varName].missing_value[1],
    #                   np.nan, varData) 

    # re-arrange varData that it is 3-D (elev, azi, range)
    varData = np.array([varData[scan, aziArgs[scan, :], :] for
                        scan in range(varData.shape[0])])

    # TODO: Temporary kludge until the station name is fixed in the file.
    from os.path import basename
    siteLoc = ByName(basename(filename)[0:4])

    statLat = siteLoc[0]['LAT']
    statLon = siteLoc[0]['LON']
    gateLength = np.median(np.diff(ranges))
    scanTime = datetime.datetime.strptime(nc.time_coverage_start, "%Y-%m-%dT%H:%M:%SZ")
    # Yes, I know it is spelled wrong, but this is how it is spelled in the metadata...
    beamWidth = nc.HorizonatalBeamWidthInDegrees
    nc.close()

    return {'vals': varData,
            'azimuth': azimuths,
            'range_gate': ranges[np.newaxis, np.newaxis, :],
            'elev_angle': elevAngle,
            'stat_lat': statLat, 'stat_lon': statLon,
            'scan_time': scanTime, 'var_name': varName,
            'gate_length': gateLength,
            'beam_width': beamWidth}

                                         
def SaveRastRadar(filename, rastData, latAxis, lonAxis,
                  scanTime, varName, station) :
    """
    For saving radar data stored in Lat/Lon coordinates.
    """
    nc = netcdf.netcdf_file(filename, 'w')
    
    # Setting Global Attribute
    nc.title = 'Rasterized %s %s %s' % (station, varName, 
                datetime.datetime.utcfromtimestamp(scanTime).strftime('%H:%M:%S UTC %m/%d/%Y'))
    nc.varName = varName
    nc.station = station
    
    # Setting the dimensions
    nc.createDimension('lat', len(latAxis))
    nc.createDimension('lon', len(lonAxis))
    nc.createDimension('time', 1)
    
    # Setting the variables
    valueVar = nc.createVariable('value', 'f', ('time', 'lat', 'lon'))
    valueVar.long_name = 'Rasterized ' + varName
    valueVar[:] = rastData.reshape((1, len(latAxis), len(lonAxis)))
    
    latVar = nc.createVariable('lat', 'f', ('lat',))
    latVar.units = 'degrees_north'
    latVar.spacing = np.diff(latAxis).mean()
    latVar[:] = latAxis
    
    lonVar = nc.createVariable('lon', 'f', ('lon',))
    lonVar.units = 'degrees_east'
    lonVar.spacing = np.diff(lonAxis).mean()
    lonVar[:] = lonAxis
    
    timeVar = nc.createVariable('time', 'i', ('time',))
    timeVar.units = 'seconds since 1970-1-1'
    timeVar.assignValue(scanTime)
    
    nc.close()


def LoadRastRadar(infilename, force_int=False) :
    """
    Load a netcdf file produced by :func:`SaveRastRadar` or
    by the NCEP Radar Data Viewer that contains rasterized
    radar data.

    *infilename*    The file name, of course.

    *force_int*     For computers with limited memory,
                    forcing the radar data into integer rather
                    than floats may be very helpful.

    Returns a dictionary of info:
        "title"
        "lats"
        "lons"
        "vals"
        "scan_time"
        "var_name"  -- might not be very useful...
        "station"
    """
    nc = netcdf.netcdf_file(infilename, 'r')

    # Correction for older rasterized files that used the wrong term.
    titleStr = (nc.title).replace("Rastified", "Rasterized")
    try :
        varName = nc.varName
    except :
        varName = 'Reflectivity'

    if varName not in nc.variables :
        # Fall back to "value"
        varName = 'value'

    try :
        station = nc.station
    except :
        station = "NWRT"

    lats = nc.variables['lat'][:]
    lons = nc.variables['lon'][:]
    vals = nc.variables[varName][:]

    if force_int :
        vals = vals.astype('i')

    timestamp = nc.variables['time'][0]

    nc.close()

    return {'title': titleStr, 'lats': lats, 'lons': lons,
            'vals': vals, 'scan_time': timestamp,
            'var_name': varName, 'station': station}

class RadarCache(object) :
    def __init__(self, files, cachewidth=3, load_func=None) :
        """
        Initialize a rolling caching reversible iterator object.

        Each iteration returns the radar data loaded from the files.
        If it is within the cache, then the data is loaded from memory.
        If it is not within the cache, then load the data from the file.

        *files*         list of strings
            List of filenames containing radar data.

        *cachewidth*    integer
            Width of the rolling cache. Must be greater than one.

        *load_func*     method
            Function that takes a filename string and returns a radar
            data dictionary.  If None, then default to
            :func:`LoadRastRadar`.
        """
        if cachewidth < 2 :
            raise ValueError("cachewidth must be greater than 1")

        self._filenames = files
        self._cachewidth = cachewidth
        self._startIndex = 0
        self._endIndex = 0
        self._currIndex = 0
        self._load_func = (load_func if load_func is not None else
                           LoadRastRadar)

        self._cacheIndex = 0
        self._cacher = []

    def _get_filename(self) :
        return self._filenames[self._currIndex]

    name = property(_get_filename, None, None, "Filename of current data")

    def __iter__(self) :
        return self

    def curr(self, lookahead=0) :
        self._check_cache_state(lookahead)
        return self._cacher[self._cacheIndex + lookahead]

    def _check_cache_state(self, lookahead=0) :
        """
        advance or step back the cache if needed, and adjust the index
        """
        filename = self._filenames[self._currIndex + lookahead]
        # are we on the right edge of the cache?
        if (self._cacheIndex + lookahead) >= len(self._cacher) :
            # is the cache at the maximum size?
            if len(self._cacher) >= self._cachewidth :
                self._cacher.pop(0)
                self._cacheIndex -= 1

            # add an item to the right edge of the cache
            self._cacher.append(self._load_func(filename))

        # are we on the left edge of the cache?
        elif (self._cacheIndex + lookahead) < 0 :
            # is the cache at the maximum size?
            if len(self._cacher) >= self._cachewidth :
                self._cacher.pop()

            # add an item to the left edge of the cache
            self._cacher.insert(0, self._load_func(filename))
            self._cacheIndex += 1

    def next(self) :
        if self._currIndex >= (len(self) - 1) :
            raise StopIteration

        self._currIndex += 1
        self._cacheIndex += 1
        return self.curr()

    def peek_next(self) :
        """
        Advance cache only if you absolutely have to.

        If there is nothing next, then return None.
        """
        if self._currIndex >= (len(self) - 1) :
            return None

        return self.curr(1)

    def prev(self) :
        if self._currIndex <= 0 :
            raise StopIteration

        self._currIndex -= 1
        self._cacheIndex -= 1
        return self.curr()

    def peek_prev(self) :
        """
        Step back the cache only if you absolutely have to.

        If there is nothing previous, then return None.
        """
        if self._currIndex <= 0 :
            return None

        return self.curr(-1)

    def __len__(self) :
        return len(self._filenames)

