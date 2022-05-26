#!/usr/bin/env python
# coding: utf-8

# In[1]:


import scrapy
import time
import pandas as pd
from scrapy.crawler import CrawlerProcess
import numpy as np
from bs4 import BeautifulSoup


# In[2]:


parent = 'https://www.edx.org/sitemap-0.xml'
masters=[]
masters_clean=[]


# In[3]:


names=[]
links=[]
images=[]
metas=[]
subjects=[]
dur_data=[] ## Check
skills=[]
descs=[]
courses=[] ##Check
outlooks=[]
insts=[]
partners=[]


# In[4]:


class EDX_Course_Scrape(scrapy.Spider):
    name='Course_scraper'
    def start_requests(self):
        #
        print(parent)
        yield scrapy.Request(url=parent,callback=self.get_links)
        
    def get_links(self,response):
        data = response.xpath('//text()').extract()
        #data2=response.xpath('//url/text()').extract()
        #print(data2)
        for i in data:
            if '/micromasters/' in i:
                masters.append(i)
                
        for i in masters:
            if '/es/' not in i:
                masters_clean.append(i)

        for m in masters_clean:
            yield scrapy.Request(url=m,callback=self.get_data)
            
    def get_data(self,response):
        name=response.xpath('//*[@id="main-content"]/div[2]/div/div/div/div[2]/div[1]/div/text()').extract()
        names.append(name)
        
        links.append(response)
        
        image= response.xpath('//*[@id="main-content"]/div[2]/div/div/div/div[1]/div/img/@src').extract()
        images.append(image)
        
        meta = response.xpath('//*[@id="main-content"]/div[1]/div/header/div/h1/text()').extract()
        metas.append(meta)
        
        subject = response.xpath('//*[@id="main-content"]/div[1]/div/header/div/div/nav/ol/li[3]/a/text()').extract()
        subjects.append(subject)
        
        duration = response.xpath('//*[@id="main-content"]/div[3]/div/div[1]/div[2]/div[2]/div//text()').extract()
        dur_data.append(duration)
        
        skill= response.xpath('//*[@id="main-content"]/div[3]/div/div[1]/div[2]/div[1]/ul//text()').extract()
        skills.append(skill)
        
        desc=response.xpath('//*[@id="main-content"]/div[3]/div/div[1]/div[2]/div[1]/div[2]/div/div//text()').extract()
        descs.append(desc)
        
        course=response.xpath('//span[@class="mr-2"]/text()').extract()
        courses.append(course)
        
        job = response.xpath('//*[@id="main-content"]/div[3]/div/div[3]/div/div/div/ol/li[8]/div[2]/div/div/ul//text()').extract()
        outlooks.append(job)
        
        inst= response.xpath('//*[@id="main-content"]/div[4]/div[1]/div/div[1]/div[2]/div/div//@href').extract()
        insts.append(inst)
        
        partner = response.xpath('//*[@id="main-content"]/div[4]/div[1]/h2/div/span/text()').extract()
        partners.append(partner)


# In[5]:


process= CrawlerProcess()
process.crawl(EDX_Course_Scrape)
process.start()


# In[6]:


#print(dur_data)
time=[]
price=[]
pace=[]
for i in dur_data:
    cost=[]
    dur=[]
    pac=[]
    for m in i:
        if '$' in m:
            cost.append(m)
        if ' per ' in m:
            pac.append(m)
            a= i.index(m)
            dur.append(i[a-1])
    price.append(cost)
    time.append(dur)
    pace.append(pac)


# In[7]:



for i in courses:
    i.remove('Program Overview')
    i.remove('Certificate & Credit Pathways')
    i.remove('Job Outlook')


# In[ ]:





# In[9]:


masters=pd.DataFrame()

masters['Name']=names
masters['Link']=links
masters['University Image']=images
masters['Meta Desc']=metas
masters['Subject']=subjects
masters['Skills']=skills
masters['Description']=descs
masters['Job Outlook']=outlooks
masters['Instructors']=insts
masters['Partner']=partners
masters['Price']=price
masters['Duration']=time
masters['Pace']=pace
masters['Courses']=courses


# In[11]:


#masters.to_excel('EDX_masters.xlsx')

