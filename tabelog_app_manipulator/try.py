#正規化する関数
#入力値: 「項目」ごとのデータセット
#出力値: 「項目」ごとに標準化されたデータセット
import pandas as pd
from selenium import webdriver

import time


if '__main__' == __name__:
    driver = webdriver.Chrome()
    time.sleep(10)
    data = [3.18, 3.59, 3.46, 3.02, 3.52, 3.03, 3.53 ,3.01, 3.02, 3.38, 3.15]



    print('ok')