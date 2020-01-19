from flask import Flask,make_response,request,jsonify
import time
import pprint

import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/webhook', methods=['GET','POST'])
def hello():
    # 파라미터 받아오는 부분
    req = request.get_json(force=True)
    intent_name = req.get("queryResult").get("intent").get("displayName")

    print(intent_name)

    if intent_name=='emotion':
        queryText = req.get("queryResult").get("queryText")
        return {'fulfillmentText': queryText + "? 그럼 여행은 어떠세요?"}


    elif intent_name=='emotion - yes - seoul - entities - day':

        hoho = req.get("queryResult").get("outputContexts")
        hoho_map = hoho[1].get("parameters")

        strr = hoho_map["date-time"]

        city = hoho_map["seoul_entities"]  # 가고싶은 도시
        checkin = strr[:10]  # 체크인 날짜
        checkout = strr[:10]  # 체크아웃 날짜
        # ib = True  # 즉시 예약 가능 여부
        # guest_count = 1  # 사람 수 (Only Adult)

        # 크롤링해서 결과 가져오는 부분
        base_url = "https://www.airbnb.co.kr"
        url_format = "https://www.airbnb.co.kr/s" \
                     "/{city}/homes?" \
                     "&checkin={checkin}" \
                     "&checkout={checkout}" \
            .format(city=city,
                    checkin=checkin,
                    checkout=checkout
                    )

        response = requests.get(url_format)
        soup = BeautifulSoup(response.content, 'lxml')

        rows = soup.find_all('div', class_="_ylefn59")
        airbnbs = []
        for row in rows:
            name = row.find('div', class_="_1ebt2xej")
            star = row.find('span', class_="_ky9opu0")
            url = row.find('a', class_="_i24ijs").attrs['href']
            image_url = row.find('div', class_="_10xjrv2u").attrs['style']

            image_url = image_url.split('(')[1].split(')')[0]

            if (star == None):
                continue
            airbnbs.append([name.string, float(star.string), base_url + url, image_url])

        sorted_airbnbs = sorted(airbnbs, key=lambda x: (x[1], x[0]), reverse=True)

        #review_cr(sorted_airbnbs[0][2])
        #time.sleep(20)

        return {"fulfillmentMessages": [
            {
                "card": {
                    "title": sorted_airbnbs[0][0],
                    "imageUri": sorted_airbnbs[0][3],
                    "buttons": [
                        {
                            "text": "보러가기",
                            "postback": sorted_airbnbs[0][2]
                        }
                    ]
                },
                "platform": "LINE"
            },
            {
                "card": {
                    "title": sorted_airbnbs[1][0],
                    "imageUri": sorted_airbnbs[1][3],
                    "buttons": [
                        {
                            "text": "보러가기",
                            "postback": sorted_airbnbs[1][2]
                        }
                    ]
                },
                "platform": "LINE"
            },
            {
                "card": {
                    "title": sorted_airbnbs[2][0],
                    "imageUri": sorted_airbnbs[2][3],
                    "buttons": [
                        {
                            "text": "보러가기",
                            "postback": sorted_airbnbs[2][2]
                        }
                    ]
                },
                "platform": "LINE"
            },
            {
                "text": {
                    "text": [
                        "옵션을 선택할수있어요! 선택하시겠어요?"
                    ]
                },
                "platform": "LINE"
            }

        ]
        }


    elif intent_name== 'emotion - yes - seoul - entities - day - yes - pricedetail':


        hoho = req.get("queryResult").get("outputContexts")
        hoho_map = hoho[0].get("parameters")
        # print(hoho)
        #hoho_map["number-integer"]
        strr = hoho_map["date-time"]
        print(strr[:10])


        city = hoho_map["seoul_entities"] # 가고싶은 도시
        checkin = strr[:10]  # 체크인 날짜
        checkout = strr[:10]  # 체크아웃 날짜
        price_max = str(int(hoho_map["number-integer"]))  # 최대 숙소 금액
        # ib = True  # 즉시 예약 가능 여부
        # guest_count = 1  # 사람 수 (Only Adult)

        # 크롤링해서 결과 가져오는 부분
        base_url = "https://www.airbnb.co.kr"
        url_format = "https://www.airbnb.co.kr/s" \
                     "/{city}/homes?" \
                     "&checkin={checkin" \
                     "}&checkout={checkout}" \
                     "&price_max={price_max}" \
            .format(city=city,
                    checkin=checkin,
                    checkout=checkout,
                    price_max=price_max,
                    )
        print(url_format)
        response = requests.get(url_format)
        soup = BeautifulSoup(response.content, 'lxml')

        rows = soup.find_all('div', class_="_ylefn59")
        airbnbs = []
        for row in rows:
            name = row.find('div', class_="_1ebt2xej")
            star = row.find('span', class_="_ky9opu0")
            url = row.find('a', class_="_i24ijs").attrs['href']
            image_url = row.find('div', class_="_10xjrv2u").attrs['style']

            image_url = image_url.split('(')[1].split(')')[0]

            if (star == None):
                continue
            airbnbs.append([name.string, float(star.string), base_url + url, image_url])

        sorted_airbnbs = sorted(airbnbs, key=lambda x: (x[1], x[0]), reverse=True)

        return  {   "fulfillmentMessages": [
      {
        "card": {
          "title": sorted_airbnbs[0][0],
          "imageUri": sorted_airbnbs[0][3],
          "buttons": [
            {
              "text": "보러가기",
              "postback": sorted_airbnbs[0][2]
            }
          ]
        },
        "platform": "LINE"
      },
            {
                "card": {
                    "title": sorted_airbnbs[1][0],
                    "imageUri": sorted_airbnbs[1][3],
                    "buttons": [
                        {
                            "text": "보러가기",
                            "postback": sorted_airbnbs[1][2]
                        }
                    ]
                },
                "platform": "LINE"
            },
            {
                "card": {
                    "title": sorted_airbnbs[2][0],
                    "imageUri": sorted_airbnbs[2][3],
                    "buttons": [
                        {
                            "text": "보러가기",
                            "postback": sorted_airbnbs[2][2]
                        }
                    ]
                },
                "platform": "LINE"
            },
      {
        "text": {
          "text": [
            ""
          ]
        }
      }
    ]
    }


    elif intent_name == 'emotion - yes - seoul - entities - day - yes - persondetail':
        hoho = req.get("queryResult").get("outputContexts")
        hoho_map = hoho[0].get("parameters")
        print("#########")
        print(hoho)
        print(hoho_map)
        print("#########")
        # hoho_map["number-integer"]
        strr = hoho_map["date-time"]

        city = hoho_map["seoul_entities"]  # 가고싶은 도시
        checkin = strr[:10]  # 체크인 날짜
        checkout = strr[:10]  # 체크아웃 날짜
        # ib = True  # 즉시 예약 가능 여부
        guest_count = hoho_map["number"]  # 사람 수 (Only Adult)

        # 크롤링해서 결과 가져오는 부분
        base_url = "https://www.airbnb.co.kr"
        url_format = "https://www.airbnb.co.kr/s" \
                     "/{city}/homes?" \
                     "&checkin={checkin" \
                     "}&checkout={checkout}" \
                     "&adults={guest_count}" \
            .format(city=city,
                    checkin=checkin,
                    checkout=checkout,
                    guest_count=guest_count
                    )
        print(url_format)
        response = requests.get(url_format)
        soup = BeautifulSoup(response.content, 'lxml')

        rows = soup.find_all('div', class_="_ylefn59")
        airbnbs = []
        for row in rows:
            name = row.find('div', class_="_1ebt2xej")
            star = row.find('span', class_="_ky9opu0")
            url = row.find('a', class_="_i24ijs").attrs['href']
            image_url = row.find('div', class_="_10xjrv2u").attrs['style']

            image_url = image_url.split('(')[1].split(')')[0]

            if (star == None):
                continue
            airbnbs.append([name.string, float(star.string), base_url + url, image_url])

        sorted_airbnbs = sorted(airbnbs, key=lambda x: (x[1], x[0]), reverse=True)

        return {"fulfillmentMessages": [
            {
                "card": {
                    "title": sorted_airbnbs[0][0],
                    "imageUri": sorted_airbnbs[0][3],
                    "buttons": [
                        {
                            "text": "보러가기",
                            "postback": sorted_airbnbs[0][2]
                        }
                    ]
                },
                "platform": "LINE"
            },
            {
                "card": {
                    "title": sorted_airbnbs[1][0],
                    "imageUri": sorted_airbnbs[1][3],
                    "buttons": [
                        {
                            "text": "보러가기",
                            "postback": sorted_airbnbs[1][2]
                        }
                    ]
                },
                "platform": "LINE"
            },
            {
                "card": {
                    "title": sorted_airbnbs[2][0],
                    "imageUri": sorted_airbnbs[2][3],
                    "buttons": [
                        {
                            "text": "보러가기",
                            "postback": sorted_airbnbs[2][2]
                        }
                    ]
                },
                "platform": "LINE"
            },
            {
                "text": {
                    "text": [
                        ""
                    ]
                }
            }
        ]
        }


    elif intent_name == 'emotion - yes - seoul - entities - day - yes - starpoint':

        hoho = req.get("queryResult").get("outputContexts")
        hoho_map = hoho[0].get("parameters")
        # print(hoho)
        # hoho_map["number-integer"]
        strr = hoho_map["date-time"]
        print(strr[:10])

        city = hoho_map["seoul_entities"]  # 가고싶은 도시
        checkin = strr[:10]  # 체크인 날짜
        checkout = strr[:10]  # 체크아웃 날짜
        #price_max = str(int(hoho_map["number-integer"]))  # 최대 숙소 금액
        # ib = True  # 즉시 예약 가능 여부
        # guest_count = 1  # 사람 수 (Only Adult)

        # 크롤링해서 결과 가져오는 부분
        base_url = "https://www.airbnb.co.kr"
        url_format = "https://www.airbnb.co.kr/s" \
                     "/{city}/homes?" \
                     "&checkin={checkin" \
                     "}&checkout={checkout}" \
            .format(city=city,
                    checkin=checkin,
                    checkout=checkout,
                    )
        print(url_format)
        response = requests.get(url_format)
        soup = BeautifulSoup(response.content, 'lxml')

        rows = soup.find_all('div', class_="_ylefn59")
        airbnbs = []
        for row in rows:
            name = row.find('div', class_="_1ebt2xej")
            star = row.find('span', class_="_ky9opu0")
            url = row.find('a', class_="_i24ijs").attrs['href']
            image_url = row.find('div', class_="_10xjrv2u").attrs['style']

            image_url = image_url.split('(')[1].split(')')[0]

            if (star == None):
                continue
            airbnbs.append([name.string, float(star.string), base_url + url, image_url])

        sorted_airbnbs = sorted(airbnbs, key=lambda x: (x[1], x[0]), reverse=True)

        return {"fulfillmentMessages": [
            {
                "card": {
                    "title": sorted_airbnbs[0][0],
                    "imageUri": sorted_airbnbs[0][3],
                    "buttons": [
                        {
                            "text": "보러가기",
                            "postback": sorted_airbnbs[0][2]
                        }
                    ]
                },
                "platform": "LINE"
            },
            {
                "card": {
                    "title": sorted_airbnbs[1][0],
                    "imageUri": sorted_airbnbs[1][3],
                    "buttons": [
                        {
                            "text": "보러가기",
                            "postback": sorted_airbnbs[1][2]
                        }
                    ]
                },
                "platform": "LINE"
            },
            {
                "card": {
                    "title": sorted_airbnbs[2][0],
                    "imageUri": sorted_airbnbs[2][3],
                    "buttons": [
                        {
                            "text": "보러가기",
                            "postback": sorted_airbnbs[2][2]
                        }
                    ]
                },
                "platform": "LINE"
            },
            {
                "text": {
                    "text": [
                        ""
                    ]
                }
            }
        ]
        }

    elif intent_name == 'emotion - yes - seoul - entities - day - yes - reservation':

        hoho = req.get("queryResult").get("outputContexts")
        hoho_map = hoho[0].get("parameters")
        # print(hoho)
        # hoho_map["number-integer"]
        strr = hoho_map["date-time"]
        print(strr[:10])

        city = hoho_map["seoul_entities"]  # 가고싶은 도시
        checkin = strr[:10]  # 체크인 날짜
        checkout = strr[:10]  # 체크아웃 날짜
        #price_max = str(int(hoho_map["number-integer"]))  # 최대 숙소 금액
        ib = True  # 즉시 예약 가능 여부
        # guest_count = 1  # 사람 수 (Only Adult)

        # 크롤링해서 결과 가져오는 부분
        base_url = "https://www.airbnb.co.kr"
        url_format = "https://www.airbnb.co.kr/s" \
                     "/{city}/homes?" \
                     "&checkin={checkin" \
                     "}&checkout={checkout}" \
                     "&ib={ib}"\
            .format(city=city,
                    checkin=checkin,
                    checkout=checkout,
                    ib=ib
                    )
        print(url_format)
        response = requests.get(url_format)
        soup = BeautifulSoup(response.content, 'lxml')

        rows = soup.find_all('div', class_="_ylefn59")
        airbnbs = []
        for row in rows:
            name = row.find('div', class_="_1ebt2xej")
            star = row.find('span', class_="_ky9opu0")
            url = row.find('a', class_="_i24ijs").attrs['href']
            image_url = row.find('div', class_="_10xjrv2u").attrs['style']

            image_url = image_url.split('(')[1].split(')')[0]

            if (star == None):
                continue
            airbnbs.append([name.string, float(star.string), base_url + url, image_url])

        sorted_airbnbs = sorted(airbnbs, key=lambda x: (x[1], x[0]), reverse=True)

        return {"fulfillmentMessages": [
            {
                "card": {
                    "title": sorted_airbnbs[0][0],
                    "imageUri": sorted_airbnbs[0][3],
                    "buttons": [
                        {
                            "text": "보러가기",
                            "postback": sorted_airbnbs[0][2]
                        }
                    ]
                },
                "platform": "LINE"
            },
            {
                "card": {
                    "title": sorted_airbnbs[1][0],
                    "imageUri": sorted_airbnbs[1][3],
                    "buttons": [
                        {
                            "text": "보러가기",
                            "postback": sorted_airbnbs[1][2]
                        }
                    ]
                },
                "platform": "LINE"
            },
            {
                "card": {
                    "title": sorted_airbnbs[2][0],
                    "imageUri": sorted_airbnbs[2][3],
                    "buttons": [
                        {
                            "text": "보러가기",
                            "postback": sorted_airbnbs[2][2]
                        }
                    ]
                },
                "platform": "LINE"
            },
            {
                "text": {
                    "text": [
                        ""
                    ]
                }
            }
        ]
        }


def review_cr(urll):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import time
    import pandas as pd
    from bs4 import BeautifulSoup

    # In[37]:

    url = urll

    # In[38]:

    driver = webdriver.Chrome('C:/Users/multicampus/PycharmProjects/airbnb_bot/chromedriver')
    driver.implicitly_wait(3)
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # In[39]:

    reviews = soup.find('div', {'id': 'reviews'}).findAll('div', {'class': '_czm8crp'})
    review_list = []
    for review in reviews:
        review_list.append(review.string)
    print(review_list)

    # In[40]:

    df = pd.DataFrame(review_list, columns=['review'])

    # In[41]:

    from soynlp.tokenizer import RegexTokenizer, LTokenizer, MaxScoreTokenizer

    tokenizer = RegexTokenizer()
    tokenizer

    # In[42]:

    parsed_list = []
    for i in df['review']:
        temp = tokenizer.tokenize(i)
        parsed_list.append(temp)

    df['review_parsed'] = parsed_list
    # print(df)

    # In[43]:

    STOP_WORDS = ['.', '(', ')', '!', '[', ']', '▣', '※']

    # In[44]:

    def remove_stopwords(tokens):
        return [t for t in tokens if t not in STOP_WORDS]

    # In[45]:

    df['review_parsed'] = df['review_parsed'].apply(remove_stopwords)

    # In[118]:

    from collections import Counter
    from matplotlib import pyplot as plt

    faq_answer_parsed_lst = [y for x in df['review_parsed'].to_list() for y in x]

    counter = Counter(faq_answer_parsed_lst)
    counter.most_common(20)
    counter = counter.most_common(20)

    print(counter)
    return counter


if __name__ == '__main__':
    app.run()
