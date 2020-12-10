
import os, sys

# path to parents module
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# setting up selenium environment
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# to wait server response
import time

# custom json handler
import json_account_handler

# path to chrome driver
DRIVER_PATH = f"{parentdir}/chromedriver/chromedriver"

class ModdleScraper(object):
    def __init__(self,*,json_handler, json_key, lecture_login_url):
    
        JSON_Account_Handler = json_account_handler.JSON_Account_Handler
        if isinstance(json_handler, JSON_Account_Handler) == False:
            raise TypeError("json_handler is not an instance of JSON_Account_Handler")
        data = json_handler.data
    
        # setting up class attributes            
        self.browser = None
        self.__verbose = []
        
        # initial login page
        self.lecture_login_url = lecture_login_url
        
        # injecting userdata form json
        self.username = data[json_key][0].get('username')
        self.password = data[json_key][0].get('password')
        
        
        ModdleScraper.__driver_setup(self)
        ModdleScraper.__login_with_json_data_and_scrape(self)
        
    def __driver_setup(self):
        try:
            self.browser = webdriver.Chrome(executable_path=DRIVER_PATH)
        except:
            print(f"automation browser cannot be initialized , error:{len(self.__verbose)}")

    
    def __login_with_json_data_and_scrape(self):
        browser = self.browser
        
        lecture_login_url = self.lecture_login_url
        login_page = browser.get(lecture_login_url)
        
        # scraping url datas
        username_input = browser.find_element_by_id("username")
        password_input = browser.find_element_by_id("password")
        login_button = browser.find_element_by_id("loginbtn")
        
        # sending inputs to login page
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        
        # clicking the login button
        login_button.click()
        
        content_list = browser.find_element_by_id("pc-for-in-progress")
        lecture_centents = content_list.find_elements_by_tag_name('a')
        lecture_dict = {}
        
        for i,sub in enumerate(lecture_centents):
            lecture_dict[i] = {'name': sub.text,
                               'link': sub.get_attribute('href')}
            
        ModdleScraper.menu(self,lecture_dict)
    
    def menu(self, lecture_dict):
        browser = self.browser
        
        __q = None
        while __q != "q":
            for i in lecture_dict:
                print(f"{i+1}: {lecture_dict[i]['name']}")
            print("'q': Quit")
            lec_code = input("Go to: ")
            if lec_code == 'q':
                __q = lec_code
            elif 1 <= int(lec_code) <= len(lecture_dict):
                browser.get(lecture_dict[int(lec_code) - 1]['link'])
            else:
                print("Invalid lecture code")
        
        ModdleScraper.__regular_terminate(self)
            
    def __immediate_terminate(self):
        self.browser = None
        __verbose = self.__verbose
        
        print(*__verbose,sep='\n')
        sys.exit(1)
        
    def __regular_terminate(self):
        #time.sleep(1000)
        browser = self.browser
        browser.close()
        
    @property
    def verbose(self):
        return self.__verbose
    
    @verbose.setter
    def verbose(self, *, new_verbose):
        return self.__verbose
    
    def __str__(self):
        pass
    def __del__(self):
        pass
            

if __name__ == '__main__':
    test_json = json_account_handler.JSON_Account_Handler(
                                json_key='name',
                                json_value_list=[
                                    {
                                        # place username
                                        'username': '171044**',
                                        
                                        # place password
                                        'password': 'password'
                                    }
                                ])
    
    lecture_login_url = "https://bilmuh.gtu.edu.tr/moodle/login/index.php"
    
    moddle_scraper = ModdleScraper(json_handler=test_json,
                                   json_key='name',
                                   lecture_login_url=lecture_login_url)
    
    
    




    
