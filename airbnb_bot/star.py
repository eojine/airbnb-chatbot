import pprint

import requests
from bs4 import BeautifulSoup

city = "jongrogu" # 가고싶은 도시
checkin = "2020-01-18" # 체크인 날짜
checkout = "2020-01-20" # 체크아웃 날짜
price_max = 200000 # 최대 숙소 금액
ib = True # 즉시 예약 가능 여부
guest_count = 1 # 사람 수 (Only Adult)

base_url = "https://www.airbnb.co.kr"
url_format = "https://www.airbnb.co.kr/s" \
             "/{city}/homes?" \
             "&checkin={checkin" \
             "}&checkout={checkout}" \
             "&adults={guest_count}" \
             "&price_max={price_max}" \
             "&ib={ib}".format(city=city,
                               checkin=checkin,
                               checkout=checkout,
                               guest_count=guest_count,
                               price_max=price_max,
                               ib=ib)

print(url_format)
response = requests.get(url_format)
soup = BeautifulSoup(response.content, 'lxml')

# print(soup.prettify())

rows = soup.find_all('div', class_="_ylefn59")
airbnbs = []
for row in rows:
    name = row.find('div', class_="_1ebt2xej")
    star = row.find('span', class_="_ky9opu0")
    url = row.find('a', class_="_i24ijs").attrs['href']
    image_url = row.find('div', class_="_10xjrv2u").attrs['style']

    image_url = image_url.split('(')[1].split(')')[0]

    if (star==None):
        continue
    airbnbs.append([name.string, float(star.string), base_url + url, image_url])

sorted_airbnbs = sorted(airbnbs, key=lambda x: (x[1], x[0]), reverse=True)
pprint.pprint(sorted_airbnbs)

