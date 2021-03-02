# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 11:54:44 2021

@author: urooj
"""


from selenium import webdriver
import pandas as pd
#webdriver
driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
driver.get("https://supremedatabase.com/")


#Create list for all items, to be transformed into a pandas dataframe
itemlist = []

#get all Seasons
seasonlist = driver.find_elements_by_class_name("season")
sznlist = [season.get_attribute("href") for season in seasonlist]
for szn in sznlist:
    driver.get(szn)
    #Category Information
    catlist_container = driver.find_element_by_class_name("category-list")
    catlist_html = catlist_container.find_elements_by_xpath(".//*")
    catlist = [cat1.get_attribute("href") for cat1 in catlist_html]
    #Open Specific Category
    for cat in catlist[:-1]:
        driver.get(cat)
        #Item URL Information
        itemlist_html = driver.find_element_by_class_name("item-list").find_elements_by_class_name("item")
        item_urls = [item_container.find_element_by_tag_name("a").get_attribute("href") for item_container in itemlist_html]
        for item in item_urls:
            driver.get(item)
            #Item Name
            iteminfo = [driver.find_element_by_class_name("page-heading").get_attribute("innerText")]    
            #detailinfo
            itemdetails = driver.find_element_by_class_name("item-details").find_elements_by_tag_name("p")
            detaillist = [detail.get_attribute("innerText") for detail in itemdetails]
            #Combine the two lists together
            iteminfo.extend(detaillist)
            #Add colors
            colorway = driver.find_element_by_class_name("item-colorways").find_elements_by_class_name("item-colorways__colorway")
            colorinfo = [color.find_element_by_tag_name("h2").get_attribute("innerText") for color in colorway]
            iteminfo.append(colorinfo)
            #add category
            iteminfo.append(cat)
            #add season
            iteminfo.append(szn)  
            #resale link
            iteminfo.append(driver.find_element_by_class_name("stockx-link-container").find_element_by_tag_name("a").get_attribute("href"))
            #add item to itemlist
            itemlist.append(iteminfo)


df=pd.DataFrame(itemlist,columns=['Item_Name','Date','Desc','Retail Price','Colorways','Category','Season','Resale Link'])
df.to_excel('SupremeTable.xlsx','Table',index=False)