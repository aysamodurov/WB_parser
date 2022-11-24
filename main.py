from wildberies_request import load_items_from_wb
import json


def test_load_items():
    url = 'https://www.wildberries.ru/catalog/muzhchinam/odezhda/bryuki-i-shorty'
    items = load_items_from_wb(url, 3)

    print('Получены данные о {} товарах'.format(len(items)))
    
    # сохранение данных в файл
    with open('res.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(items, jsonfile, indent=3, ensure_ascii=False)

def test_load_from_file():
    print('Начало работы с товарами')
    items = []
    with open('res.json', 'r', encoding='utf-8') as jsonfile:
        items = json.load(jsonfile)
    if items:
        print(len(items))
        print(items[0])

if __name__ == '__main__':
    test_load_from_file()
