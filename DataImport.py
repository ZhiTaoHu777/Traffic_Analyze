import pandas as pd



def load_data():
    """
    :return: data的pandas对象
    """
    file_path = "Data/decrypt_data2.csv"
    df = pd.read_csv(file_path,sep=",",encoding="GBK")
    print(df)
    return df



