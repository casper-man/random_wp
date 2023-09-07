import requests
import os
import ctypes
from random import randrange
from bs4 import BeautifulSoup as bs


# текстовый запрос
q = 'spider-man'
# Категории 100(общиая), 010(аниме) и 001(люди) 
# можно комбинировать 101 110 011 и т.д.
categories = 111
# 100(SFW) 010(Sketchy)
purity = 100
# Разрешение atleast >=, resolutions =
atleast = '1920x1080'
resolutions = '1920x1080'
# соотношение сторон
ratios = '16x9'
# Сортировка relevance, random, date_added, views
# favorites, toplist,hot 
sorting = 'random'
# порядок сортировки desc и asc
order = 'desc'
# HEX цвет
colors = ''
# Сожанные AI = 1, 0 для отключения фильтра
ai_art_filter = 1

seed = 'MaxHammer'
# seed = '9uHASZ'



def get_random_wp(url,params,headers):
    s = requests.session()
    r = s.get(url=url,params=params,headers=headers)
    if not r:
        return    
    soup = bs(r.content, features='html.parser')
    # https://th.wallhaven.cc/small/g7/g76657.jpg
    # https://w.wallhaven.cc/full/g7/wallhaven-g76657.jpg
    figures = soup.find_all('figure')
    img_list = []
    for figure in figures:
        img_list.append(f"https://w.wallhaven.cc/full/"
                        f"{figure.find('img').attrs['data-src'].split('/')[4]}"
                        f"/wallhaven-{figure.find('img').attrs['data-src'].split('/')[5]}")
    i = 0
    while True:
        random_num = randrange(0,len(img_list))
        get_img = requests.get(img_list[random_num])
        if get_img:
            set_wp(get_img)
            break
        i += 1
        if i == len(img_list):
            break

def set_wp(img):
    if os.name == 'posix':
        WALLPAPER_PATH = os.environ['HOME'] + "/daily_image.jpg"
    else:
        WALLPAPER_PATH = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] + "\daily_image.jpg"
    print(f'Get wallpaper from: {img.url}')
    f = open(WALLPAPER_PATH,'wb')
    f.write(img.content) 
    f.close()    
    print(f'Save to {os.path.abspath(WALLPAPER_PATH)}')
    if os.name == 'posix':
        pass
    else:
        SPI_SETDESKWALLPAPER = 20 
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, os.path.abspath(WALLPAPER_PATH) , 0)


def main():
    params = {
        'q': q,
        'categories': categories,
        'purity': purity,
        'resolutions': resolutions,
        'ratios': ratios,
        'sorting': sorting,
        'order': order,
        'colors': colors,
        'ai_art_filter': ai_art_filter,
        'seed': seed
    }
    headers = {'Content-Type': 'text/html'}
    # get_random_wp(url='https://wallhaven.cc/search?q=spider-man&categories=100&purity=110&atleast=1920x1080&ratios=16x9&sorting=random&order=desc&colors=000000&ai_art_filter=0&seed=9uHASZ')
    get_random_wp(url='https://wallhaven.cc/search',params=params, headers=headers)


if __name__ == '__main__':
    main()