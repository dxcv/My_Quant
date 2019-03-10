# encoding = utf-8
def addMaxMinData(df_origin, days):

    """
    原始数据可能要用到high、low和close信息
    :param df_origin:
    :param days:
    :return:
    """
    df = df_origin

    df['Max'+str(days)] = df['close'].rolling(window=days, center=False).max()
    df['Min' + str(days)] = df['close'].rolling(window=days, center=False).min()

    return df
