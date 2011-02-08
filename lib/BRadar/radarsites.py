"""
This module contains radar site information in the Sites list.
Filtering of the sites can be done by using the ByType() and ByName()
functions.

Author: Ben Root
Copyright: Public Domain
"""

def ByType(siteTypes, sites):
    """
    Returns the radarSites list with only the sites
    whose TYPE matches one of the given 'siteTypes'. Not giving
    a list of radarSites for 'sites' results in using the original list.

    SEE ALSO: ByName()

    EXAMPLE:

    import radarsites as radar
    wsrSites = radar.ByType(['WSR-88D'], radar.Sites)

    researchSites = radar.ByType(['2POL', 'CASA', 'NWRT'], radar.Sites)
    """
    return [rec for rec in sites if rec['TYPE'] in siteTypes]

def ByName(siteNames, sites):
    """
    Returns the radarSites list with only the sites
    whose sitename matches one of the given 'siteNames'. Not giving
    a list of radarSites for 'sites' results in using the original list.

    SEE ALSO: ByType()

    EXAMPLE:

    import radarsites as radar
    wsrSites = radar.ByName(['KTLX', 'KINX', 'KCYS'], radar.Sites)

    researchSites = radar.ByType(['2POL', 'CASA', 'NWRT'], radar.Sites)
    others = radar.ByName(['KLWE', 'KSAO', 'KRSP'], researchSites)
    """

    return [rec for rec in sites if rec['SITE'] in siteNames]

def Matricized(sites):
    return {'SITE': [rec['SITE'] for rec in sites], 'LAT': [rec['LAT'] for rec in sites], 
	    'LON': [rec['LON'] for rec in sites], 'TYPE': [rec['TYPE'] for rec in sites]}

def AllNames(sites):
    return [rec['SITE'] for rec in sites]

def AllTypes(sites):
    return list(set([rec['TYPE'] for rec in sites]))


Sites = [{'SITE': 'KTLX', 'LAT':   35.3341000, 'LON':  -97.2778000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KFDR', 'LAT':   34.3624000, 'LON':  -98.9750000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KINX', 'LAT':   36.1754000, 'LON':  -95.5640000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KVNX', 'LAT':   36.7412000, 'LON':  -98.1279000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KBMX', 'LAT':   33.1720000, 'LON':  -86.7700000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KEOX', 'LAT':   31.4600000, 'LON':  -85.4590000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KHTX', 'LAT':   34.9310000, 'LON':  -86.0840000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KMXX', 'LAT':   32.5372000, 'LON':  -85.7900000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KMOB', 'LAT':   30.6790000, 'LON':  -88.2400000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KFSX', 'LAT':   34.5740000, 'LON': -111.1971000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KIWA', 'LAT':   33.2890000, 'LON': -111.6700000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KEMX', 'LAT':   31.8940000, 'LON': -110.6300000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KYUX', 'LAT':   32.4949000, 'LON': -114.6560000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KSRX', 'LAT':   35.2910000, 'LON':  -94.3620000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KLZK', 'LAT':   34.8360000, 'LON':  -92.2621000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KBBX', 'LAT':   39.4963000, 'LON': -121.6320000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KEYX', 'LAT':   35.0980000, 'LON': -117.5609000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KBHX', 'LAT':   40.4990000, 'LON': -124.2910000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KVTX', 'LAT':   34.4120000, 'LON': -119.1791000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KDAX', 'LAT':   38.5010000, 'LON': -121.6770000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KNKX', 'LAT':   32.9190000, 'LON': -117.0411000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KMUX', 'LAT':   37.1550000, 'LON': -121.8970000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KHNX', 'LAT':   36.3140000, 'LON': -119.6310000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KSOX', 'LAT':   33.8180000, 'LON': -117.6359000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KVBX', 'LAT':   34.8391000, 'LON': -120.3981000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KFTG', 'LAT':   39.7860000, 'LON': -104.5450000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KGJX', 'LAT':   39.0620000, 'LON': -108.2140000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KPUX', 'LAT':   38.4600000, 'LON': -104.1809000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KDOX', 'LAT':   38.8260000, 'LON':  -75.4400000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KJAX', 'LAT':   30.4851000, 'LON':  -81.7020000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KBYX', 'LAT':   24.5970000, 'LON':  -81.7030000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KMLB', 'LAT':   28.1129000, 'LON':  -80.6541000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KAMX', 'LAT':   25.6111000, 'LON':  -80.4131000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KEVX', 'LAT':   30.5651000, 'LON':  -85.9220000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KTLH', 'LAT':   30.3980000, 'LON':  -84.3289000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KTBW', 'LAT':   27.7049000, 'LON':  -82.4020000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KFFC', 'LAT':   33.3630000, 'LON':  -84.5659000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KVAX', 'LAT':   30.8900000, 'LON':  -83.0019000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KJGX', 'LAT':   32.6749000, 'LON':  -83.3510000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KCBX', 'LAT':   43.4900000, 'LON': -116.2359000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KSFX', 'LAT':   43.1060000, 'LON': -112.6859000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KLOT', 'LAT':   41.6040000, 'LON':  -88.0850000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KILX', 'LAT':   40.1500000, 'LON':  -89.3371000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KVWX', 'LAT':   38.2600000, 'LON':  -87.7241000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KIND', 'LAT':   39.7080000, 'LON':  -86.2800000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KIWX', 'LAT':   41.3591000, 'LON':  -85.7001000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KDMX', 'LAT':   41.7310000, 'LON':  -93.7230000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KDVN', 'LAT':   41.6121000, 'LON':  -90.5810000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KDDC', 'LAT':   37.7610000, 'LON':  -99.9690000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KGLD', 'LAT':   39.3671000, 'LON': -101.7000000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KTWX', 'LAT':   38.9970000, 'LON':  -96.2320000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KICT', 'LAT':   37.6540000, 'LON':  -97.4431000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KHPX', 'LAT':   36.7370000, 'LON':  -87.2850000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KJKL', 'LAT':   37.5910000, 'LON':  -83.3130000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KLVX', 'LAT':   37.9749000, 'LON':  -85.9441000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KPAH', 'LAT':   37.0681000, 'LON':  -88.7720000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KPOE', 'LAT':   31.1550000, 'LON':  -92.9759000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KLCH', 'LAT':   30.1249000, 'LON':  -93.2161000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KLIX', 'LAT':   30.3371000, 'LON':  -89.8250000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KSHV', 'LAT':   32.4510000, 'LON':  -93.8410000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KCBW', 'LAT':   46.0390000, 'LON':  -67.8070000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KGYX', 'LAT':   43.8910000, 'LON':  -70.2570000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KBOX', 'LAT':   41.9560000, 'LON':  -71.1380000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KAPX', 'LAT':   44.9060000, 'LON':  -84.7200000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KDTX', 'LAT':   42.6999000, 'LON':  -83.4720000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KGRR', 'LAT':   42.8940000, 'LON':  -85.5449000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KMQT', 'LAT':   46.5310000, 'LON':  -87.5480000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KDLH', 'LAT':   46.8370000, 'LON':  -92.2100000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KMPX', 'LAT':   44.8490000, 'LON':  -93.5649000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KGWX', 'LAT':   33.8969000, 'LON':  -88.3290000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KDGX', 'LAT':   32.2800000, 'LON':  -89.9840000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KEAX', 'LAT':   38.8104000, 'LON':  -94.2480000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KSGF', 'LAT':   37.2351000, 'LON':  -93.4000000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KLSX', 'LAT':   38.6990000, 'LON':  -90.6829000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KBLX', 'LAT':   45.8540000, 'LON': -108.6070000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KGGW', 'LAT':   48.2060000, 'LON': -106.6250000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KTFX', 'LAT':   47.4599000, 'LON': -111.3849000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KMSX', 'LAT':   47.0410000, 'LON': -113.9859000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KUEX', 'LAT':   40.3210000, 'LON':  -98.4421000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KLNX', 'LAT':   41.9580000, 'LON': -100.5759000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KOAX', 'LAT':   41.3199000, 'LON':  -96.3661000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KLRX', 'LAT':   40.7401000, 'LON': -116.8030000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KESX', 'LAT':   35.7010000, 'LON': -114.8910000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KRGX', 'LAT':   39.7540000, 'LON': -119.4610000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KABX', 'LAT':   35.1501000, 'LON': -106.8240000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KFDX', 'LAT':   34.6354000, 'LON': -103.6303000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KHDX', 'LAT':   33.0768000, 'LON': -106.1229000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KENX', 'LAT':   42.5859000, 'LON':  -74.0639000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KBGM', 'LAT':   42.2010000, 'LON':  -75.9850000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KBUF', 'LAT':   42.9490000, 'LON':  -78.7370000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KTYX', 'LAT':   43.7560000, 'LON':  -75.6800000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KOKX', 'LAT':   40.8660000, 'LON':  -72.8641000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KMHX', 'LAT':   34.7760000, 'LON':  -76.8760000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KRAX', 'LAT':   35.6649000, 'LON':  -78.4900000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KLTX', 'LAT':   33.9890000, 'LON':  -78.4290000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KBIS', 'LAT':   46.7710000, 'LON': -100.7601000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KMVX', 'LAT':   47.5280000, 'LON':  -97.3251000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KMBX', 'LAT':   48.3930000, 'LON': -100.8689000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KCLE', 'LAT':   41.4130000, 'LON':  -81.8600000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KILN', 'LAT':   39.4199000, 'LON':  -83.8220000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KMAX', 'LAT':   42.0810000, 'LON': -122.7161000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KPDT', 'LAT':   45.6910000, 'LON': -118.8519000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KRTX', 'LAT':   45.7151000, 'LON': -122.9639000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KDIX', 'LAT':   39.9470000, 'LON':  -74.4110000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KPBZ', 'LAT':   40.5310000, 'LON':  -80.2179000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KCCX', 'LAT':   40.9230000, 'LON':  -78.0041000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KCLX', 'LAT':   32.6550000, 'LON':  -81.0420000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KCAE', 'LAT':   33.9490000, 'LON':  -81.1190000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KGSP', 'LAT':   34.8829000, 'LON':  -82.2200000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KABR', 'LAT':   45.4560000, 'LON':  -98.4129000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KUDX', 'LAT':   44.1250000, 'LON': -102.8300000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KFSD', 'LAT':   43.5880000, 'LON':  -96.7291000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KMRX', 'LAT':   36.1680000, 'LON':  -83.4020000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KNQA', 'LAT':   35.3451000, 'LON':  -89.8730000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KOHX', 'LAT':   36.2470000, 'LON':  -86.5629000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KAMA', 'LAT':   35.2332000, 'LON': -101.7091000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KBRO', 'LAT':   25.9161000, 'LON':  -97.4190000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KCRP', 'LAT':   27.7830000, 'LON':  -97.5109000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KFWS', 'LAT':   32.5730000, 'LON':  -97.3030000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KGRK', 'LAT':   30.7222000, 'LON':  -97.3830000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KDYX', 'LAT':   32.5379000, 'LON':  -99.2540000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KEPZ', 'LAT':   31.8730000, 'LON': -106.6980000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KHGX', 'LAT':   29.4720000, 'LON':  -95.0791000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KDFX', 'LAT':   29.2724000, 'LON': -100.2801000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KLBB', 'LAT':   33.6540000, 'LON': -101.8141000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KMAF', 'LAT':   31.9429000, 'LON': -102.1891000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KSJT', 'LAT':   31.3710000, 'LON': -100.4919000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KEWX', 'LAT':   29.7040000, 'LON':  -98.0290000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KICX', 'LAT':   37.5910000, 'LON': -112.8620000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KMTX', 'LAT':   41.2630000, 'LON': -112.4480000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KCXX', 'LAT':   44.5111000, 'LON':  -73.1659000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KAKQ', 'LAT':   36.9840000, 'LON':  -77.0079000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KFCX', 'LAT':   37.0240000, 'LON':  -80.2741000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KLWX', 'LAT':   38.9749000, 'LON':  -77.4780000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KATX', 'LAT':   48.1950000, 'LON': -122.4940000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KOTX', 'LAT':   47.6810000, 'LON': -117.6260000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KRLX', 'LAT':   38.3110000, 'LON':  -81.7229000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KGRB', 'LAT':   44.4990000, 'LON':  -88.1111000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KARX', 'LAT':   43.8230000, 'LON':  -91.1909000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KMKX', 'LAT':   42.9680000, 'LON':  -88.5509000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KCYS', 'LAT':   41.1520000, 'LON': -104.8059000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KRIW', 'LAT':   43.0660000, 'LON': -108.4770000, 'TYPE': 'WSR-88D'} ,
{'SITE': 'KOUN', 'LAT':   35.2362080, 'LON':  -97.4631610, 'TYPE': '2POL'} ,
{'SITE': 'PAR', 'LAT':   35.2362080, 'LON':  -97.4631610, 'TYPE': 'NWRT'} ,
{'SITE': 'KCYR', 'LAT':   34.8739100, 'LON':  -98.2521400, 'TYPE': 'CASA'} ,
{'SITE': 'KLWE', 'LAT':   34.6238100, 'LON':  -98.2720100, 'TYPE': 'CASA'} ,
{'SITE': 'KRSP', 'LAT':   34.8128600, 'LON':  -98.9312900, 'TYPE': 'CASA'} ,
{'SITE': 'KSAO', 'LAT':   35.0312230, 'LON':  -97.9566900, 'TYPE': 'CASA'} ]
