import requests
import json
from bs4 import BeautifulSoup

URL_OLIYGOHLAR = "https://abt.uz/university"
URL_YONALISHLAR_YILLAR = "https://abt.uz/university/view?slug=andijon-davlat-chet-tillari-instituti&year=2023&type=kunduzgi&lang=uz"
HOST = "https://abt.uz"

SESSION = requests.Session()

#  oliygotlar link keladi ularni royxati qaytadi
def oliygohlar(url:str)->list:
    oliygohlar_html = SESSION.get(url)
    oliygohlar_bs4 = BeautifulSoup(oliygohlar_html.text,'lxml')
    tds =  oliygohlar_bs4.find_all("td")
    data = []
    for td in tds:
        a = td.find('a')
        div = td.find('div')
        d = {
            'nomi':      a.text if a else '',
            'url':       a['href'] if a else '',
            'shahar':    div.text if div else '',
        }
        data.append(d)
    return data 

def yonalishlarni_olish(url:str)->list:
    yonalishlar_html = SESSION.get(url)
    yonalishlar_bs4 = BeautifulSoup(yonalishlar_html.text,'lxml')
    trs = yonalishlar_bs4.find_all("tr")
    data = []
    for index, tr in enumerate(trs):
        if index==0:
            continue
        tds = tr.find_all('td')
        if len(tds) < 4:
            print(tds)
            continue
        td1, td2, td3, td4 = tds if tds else [None]*4
        d = {
            "yonalish": td1.text if td1 else 'malumot topilmadi',
            'url':      td1.find('a')['href'],
            "shifr":    td2.text if td2 else 'malumot topilmadi',
            "grant":    td3.text if td3 else 'malumot topilmadi',
            "kontrakt": td4.text if td4 else 'malumot topilmadi',
        }
        data.append(d)
    return data

# oliygohlardagi yonalishlarni oladi
def yonalishlar(url:str)-> list:
    url = HOST + url
    data = yonalishlarni_olish(url)
    return data

# yo'nalishdagi bloklarni oladi
def bloklar(url:str)->list:
    bloklar_html = SESSION.get(url)
    bloklar_bs4 = BeautifulSoup(bloklar_html.text,'lxml')
    pass

def yonalishlar_yillar(slug:str, year:str, lang:str = "uz", type:str="kunduzgi")-> list:
    slug = slug.split('/')[-1]
    "https://abt.uz/university/view?slug=andijon-davlat-chet-tillari-instituti&year=2023&type=kunduzgi&lang=uz"
    url = f"{URL_OLIYGOHLAR}/view?slug={slug}&year={year}&type={type}&lang={lang}"
    data = yonalishlarni_olish(url=url)
    return data

def write_data(lst:list, file_name:str):
    data =  json.dumps(lst)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(data)
    pass

def main():
    oliygoh = oliygohlar(URL_OLIYGOHLAR)
    # write_data(oliygoh,'./malumotlar/oliygohlar.json')
    # print(yonalishlar_yillar(oliygoh[0]['url'],2024))
    for i, data in enumerate(oliygoh):
        # t = yonalishlar(data['url'])
        for y in [2020, 2021, 2022, 2023, 2024]:
            d = yonalishlar_yillar(data['url'],y)
            write_data(d, f"./malumotlar/static/{y}/{i}{data['shahar']}.json")
        # print(yonalishlar_yillar(d['url'],2024))
        # write_data(t, f"./malumotlar/info/{i}{d['shahar']}.json")
        
if __name__ == '__main__':
    main()