# Python实用宝典
# https://pythondict.com

from tasks import get_stock_daily

def delay_stock_data(start_date, end_date):
    """
    获得A股所有股票日线行情数据

    Args:
        start_date (str): 起始日
        end_date (str): 结束日
    """

    codes = open('./codes.csv', 'r', encoding='utf-8').readlines()

    # 遍历所有股票ID
    for code in codes:
        get_stock_daily.apply_async(
            (start_date, end_date, code), retry=True
        )

delay_stock_data("20180101", "20200725")
