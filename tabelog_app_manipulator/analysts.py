import pandas as pd
import numpy as np
import os

class data_analysts:
    def __init__(self, voice, strict, ratio, data, station_name):
        self.strict = strict
        self.ratio = ratio
        self.voice = voice
        self.data = data
        self.station_name = station_name
        self.price_column = self.strict['dinner or lunch'] + '(~以内の値段で食べられる)'

    def invert_column(self, column_name, new_column_name):
        self.data[new_column_name] = np.where(self.data[column_name] != 0, 1 / self.data[column_name], 0)

    def normalize_column(self, column_name, new_column_name): 
        max_value = self.data[column_name].max()
        min_value = self.data[column_name].min()
        # データの確認
        print(f"Normalizing {column_name}: min={min_value}, max={max_value}")
        # 最大値と最小値が同じ場合（分母が0になる場合）には、すべての値を0にする
        if max_value == min_value:
            self.data[new_column_name] = 0
        else:
            self.data[new_column_name] = (self.data[column_name] - min_value) / (max_value - min_value)
 
    def evaluate(self):
        self.data = self.data[self.data[self.price_column] > 0]
        self.data['声の大きさ'] = self.data['項目'].map(self.voice)

        walk_time_column = self.station_name + '駅から徒歩(分)'
        conditions = (
            (self.data[walk_time_column] <= self.strict['徒歩何分以内']) &
            (self.data[self.price_column] <= self.strict['予算'])
        )
        self.data = self.data[conditions]

        self.invert_column(walk_time_column, walk_time_column + '(逆数)')
        self.invert_column(self.price_column, self.price_column + '(逆数)')
        
        self.normalize_column('星5段階評価', '星5段階評価(標準化)')
        self.normalize_column(self.price_column + '(逆数)', self.price_column + '(標準化)')
        self.normalize_column(walk_time_column + '(逆数)', walk_time_column + '(標準化)')
        #self.normalize_column('声の大きさ', '声の大きさ(標準化)')

        for index, row in self.data.iterrows():
            value = (
                row['星5段階評価(標準化)'] * self.ratio['星'] +
                row[self.price_column + '(標準化)'] * self.ratio['予算'] +
                row[walk_time_column + '(標準化)'] * self.ratio['徒歩']
            ) * row['声の大きさ']
            self.data.at[index, '最終評価'] = value

        self.data.sort_values(by='最終評価', ascending=False, inplace=True)

    def run(self):
        self.evaluate()
        print('run-ok')
        return self.data

class data_analysts_run:
    def __init__(self, voice, strict, ratio, station_name):
        self.voice = voice
        self.strict = strict
        self.ratio = ratio
        self.station_name = station_name

        self.base_dir = 'datas'
        self.dir_name = 'maked_menus_datas'
        self.file_name = 'combined_data.csv'

        self.output_base_dir = 'result_data'
        self.ana_file_name = 'analysts_data.csv'
        self.ana_result_file_name = 'result.csv'
        print('ok')

    def file_read(self):
        print(f'現在のパス{os.getcwd()}')
        dir_path = os.path.join(self.base_dir, self.dir_name)
        print('移動するフォルダ' + dir_path)

        if not os.path.exists(dir_path):
            print('指定したディレクトリが存在しません')
            
        os.chdir(dir_path)
        
        if not os.path.isfile(self.file_name):
            print('指定したファイルは存在しません')
            
        data = pd.read_csv(self.file_name, encoding='utf-8-sig')
        return data

    def file_output(self, output_data):
        print(f'現在のパス{os.getcwd()}')
        os.chdir("..")
        os.makedirs(self.output_base_dir, exist_ok=True)
        os.chdir(self.output_base_dir)

        data = pd.DataFrame(output_data)
        data.to_csv(self.ana_file_name, encoding='utf-8-sig', index=False, errors="ignore")
        data = data[['最終評価', '店名','項目','星5段階評価',  self.strict['dinner or lunch'] + '(~以内の値段で食べられる)', self.station_name + '駅から徒歩(分)', 'お問い合わせ', '予約可否', '営業時間', '支払い方法']]
        data.to_csv(self.ana_result_file_name, encoding='utf-8-sig', index=False, errors="ignore")

    def run(self):
        read_data = self.file_read()
        analysts = data_analysts(self.voice, self.strict, self.ratio, read_data, self.station_name)
        output_data = analysts.run()
        self.file_output(output_data)

if '__main__' == __name__:
    voice = {'かき氷': 2, '寿司': 1}
    strict = {'徒歩何分以内': 10, 'dinner or lunch': 'dinner', '予算': 5000}
    ratio = {'徒歩': 1, '予算': 1.2, '星': 1.3}
    station_name = '北千住'
    app = data_analysts_run(voice, strict, ratio, station_name)
    app.run()

    print('analysts_test')
