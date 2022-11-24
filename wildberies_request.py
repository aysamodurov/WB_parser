"""
    Модуль для работы с запросами к WILDBERRIES
"""
import json
import os
from datetime import datetime
import requests
from config import URL_CATEGORY, HEADERS, ALL_CATAGORY_FILENAME, UPDATE_CATEGORY_TIMES


def update_all_categories_file():
    """
    Обновить файл с категориями WILDBERRIES
    все категории сохранены в файл ALL_CATAGORY_FILENAME
    """
    # Если прошло больше суток, то обновить файл all_categories_filename
    update_file = os.path.exists(ALL_CATAGORY_FILENAME) and \
    datetime.now().timestamp() - os.path.getctime(ALL_CATAGORY_FILENAME) > UPDATE_CATEGORY_TIMES
    
    # Сохранить все категории, полученные с Wildberries в файл
    if not os.path.exists(ALL_CATAGORY_FILENAME) or update_file:
        try:
            print('Обновление данных с WILDBERRIES ...')
            response = requests.get(URL_CATEGORY, headers=HEADERS, timeout=10)
            with open(ALL_CATAGORY_FILENAME, 'w', encoding='utf-8') as file:
                json.dump(response.json(), file, indent=3, ensure_ascii=False)
            print('Данные успешно обновлены')
        except:
            print('Не удалось обновить данные')


def get_all_categories():
    """
    Получить json со списком категорий из файла ALL_CATAGORY_FILENAME

    Returns:
        json : информация полученная о всех категориях 
    """
    update_all_categories_file()
    with open(ALL_CATAGORY_FILENAME, 'r', encoding='utf-8') as file:
        categories = json.load(file)
        return list(filter(lambda x: 'url' in x, categories))


def find_category_by_url(categories, url:str):
    """Рекурсивный поиск категории в json по url
    url категории хранится в categories[i][url]

    Args:
        categories (list): список из всех категорий полученный с WB, json формат
        url (str): url категории, который ищем

    Returns:
        dict{'id', 'parent', 'name', 'seo', 'url', 'shard', 'query'}:
        информация о категории с url
        
    """
    for category in categories:
        if 'url' in category and  (category['url'] == url):
            return category
        if 'childs' in category:
            res = find_category_by_url(category['childs'], url)
            if res:
                res.pop('childs', None)
                return res


def get_category_by_url(category_url):
    """Получить информацию о категории по url

    Args:
        category_url (str): ссылка на категорию на WB

    Returns:
        dict{'id', 'parent', 'name', 'seo', 'url', 'shard', 'query'}: информация о категории
    """
    # получить url категории для загрузки данных
    find_url = category_url.split("https://www.wildberries.ru")[1]
    categories = get_all_categories()
    # получаем информацию о категории из каталога
    category = find_category_by_url(categories, find_url)
    return category


def load_items_from_wb(url_category, countpage):
    """Загрузка страниц выбранной категории с сайта WB 

    Args:
        url_category: ссылка на страницу с категорий
        countpage(int): количество страниц для загрузки с сайта 
        1 страница - 100 товаров
    """
    category = get_category_by_url(url_category)
    res = []
    for page in range(countpage):
        items_query = f'https://catalog.wb.ru/catalog/{category["shard"]}/catalog?appType=1&couponsGeo=12,7,3,6,18,21&'\
                    f'curr=rub&dest=-1029256,-72181,-1144811,12358283&emp=0&lang=ru&locale=ru&page={page+1}&pricemarginCoeff=1.0&'\
                    f'reg=0&regions=80,64,83,4,38,33,70,82,69,68,86,30,40,48,1,22,66,31&sort=popular&spp=0&{category["query"]}'

        try:
            print(f'Запрос {page+1} страницы из {countpage}')
            response = requests.get(items_query, headers=HEADERS, timeout=10)
            res.extend(response.json()['data']['products'])
        except:
            print(f'Ошибка при получении {page} страницы из {countpage}')
    return res



    
