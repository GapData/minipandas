from pandas.core.frame import DataFrame

def test_creation():
    dic = {"id":[1,2,3]}
    df = DataFrame(dic)
    print("Our first DataFrame", df)
    assert isinstance(df, DataFrame)

if __name__ == '__main__':
    test_creation()