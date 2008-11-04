"""This module provides a conversion layer for data types passed to/from
   Geoprocessing tasks on an ArcGIS REST server."""

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise ImportError("Please install the simplejson module "\
                          "from http://www.undefined.org/python/ "\
                          "or use arcrest with Python 2.6")

import datetime

class GPBaseType(object):
    """Base type for Geoprocessing argument types"""
    def __str__(self):
        return json.dumps(self._json_struct)
    @property
    def _json_struct(self):
        return None

class GPSimpleType(GPBaseType):
    """For geoprocessing types that simplify to base Python types, such as 
       int, bool, or string."""
    __conversion__ = None
    def __init__(self, val):
        self.value = val
    @property
    def _json_struct(self):
        return self.__conversion__(self.value)

class GPBoolean(GPSimpleType):
    """Represents a geoprocessing boolean parameter"""
    __conversion__ = bool

class GPDouble(GPSimpleType):
    """Represents a geoprocessing double parameter"""
    __conversion__ = float

class GPLong(GPSimpleType):
    """Represents a geoprocessing long parameter"""
    __conversion__ = long

class GPString(GPSimpleType):
    """Represents a geoprocessing long parameter"""
    __conversion__ = str

class GPLinearUnit(GPBaseType):
    """Represents a geoprocessing linear unit parameter"""
    allowed_units = set(['esriCentimeters',
                         'esriDecimalDegrees',
                         'esriDecimeters',
                         'esriFeet',
                         'esriInches',
                         'esriKilometers',
                         'esriMeters',
                         'esriMiles',
                         'esriMillimeters',
                         'esriNauticalMiles',
                         'esriPoints',
                         'esriUnknownUnits',
                         'esriYards'])
    def __init__(self, value, unit=None):
        if isinstance(value, (list, tuple)) and len(value) == 2:
            value, unit = value
        value = float(value)
        # Default to meters? Maybe take this out.
        if unit is None:
            unit = 'esriMeters'
        else:
            assert unit in self.allowed_units, "Unit %r not valid" % unit
        self.distance, self.units = value, units
    @property
    def _json_struct(self):
        return {'distance': self.distance, 'units': self.units}

class GPFeatureRecordSetLayer(GPBaseType):
    """Represents a geoprocessing feature recordset parameter"""
    pass

class GPRecordSet(GPBaseType):
    """Represents a geoprocessing recordset parameter"""
    pass

class GPDate(GPBaseType):
    """Represents a geoprocessing date parameter. The format parameter
       in the object constructor varies from the REST API's format parameters
       in that each date field in the format string must be preceded by a
       percent sign, as in the strftime function. For further information
       about Python strftime format strings, please refer to
       http://docs.python.org/library/time.html#time.strftime"""
    def __init__(self, date, format="%Y-%m-%d"):
        if isinstance(date, basestring):
            self.date = datetime.strptime(date, format)
        elif isinstance(date, (datetime.date, datetime.datetime)):
            self.date = date
        else:
            raise ValueError("Cannot convert %r to a date" % date)
    def _json_struct(self):
        return {'date': self.date.strftime(self.format),
                'format': self.format.replace('%', '')}

class GPDataFile(GPBaseType):
    """A URL for a geoprocessing data file parameter"""
    #: The URL of the data file
    url = ''
    def __init__(self, url):
        self.url = url
    def _json_struct(self):
        return {'url': self.url}

class GPUrlWithFormatType(GPBaseType):
    """A class for representing Raster data and Raster layers -- both have a 
       URL and a Format attribute."""
    #: The URL of the resource
    url = ''
    #: The data format of the raster: jpeg, png, etc.
    format = ''
    def __init__(self, url, format):
        self.url, self.format = url, format
    @property
    def _json_struct(self):
        return {'url': self.url, 'format': self.format}

class GPRasterData(GPUrlWithFormatType):
    """A URL for a geoprocessing raster data file parameter, with format."""

class GPRasterLayer(GPUrlWithFormatType):
    """A URL for a geoprocessing raster data layer file parameter,
       with format."""