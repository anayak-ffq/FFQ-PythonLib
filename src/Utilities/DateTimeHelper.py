'''
helper class for date times
'''
from datetime import timezone

import pandas as pd


def datetime_unifier_1(data_Series: pd.Series) -> pd.Series:
    """
    unify non-uniform datetime series
    :param data_Series:
    sample input:
    20        2016-01-03T18:15:00Z
    21        2016-01-03T18:15:00Z
    22        2016-01-03T18:15:00Z
    23        2016-01-03T18:15:00Z
    24        2016-01-03T18:15:00Z
                  ...
    289509              1637106600
    289510              1637106600
    289511              1637106600
    289512              1637106600
    289513              1637106600
    Name: release_time, Length: 289490, dtype: object

    :return: Pd.Series
    sample output:
	20       2016-01-03 18:15:00+00:00
	21       2016-01-03 18:15:00+00:00
	22       2016-01-03 18:15:00+00:00
	23       2016-01-03 18:15:00+00:00
	24       2016-01-03 18:15:00+00:00
	                    ...
	289509   2021-11-16 23:50:00+00:00
	289510   2021-11-16 23:50:00+00:00
	289511   2021-11-16 23:50:00+00:00
	289512   2021-11-16 23:50:00+00:00
	289513   2021-11-16 23:50:00+00:00
	Name: release_time, Length: 289490, dtype: datetime64[ns]
    """
    return data_Series \
        .apply(lambda x: pd.Timestamp(float(x), unit='s', tz=timezone.utc) if x.replace('.', '', 1).isdigit() else pd.Timestamp(x, tz=timezone.utc)) \
        .dt \
        .tz_convert(None)


def resample_mean(df: pd.DataFrame, Column: str, freq: str = '1H') -> pd.DataFrame:
    """
    :param df:
    :param Column:
    :param freq:
    :return:
    """
    return df.groupby(df[Column].floor(freq)).mean()
