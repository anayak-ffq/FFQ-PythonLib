import pandas as pd

from src.Utilities.IOHelper import getRootPath

filePath = getRootPath(None).joinpath('test').joinpath('test_DateTimeHelper').joinpath('data')


def test_datetime_unifier_1():
    from src.Utilities.DateTimeHelper import datetime_unifier_1
    df = pd.read_csv(filePath.joinpath('USDJPY_processed_full_event.csv'))
    assert df['trans_release_time'].dtype == 'object'

    df['trans_release_time'] = datetime_unifier_1(df['trans_release_time'])
    assert not df['trans_release_time'].dtype == 'object'
    assert df['trans_release_time'].dtype == 'datetime64[ns]'


def test_resample_mean():
    from src.Utilities.DateTimeHelper import resample_mean
    freq = '1T'
    Column = 'impact'
    df = pd.read_csv(filePath.joinpath('USDJPY_processed_full_event.csv'),
                     parse_dates=["trans_release_time"], index_col=["trans_release_time"])
    resampled_col = resample_mean(df, Column, freq)
    assert resampled_col.shape[0] == df.index.floor(freq).unique().shape[0], "resampled periods must be consistent"
    assert resampled_col.dtype == df[Column].dtype, "datatype must be same"
