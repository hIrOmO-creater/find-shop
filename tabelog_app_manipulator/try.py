#正規化する関数
#入力値: 「項目」ごとのデータセット
#出力値: 「項目」ごとに標準化されたデータセット
import pandas as pd

def add_normalized_column_from_csv(csv_file, column_name, new_column_name):
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file)

    # 指定された列のデータを取り出す
    data = df[column_name]

    # min-maxスケーリングを適用する
    normalized_data = (data - data.min()) / (data.max() - data.min())

    # 正規化されたデータを新しいデータフレームとして作成
    df[new_column_name] = normalized_data

    return df

# 使用例
csv_file = 'data.csv'  # CSVファイルのパス
column_name = 'target_column'  # 正規化する対象の列名
new_column_name = 'normalized'  # 新しく追加する列の名前

result_df = add_normalized_column_from_csv(csv_file, column_name, new_column_name)
print(result_df)

if '__main__' == __name__:
    data = [3.18, 3.59, 3.46, 3.02, 3.52, 3.03, 3.53 ,3.01, 3.02, 3.38, 3.15]



    print('ok')