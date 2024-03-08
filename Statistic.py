import pandas as pd
from DataImport import load_data
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'FangSong'  # 设置字体为仿宋
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示汉字
plt.rcParams['font.size'] = 10  # 设置字体的大小为10
plt.rcParams['axes.unicode_minus'] = False  # 显示正、负的问题
print(plt.style.available)


# plt.style.use("seaborn")

def convert_datetime_to_datetime_obj(datetime_str):
    """
    :param datetime_str: 日期字符串
    :return: pd日期对象
    """
    return pd.to_datetime(datetime_str)


"""
   :param data:  输入数据（必选）
   :param time_range: 时间范围（可选）
   :param time_granularity: 颗粒度（必选，大于1min）
   :param kwargs: 条件（可选参数）
   :return: 时间范围内以颗粒度为单位的车流量分箱统计信息
   """


# 统计功能需求1:时间范围内条件下分箱统计
def statistic(data, time_range=None, time_granularity=1, selected_atr=[], condition_dict={}):
    grouped_reference = ['时间段']

    # 如果列名存在于data中，则加入
    for i in selected_atr:
        if i in data.columns:
            grouped_reference.extend(selected_atr)  # 将选定的属性添加到分组参考列中
        else:
            print(f"列名{i}无效")
    # 对 condition_dict 进行筛选
    for key, value in condition_dict.items():
        if key not in data.columns:
            raise ValueError(f"列名{key}无效")
        # 通过列的取值过滤数据
        data = data[data[key].isin(value)]



    if time_range:
        start_time, end_time = map(convert_datetime_to_datetime_obj, time_range)
        print(start_time, end_time)
        data['经过时间'] = pd.to_datetime(data['经过时间'])
        data = data[(data['经过时间'] >= start_time) & (data['经过时间'] <= end_time)]

    if time_granularity < 1:
        raise ValueError("时间粒度必须大于等于1分钟")

    data.loc[:, '时间段'] = data['经过时间'].dt.strftime('%Y-%m-%d %H:%M')
    data['时间段'] = pd.to_datetime(data['时间段']).dt.round(f'{time_granularity}min').dt.strftime('%Y-%m-%d %H:%M')

    grouped_data = data.groupby(grouped_reference).agg({
        '脱敏车牌编号': 'count',
        '车速(km/h)': 'mean'
    }).reset_index()

    grouped_data = grouped_data.rename(columns={'脱敏车牌编号': '小时过车数量', '车速(km/h)': '平均车速'})
    print(grouped_reference)
    print(grouped_data)
    if len(grouped_reference) == 1:
        grouped_data.plot(x="时间段", y="小时过车数量", kind="line")
        xticks_labels = [time.split(' ')[1] for time in grouped_data['时间段']]
        plt.xticks(range(len(grouped_data)), xticks_labels, rotation=45)  # 应用xticks参数并进行适当的旋转
        plt.show()
    elif len(grouped_reference) == 2:
        # 使用seaborn绘制条形图
        sns.barplot(data=grouped_data, x='时间段', y='小时过车数量', hue='车辆类型')
        xticks_labels = [time.split(' ')[1] for time in grouped_data['时间段']]
        plt.xticks(range(len(grouped_data)), xticks_labels, rotation=45)
    plt.show()

    return grouped_data


# 统计功能需求2:绘制如在车牌种类、车牌颜色、采集设备或无条件关于车流量的时间函数统计


if __name__ == "__main__":
    data = load_data()
    time_range = ['2024-03-06 06:00', '2024-03-06 09:00']
    selected_columns = ["车辆类型"]  # 选定的属性列表
    conditions = {"号牌颜色": ["红色", "蓝色"]}  # 条件字典
    filtered_data = statistic(data, time_range=time_range, time_granularity=15, selected_atr=selected_columns, condition_dict=conditions)
    print(filtered_data)
