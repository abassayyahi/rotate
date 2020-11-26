# Importing required libraries, obviously
from typing import Dict, List, Any, Union

import streamlit as st
from PIL import Image
import re
import numpy as np
from numpy import genfromtxt
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep, strftime
from random import randint
import pandas as pd
from bs4 import BeautifulSoup as b
import lxml
import datetime
from instapy import InstaPy
from instapy import smart_run
import base64
from io import BytesIO
import xlsxwriter
import csv


st.set_option('deprecation.showfileUploaderEncoding', False)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FF_DIR = os.path.join(BASE_DIR, 'geckodriver.exe')
CR_DIR = os.path.join(BASE_DIR, 'chromedriver.exe')
PH_DIR = os.path.join(BASE_DIR, 'phantomjs.exe')
IG_URL = 'https://instagram.com'
hashtag_list = ['تولیدی', 'رژلب', 'عمده']
prev_user_list = []  # - if it's the first time you run it, use this line and comment the two below
# prev_user_list = pd.read_csv('20200821-023713_users_followed_list.csv', delimiter=',').iloc[:,1:2] # useful to build a user log
# prev_user_list = list(prev_user_list['0'])

new_followed = []
tag = -1
followed = 0
likes = 0
comments = 0
bio_data2 = []
age = []
captions = ""
hashtags = ""
mentions = ""
post_details = {}
url = []
post_type = []
likes = []
age = []
captions = []
hashtags = []
mentions = []
cm_num = []
comms = []
hash_comm = []
ment_comm = []
data = []
user_id = ''
user_pass = ''

def about():
    st.write(
        '''
        **Professor Like** is a useful web application.
        It can be used to Scraping Instagram contents to collect post information like number of likes,comments, posts and etc.
        also you can grab information of users like hashtags, followers and following list, contents of post captions,comments and etc. 
        It is a part of our insta-bot.

        The Insta-bot has four Applications:

            1. Scraping Members Contents 
            2. Scraping Members Relationship network
            3. Automate tasks
            4. Get Real and Targeted Followers



If you want more visit our site :point_right: http://www.professorlike.ir .

To contact me please use my email :point_right: abassayyahi@gmail.com
        ''')


class BOT:
    def __init__(self):
        # options = Options()
        # options.headless = True
        # self.driver = webdriver.Firefox(options=options, executable_path=FF_DIR)

        # self.driver= webdriver.firefox(executable_path=FF_DIR)
        # options = webdriver.FirefoxOptions()
        # options.add_argument("headless")
        # self.driver = webdriver.PhantomJS(executable_path=PH_DIR)
        self.driver = webdriver.Firefox(executable_path=FF_DIR)
        # self.driver = webdriver.Chrome(executable_path=CR_DIR,)

    # instapy

    def login(self):
        self.driver.get(IG_URL)
        sleep(1)
        xpth = '/html/body/div[2]/div/div/div/div[2]/button[1]'
        if self.check_exists_by_xpath(xpth):
            self.driver.find_element_by_xpath(xpth).click()

        # except NoSuchElementException:
        #     return True
        # except TimeoutException:
        #     return True

        un_id = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.-MzZI:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)')))
        un_id.click()
        un_id.send_keys(user_id)

        pw_id = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.-MzZI:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)')))
        pw_id.click()
        pw_id.send_keys(user_pass)
        sleep(1)

        btn = self.driver.find_element_by_css_selector('.L3NKy > div:nth-child(1)')
        btn.click()
        sleep(5)
        # self.driver.Manage().Window.Size = newSize(240, 360)

        # self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button').click()
        # sleep(2)

    def auto(self):
        global tag, likes, comments, followed
        for hashtag in hashtag_list:
            tag += 1
            self.driver.get('https://www.instagram.com/explore/tags/' + hashtag_list[tag] + '/')
            sleep(5)
            first_thumbnail = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
            first_thumbnail.click()
            sleep(randint(1, 2))

            try:
                for x in range(1, 3):
                    username = self.driver.find_element_by_xpath(
                        '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a').text
                    print('user2= ', username)
                    if username not in prev_user_list:
                        # If we already follow, do not unfollow
                        if self.driver.find_element_by_xpath(
                                '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':

                            self.driver.find_element_by_xpath(
                                '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()

                            new_followed.append(username)
                            followed += 1

                            # Liking the picture
                            button_like = self.driver.find_element_by_xpath(
                                '/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button')

                            button_like.click()
                            likes += 1
                            sleep(randint(18, 25))

                            # Comments and tracker
                            comm_prob = randint(1, 10)
                            print('{}_{}: {}'.format(hashtag, x, comm_prob))
                            if comm_prob > 7:
                                comments += 1
                                self.driver.find_element_by_xpath(
                                    '/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[2]/button').click()
                                comment_box = self.driver.find_element_by_xpath(
                                    '/html/body/div[4]/div[2]/div/article/div[3]/section[3]/div/form/textarea')

                                if (comm_prob < 7):
                                    comment_box.send_keys('کیفیت عالی !')
                                    sleep(1)
                                elif (comm_prob > 6) and (comm_prob < 9):
                                    comment_box.send_keys('خوب بفروشی همکار عزیزم :)')
                                    sleep(1)
                                elif comm_prob == 9:
                                    comment_box.send_keys('ایول کارتون درسته همکار عزیز!!')
                                    sleep(1)
                                elif comm_prob == 10:
                                    comment_box.send_keys('خدا بده برکت، آمین :)')
                                    sleep(1)
                                # Enter to post comment
                                comment_box.send_keys(Keys.ENTER)
                                sleep(randint(22, 28))

                        # Next picture
                        self.driver.find_element_by_link_text('Next').click()
                        sleep(randint(25, 29))
                    else:
                        self.driver.find_element_by_link_text('Next').click()
                        sleep(randint(20, 26))
            # some hashtag stops refreshing photos (it may happen sometimes), it continues to the next
            except:
                continue

        for n in range(0, len(new_followed)):
            prev_user_list.append(new_followed[n])

        updated_user_df = pd.DataFrame(prev_user_list)
        updated_user_df.to_csv('{}_users_followed_list.csv'.format(strftime("%Y%m%d-%H%M%S")))
        # updated_user_df.to_csv('{}_users_followed_list.csv')

        print('Liked {} photos.'.format(likes))
        print('Commented {} photos.'.format(comments))
        print('Followed {} new people.'.format(followed))

    def get_page_information(self, page_id):
        page_url = 'https://www.instagram.com/' + page_id
        self.driver.get(page_url)
        # self.driver.find_element_by_class_name('ltEKP').
        # username = self.post.find_element_by_class_name('e1e1d').find_element_by_tag_name('a').text
        page_content = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main')))
        slfw = b(page_content.get_attribute('innerHTML'), 'html.parser')
        bio = slfw.findAll('div', {'class': '-vDIg'})
        bio_caption = bio[0].getText()
        # print('bio caption = ', bio_caption)
        numbers_bio = slfw.findAll('span', {'class': 'g47SY'})
        num_followers = numbers_bio[1].getText()
        num_following = numbers_bio[2].getText()
        num_post = numbers_bio[0].getText()
        bio_data = {'biography': bio_caption, 'post number': num_post,
                    'followers number': num_followers, 'following number': num_following}
        bio_data_df = pd.DataFrame(bio_data, index=[0])
        # print(bio_data_df)

        return bio_data_df

    def get_page_list_information(self, page_list):
        # behtare func ha joda amal konan bejaye edgham !!
        # mikham vaghti username vared mishe liste followerha va followingesh ro begire , bara harkodum biad une dune listeshun ro begire ba etelaat bio harkodoom
        # bio_data_df2 =pd.DataFrame(index=index, columns=columns)

        global bio_data
        bio_data2 = []
        for page in page_list:
            page_url = 'https://www.instagram.com/' + page
            self.driver.get(page_url)
            page_content = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main')))
            slfw = b(page_content.get_attribute('innerHTML'), 'html.parser')
            bio = slfw.findAll('div', {'class': '-vDIg'})
            bio_caption = bio[0].getText()
            # print('bio caption = ', bio_caption)
            numbers_bio = slfw.findAll('span', {'class': 'g47SY'})
            num_followers = numbers_bio[1].getText()
            num_following = numbers_bio[2].getText()
            num_post = numbers_bio[0].getText()
            bio_data = [num_post, num_followers, num_following, bio_caption]
            bio_data2.append(bio_data)

            # bio_data = {'biography': [bio_caption], 'post number': [num_post],
            #             'followers number': [num_followers], 'following number': [num_following]}
            # bio_data.update(bio_data)
            # bio_data_df = pd.DataFrame(bio_data, index=[0])
            # print('bio data2 is =====', bio_data2)

        return bio_data2

    def get_folowers_following(self, page_id):
        page_url = 'https://www.instagram.com/' + page_id
        self.driver.get(page_url)
        sleep(2)
        page_content = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main')))
        slfw = b(page_content.get_attribute('innerHTML'), 'html.parser')
        numbers_bio = slfw.findAll('span', {'class': 'g47SY'})
        followers_number = numbers_bio[1].getText()
        following_number = numbers_bio[2].getText()
        # followers_number = WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located(
        #         (By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span'))).text
        sleep(1)
        followers_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')))
        followers_btn.click()
        sleep(3)
        pup = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'isgrP')))
        last_height, current_height = 0, 1
        while last_height != current_height:
            sleep(2)
            last_height = current_height
            current_height = self.driver.execute_script("""
       			arguments[0].scrollTo(0, arguments[0].scrollHeight);
       			return arguments[0].scrollHeight;
       			""", pup)
        links = pup.find_elements_by_tag_name('a')
        links2 = links[0:(int(followers_number) - 1) * 2]
        # print('links 1 ta 12=', [name.text for name in links[0:12]], 'links2=', [name.text for name in links2], 'int ====', int(followers_number))
        # links_list_df = pd.DataFrame(links)
        # links_list_df.to_csv('links_list_df')

        followers_list = [name.text for name in links2 if name.text != '']
        # print('followers =', followers_list)
        # followers_list_df = pd.DataFrame(followers_list)
        # followers_list_df.to_csv('{}_followers_list_df.csv'.format(page_id))
        sleep(2)
        close_followers_window = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[4]/div/div/div[1]/div/div[2]/button')))
        close_followers_window.click()
        sleep(2)
        # following_number = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
        #     (By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span'))).text
        sleep(1)
        following_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a')))
        following_btn.click()
        sleep(3)
        last_height2, current_height2 = 0, 1
        while last_height2 != current_height2:
            sleep(2)
            pup2 = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'isgrP')))
            last_height2 = current_height2
            current_height2 = self.driver.execute_script("""
             			arguments[0].scrollTo(0, arguments[0].scrollHeight);
             			return arguments[0].scrollHeight;
             			""", pup2)
        links3 = pup2.find_elements_by_tag_name('a')
        links4 = links3[0:(int(following_number) - 1) * 2]
        following_list = [name.text for name in links4 if name.text != '']

        ### RESULT ####
        followers = followers_list
        following = following_list
        # print(followers)

        return followers, following

    def recent_post_links(self, page_id, post_count):
        """
        With the input of an account page, scrape the 10 most recent posts urls

        Args:
        username: Instagram username
        post_count: default of 10, set as many or as few as you want

        Returns:
        A list with the unique url links for the most recent posts for the provided user
        """
        page_url = 'https://www.instagram.com/' + page_id
        self.driver.get(page_url)
        sleep(1)
        post = 'https://www.instagram.com/p/'
        post_links = []
        while len(post_links) < post_count:
            links = [a.get_attribute('href')
                     for a in self.driver.find_elements_by_tag_name('a')]
            for link in links:
                if post in link and link not in post_links:
                    post_links.append(link)
            scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
            self.driver.execute_script(scroll_down)
            sleep(10)
        else:
            self.driver.stop_client()
            return post_links[:post_count]

    def insta_link_details(self, url):
        global captions, mentions, hashtags, post_details, df_ps_dt, data_2, likes, age, captions, hashtags, mentions, data

        self.driver.get(url)
        sleep(2)
        # self.driver.find_element_by_class_name('v1Nh3').click()
        sleep(3)
        try:
            # This captures the standard like count.
            likes = self.driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/button/span').text
            post_type = 'photo'
            sleep(2)
            # users_like = self.driver.find_element_by_xpath(
            #     '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/button').click()
            #
            # print('likes num :', likes)
        except:
            # This captures the like count for videos which is stored
            likes = self.driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/span').text
            post_type = 'video'
            sleep(2)
            # users_like =

        age = self.driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[2]/a/time').text
        # print('likes=====', likes, age)

        try:
            captions = self.driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span').text
            cap_splt = self.driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span').text.split()

            string = ''.join(cap_splt)
            hashtags = self.hashtags(string)
            mentions = self.mentions(string)
            # comments
            xpth = '/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul/li/div/button'
            chk_xpath = self.check_exists_by_xpath(xpth)
            comms = self.get_comments()
            cm_num = len(comms)
            hash_comm = self.hashtags(str(comms))
            ment_comm = self.mentions(str(comms))
            data = [url, post_type, likes, age, captions, hashtags,
                    mentions, cm_num, comms, hash_comm, ment_comm]

        finally:
            return data

    def caption_list(self, page_id, post_count=10):
        page_url = 'https://www.instagram.com/' + page_id
        self.driver.get(page_url)
        sleep(1)
        post = 'https://www.instagram.com/p/'
        post_links = []
        caption = []
        hashtags2 = []
        caption_temp = []
        while len(post_links) < post_count:
            links = [a.get_attribute('href')
                     for a in self.driver.find_elements_by_tag_name('a')]
            for link in links:
                if post in link and link not in post_links:
                    self.driver.get(link)
                    # hashtags = re.findall('#[A-Za-z]+', comment)
                    try:
                        caption_temp = self.driver.find_element_by_class_name('C4VMK').text
                        # hashtags = re.findall('#[A-Za-z]+', str(caption_temp))

                        # print('{}_cap_temp'.format(caption_temp))
                        sleep(2)
                    except:
                        continue

                    caption.append(caption_temp)
                    # hashtags = re.findall('#[A-Za-z]+', )
                    print('hashtags 2====', hashtags)

                    # hashtags.append(hashtags)
                    post_links.append(link)
            # scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
            # self.driver.execute_script(scroll_down)
            sleep(10)
            # Define dataframe to store hashtag information
            # tag_df = pd.DataFrame(columns=['Hashtag', 'Number of Posts', 'Posting Freq (mins)'])
            # print('tag df =', tag_df)
        else:
            post_links_df = pd.DataFrame(post_links[:post_count])
            caption_df = pd.DataFrame(caption[:post_count])
            caption_df.to_csv('{}_captions_df.csv'.format(page_id))

            print('hashtags ====', hashtags)
            self.driver.stop_client()
            return caption[:post_count], post_links[:post_count]

    def hashtag_caption(self, caption):
        sleep(5)
        # print('type of caption', type(caption))
        hashtags = re.findall('#[A-Za-z]+', caption)
        # with_s = [x for x in caption if x.startswith('#')]
        # without_s = [x for x in caption if x not in with_s]
        # print('with-s = ', with_s)
        # print('without-s = ', without_s)

        return hashtag

    def hashtags(self, string):
        hashtags = re.findall('#[A-Za-z0-9آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ\_\-]+', string)
        if (len(hashtags) > 1) & (len(hashtags) != 1):
            return hashtags
        elif len(hashtags) == 1:
            return hashtags[0]
        else:
            return ""

    def mentions(self, string):
        mentions = re.findall('@[A-Za-z0-9آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ\_\-]+', string)
        if (len(mentions) > 1) & (len(mentions) != 1):
            return mentions
        elif len(mentions) == 1:
            return mentions[0]
        else:
            return ""

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def get_comments(self):
        while self.check_exists_by_xpath("//div/ul/li/div/button"):
            load_more_comments_element = self.driver.find_element_by_xpath("//div/ul/li/div/button")
            load_more_comments_element.click()
            sleep(1)

        sleep(2)
        soup = b(self.driver.page_source, 'lxml')
        comms = soup.find_all('div', attrs={'class': 'C4VMK'})
        # print(len(comms))
        # comms_2 = soup.find('div', attrs={'class': 'C4VMK'}).children
        # print('children', comms_2)
        soup_2 = b(str(comms), 'lxml')
        spans = soup_2.find_all('span')
        comments = [i.text.strip() for i in spans if i != '']
        return comments

    def extract_followers(self, page_id):
        page_url = 'https://www.instagram.com/' + page_id
        self.driver.get(page_url)
        sleep(4)
        # try:
        #     user_link = "https://www.instagram.com/{}".format(username)
        #     web_adress_navigator(browser, user_link)
        # except PageNotFound404 as e:
        #     raise NoInstaProfilePageFound(e)
        # sleep(5)

        followers = []

        # find number of followers
        elem = self.driver.find_element_by_xpath(
            "//div[@id='react-root']//header[@class='vtbgv ']//ul[@class='k9GMp ']/child::li[2]/a/span")
        elem.click()
        sleep(15)

        # remove suggestion list and load 24 list elements after this
        self.driver.execute_script("document.getElementsByClassName('isgrP')[0].scrollTo(0,500)")

        sleep(10)

        elems = self.driver.find_elements_by_xpath(
            "//body//div[@class='PZuss']//a[@class='FPmhX notranslate  _0imsa ']")
        for i in range(12):
            val = elems[i].get_attribute('innerHTML')
            followers.append(val)

        for i in range(12):
            self.driver.execute_script("document.getElementsByClassName('PZuss')[0].children[0].remove()")

        isDone = False

        while 1:
            try:

                start = time()
                self.driver.execute_script(
                    "document.getElementsByClassName('isgrP')[0].scrollTo(0,document.getElementsByClassName('isgrP')[0].scrollHeight)")

                while 1:
                    try:
                        if int(self.driver.execute_script(
                                "return document.getElementsByClassName('PZuss')[0].children.length")) == 24:
                            break
                    except (KeyboardInterrupt, SystemExit):
                        # f.close()
                        raise
                    except:
                        continue
                    if time() - start > 10:
                        isDone = True
                        break

                if isDone:
                    break

                elems = self.driver.find_elements_by_xpath(
                    "//body//div[@class='PZuss']//a[@class='FPmhX notranslate  _0imsa ']")
                list_segment = ""
                for i in range(12):
                    val = elems[i].get_attribute('innerHTML')
                    list_segment += (val + '\n')
                    followers.append(val)

                for i in range(12):
                    self.driver.execute_script("document.getElementsByClassName('PZuss')[0].children[0].remove()")

                # InstaLogger.logger().info(time() - start)

            except (KeyboardInterrupt, SystemExit):
                # f.close()
                raise
            except:
                continue

        list_segment = ""
        elems = self.driver.find_elements_by_xpath(
            "//body//div[@class='PZuss']//a[@class='FPmhX notranslate  _0imsa ']")
        for i in range(len(elems)):
            val = elems[i].get_attribute('innerHTML')
            list_segment += (val + '\n')
            followers.append(val)

        return followers

    def get_table_download_link(self, df):
        """Generates a link allowing the data in a given panda dataframe to be downloaded
        in:  dataframe
        out: href string
        """
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
        return href

    def to_excel(self, df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        processed_data = output.getvalue()
        return processed_data

    def get_table_download_link2(self, df):
        """Generates a link allowing the data in a given panda dataframe to be downloaded
        in:  dataframe
        out: href string
        """
        val = self.to_excel(df)
        b64 = base64.b64encode(val)  # val looks like b'...'
        return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="professorlike.ir_extract.xlsx">Download csv file</a>'  # decode b'abc' => abc

    def login_instapy(self, page_id):
        # login credentials
        # insta_username = 'sohrab.simini'  # <- enter username here
        # insta_password = 'adamha'  # <- enter password here

        # get an InstaPy session!
        # set headless_browser=True to run InstaPy in the background
        session = InstaPy(username=user_id,
                          password=user_pass,
                          headless_browser=False)

        with smart_run(session, threaded=True):
            """ Activity flow """
            # general settings
            session.set_relationship_bounds(enabled=True,
                                            delimit_by_numbers=True,
                                            max_followers=4590,
                                            min_followers=45,
                                            min_following=77)

            session.set_dont_include(["friend1", "friend2", "friend3"])
            session.set_dont_like(["pizza", "#store"])
            followings = session.grab_followers(page_id, amount="full", live_match=True, store_locally=True)
            followers = session.grab_followers(page_id, amount="full", live_match=True, store_locally=True)
            df_followers = pd.DataFrame(followers)
            df_following = pd.DataFrame(followings)
            df_followers.to_csv('df_followers.csv')
            df_following.to_csv('df_following.csv')
            contact = followers + followings
            print('contact=======', contact)


def main():
    st.title("Welcome to ProfessorLike.IR :sunglasses: ")
    st.write("**(Made by Abbas Sayahi)**")

    activities = ["Home", "About"]
    choice = st.sidebar.selectbox("Pick something fun", activities)
    # st.checkbox("ddddd")

    if choice == "Home":
        st.write("Go to the About section from the sidebar to learn more about me.")
        # html = '    <a href="https://api.whatsapp.com/send?phone=15551234567">Send Message</a> '
        # st.components.v1.html(html, width=None, height=None, scrolling=False)

        global user_id, user_pass
        user_id = st.sidebar.text_input(':آیدی اینستاگرام خود را وارد نمایید و سپس اینتر را بزنید', value='',
                                        max_chars=None,
                                        key=None, type='default')
        user_pass = st.sidebar.text_input(' :رمز عبور اینستاگرام خود را وارد نمایید و سپس اینتر را بزنید', value='',
                                          max_chars=None,
                                          key=None, type='password')
        id_page = st.sidebar.text_input(' آیدی پیج را بدون @ وارد کنید و سپس اینتر را بزنید', value='eprofessorlike',
                                        max_chars=None,
                                        key=None, type='default')

        filename = st.sidebar.file_uploader("Choose a file", type=['xlsx', 'csv'])
        if filename is not None:
            delimiter_choice = st.sidebar.selectbox("In case you uploaded a CSV file, "
                                                    "how is your data delimited?", [';', ','])

            st.sidebar.markdown("---")

            # Function that tries to read file as a csv
            # if selected file is not a csv file then it will load as an excel file
            @st.cache
            def try_read_df(f):
                try:
                    return pd.read_csv(f, sep=delimiter_choice)
                except:
                    return pd.read_excel(f)

            if filename:
                df_pg_lst = try_read_df(filename)

            df_pg_lst.columns = ['names']
            col_one_list = df_pg_lst['names'].tolist()

            print(col_one_list)

        if id_page is not None:
            st.markdown('**Single processing :**')
            st.write(".ابتدا از قسمت سمت چپ آیدی را وارد نمایید")
            if st.button("Page information"):
                bt = BOT()
                bt.login()
                page_info = bt.get_page_information(id_page)
                flw_list = bt.get_folowers_following(id_page)
                df_flw = pd.DataFrame(flw_list)
                df_flw = df_flw.transpose()

                # df_flw =  df_flw.rename(columns={'0': 'Followers', '1' : 'Following'})
                df_flw.columns = ['Followers', 'Following']
                df_pg_inf = pd.DataFrame(page_info)
                df_pg_inf.to_csv('df_page_info.csv', encoding='utf-8-sig')
                df_scv = df_flw.to_csv('df_flw.csv', encoding='utf-8-sig')
                # st.dataframe(df_scv)
                st.markdown(bt.get_table_download_link2(df_pg_inf), unsafe_allow_html=True)
                st.markdown(bt.get_table_download_link2(df_flw), unsafe_allow_html=True)

                # print('post links======', post_links[0])
                # post_details= bt.recent_post_links(post_links[0])
                # bio_data_df.to_csv(f'{page_id}_biography_data.csv', encoding='utf-8-sig')
                # print(post_details)

            # if st.button('grab instapy'):
            #     bt = BOT()
            #     bt.login_instapy(id_page)

            # if st.button("FOLLOWERS"):
            #     bt = BOT()
            #     bt.login()
            #     followersss = bt.extract_followers(id_page)
            #     # print(followersss)

            # if st.button("Contact DATA"):
            #     bt = BOT()
            #     bt.login()
            #     flw_list = bt.get_folowers_following(id_page)
            #     sleep(2)
            #     df_flwr_list = pd.DataFrame(flw_list[0])
            #     df_flwing_list = pd.DataFrame(flw_list[1])
            #     followrs_information = bt.get_page_list_information(flw_list[0])
            #     df_follower = pd.DataFrame(followrs_information)
            #     sleep(2)
            #     follwing_information = bt.get_page_list_information(flw_list[1])
            #     df_following = pd.DataFrame(follwing_information)
            #     df_follower.insert(1, 'FI', 'followers')
            #     df_following.insert(1, 'FI', 'following')
            #     frames_followers = [df_flwr_list, df_follower]
            #     result_followers = pd.concat(frames_followers, axis=1)
            #     frames_following = [df_flwing_list, df_following]
            #     result_following = pd.concat(frames_following, axis=1)
            #     # print(result_following)
            #     result_followers.to_csv('FOLLOWER.csv', encoding='utf-8-sig')
            #     result_following.to_csv('FOLLOWing.csv', encoding='utf-8-sig')
            #     frames = [result_followers, result_following]
            #     result = pd.concat(frames, ignore_index=True)
            #     result.columns = ['Page_Id', 'Posts', 'Status', 'Followers', 'Following', 'Bio']
            #     result.to_csv("RESULT.csv", encoding='utf-8-sig')
            #     st.markdown(bt.get_table_download_link2(result_followers), unsafe_allow_html=True)
            #     st.markdown(bt.get_table_download_link2(result_following), unsafe_allow_html=True)
            #     st.markdown(bt.get_table_download_link2(result), unsafe_allow_html=True)

            # if st.button("Caption"):
            #     bt = BOT()
            #     bt.login()
            #     cap = bt.caption_list(id_page, 5)
            #     # print('cap', cap)
            #
            # if st.button("post links"):
            #     bt = BOT()
            #     bt.login()
            #     post_links = bt.recent_post_links(id_page, 10)
            #     # print('cap is ====', cap[0], 'post links are ==', cap[1])
            #     # hashtag_cap = bt.hashtag_caption(cap)
            #     # print('hashtags of captions are =', hashtag_cap)
            #     print(post_links)
            #
            # if st.button("bio"):
            #     capii = ['salam #amir has #tar #minoo saad']
            #
            #     hashtags = re.findall('#[A-Za-z]+', str(capii))
            #     print(hashtags)
            #     # bt = BOT()
            #     # bt.login()
            #     # posts = bt.get_followers_number(id_page)
            #
            # if st.button("email"):
            #     bt = BOT()
            #     bt.login()
            #     posts = bt.get_followers_number(id_page)

            if st.button('Posts DATA'):
                data_list = []
                bt = BOT()
                bt.login()

                # after collect post links make the below 5 lines into comment
                #
                post_links = bt.recent_post_links(id_page, 10)
                # print(post_links)
                # spl = np.array_split(np.array(post_links), 2)
                # np.savetxt("spl.csv", spl, delimiter=",", fmt='%s')
                # print("spl ===", spl)

                # my_spl = genfromtxt('spl.csv', delimiter=',')
                # my_data = list(my_spl)
                # print("my data =====", my_data)
                
                # with open('spl.csv', newline='') as f:
                #     reader = csv.reader(f)
                #     my_data = list(reader)

                # print("my data =====", my_data)
                # chunks = [post_links[10 * i:10 * (i + 1)] for i in range(len(post_links) / 10 + 1)]
                # print("chunks ===", chunks)

                # for i in range(len(spl)):
                # for link in my_data[1]:
                for link in post_links:
                    pst_dts = bt.insta_link_details(link)
                    data_list.append(pst_dts)
                # print('data_list =====', data_list)
                df_dt = pd.DataFrame(data=data_list, columns=['link', 'type', 'likes/views', 'age', 'caption',
                                                              'hashtags', 'mentions', 'comments number', 'comments',
                                                              'hashtags in comments', 'mentions in comments'])
                df_dt.to_csv('{}_df_dt.csv'.format(id_page), encoding='utf-8-sig')
                st.markdown(bt.get_table_download_link2(df_dt), unsafe_allow_html=True)

            # if st.button("Trusted Friends"):
            #     bt = BOT()
            #     bt.login()
            #     trusted = bt.get_following(id_page)
            #     print(trusted)

            st.markdown('**Mass processing :**')
            st.write(".ابتدا از قسمت سمت چپ فایل محتوی آیدی ها را آپلود نمایید")

            if st.button("PAGE LIST INFO"):
                bt = BOT()
                bt.login()
                # page_list = ['rezagolzar', 'mahnaz_afshar', 'mehranmodiri', 'reyhaneparsaj']
                page_information = bt.get_page_list_information(col_one_list)
                df_page_information = pd.DataFrame(page_information)
                df_page_information.to_csv("df_page_information.csv", encoding='utf-8-sig')
                st.markdown(bt.get_table_download_link2(df_page_information), unsafe_allow_html=True)

            if st.button('Posts DATA of PAGES List'):
                bt = BOT()
                bt.login()
                for id in col_one_list:
                    data_list = []
                    post_links = bt.recent_post_links(id, 3)
                    print(post_links)
                    for link in post_links:
                        post_details = bt.insta_link_details(link)
                        data_list.append(post_details)
                    # print('data_list =====', data_list)
                    df_dt = pd.DataFrame(data=data_list, columns=['link', 'type', 'likes/views', 'age', 'caption',
                                                                  'hashtags', 'mentions', 'comments number', 'comments',
                                                                  'hashtags in comments', 'mentions in comments'])
                    df_dt.to_csv('{}_df_dt.csv'.format(id), encoding='utf-8-sig')
                    st.markdown(bt.get_table_download_link2(df_dt), unsafe_allow_html=True)

        # file_buffer = st.file_uploader("Upload image", type=['jpeg', 'png', 'jpg', 'webp'])
        # image_file = io.TextIOWrapper(file_buffer)
        # image_file = st.file_uploader("Upload image", type=['jpeg', 'png', 'jpg', 'webp'])

        # if image_file is not None:
        #
        #     image = Image.open(image_file)
        #     if st.button("Show"):
        #         st.image(image, use_column_width=True)
        st.sidebar.markdown("<h1 style='text-align: center; color: red;'>نکات مهم</h1>", unsafe_allow_html=True)
        st.sidebar.info('باتوجه به محدودیتهای اینستاگرام '
                        'استخراج اطلاعات تنها با لاگین کردن امکان پذیر است\n'
                        '\nسفارش پروژه اختصاصی :point_right: [Professorlike]('
                        ' mailto:eprofessorlike@gmail.com).\n\n'
                        'خرید فالوئر واقعی و هدفمند: http://www.professorlike.ir')






    elif choice == "About":
        about()


if __name__ == "__main__":
    main()
