# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, InvalidSessionIdException, \
    InvalidSelectorException, WebDriverException
import re
import pandas as pd
import numpy as np
import time
from selenium.webdriver.chrome.service import Service


from selenium.webdriver.common.by import By


class WebScraper:
    def scroll_to_bottom(self, driver):

        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
        # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            html = driver.page_source
        # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(12)
        html=  driver.page_source



    def indexExists(self,list, index):
        if 0 <= index < len(list):
            return True
        else:
            return False

    def Obtain_Links(self):

        #Instantiate an webdriver
        #Open the HTML page and its contents locally to be parsed
        with open("0x00sec - The Home of the Hacker.html",encoding="utf8") as f:
            soup = BeautifulSoup(f,'html')

        #Creating arrays and dictionary to store the URL and the
        thread_id = []
        webpage_url = []
        num_of_comments =[]
        data = {
            'URL ':[],
            'ThreadID':[],
            'Number of Comments':[]
        }

        #parsing and cleaning HTML text
        #Find all the a tags in the HTML
        for link in soup.find_all('a'):
            #For every string seperated with an href set it equal to variable href
            href = link.get('href')

            #If the href has a  /t in it get rid of it.
            if '/t' in href:

                #If there is /tag in the href
                if '/tag' not in href:
                    tags = href.split("/")
                #If there is a tag and theres the number of posts mentioned in the URL thread
                    if self.indexExists(tags,6) == True :

                        if tags not in thread_id:
                            num_of_comments.append(tags[6])
                            thread_id.append(tags[5])
                            webpage_url.append(href)
                            print(href)
        #Fit the data in to dictionary with an array of
        data['URL'] = webpage_url
        data['ThreadID'] = thread_id
        data['Number of Comments'] = num_of_comments
        csv_path = "0x00sec_data.csv"
        d = dict(  URL = np.array(data['URL']), ThreadID = np.array(data['ThreadID']), NumberOfComments = np.array(data['Number of Comments'])  )
        self.Dict_To_CSV(csv_path, d)

        return data
    def Dict_To_CSV(self,PATH, d):
        dict_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in d.items()]))
        dict_df.to_csv(PATH, index=False)




    def driver_scraper(self):

        PATH = "C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        os.environ['PATH'] += "C:/SeleniumDrivers"
        df = pd.read_csv('0x00sec_data.csv', index_col='URL')


        for column in df:
            url = str(df.iloc[i]['URL'])
            print(url)
            xpath_array = []
            driver.implicitly_wait(3)


            #/html/body/section/div/div[2]/div/div[5]/div[2]/div/div/div[2]/table/tbody/tr[1340]/td[1]/span/a



            #getting xpath info from posts and storing in array of xpaths
            match = False
            i = 1
            lenOfPage = 0
            lastCount = 0


            while i < 1340 and (match == False):
                i = i + 1




                 #   match = True
                        #/html/body/section/div/div[2]/div/div[5]/div[2]/div/div/div[2]/table/tbody/tr[5]/td[1]/span/a
                        #/html/body/section/div/div[2]/div/div[5]/div[2]/div/div/div[2]/table/tbody/tr[2]/td[1]/span/a
                path = "/html/body/section/div/div[2]/div/div[5]/div[2]/div/div/div[2]/table/tbody/tr["+ str(i)+"]/td[1]/span/a"
                try:

                    xpath =  driver.find_element_by_xpath(path)
                    xpath_array.append(xpath)  # /html/body/section/div/div[2]/div/div[5]/div[2]/div/div/div[2]/table/tbody/tr[4]/td[3]/button/span
                    title = xpath.accessible_name
                    time.sleep(1)

                except NoSuchElementException:
                    xpath = "na"
                    title = "na"
                try:
                    driver.find_element_by_xpath(path).click()
                except ElementClickInterceptedException:
                    xpath = "na"


                try:
                    num_of_posts = driver.find_element_by_xpath("/html/body/section/div/div[2]/div/div[5]/div[2]/div/div/div[2]/table/tbody/tr["+ str(i)+"]/td[3]/button/span").text
                    time.sleep(1)
                except NoSuchElementException:
                    num_of_posts = "na"
                try:
                    driver.find_element_by_xpath(path).click()
                except NoSuchElementException:
                    num_of_posts = "na"

                #/html/body/section/div/div[2]/div/div[5]/div[2]/div/div/div[2]/table/tbody/tr[4]/td[1]/span/a
                #/html/body/section/div/div[2]/div/div[5]/div[2]/div/div/div[2]/table/tbody/tr[3]/td[1]/span/a
                try:
                    time_of_post = driver.find_element_by_xpath("/html/body/section/div/div[2]/div/div[2]/div[3]/div[3]/section/div[1]/div[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/a/span").text
                except NoSuchElementException:
                    time_of_post = "na"

                try:
                    user = driver.find_element_by_xpath("/html/body/section/div/div[2]/div/div[2]/div[3]/div[3]/section/div[1]/div[2]/div/div[1]/article/div/div[2]/div[1]/div[1]/span/a").text
                except NoSuchElementException:
                    user = "na"
                try:
                    post = driver.find_element_by_class_name("cooked").text
                except NoSuchElementException:
                    post = "na"

                print(title)
                print(num_of_posts[4:])
                print(time_of_post)
                print(user)
                print(post)
                data = [str(title), str(time_of_post), str(num_of_posts[4:]), str(user), str(post), str(title)]

                driver.back()
        time.sleep(6000)

    def save_raw_HTML(self):

        PATH = "C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        os.environ['PATH'] += "C:/SeleniumDrivers"

        raw_html  = []
        #make a dataframe and read the csv file

        df = pd.read_csv("0x00sec_data.csv")
        data = {
            "Html Content" : []
         }
        for index, row in df.iterrows():
            try:
                url = row['URL']
                driver.get(url)
                html_content = driver.page_source
                print(html_content)
                raw_html.append(html_content)
            except WebDriverException:
                html_content = "NA"
                print(html_content)
                raw_html.append("NA")

        data["Html Content"] = raw_html
        csv_path = "html_content.csv"
        self.Dict_To_CSV(csv_path, data)







    def post_CSV(self):
        print("hello World")
        #get Threadid
        #parse table for number of posts





if __name__ == '__main__':
    webscraper = WebScraper()

    #webscraper.Obtain_Links()

    #webscraper.driver_scraper()
    df = pd.read_csv('0x00sec_data.csv', index_col='ThreadID')
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    #s = Service('C:/Users/Morteza/Documents/Dev/chromedriver.exe')
    driver = webdriver.Chrome(PATH)
    os.environ['PATH'] += "C:/SeleniumDrivers"



    raw_html = []
    # make a dataframe and read the csv file
    #csv to dataframe
    df = pd.read_csv("0x00sec_data.csv")

    #Keeping a dict of urls
    url_dict = df.to_dict()

    #Creating a dataframe to store the data of interest
    data = {
        "User ID": [],
        "Post ID": [],
        "Username": [],
        "Thread ID": [],
        "Post Content": [],
        "Date": []
    }

    #intializng important variables to be used later
    data_names = ["User ID","Post ID","Username", "Thread ID","Post Content", "Date"]
    csv_path = "0x00secUserData.csv"
    d = dict(PostContent=np.array(data['Post Content']), ThreadID=np.array(data['Thread ID']),Date=np.array(data['Date']), Username=np.array(data['Username']), UserID=np.array(data['User ID']),PostID=np.array(data['Post ID']))
    dict_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in d.items()]))
    dict_df.to_csv(csv_path, index=False)

    #The range from 1 all the way to the max number of html pages

    for i in range(5):
        #Open and click on the link given
        try:
            url = url_dict["URL"][i]
            driver.get(url)

            SCROLL_PAUSE_TIME = 0.5

            # Get scroll height
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                html = driver.page_source
                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            time.sleep(30)

            html_content = driver.page_source

            raw_html.append(html_content)
        except WebDriverException:
            html_content = "NA"
            raw_html.append("NA")
        #
        soup = BeautifulSoup(html_content, "html")



    #class="relative-date"": this contains the date of the post
    #class="cooked" (between p tags): contains the post content itself
    #data-topic-id: contains the posts thread id

        for post in soup.find_all('article', id=re.compile('^post_')):
            # data-usr-id: this contains the unique user id number for user on this site
            pattern = "<article aria-label=.*?</article>"
            match_results = re.search(pattern, str(post), re.IGNORECASE)
            print(post)

            pattern = "data-topic-id=.*?data"
            match_results = re.search(pattern, str(post), re.IGNORECASE)
            data_topic_id = match_results.group()

            print("\n")


            topic_id_num = [int(s) for s in re.findall(r'\b\d+\b', data_topic_id)]
            data["Thread ID"].append(topic_id_num)


            #print(topic_id_num)
           # data-post-id: this contains unique post id

            pattern = "data-post-id=.*?data"
            match_results = re.search(pattern, str(post), re.IGNORECASE)
            post_id = match_results.group()

            post_id_num = [int(s) for s in re.findall(r'\b\d+\b', post_id)]
            data["Post ID"].append(post_id_num)
            #print(post_id_num)


            #data-usr-id: this contains the unique user id number for user on this site
            pattern = "data-user-id=.*?id"
            match_results = re.search(pattern, str(post), re.IGNORECASE)
            data_user_id = match_results.group()
            data_user_id_num = [int(s) for s in re.findall(r'\b\d+\b', data_user_id)]
            data["User ID"].append(data_user_id_num)
            #print(data_user_id_num)

            # data-usr-card: this contains the username for each user
            pattern = "data-user-card=.*?href"
            match_results = re.search(pattern, str(post), re.IGNORECASE)
            data_user_card = match_results.group()
            username  = data_user_card.split('"')
            #print(username)
            data["Username"].append(username[1])


            pattern = 'data-time=.*?class="read-state read"'
            match_results = re.search(pattern, str(post), re.IGNORECASE)
            date_array = match_results.group()
            date = date_array.split('"')

            data["Date"].append(date[3])
            #print(date[3])

            #Getting the post  class="cooked" (between p tags): contains the post content itself
            try:
                post_content = post.find('p').getText()
            except AttributeError:
                post_content = "NA"

            #print(post_content)
            data["Post Content"].append(post_content)


    csv_path = "0x00secUserData.csv"
    df = pd.DataFrame.from_dict(data, orient='index').transpose()
    df.to_csv('0x00secUserData.csv')

























