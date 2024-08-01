import re
import pandas as pd
import os
from glob import glob

class data_maked_manipulate():
    def __init__(self, file, filename, station_name):
        self.file = file
        self.filename = filename
        self.station_name = station_name
        print('class_init_is_ok')

    def extract_food_type(self, filename):
        return filename.split('_')[0]
    
    def extract_distance(self, text):
        pattern = rf'{self.station_name}駅から(\d+)m'
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
        else:
            return None
        
    def process_budget(self, budget_str):
        if "None-info" in budget_str or pd.isna(budget_str):
            return 0
        budget_str = budget_str.replace('\\', '').replace(',', '').strip()
        if '￥' in budget_str:
            budget_str = budget_str.lstrip('￥')
            if '￥' in budget_str:
                low, high = budget_str.split('￥')
                return int(high)
            else:
                return int(budget_str)
        else:
            return int(budget_str)
    
    def walk_alt_distance(self, walk):
        walk = walk / 75
        return int(walk)

    def run(self):
        self.file = self.file.loc[
            ~self.file['星5段階評価'].isin(['-', 'None-info']) & 
            self.file['星5段階評価'].notna()
        ]

        self.file['dinner(~以内の値段で食べられる)'] = self.file['dinner'].apply(self.process_budget)
        self.file['lunch(~以内の値段で食べられる)'] = self.file['lunch'].apply(self.process_budget)

        self.file[f'{self.station_name}駅からの距離'] = self.file['交通手段'].apply(self.extract_distance)

        self.file = self.file.dropna(subset=[f'{self.station_name}駅からの距離'])

        food_type = self.extract_food_type(self.filename)
        self.file['項目'] = food_type

        self.file[f'{self.station_name}駅から徒歩(分)'] = self.file[f'{self.station_name}駅からの距離'].apply(self.walk_alt_distance)

        self.file = self.file[['店名', '星5段階評価', 'dinner(~以内の値段で食べられる)', 'lunch(~以内の値段で食べられる)', f'{self.station_name}駅からの距離', f'{self.station_name}駅から徒歩(分)', '項目', 'お問い合わせ', '予約可否', '営業時間', '支払い方法']]

        print(self.file)
        print('run_method_ok')
        return self.file


class data_maked_manipulate_run():
    def __init__(self, station_name):
        self.station_name = station_name
        print('ok')
        
    def run(self):
        print("現在のディレクトリ:", os.getcwd())
        
        os.chdir("../..")
        
        list_dir = os.listdir(r'datas\menus_detas')
        print("ディレクトリ内のファイル全て表示する")
        print(list_dir)
        
        list_files = glob(r'datas\menus_detas\*_deta.csv')
        print('ディレクトリ内の～_data.csvファイルを取得')
        print(list_files)

        all_data = []
        
        for i in range(len(list_files)):
            file = pd.read_csv(list_files[i], encoding='utf-8-sig', dtype=object)
            print(f'{list_files[i]}ファイルの内容を取得しました')
            maked_mani = data_maked_manipulate(file, os.path.basename(list_files[i]), self.station_name)
            file = maked_mani.run()

            output_dir = r'datas\maked_menus_datas'
            os.makedirs(output_dir, exist_ok=True)
            
            output_file = os.path.join(output_dir, os.path.basename(list_files[i]))
            file.to_csv(output_file, encoding='utf-8-sig', index=False, errors="ignore")

            all_data.append(file)
            
        combined_data = pd.concat(all_data, axis=0, ignore_index=True)

        output_dir = r'datas\maked_menus_datas'
        output_file = os.path.join(output_dir, 'combined_data.csv')
        combined_data.to_csv(output_file, encoding='utf-8-sig', index=False, errors="ignore")

        print('maked_complete')

if '__main__' == __name__:
    station_name = input("駅名を入力してください: ")
    mani = data_maked_manipulate_run(station_name)
    mani.run()
    print('ok')
