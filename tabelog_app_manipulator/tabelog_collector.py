import time
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os



class application_manipulate:
    def __init__(self, place, menus):
        self.place = place
        self.menus = menus
    
    def run(self):
        #ディレクトリのパスを作成する
        base_dir = 'datas'
        dir_name = 'menus_detas'
        dir_path = os.path.join(base_dir, dir_name)
        
        #ディレクトリを作成する
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f'{dir_path}フォルダを作成しました')
        else:
            print(f'{dir_path}フォルダは既に存在しています')
        
        #指定したフォルダに移動する
        os.chdir(dir_path)
        print(f'現在のディレクトリ: {os.getcwd()}')

        for i in self.menus:
            tabelog = tabelog3_manipulate(self.place, i)
            tabelog.run()
        print('application_manipulate_run-ok')



class tabelog3_manipulate:

    BASE_URL = 'https://tabelog.com/'

    def __init__(self, area, keyword):
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)

        #検索するときのareaとキーワードの設定
        self.area_word = area
        self.keyword = keyword

        self.items_urls = list()
        self.detail_infos = list()

    #tabelogサイトの検索欄にkeywordを入力する
    def go_to_keyword_page(self):

        area_element = self.driver.find_element(By.CSS_SELECTOR, '#sa')
        key_word_element = self.driver.find_element(By.CSS_SELECTOR, '#sk')

        area_element.send_keys(self.area_word)
        key_word_element.send_keys(self.keyword)

        botton_element = self.driver.find_element(By.CSS_SELECTOR, '#js-global-search-btn')
        time.sleep(3)

        self.driver.execute_script("arguments[0].click();", botton_element)
        print('ok_insertinto_keyword')

    #検索後のページに行く
    def go_to_top_page(self):
        self.driver.get(self.BASE_URL)
        self.go_to_keyword_page()
        print('ok-go_to_keyword_page')


    #現在のページが最終かどうか
    def is_last_page(self):
        last_page_flag = False

        try:
            #そもそもページネーションが存在しているかどうか?
            self.driver.find_element(By.CSS_SELECTOR, '#container > div.rstlist-contents.clearfix > div.flexible-rstlst > div > div.list-pagenation > div')
            try:
                #ページネーションの「次」があるかどうか
                self.driver.find_element(By.CLASS_NAME, 'c-pagination__arrow--next')
            except:
                last_page_flag = True
        except:
            last_page_flag = True
        
        #最終ページ→True, 最終ページではない→False
        print(last_page_flag)
        return last_page_flag


    #次の画面遷移する
    def go_to_next_page(self, num_page):

        #現在のページネーション番号
        print(num_page)

        #現在のページネーション番号とと一致するページネーション要素を探す
        paginations = self.driver.find_elements(By.CLASS_NAME, 'c-pagination__item')
        for i in paginations:
            if i.text == str(num_page):
                print('ok-find-pagenation-page')

                try:
                    #見つけた要素に対してクリック操作を行う
                    a_tagi_of_i = i.find_element(By.TAG_NAME, 'a')
                    print('ok-find-a-tag')
                    time.sleep(2)
                    a_tagi_of_i.click()
                    break
                except:
                    continue
        print('ok_goto_pagenation')
    
    #画面にあるURLを取得する
    def get_items_urls(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-rstlist-info'))
        )
        one_page_rst_body = self.driver.find_element(By.CLASS_NAME, 'js-rstlist-info')
        one_page_rst_body_componets = one_page_rst_body.find_elements(By.CLASS_NAME, 'list-rst__rst-data')
        one_page_components_a_tag = [i.find_element(By.CLASS_NAME, 'list-rst__rst-name-target') for i in one_page_rst_body_componets]
        one_page_detail_urls = [i.get_attribute("href") for i in one_page_components_a_tag]
        self.items_urls.extend(one_page_detail_urls)
        print('ok-get-onepage-urls')
    
    #URLsを収集する関数
    def get_urls_method(self):
        self.go_to_top_page()
        #現在のページネーション
        num_page = 1
        while(True):
            # 画面にあるURLを取得
            self.get_items_urls()
            # 現在のページが最終ページか判定
            if self.is_last_page():
                break
            # 画面を遷移する
            num_page += 1
            self.go_to_next_page(num_page)
    print('ok-geturls_is_ok')


    #店の詳細情報を取得する
    def get_detail_info(self):
        for i in self.items_urls:
            
            #1つの店の詳細情報
            detail_one_info = {}

            #URLを取り出してお店のページに行く
            self.driver.get(i)
            WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#js-detail-score-open > p > b > span'))
                )

            #そのお店の評価(星)を取り出す
            star_evaluation = self.driver.find_element(By.CSS_SELECTOR, '#js-detail-score-open > p > b > span').text
            star_evaluation = 'None-info' if star_evaluation == '' else star_evaluation
            detail_one_info['星5段階評価'] = star_evaluation
            print('ok0')

            #詳細ページから店舗基本情報を取り出す
            detail_infos_element = self.driver.find_element(By.CSS_SELECTOR, '#rst-data-head > table:nth-child(2)')
            print('ok1')

            #項目とその値のelementsをを見つける
            detail_info_trs = detail_infos_element.find_elements(By.TAG_NAME, 'tr')
            print('ok2')
            time.sleep(1)
            

            #項目とその情報をひとつづつ取り出して辞書にして格納する
            for tr in detail_info_trs:
                #項目名を取り出し
                th_text = tr.find_element(By.TAG_NAME, 'th').text
                print('ok3')

                #項目名の文字整形
                #「お問い合わせ」項目の文字の整形
                th_text = th_text.replace('\n', ' ')
                th_text = th_text.replace('予約・ お問い合わせ', 'お問い合わせ')

                #「予算」の項目は飛ばす
                if th_text == '予算':
                    continue
                
                #「口コミ予算」のdinnerとlunchの項目ごとにする
                if th_text == '予算（口コミ集計）':
                    arial_elements = tr.find_elements(By.TAG_NAME, 'span')
                    print('ok4')
                    dinner_price = ''
                    lunch_price = ''
                    for i in arial_elements:
                        try:
                            arial_element = i.find_element(By.TAG_NAME, 'i')
                            print('ok5')
                            label = arial_element.get_attribute('aria-label')
                            print('ok6')
                            
                            if label == 'Dinner':
                                dinner_price = i.text 
                            if label == 'Lunch':
                                lunch_price = i.text
                        except:
                            continue
                    detail_one_info['dinner'] = dinner_price if dinner_price != '' else 'None-info'
                    detail_one_info['lunch'] = lunch_price if lunch_price != '' else 'None-info'
                    continue


                #項目名の値の取り出し
                td_text = tr.find_element(By.TAG_NAME, 'td').text
                print('ok7')
                
                td_text = td_text.replace('\n', ' ')
                td_text = td_text.replace('大きな地図を見る', '')
                td_text = td_text.replace('周辺のお店を探す', '')
                td_text = td_text.replace('利用金額分布を見る', '')

                if td_text == '':
                    td_text = 'None-info'
            
                detail_one_info[th_text] = td_text
            

            self.detail_infos.append(detail_one_info)
        print('ok-get_detail_info')


    #作成データフレームをファイルを作成する
    def out_put_infos(self):
        df = pd.DataFrame(self.detail_infos)
        df.to_csv(f'{self.keyword}_deta.csv', encoding='utf-8-sig', index=False, errors="ignore")



    def run(self):
        try:
            #URLを収集
            self.get_urls_method()
            print(self.items_urls)
            print(len(self.items_urls))

            # URLからデータを取得
            self.get_detail_info()
            

            # 出力をCSVに変換する
            self.out_put_infos()
            
        except Exception as e:
            print(e)

        finally:
            self.driver.quit()

if __name__ == "__main__":
   print('ok')

