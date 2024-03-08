import pandas as pd

from DataImport import load_data


def convert_datetime_to_datetime_obj(datetime_str):
    return pd.to_datetime(datetime_str)


def statistic(data, time_range=None, time_granularity=1, **kwargs):
    if not isinstance(data, pd.DataFrame):
        raise ValueError("输入数据不是有效的pandas DataFrame")

    for key, value in kwargs.items():
        if key not in data.columns:
            raise ValueError(f"列名{key}无效")
        if not all(val in data[key].unique() for val in value):
            raise ValueError(f"取值{value}无效")
        data = data[data[key].isin(value)]

    if time_range:
        start_time, end_time = map(convert_datetime_to_datetime_obj, time_range)
        data['经过时间'] = pd.to_datetime(data['经过时间'])
        data = data[(data['经过时间'] >= start_time) & (data['经过时间'] <= end_time)]

    if time_granularity < 1:
        raise ValueError("时间粒度必须大于等于1分钟")

    data['时间段'] = data['经过时间'].dt.strftime('%Y-%m-%d %H:%M')
    data['时间段'] = pd.to_datetime(data['时间段']).dt.round(f'{time_granularity}min').dt.strftime('%Y-%m-%d %H:%M')

    grouped_data = data.groupby(['时间段', '号牌种类', '号牌颜色', '采集设备', '车辆类型']).agg({
        '脱敏车牌编号': 'count',
        '车速(km/h)': 'mean'
    }).reset_index()

    grouped_data = grouped_data.rename(columns={'脱敏车牌编号': '小时过车数量', '车速(km/h)': '平均车速'})

    return grouped_data


if __name__ == "__main__":
    data = load_data()
    time_range = ['2024-03-06 06:00', '2024-03-06 08:00']
    filtered_data = statistic(data, time_range=time_range, time_granularity=15, 号牌种类=['小型汽车'],
                              采集设备=['高速K164+750M方向1'])
    print(filtered_data)
