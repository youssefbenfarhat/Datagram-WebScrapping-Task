from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from urllib.request import Request, urlopen

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.touch_actions import TouchActions

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from xlwt import Workbook
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from fake_useragent import UserAgent
import time
import os
import sys
import random
import time

from selenium.common.exceptions import NoSuchElementException   
import json  




def configure_driver():
    # Add additional Options to the webdriver
    chrome_options = Options()
    ua = UserAgent()
    #THIS IS FAKE AGENT IT WILL GIVE YOU NEW AGENT EVERYTIME
    userAgent = ua.random                                     
    print('UserAgent:',userAgent)
    chrome_options.add_argument(f'user-agent={userAgent}')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
    return driver

def getdata(drive,list_of_product_ex1,list_of_product_ex2):



     

    #Searching The Webpage
    driver.get("https://www.norauto.fr/t/pneu/w-205-h-55-r-16/ete-s.html/1/")

    
    #Explicit Wait Until  Solving the Captcha And Accept The Cookies Page Is Visible  (We Have generated our own xpath, took button tag and what is written in it)
    WebDriverWait(driver,100).until(expected_conditions.visibility_of_element_located((By.XPATH,"//button[text()='Accepter et continuer']")))
    
    #Clicking Accept Button
    driver.find_element_by_xpath("//button[text()='Accepter et continuer']").click()
    
  
    
    
    # Explicit Wait until Form Appears (Using id of form / We can also construct xpath for this too
    WebDriverWait(driver, 100).until(expected_conditions.visibility_of_element_located((By.ID, 'ProductCompare')))
   

    # Store form in variable
    formmain = driver.find_element_by_id('ProductCompare')
    

    # inside form getting all tags li by classname  (.// represent inside that element)
    container = formmain.find_elements_by_xpath(".//li[@class='product_list ws-product-list-item']") #List of products

    #We removed the first word (Pneu)
    get_dimension=lambda x:x.split(" ",1)
    #We took the second,third and fourth word 
    get_keyword=g=lambda x:(" ").join(x.split(" ")[1:3])
    #Initialise rank to 1
    rank=1

    # loop through each li
    for contain in container:
        # Getting title from h2 tag
        try:
            #Dictionary of products
            products_ex1={}
            products_ex2={}

            title = contain.find_element_by_xpath(".//h2[@data-cerberus='listing-title']").text
            dimension=contain.find_element_by_xpath(".//h3[@class='text-content text-gray-second font-weight-normal mb-0']").text
            urls=contain.find_element_by_xpath(".//h2[@data-cerberus='listing-title']/a").get_attribute('href')
            price=float(contain.find_element_by_xpath(".//span[@data-cerberus='product-price']").get_attribute('content'))
            products_ex1['name']=title+" "+get_dimension(dimension)[1]
            products_ex1['price']=round(price,2)
            products_ex1['url']=urls


            products_ex2['url']=urls
            products_ex2['rank']=rank
            products_ex2['keyword']=get_keyword(dimension)

            
            
            
            list_of_product_ex1.append(products_ex1)
            list_of_product_ex2.append(products_ex2)

            rank+=1
            
            
        except Exception:
            #incase title url price if not there or script fails. title will be set to empty
            title=''
            dimension=''
            urls=''
            price=0
            pass

        
                          
#List of products
list_of_product_ex1=[]
list_of_product_ex2=[]
# create the driver object.
driver= configure_driver()

getdata(driver,list_of_product_ex1,list_of_product_ex2)
#print('Dic',list_of_product_ex1)
print('list_of_product_ex2',list_of_product_ex2)
with open('ex1.json', 'w') as f:
    json.dump(list_of_product_ex1, f)

with open('ex2.json', 'w') as f:
    json.dump(list_of_product_ex2, f)

driver.quit()

#driver.close()














