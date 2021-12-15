import pandas as pd

from src.Utilities.IOHelper import getRootPath

filePath=getRootPath(None).joinpath('test').joinpath('test_DateTimeHelper').joinpath('data')

def test_datetime_unifier_1():
    from src.Utilities.DateTimeHelper import datetime_unifier_1
    df = pd.read_csv(filePath.joinpath('USDJPY_processed_full_event.csv'))
    assert df['trans_release_time'].dtype == 'object'

    df['trans_release_time'] = datetime_unifier_1(df['trans_release_time'])
    assert not df['trans_release_time'].dtype == 'object'
    assert df['trans_release_time'].dtype == 'datetime64[ns]'
