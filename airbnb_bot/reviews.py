from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from bs4 import BeautifulSoup


# In[37]:


url = "https://www.airbnb.co.kr/rooms/20770469?adults=1&check_in=2020-01-17&check_out=2020-01-18"


# In[38]:


driver = webdriver.Chrome('C:/Users/multicampus/PycharmProjects/airbnb_bot/chromedriver')
driver.implicitly_wait(3)
driver.get(url)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
soup = BeautifulSoup(driver.page_source,'html.parser')


# In[39]:


reviews = soup.find('div',{'id' : 'reviews'}).findAll('div',{'class' : '_czm8crp'})
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
#print(df)


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
print("#########")
for i in range(1,5):
    print(counter[i][0])
print("#########")





