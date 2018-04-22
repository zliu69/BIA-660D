
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import random
import time
import pandas as pd
import requests
import bs4


# In[2]:


driver = webdriver.Firefox(executable_path=r"E:\geckodriver-v0.19.1-win64\geckodriver.exe")
driver.get('https://www.amazon.com/RockBirds-Flashlights-Bright-Aluminum-Flashlight/product-reviews/B00X61AJYM')
time.sleep(3)


# In[3]:


driver.fullscreen_window()


# In[4]:


driver.execute_script('window.scrollBy(0,800)')


# In[5]:


def select_element_by_text(elements, text):
    for e in elements:
        if e.text == text:
            return e
        
    return None


# In[6]:


filter_bar_list = driver.find_elements_by_class_name('a-dropdown-prompt')


# In[7]:


purchase_filter_bar = select_element_by_text(filter_bar_list,"All reviewers")


# In[8]:


purchase_filter_bar.click()


# In[9]:


purchased_only_bar = driver.find_element_by_id('reviewer-type-dropdown_1')


# In[10]:


purchased_only_bar.click()


# In[11]:


Sort_bar = select_element_by_text(filter_bar_list,"Top rated")


# In[12]:


Sort_bar.click()


# In[13]:


Most_recent_bar = driver.find_element_by_id('sort-order-dropdown_1')


# In[14]:


Most_recent_bar.click()


# In[15]:


Review_list = driver.find_element_by_id('cm_cr-review_list')


# In[16]:


Review_list.click()
timesleep(5)


# In[22]:


url = driver.current_url


# In[23]:


Review_list = driver.find_element_by_id("cm_cr-review_list")


# In[24]:




soup = bs4.BeautifulSoup(requests.get(url).text, 'html5lib')



# In[25]:


Review_all_list = soup.find_all('div', attrs={'class': 'a-section review'})


# In[26]:


len(Review_all_list)


# In[82]:


# for review in Review_all_list:
#     star = review.find('span',attrs={'class':'a-icon-alt'}).text[:3]
#     title = review.find('a',attrs={'data-hook':'review-title'}).text
#     author = review.find('a',attrs={'data-hook':'review-author'}).text
#     date = review.find('span',attrs={'data-hook':'review-date'}).text
#     format_strip = review.find('a',attrs={'data-hook':'format-strip'}).text
#     review_body = review.find('span',attrs={'data-hook':'review-body'}).text
#     print(star)
#     print(title)
#     print(author)
#     print(date)
#     print(format_strip)
#     print(review_body)
    


# In[107]:


# a_list = driver.find_elements_by_tag_name('a')
# driver.execute_script('window.scrollBy(0,1600)')


# In[108]:


# next_bar = select_element_by_text(driver.find_elements_by_tag_name('a'),"Next→")


# In[109]:


# next_bar.click()


# In[27]:


df_reviews = pd.DataFrame(columns=['Rating','Title','Author','Date','Format','Review_body'])


# In[28]:


df_reviews


# In[50]:


review_count=0
page = 1
x=0
while(1):
    time.sleep(4)
    read = 0
    print(review_count)
    print(page)
    
    while(read!=10):
#         if page==1:
        url = driver.current_url
#     else:
#         url = 'https://www.amazon.com/RockBirds-Flashlights-Bright-Aluminum-Flashlight/product-reviews/B00X61AJYM/ref=cm_cr_getr_d_paging_btm_next_'+str(page)+'?reviewerType=avp_only_reviews&pageNumber='+str(page)+'&sortBy=recent'
        print(url)
        time.sleep(4)
        res = requests.get(url)

        time.sleep(4)
        soup = bs4.BeautifulSoup(res.text, 'html5lib')
        time.sleep(4)
        Review_all_list = soup.find_all('div', attrs={'data-hook': 'review'})
        read = len(Review_all_list)
    print(len(Review_all_list))
    for review in Review_all_list:
        star = review.find('span',attrs={'class':'a-icon-alt'}).text[:3]
        title = review.find('a',attrs={'data-hook':'review-title'}).text
        author = review.find('a',attrs={'data-hook':'review-author'}).text
        date = review.find('span',attrs={'data-hook':'review-date'}).text
        format_strip = review.find('a',attrs={'data-hook':'format-strip'}).text
        review_body = review.find('span',attrs={'data-hook':'review-body'}).text
#         print(star)
#         print(title)
#         print(author)
        
#         if "2018" in date:
#             print(date)
        if "2016" in date:
            x = 1
            break
#         print(format_strip)
#         print(review_body)
        Review_chunk = [star,title,author,date,format_strip,review_body]
        df_reviews.loc[review_count]=Review_chunk
        review_count = review_count+1
    if x:
        break
    driver.execute_script('window.scrollBy(0,1600)')
    next_bar = select_element_by_text(driver.find_elements_by_tag_name('a'),"Next→")
    next_bar.click()
    
    page = page + 1


# In[51]:


df_reviews


# In[52]:


df_reviews.to_csv('Reviews.csv')


# In[ ]:


df_reviews.to_json('reviews.json')

