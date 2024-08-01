from collections import Counter
from data_maked import data_maked_manipulate_run
from analysts import data_analysts_run
from tabelog_collector import application_manipulate

if '__main__' == __name__:
  
     #入力値の設定
    place = input('現在地(駅名):')
    time_is = input('dinner or lunch:')
    price_max = int(input('予算の上限:'))
    max_distance = int(input('徒歩何分以内か:'))
    
    menus = list()
    
    while True:
        menu = input('食べたいもの:')
        if menu == 'end':
            break
        menus.append(menu)
    print('input-ok!')
    

    items_count = Counter(menus)
    items_voice = dict(items_count)
    
    
    number = len(menus)
    menus_resource = list(set(menus))

    print('駅名:' + place)
    print('項目:')
    print(menus)
    print(time_is)
    print('予算の上限:' + str(price_max))
    
    print('各項目が何回入力されたか:')
    print(items_voice)

    print('人数:' + str(number))
    print('重複したものを取り除く')
    print(menus_resource)

    mani = application_manipulate(place, menus_resource)
    mani.run()

    maked_mani = data_maked_manipulate_run(place)
    maked_mani.run()

    strict = {'徒歩何分以内': max_distance, 'dinner or lunch': time_is, '予算': price_max}

    #項目の優先順位(学生を想定)
    ratio = {'徒歩': 1, '予算': 1.2, '星': 1.3 }
    app = data_analysts_run(items_voice, strict, ratio, place)
    app.run()
    print('proguraming_is_ok')