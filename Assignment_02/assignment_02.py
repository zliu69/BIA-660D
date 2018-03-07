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

# In[2]:


driver = webdriver.Firefox(executable_path=r"geckodriver.exe")
driver.get('http://www.mlb.com')
wait = WebDriverWait(driver, 10)
stats_header_bar = wait.until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'megamenu-navbar-overflow__menu-item-link--stats')))
normal_delay = random.normalvariate(2, 0.5)
time.sleep(normal_delay)
ActionChains(driver).move_to_element(stats_header_bar).perform()

# In[3]:


time.sleep(15)
stats_header_bar.click()
# stats_line_items = stats_header_bar.find_elements_by_tag_name('li')
# [li.text for li in stats_line_items]


# In[4]:


time.sleep(5)
hitting_season_element = driver.find_element_by_id('sp_hitting_season')
season_select = Select(hitting_season_element)

# In[5]:


season_select.select_by_value('2015')

# In[6]:


time.sleep(5)
hitting_game_element = driver.find_element_by_id('sp_hitting_game_type')
game_select = Select(hitting_game_element)
game_select.select_by_visible_text('Regular Season')

# In[7]:


time.sleep(5)
team_bar = driver.find_element_by_id('st_parent')
team_bar.click()

# In[8]:


import pandas as pd
import requests
import bs4

# In[9]:


time.sleep(5)
data_div = driver.find_element_by_id('datagrid')
data_html = data_div.get_attribute('innerHTML')
soup = bs4.BeautifulSoup(data_html, "html5lib")
head = [t.text.replace("▼", "") for t in soup.thead.find_all("th")]
df_home_run = pd.DataFrame(columns=head)

# In[10]:


context_table_q1 = []
for t in soup.tbody.find_all("tr"):
    for a in t.find_all("td"):
        context_table_q1.append(a.text)

# In[11]:


context_table_q1_prettify = []
for i in range(int(len(context_table_q1) / len(head))):
    s = context_table_q1[i * len(head): (i + 1) * len(head)]
    context_table_q1_prettify.append(s)

# In[12]:


context_table_q1_prettify
for i in range(30):
    df_home_run.loc[i] = context_table_q1_prettify[i]

df_home_run.drop("", axis=1)

# In[13]:


df_home_run.drop("", axis=1).to_csv('Question_1.csv')

# In[14]:


df_home_run.sort_values(by=['HR'], ascending=False)
# df_home_run.sort_values(by = ['HR'])


# In[15]:


max_hr_team_name = df_home_run.iloc[1, 1]
max_hr_team_name

# In[16]:


AL_bar = driver.find_element_by_css_selector(
    '#st_hitting-0 > fieldset:nth-child(2) > label:nth-child(4) > span:nth-child(1)')
AL_bar.click()

# In[17]:


time.sleep(5)
data_div_AL = driver.find_element_by_id('datagrid')
data_html_AL = data_div_AL.get_attribute('innerHTML')
soup_AL = bs4.BeautifulSoup(data_html_AL, "html5lib")
head_AL = [t.text.replace("▼", "") for t in soup_AL.thead.find_all("th")]
df_home_run_AL = pd.DataFrame(columns=head_AL)

# In[18]:


context_table_q2_a_AL = []
for t in soup_AL.tbody.find_all("tr"):
    for a in t.find_all("td"):
        context_table_q2_a_AL.append(a.text)

context_table_q2_a_AL_prettify = []
for i in range(int(len(context_table_q2_a_AL) / len(head_AL))):
    s = context_table_q2_a_AL[i * len(head_AL): (i + 1) * len(head_AL)]
    context_table_q2_a_AL_prettify.append(s)

context_table_q2_a_AL_prettify
for i in range(15):
    df_home_run_AL.loc[i] = context_table_q2_a_AL_prettify[i]

df_home_run_AL.drop("", axis=1).to_csv('Question_2_a_AL.csv')

# In[19]:


time.sleep(10)
NL_bar = driver.find_element_by_css_selector(
    '#st_hitting-0 > fieldset:nth-child(2) > label:nth-child(6) > span:nth-child(1)')
NL_bar.click()

# In[20]:


time.sleep(5)
data_div_NL = driver.find_element_by_id('datagrid')
data_html_NL = data_div_NL.get_attribute('innerHTML')
soup_NL = bs4.BeautifulSoup(data_html_NL, "html5lib")
head_NL = [t.text.replace("▼", "") for t in soup_NL.thead.find_all("th")]
df_home_run_NL = pd.DataFrame(columns=head_NL)

context_table_q2_a_NL = []
for t in soup_NL.tbody.find_all("tr"):
    for a in t.find_all("td"):
        context_table_q2_a_NL.append(a.text)

context_table_q2_a_NL_prettify = []
for i in range(int(len(context_table_q2_a_NL) / len(head_NL))):
    s = context_table_q2_a_NL[i * len(head_NL): (i + 1) * len(head_NL)]
    context_table_q2_a_NL_prettify.append(s)

for i in range(15):
    df_home_run_NL.loc[i] = context_table_q2_a_NL_prettify[i]

df_home_run_NL.drop("", axis=1).to_csv('Question_2_a_NL.csv')

# In[21]:


time.sleep(10)
# home_run_AL_a_mean = df_home_run_AL.groupby('HR').mean()
# # home_run_AL_a_mean.mean(axis = 1)
AL_data = pd.read_csv('Question_2_a_AL.csv')
AL_mean_q2_a = AL_data['HR'].mean()
NL_data = pd.read_csv('Question_2_a_NL.csv')
NL_mean_q2_a = NL_data['HR'].mean()
if AL_mean_q2_a >= NL_mean_q2_a:
    print("American League average home run : ", AL_mean_q2_a)
else:
    print("Nation League average home run : ", NL_mean_q2_a)

# In[22]:


AL_bar = driver.find_element_by_css_selector(
    '#st_hitting-0 > fieldset:nth-child(2) > label:nth-child(4) > span:nth-child(1)')
AL_bar.click()

# In[23]:


time.sleep(5)
hitting_splits_element = driver.find_element_by_id('st_hitting_hitting_splits')
splits_select = Select(hitting_splits_element)
splits_select.select_by_visible_text('First Inning')

# In[24]:


time.sleep(5)
data_div_AL = driver.find_element_by_id('datagrid')
data_html_AL = data_div_AL.get_attribute('innerHTML')
soup_AL = bs4.BeautifulSoup(data_html_AL, "html5lib")
head_AL = [t.text.replace("▼", "") for t in soup_AL.thead.find_all("th")]
df_home_run_AL_b = pd.DataFrame(columns=head_AL)

context_table_q2_a_AL = []
for t in soup_AL.tbody.find_all("tr"):
    for a in t.find_all("td"):
        context_table_q2_a_AL.append(a.text)

context_table_q2_a_AL_prettify = []
for i in range(int(len(context_table_q2_a_AL) / len(head_AL))):
    s = context_table_q2_a_AL[i * len(head_AL): (i + 1) * len(head_AL)]
    context_table_q2_a_AL_prettify.append(s)

context_table_q2_a_AL_prettify
for i in range(15):
    df_home_run_AL_b.loc[i] = context_table_q2_a_AL_prettify[i]

df_home_run_AL_b.drop("", axis=1).to_csv('Question_2_b_AL.csv')

# In[25]:


NL_bar = driver.find_element_by_css_selector(
    '#st_hitting-0 > fieldset:nth-child(2) > label:nth-child(6) > span:nth-child(1)')
NL_bar.click()
time.sleep(5)
hitting_splits_element = driver.find_element_by_id('st_hitting_hitting_splits')
splits_select = Select(hitting_splits_element)
splits_select.select_by_visible_text('First Inning')

# In[26]:


data_div_NL = driver.find_element_by_id('datagrid')
data_html_NL = data_div_NL.get_attribute('innerHTML')
soup_NL = bs4.BeautifulSoup(data_html_NL, "html5lib")
head_NL = [t.text.replace("▼", "") for t in soup_NL.thead.find_all("th")]
df_home_run_NL_b = pd.DataFrame(columns=head_NL)

context_table_q2_a_NL = []
for t in soup_NL.tbody.find_all("tr"):
    for a in t.find_all("td"):
        context_table_q2_a_NL.append(a.text)

context_table_q2_a_NL_prettify = []
for i in range(int(len(context_table_q2_a_NL) / len(head_NL))):
    s = context_table_q2_a_NL[i * len(head_NL): (i + 1) * len(head_NL)]
    context_table_q2_a_NL_prettify.append(s)

for i in range(15):
    df_home_run_NL_b.loc[i] = context_table_q2_a_NL_prettify[i]

df_home_run_NL_b.drop("", axis=1).to_csv('Question_2_b_NL.csv')

# In[27]:


time.sleep(10)
# # home_run_AL_a_mean.mean(axis = 1)
AL_data_b = pd.read_csv('Question_2_b_AL.csv')
AL_mean_q2_b = AL_data_b['HR'].mean()
NL_data_b = pd.read_csv('Question_2_b_NL.csv')
NL_mean_q2_b = NL_data_b['HR'].mean()
if AL_mean_q2_b >= NL_mean_q2_b:
    print("American League average home run first inning : ", AL_mean_q2_b)
else:
    print("Nation League average home run first inning : ", NL_mean_q2_b)

# In[28]:


game_select.select_by_visible_text('Regular Season')

# In[29]:


splits_select.select_by_visible_text('Select Split')
time.sleep(5)

# In[30]:


hitting_season_element = driver.find_element_by_id('st_hitting_season')
season_select = Select(hitting_season_element)
season_select.select_by_value('2017')
time.sleep(5)

# In[31]:


Player_bar = driver.find_element_by_id('sp_parent')

# In[32]:


Player_bar.click()

# In[33]:


time.sleep(5)
MLB_bar = driver.find_element_by_css_selector(
    '#sp_hitting-1 > fieldset:nth-child(1) > label:nth-child(2) > span:nth-child(1)')
MLB_bar.click()
time.sleep(5)
team_name_element = driver.find_element_by_id('sp_hitting_team_id')
time.sleep(5)
team_select = Select(team_name_element)
time.sleep(5)
team_select.select_by_visible_text('New York Yankees')

# In[34]:


time.sleep(5)
data_div_NYY = driver.find_element_by_id('datagrid')

data_html_NYY = data_div_NYY.get_attribute('innerHTML')
data_html_NYY
soup_NYY = bs4.BeautifulSoup(data_html_NYY, 'html5lib')
head_NYY = [t.text.replace("▼", "") for t in soup_NYY.thead.find_all("th")]

df_NYY = pd.DataFrame(columns=head_NYY)

NYY_all = []
for lines in soup_NYY.tbody.find_all('tr'):
    for elements in lines.find_all('td'):
        NYY_all.append(elements.text)

NYY_all_format = []
for i in range(int(len(NYY_all) / len(head_NYY))):
    str = NYY_all[i * len(head_NYY):(i + 1) * len(head_NYY)]
    NYY_all_format.append(str)

NYY_all_format

for j in range(44):
    df_NYY.loc[j] = NYY_all_format[j]

df_NYY = df_NYY.drop("▲", axis=1)
df_NYY = df_NYY.drop("", axis=1)

df_NYY.to_csv('Question_3.csv')

# In[35]:


NYY_player_data = pd.read_csv('Question_3.csv')
# players_over30 = []
# for lines in df_NYY:
#     if lines['AB'] >=30 :
#         players_over30.append(lines)
NYY_player_data

# In[36]:


max = 0.0
for i in range(44):
    if NYY_player_data.loc[i]['AB'] >= 30:
        if float(NYY_player_data.loc[i]['AVG']) >= max:
            max_AB_player = NYY_player_data.loc[i]['Player']
            max_AB_player_pos = NYY_player_data.loc[i]['Pos']
            max = float(NYY_player_data.loc[i]['AVG'])

# In[37]:


player_name = max_AB_player.split(',')[0][1:]

# In[38]:


time.sleep(10)
active_player_search_div = driver.find_element_by_id('active-player-search')
ActionChains(driver).move_to_element(active_player_search_div).click().perform()
active_player_search_input = active_player_search_div.find_element_by_tag_name('input')

time.sleep(5)
ActionChains(driver).move_to_element(active_player_search_input).click().perform()
active_player_search_input.send_keys(player_name)

time.sleep(10)
search_results = active_player_search_div.find_elements_by_tag_name('li')
time.sleep(5)
ActionChains(driver).move_to_element(search_results[0]).click().perform()

# In[39]:


time.sleep(5)
full_name_bar = driver.find_element_by_class_name('full-name')
print('Full name of best overall batting average in the 2017 regular season is : ', full_name_bar.text, ', Pos: ',
      max_AB_player_pos)

# In[40]:


driver.back()

# In[41]:


NYY_player_data

# In[42]:


max_outfield = 0.0

for i in range(44):
    if NYY_player_data.loc[i]['Pos'] == 'LF' or NYY_player_data.loc[i]['Pos'] == 'RF' or NYY_player_data.loc[i][
        'Pos'] == 'CF':

        if NYY_player_data.loc[i]['AVG'][1:].isdigit():

            if float(NYY_player_data.loc[i]['AVG']) >= max_outfield:
                max_AB_player_outfield = NYY_player_data.loc[i]['Player']
                max_AB_player_pos_outfield = NYY_player_data.loc[i]['Pos']
                max_outfield = float(NYY_player_data.loc[i]['AVG'])

print(max_AB_player_outfield)

# In[43]:


max_AB_player_name = max_AB_player_outfield.split(',')[0][1:]
max_AB_player_name

# In[44]:


active_player_search_div = driver.find_element_by_id('active-player-search')
ActionChains(driver).move_to_element(active_player_search_div).click().perform()
time.sleep(5)
active_player_search_input = active_player_search_div.find_element_by_tag_name('input')

time.sleep(5)
ActionChains(driver).move_to_element(active_player_search_input).click().perform()
active_player_search_input.send_keys(max_AB_player_name)
time.sleep(5)
search_results = active_player_search_div.find_elements_by_tag_name('li')
time.sleep(5)
ActionChains(driver).move_to_element(search_results[0]).click().perform()
time.sleep(5)
full_name_bar = driver.find_element_by_class_name('full-name')
print('Full name of best overall batting average in the 2017 regular season played outfield  is : ', full_name_bar.text,
      ', Pos: ', max_AB_player_pos_outfield)

# In[45]:


driver.back()

# In[46]:


time.sleep(10)
# soup = bs4.BeautifulSoup(driver.find_element_by_id('sp_hitting').get_attribute('innerHTML'), 'html5lib')
AL_bar = driver.find_element_by_css_selector(
    '#sp_hitting-1 > fieldset:nth-child(1) > label:nth-child(4) > span:nth-child(1)')
AL_bar.click()

# In[47]:


time.sleep(5)
team_name_element = driver.find_element_by_id('sp_hitting_team_id')
team_select = Select(team_name_element)
team_select.select_by_visible_text('All Teams')

# In[48]:


time.sleep(5)
hitting_season_element = driver.find_element_by_id('sp_hitting_season')
season_select = Select(hitting_season_element)
season_select.select_by_value('2015')

# In[49]:


time.sleep(10)
data_div_all = driver.find_element_by_id('datagrid')

data_html_all = data_div_all.get_attribute('innerHTML')
data_html_all
soup_all = bs4.BeautifulSoup(data_html_all, 'html5lib')
head_all = [t.text.replace("▼", "") for t in soup_all.thead.find_all("th")]

df_all = pd.DataFrame(columns=head_all)

data_all = []
for lines in soup_all.tbody.find_all('tr'):
    for elements in lines.find_all('td'):
        data_all.append(elements.text)

data_all_format = []
for i in range(int(len(data_all) / len(head_all))):
    str = data_all[i * len(head_all):(i + 1) * len(head_all)]
    data_all_format.append(str)

for j in range(50):
    df_all.loc[j] = data_all_format[j]

# In[50]:


for x in range(11):
    next_bar = driver.find_element_by_css_selector('.paginationWidget-next')
    next_bar.click()
    time.sleep(8)

    data_div_all = driver.find_element_by_id('datagrid')

    data_html_all = data_div_all.get_attribute('innerHTML')

    soup_all = bs4.BeautifulSoup(data_html_all, 'html5lib')
    data_all = []
    for lines in soup_all.tbody.find_all('tr'):
        for elements in lines.find_all('td'):
            data_all.append(elements.text)

    data_all_format = []
    for i in range(int(len(data_all) / len(head_all))):
        str = data_all[i * len(head_all):(i + 1) * len(head_all)]
        data_all_format.append(str)
    if x == 10:
        for j in range(49):
            df_all.loc[(x + 1) * 50 + j] = data_all_format[j]
    else:
        for j in range(50):
            df_all.loc[(x + 1) * 50 + j] = data_all_format[j]

# In[51]:


df_all = df_all.drop("▲", axis=1)
df_all = df_all.drop("", axis=1)

# In[52]:


df_all

# In[53]:


time.sleep(5)
df_all.to_csv('Question_4.csv')
all_player_data = pd.read_csv('Question_4.csv')

# In[54]:


all_player_data = all_player_data.sort_values(by=['AB'], ascending=False)

# In[55]:


all_player_data = all_player_data.drop('Unnamed: 0', axis=1)

# In[56]:


maxAB_all_player_name = all_player_data.iloc[0, 1:2][0].split(',')[0][1:]
maxAB_all_player_name

# In[57]:


maxAB_all_player_team_name = all_player_data.iloc[0, 2:3][0]
if maxAB_all_player_team_name == 'HOU':
    maxAB_all_player_team_name = 'Houston'
maxAB_all_player_pos = all_player_data.iloc[0, 3:4][0]

# In[58]:


js = "var q=document.documentElement.scrollTop=0"
driver.execute_script(js)
time.sleep(3)
active_player_search_div = driver.find_element_by_id('active-player-search')

ActionChains(driver).move_to_element(active_player_search_div).click().perform()
time.sleep(5)
active_player_search_input = active_player_search_div.find_element_by_tag_name('input')
time.sleep(5)
ActionChains(driver).move_to_element(active_player_search_input).click().perform()
active_player_search_input.send_keys(maxAB_all_player_name)
time.sleep(5)
search_results = active_player_search_div.find_elements_by_tag_name('li')
time.sleep(5)
ActionChains(driver).move_to_element(search_results[0]).click().perform()
time.sleep(5)
full_name_bar = driver.find_element_by_class_name('full-name')
time.sleep(5)
print('Full name of the player in the American League had the most at bats in the 2015 regular season is : ',
      full_name_bar.text, ", team name is : ", maxAB_all_player_team_name, ", Pos : ", maxAB_all_player_pos)

# In[59]:


driver.back()

# In[60]:


time.sleep(8)
hitting_season_element = driver.find_element_by_id('sp_hitting_season')
season_select = Select(hitting_season_element)
season_select.select_by_value('2014')

# In[61]:


time.sleep(8)
hitting_game_element = driver.find_element_by_id('sp_hitting_game_type')
game_select = Select(hitting_game_element)
game_select.select_by_visible_text('All-Star Game')

# In[62]:


time.sleep(8)
MLB_bar = driver.find_element_by_css_selector(
    '#sp_hitting-1 > fieldset:nth-child(1) > label:nth-child(2) > span:nth-child(1)')
MLB_bar.click()

# In[63]:


time.sleep(8)
data_div_all_star = driver.find_element_by_id('datagrid')

data_html_all_star = data_div_all_star.get_attribute('innerHTML')

soup_all_star = bs4.BeautifulSoup(data_html_all_star, 'html5lib')
head_all_star = [t.text.replace("▼", "") for t in soup_all_star.thead.find_all("th")]

df_all_star = pd.DataFrame(columns=head_all_star)

data_all_star = []
for lines in soup_all_star.tbody.find_all('tr'):
    for elements in lines.find_all('td'):
        data_all_star.append(elements.text)

data_all_star_format = []
for i in range(int(len(data_all_star) / len(head_all_star))):
    str = data_all_star[i * len(head_all_star):(i + 1) * len(head_all_star)]
    data_all_star_format.append(str)

for j in range(41):
    df_all_star.loc[j] = data_all_star_format[j]

df_all_star

# In[64]:


df_all_star = df_all_star.drop("▲", axis=1)
df_all_star = df_all_star.drop("", axis=1)

# In[65]:


df_all_star.to_csv('Question_5.csv')

# In[66]:


latin_coun = '''Argentina;Bolivia;Brazil;Chile;Colombia;Costa Rica;Cuba;Dominican Republic;Ecuador;El Salvador;French Guiana;Guadeloupe;Guatemala;Haiti;Honduras;Martinique;Mexico;Nicaragua;Panama;Paraguay;Peru;Puerto Rico;Saint Barthélemy;Saint Martin;Uruguay;Venezuela'''
latin_list = latin_coun.split(';')

# In[67]:


name_list = []
data_div_all_star = driver.find_element_by_id('datagrid')

data_html_all_star = data_div_all_star.get_attribute('innerHTML')

soup_all_star = bs4.BeautifulSoup(data_html_all_star, 'html5lib')
for name in soup_all_star.tbody.find_all('a'):
    z = 0
    if len(name_list) == 0:
        name_list.append(name.text)
    else:
        for i in range(len(name_list)):
            if name.text == name_list[i]:
                z = 1
        if z == 0:
            name_list.append(name.text)

name_list

# In[68]:


data_q5 = []
for name in name_list:
    player_bar = driver.find_elements_by_link_text(name)
    for k in range(len(player_bar)):

        print(name)
        time.sleep(3)
        player_bar_temp = driver.find_elements_by_link_text(name)
        player_bar_temp[k].click()
        player_bio = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'player-bio')))
        #             player_info = player_bio.find_elements_by_tag_name('li')

        #             for j in range(len(player_info)):
        #                 x = player_info[j].find_elements_by_tag_name('span')
        #                 for num in range(len(x)):
        #                     if x[num].text =='Born:':
        for country in latin_list:
            if country in player_bio.text:
                #                                         print(player_info[j].text)
                player_name = driver.find_element_by_class_name('full-name').text
                datahtml = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'dropdown.team'))).text
                team_name = datahtml.split('\n')[0].strip()
                print('player_name:', player_name)
                data_q5.append(player_name)
                print('team_name:', team_name)
                data_q5.append(team_name)

        time.sleep(5)
        driver.back()

# In[69]:


time.sleep(3)
js = "var q=document.documentElement.scrollTop=0"
driver.execute_script(js)
time.sleep(3)

# In[70]:


data_q5

# In[71]:


head_q5 = ['Player', 'Team']
df_q5 = pd.DataFrame(columns=head_q5)

# In[72]:


data_q5_format = []
for i in range(int(len(data_q5) / len(head_q5))):
    data_q5_format.append(data_q5[i * len(head_q5): (i + 1) * len(head_q5)])

for j in range(16):
    df_q5.loc[j] = data_q5_format[j]

df_q5

# In[73]:


df_q5.to_csv('Question_5_answer.csv')

# In[74]:


import http.client, urllib.request, urllib.parse, urllib.error, base64

# In[75]:


import json


# In[76]:


def api(html):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '50dd039638564f8687b0961e2df52ed7',
    }
    conn = http.client.HTTPSConnection('api.fantasydata.net')
    conn.request("GET", html, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close
    return data


# In[77]:


data_stats_stadium = api("/v3/mlb/stats/json/Stadiums")
time.sleep(5)
data_stats_stadium = json.loads(data_stats_stadium)
data_stats_stadium

# In[78]:


match_info = []
for i in data_stats_stadium:
    match_info.append([i["StadiumID"], i["Name"], i["City"], i["State"]])

match_info

# In[79]:


data_stats_game = json.loads(api("/v3/mlb/stats/json/Games/2016"))
data_stats_game

# In[80]:


time.sleep(5)
game_info = []
for i in data_stats_game:
    game_info.append([i["HomeTeam"], i["AwayTeam"], i["DateTime"][0:10], i["StadiumID"]])

game_info

# In[81]:


general_info = []

for i in match_info:
    for j in game_info:
        if i[0] == j[3]:
            temp = j[:-1] + i[1:]
            general_info.append(temp)

general_info

# In[82]:


data_q6 = []
for a in general_info:

    if 'HOU' in a:
        data_q6.append(a)

data_q6

# In[84]:


time.sleep(5)
df_q6 = pd.DataFrame(columns=['Home Team', 'Away Team', 'Date', 'Stadium Name', 'City', 'State'])

for i in range(len(data_q6)):
    df_q6.loc[i] = data_q6[i]

df_q6

# In[85]:


df_q6.to_csv('Question_6.csv')

# In[86]:


df_q6.to_json('Question_6_Games_Stadiums.json')

