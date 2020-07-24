# Python实用宝典
# https://pythondict.com

import pymongo
import time
import json
import tushare as ts
from celery import Celery

# 设置BROKER
BROKER_URL = 'mongodb://127.0.0.1:27017/celery'

# 新建celery任务
app = Celery('my_task', broker=BROKER_URL)

# 建立mongodb连接
client = pymongo.MongoClient(host='localhost', port=27017)

# 连接stock数据库，注意只有往数据库中插入了数据，数据库才会自动创建
stock_db = client.stock

# 创建一个daily集合，类似于MySQL中“表”的概念
daily = stock_db["daily"]

# tushare
pro = ts.pro_api(token="你的Tushare Token")

@app.task
def get_stock_daily(start_date, end_date, code):
    """
    Celery任务：获得某股票的日线行情数据

    Args:
        start_date (str): 起始日
        end_date (str): 结束日
        code (str): 股票代码
    """


    # 请求tushare数据，并转化为json格式
    try:
        df = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
    except Exception as e:
        # 触发普通用户CPS限制，60秒后重试
        print(e)
        get_stock_daily.retry(countdown=60)

    data = json.loads(df.T.to_json()).values()

    # 对股票每一天数据进行保存，注意唯一性
    # 这里也可以批量创建，速度更快，但批量创建容易丢失数据
    # 这里为了保证数据的绝对稳定性，选择一条条创建
    for row in data:
        daily.update({"_id": f"{row['ts_code']}-{row['trade_date']}"}, row, upsert=True)

    print(f"{code}: 插入\更新 完毕 - {start_date} to {end_date}")
