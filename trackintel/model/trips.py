import pandas as pd
import trackintel as ti

import trackintel.visualization.staypoints


@pd.api.extensions.register_dataframe_accessor("as_trips")
class TripsAccessor(object):
    """A pandas accessor to treat (Geo)DataFrames as collections of trips. This
    will define certain methods and accessors, as well as make sure that the DataFrame
    adheres to some requirements.

    Requires at least the following columns: 
    ``['user_id', 'started_at', 'finished_at', 'origin_staypoint_id', 'destination_staypoint_id']``

    For several usecases, the following additional columns are required:
    ``['context']``

    Examples
    --------
    >>> df.as_trips.plot()
    """

    required_columns = ['user_id', 'started_at', 'finished_at', 'origin_staypoint_id', 'destination_staypoint_id']

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        if any([c not in obj.columns for c in TripsAccessor.required_columns]):
            raise AttributeError("To process a DataFrame as a collection of staypoints, " \
                + "it must have the properties [%s], but it has [%s]." \
                % (', '.join(TripsAccessor.required_columns), ', '.join(obj.columns)))

    def plot(self, *args, **kwargs):
        """Plots this collection of trips. 
        See :func:`trackintel.visualization.trips.plot_trips`."""
        raise NotImplementedError

    def to_csv(self, filename, *args, **kwargs):
        """Stores this collection of trips as a CSV file.
        See :func:`trackintel.io.file.write_trips_csv`."""
        ti.io.file.write_trips_csv(self._obj, filename, *args, **kwargs)

    def to_postgis(self, conn_string, table_name, schema=None,
            sql_chunksize=None, if_exists='replace'):
        """Stores this collection of trips to PostGIS.
        See :func:`trackintel.io.postgis.write_trips_postgis`."""
        ti.io.postgis.write_trips_postgis(self._obj, conn_string, table_name, 
            schema, sql_chunksize, if_exists)
