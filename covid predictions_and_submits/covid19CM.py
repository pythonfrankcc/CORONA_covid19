
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[2]:


#pip install pycountry-convert
#using pycountry-convert in kaggle turned out to be a deliberate scam and it did not work out in my favor
#used the alternative which is to tweak the dataset in excel manually and added the column for the continent


# In[3]:


#let us start by reading the data using pandas
data = pd.read_csv ("../input/covid19all/train_with_continents.csv")


# In[4]:


data1 = pd.read_csv ("../input/covid19all/train_week_1_ahead.csv")
data2 = pd.read_csv ("../input/covid19all/train_week_two_data.csv")
data3 = pd.read_csv("../input/last-week-with-continents/last week with continents.csv")


# In[5]:


'''lets look at whether the data is of the same size and shape so that we can append the necessary columns to the
latest dataset which is data2
'''
print('the size and shape of the data is:',data.shape,'and',data.size)
print('the size and shape of the data1 is:',data1.shape,'and',data1.size)
print('the size and shape of the data2 is:',data2.shape,'and',data2.size)
print('the size and shape of the data3 is:',data3.shape,'and',data3.size)


# In[6]:


#lets look at how our data looks like for the first few rows
data3.head()


# In[7]:


#checking the data 1 which shows the week one after I joined the competition
data1.head()


# In[8]:


#checking the data 2 which shows the week two after I joined the competition
data2.head()


# In[9]:


#lets get the information we want to know about the whole data
display(data3.info())


# In[10]:


'''looking at the above data2 we can see that the date column comes out as an object(string) lets change that for sth 
that is going to be easily used during EDA
'''
#creating a copy of some part of the dataframe
#data3['date'] = data3['Date'].copy()
from datetime import datetime
#data2['Date'] = pd.to_datetime(data2['Date'], format = '%m/%d/%Y')
data3['Date converted'] = pd.to_datetime(data3['Date'])


# In[11]:


#lets see if the data.dtype for the date column has changed
display(data3.info())


# In[12]:


#lets look at the unique names for the columns and from there also the unique values so as to drop unwanted data
list(data3.columns)


# In[13]:


#dropping the repeated columns which are the last two
#repeated_columns_for_dropping = data[['Territory','Date']]
#data = data.drop(repeated_columns_for_dropping,axis = 1)


# In[14]:


#lets look at the train data description to better understand the data
data3.describe()


# In[15]:


print("Number of Territories: ", data['Territory'].nunique())
print("Number of Territories: ", data1['Territory'].nunique())
print("Number of Territories: ", data2['Territory'].nunique())
print("Number of Territories: ", data3['Territory'].nunique())
print("Dates go from day", min(data['Date']), "to day", max(data['Date']), ", a total of", data['Date'].nunique(), "days")
print("Dates go from day", min(data1['Date']), "to day", max(data1['Date']), ", a total of", data1['Date'].nunique(), "days")
print("Dates go from day", min(data2['Date']), "to day", max(data2['Date']), ", a total of", data2['Date'].nunique(), "days")
print("Dates go from day", min(data3['Date']), "to day", max(data3['Date']), ", a total of", data3['Date'].nunique(), "days")
#our data has no states
#print("Countries with Province/State informed: ", data[data['Province/State'].isna()==False]['Country/Region'].unique())


# In[16]:


'''#let us look at these territories just to make sure that each stands on its own
we actually do not need thia cell so we can do away with it
print(data['Territory'].nunique())
print(data2['Territory'].nunique())
'''


# In[17]:


#from the above data we can see that each country appears only once 
#lets see the number of entries per Territory
data['Territory'].value_counts()
data1['Territory'].value_counts()
data2['Territory'].value_counts()
data3['Territory'].value_counts()


# In[18]:


'''# produces Pandas Series
data.groupby('month')['duration'].sum() 
# Produces Pandas DataFrame
data.groupby('month')[['duration']].sum()
'''


# In[19]:


#lets check the number of deaths and infected confirmed cases by using plots
#importing the necessary dependency
import matplotlib.pyplot as plt
#for week one

confirmed_total_date = data.groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date = data.groupby(['Date']).agg({'target':['sum']})
total_date = confirmed_total_date.join(fatalities_total_date)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date.plot(ax=ax1)
ax1.set_title("Global confirmed cases", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date.plot(ax=ax2, color='orange')
ax2.set_title("Global deceased cases", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)

#for week  two
confirmed_total_date = data1.groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date = data1.groupby(['Date']).agg({'target':['sum']})
total_date = confirmed_total_date.join(fatalities_total_date)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date.plot(ax=ax1)
ax1.set_title("Global confirmed cases", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date.plot(ax=ax2, color='orange')
ax2.set_title("Global deceased cases", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)

#for week three 
confirmed_total_date = data2.groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date = data2.groupby(['Date']).agg({'target':['sum']})
total_date = confirmed_total_date.join(fatalities_total_date)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date.plot(ax=ax1)
ax1.set_title("Global confirmed cases", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date.plot(ax=ax2, color='orange')
ax2.set_title("Global deceased cases", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)


#for the last week 
confirmed_total_date = data3.groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date = data3.groupby(['Date']).agg({'target':['sum']})
total_date = confirmed_total_date.join(fatalities_total_date)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date.plot(ax=ax1)
ax1.set_title("Global confirmed cases", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date.plot(ax=ax2, color='orange')
ax2.set_title("Global deceased cases", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)


# we know that the virus originated from china so we can use this to compare with the China graph for both the confirmed cases against the deaths and check if the graphs flow the same remembering that during some time china changed how it considered whether somebody was considered positive (11/03/2020).This may be registered as a spike and considering other policies that are put in place that may likely affect the number of cases of the infected people.
# 

# In[20]:


#lets draw the curve excluding china
#for week one
confirmed_total_date_noChina = data[data['Territory']!='China'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_noChina = data[data['Territory']!='China'].groupby(['Date']).agg({'target':['sum']})
total_date_noChina = confirmed_total_date_noChina.join(fatalities_total_date_noChina)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date_noChina.plot(ax=ax1)
ax1.set_title("Global confirmed cases excluding China", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date_noChina.plot(ax=ax2, color='orange')
ax2.set_title("Global deceased cases excluding China", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)

#for week two 
confirmed_total_date_noChina = data1[data1['Territory']!='China'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_noChina = data1[data1['Territory']!='China'].groupby(['Date']).agg({'target':['sum']})
total_date_noChina = confirmed_total_date_noChina.join(fatalities_total_date_noChina)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date_noChina.plot(ax=ax1)
ax1.set_title("Global confirmed cases excluding China", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date_noChina.plot(ax=ax2, color='orange')
ax2.set_title("Global deceased cases excluding China", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)

#for week 3
confirmed_total_date_noChina = data2[data2['Territory']!='China'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_noChina = data2[data2['Territory']!='China'].groupby(['Date']).agg({'target':['sum']})
total_date_noChina = confirmed_total_date_noChina.join(fatalities_total_date_noChina)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date_noChina.plot(ax=ax1)
ax1.set_title("Global confirmed cases excluding China", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date_noChina.plot(ax=ax2, color='orange')
ax2.set_title("Global deceased cases excluding China", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)


#for last week
confirmed_total_date_noChina = data3[data3['Territory']!='China'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_noChina = data3[data3['Territory']!='China'].groupby(['Date']).agg({'target':['sum']})
total_date_noChina = confirmed_total_date_noChina.join(fatalities_total_date_noChina)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date_noChina.plot(ax=ax1)
ax1.set_title("Global confirmed cases excluding China", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date_noChina.plot(ax=ax2, color='orange')
ax2.set_title("Global deceased cases excluding China", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)


# Without China we should be getting a smoother curve as which more or less looks like the SIR model for epidemiology where there is a steep rise then a gentle drop in the number of cases but remember that unlike other countries that can learn from China,China had no prior warning of the contagion.

# In[21]:


#for week one
confirmed_total_date_China = data[data['Territory']=='China'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_China = data[data['Territory']=='China'].groupby(['Date']).agg({'target':['sum']})
total_date_China = confirmed_total_date_China.join(fatalities_total_date_China)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date_China.plot(ax=ax1)
ax1.set_title("China confirmed cases", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date_China.plot(ax=ax2, color='orange')
ax2.set_title("China deceased cases", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)
#for week two
confirmed_total_date_China = data1[data1['Territory']=='China'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_China = data1[data1['Territory']=='China'].groupby(['Date']).agg({'target':['sum']})
total_date_China = confirmed_total_date_China.join(fatalities_total_date_China)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date_China.plot(ax=ax1)
ax1.set_title("China confirmed cases", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date_China.plot(ax=ax2, color='orange')
ax2.set_title("China deceased cases", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)

#for week 3
confirmed_total_date_China = data2[data2['Territory']=='China'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_China = data2[data2['Territory']=='China'].groupby(['Date']).agg({'target':['sum']})
total_date_China = confirmed_total_date_China.join(fatalities_total_date_China)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date_China.plot(ax=ax1)
ax1.set_title("China confirmed cases", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date_China.plot(ax=ax2, color='orange')
ax2.set_title("China deceased cases", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)

#for last week of the prediction
confirmed_total_date_China = data3[data3['Territory']=='China'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_China = data3[data3['Territory']=='China'].groupby(['Date']).agg({'target':['sum']})
total_date_China = confirmed_total_date_China.join(fatalities_total_date_China)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date_China.plot(ax=ax1)
ax1.set_title("China confirmed cases", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date_China.plot(ax=ax2, color='orange')
ax2.set_title("China deceased cases", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)


# In[22]:


#for week one
confirmed_total_date_kenya = data[data['Territory']=='Kenya'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_kenya = data[data['Territory']=='Kenya'].groupby(['Date']).agg({'target':['sum']})
total_date_kenya = confirmed_total_date_kenya.join(fatalities_total_date_kenya)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date_kenya.plot(ax=ax1)
ax1.set_title("China confirmed cases", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date_kenya.plot(ax=ax2, color='orange')
ax2.set_title("China deceased cases", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)

#for week two
confirmed_total_date_kenya = data1[data1['Territory']=='Kenya'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_kenya = data1[data1['Territory']=='Kenya'].groupby(['Date']).agg({'target':['sum']})
total_date_kenya = confirmed_total_date_kenya.join(fatalities_total_date_kenya)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date_kenya.plot(ax=ax1)
ax1.set_title("China confirmed cases", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date_kenya.plot(ax=ax2, color='orange')
ax2.set_title("China deceased cases", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)

#for week 3
confirmed_total_date_kenya = data2[data2['Territory']=='Kenya'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_kenya = data2[data2['Territory']=='Kenya'].groupby(['Date']).agg({'target':['sum']})
total_date_kenya = confirmed_total_date_kenya.join(fatalities_total_date_kenya)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date_kenya.plot(ax=ax1)
ax1.set_title("China confirmed cases", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date_kenya.plot(ax=ax2, color='orange')
ax2.set_title("China deceased cases", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)

#for last week of prediction
confirmed_total_date_kenya = data3[data3['Territory']=='Kenya'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_kenya = data3[data3['Territory']=='Kenya'].groupby(['Date']).agg({'target':['sum']})
total_date_kenya = confirmed_total_date_kenya.join(fatalities_total_date_kenya)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17,7))
total_date_kenya.plot(ax=ax1)
ax1.set_title("China confirmed cases", size=10)
ax1.set_ylabel("Number of cases", size=10)
ax1.set_xlabel("Date", size=10)
fatalities_total_date_kenya.plot(ax=ax2, color='orange')
ax2.set_title("China deceased cases", size=10)
ax2.set_ylabel("Number of cases", size=10)
ax2.set_xlabel("Date", size=10)


# In[23]:


#looking at the worst hit countries as of now for week one
#Italy
confirmed_total_date_Italy = data[data['Territory']=='Italy'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Italy = data[data['Territory']=='Italy'].groupby(['Date']).agg({'target':['sum']})
total_date_Italy = confirmed_total_date_Italy.join(fatalities_total_date_Italy)

#Spain
confirmed_total_date_Spain = data[data['Territory']=='Spain'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Spain = data[data['Territory']=='Spain'].groupby(['Date']).agg({'target':['sum']})
total_date_Spain = confirmed_total_date_Spain.join(fatalities_total_date_Spain)
#Autralia
confirmed_total_date_Australia = data[data['Territory']=='Australia'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Australia = data[data['Territory']=='Australia'].groupby(['Date']).agg({'target':['sum']})
total_date_Australia = confirmed_total_date_Australia.join(fatalities_total_date_Australia)
#Singapore
confirmed_total_date_Singapore = data[data['Territory']=='Singapore'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Singapore = data[data['Territory']=='Singapore'].groupby(['Date']).agg({'target':['sum']})
total_date_Singapore = confirmed_total_date_Singapore.join(fatalities_total_date_Singapore)
#South Korea
#Singapore
confirmed_total_date_SouthKorea = data[data['Territory']=='Republic of Korea'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_SouthKorea = data[data['Territory']=='Republic of Korea'].groupby(['Date']).agg({'target':['sum']})
total_date_SouthKorea = confirmed_total_date_Singapore.join(fatalities_total_date_Singapore)


plt.figure(figsize=(15,10))
plt.subplot(2, 2, 1)
total_date_Italy.plot(ax=plt.gca(), title='Italy')
plt.ylabel("Confirmed infection cases", size=13)

plt.subplot(2, 2, 2)
total_date_Spain.plot(ax=plt.gca(), title='Spain')

plt.subplot(2, 2, 3)
total_date_Australia.plot(ax=plt.gca(), title='United Kingdom')
plt.ylabel("Confirmed infection cases", size=13)

'''plt.subplot(2, 2, 4)
total_date_Singapore.plot(ax=plt.gca(), title='Singapore')
'''
plt.subplot(2, 2, 4)
total_date_SouthKorea.plot(ax=plt.gca(), title='SouthKorea')


# In[24]:


#looking at the worst hit countries as of now for week 2
#Italy
confirmed_total_date_Italy = data1[data1['Territory']=='Italy'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Italy = data1[data1['Territory']=='Italy'].groupby(['Date']).agg({'target':['sum']})
total_date_Italy = confirmed_total_date_Italy.join(fatalities_total_date_Italy)

#Spain
confirmed_total_date_Spain = data1[data1['Territory']=='Spain'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Spain = data1[data1['Territory']=='Spain'].groupby(['Date']).agg({'target':['sum']})
total_date_Spain = confirmed_total_date_Spain.join(fatalities_total_date_Spain)
#Autralia
confirmed_total_date_Australia = data1[data1['Territory']=='Australia'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Australia = data1[data1['Territory']=='Australia'].groupby(['Date']).agg({'target':['sum']})
total_date_Australia = confirmed_total_date_Australia.join(fatalities_total_date_Australia)
#Singapore
confirmed_total_date_Singapore = data1[data1['Territory']=='Singapore'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Singapore = data1[data1['Territory']=='Singapore'].groupby(['Date']).agg({'target':['sum']})
total_date_Singapore = confirmed_total_date_Singapore.join(fatalities_total_date_Singapore)
#South Korea
#Singapore
confirmed_total_date_SouthKorea = data1[data1['Territory']=='Republic of Korea'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_SouthKorea = data1[data1['Territory']=='Republic of Korea'].groupby(['Date']).agg({'target':['sum']})
total_date_SouthKorea = confirmed_total_date_Singapore.join(fatalities_total_date_Singapore)


plt.figure(figsize=(15,10))
plt.subplot(2, 2, 1)
total_date_Italy.plot(ax=plt.gca(), title='Italy')
plt.ylabel("Confirmed infection cases", size=13)

plt.subplot(2, 2, 2)
total_date_Spain.plot(ax=plt.gca(), title='Spain')

plt.subplot(2, 2, 3)
total_date_Australia.plot(ax=plt.gca(), title='United Kingdom')
plt.ylabel("Confirmed infection cases", size=13)

'''plt.subplot(2, 2, 4)
total_date_Singapore.plot(ax=plt.gca(), title='Singapore')
'''
plt.subplot(2, 2, 4)
total_date_SouthKorea.plot(ax=plt.gca(), title='SouthKorea')


# In[25]:


#looking at the worst hit countries as of now for week 3
#Italy
confirmed_total_date_Italy = data2[data2['Territory']=='Italy'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Italy = data2[data2['Territory']=='Italy'].groupby(['Date']).agg({'target':['sum']})
total_date_Italy = confirmed_total_date_Italy.join(fatalities_total_date_Italy)

#Spain
confirmed_total_date_Spain = data2[data2['Territory']=='Spain'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Spain = data2[data2['Territory']=='Spain'].groupby(['Date']).agg({'target':['sum']})
total_date_Spain = confirmed_total_date_Spain.join(fatalities_total_date_Spain)
#Autralia
confirmed_total_date_Australia = data2[data2['Territory']=='Australia'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Australia = data2[data2['Territory']=='Australia'].groupby(['Date']).agg({'target':['sum']})
total_date_Australia = confirmed_total_date_Australia.join(fatalities_total_date_Australia)
#Singapore
confirmed_total_date_Singapore = data2[data2['Territory']=='Singapore'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Singapore = data2[data2['Territory']=='Singapore'].groupby(['Date']).agg({'target':['sum']})
total_date_Singapore = confirmed_total_date_Singapore.join(fatalities_total_date_Singapore)
#South Korea
#Singapore
confirmed_total_date_SouthKorea = data2[data2['Territory']=='Republic of Korea'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_SouthKorea = data2[data2['Territory']=='Republic of Korea'].groupby(['Date']).agg({'target':['sum']})
total_date_SouthKorea = confirmed_total_date_Singapore.join(fatalities_total_date_Singapore)


plt.figure(figsize=(15,10))
plt.subplot(2, 2, 1)
total_date_Italy.plot(ax=plt.gca(), title='Italy')
plt.ylabel("Confirmed infection cases", size=13)

plt.subplot(2, 2, 2)
total_date_Spain.plot(ax=plt.gca(), title='Spain')

plt.subplot(2, 2, 3)
total_date_Australia.plot(ax=plt.gca(), title='United Kingdom')
plt.ylabel("Confirmed infection cases", size=13)

'''plt.subplot(2, 2, 4)
total_date_Singapore.plot(ax=plt.gca(), title='Singapore')
'''
plt.subplot(2, 2, 4)
total_date_SouthKorea.plot(ax=plt.gca(), title='SouthKorea')


# In[26]:


#looking at the worst hit countries as of now for last week of the prediction 
#Italy
confirmed_total_date_Italy = data3[data3['Territory']=='Italy'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Italy = data3[data3['Territory']=='Italy'].groupby(['Date']).agg({'target':['sum']})
total_date_Italy = confirmed_total_date_Italy.join(fatalities_total_date_Italy)

#Spain
confirmed_total_date_Spain = data3[data3['Territory']=='Spain'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Spain = data3[data3['Territory']=='Spain'].groupby(['Date']).agg({'target':['sum']})
total_date_Spain = confirmed_total_date_Spain.join(fatalities_total_date_Spain)
#Autralia
confirmed_total_date_Australia = data3[data3['Territory']=='Australia'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Australia = data3[data3['Territory']=='Australia'].groupby(['Date']).agg({'target':['sum']})
total_date_Australia = confirmed_total_date_Australia.join(fatalities_total_date_Australia)
#Singapore
confirmed_total_date_Singapore = data3[data3['Territory']=='Singapore'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_Singapore = data3[data3['Territory']=='Singapore'].groupby(['Date']).agg({'target':['sum']})
total_date_Singapore = confirmed_total_date_Singapore.join(fatalities_total_date_Singapore)
#South Korea
#Singapore
confirmed_total_date_SouthKorea = data3[data3['Territory']=='Republic of Korea'].groupby(['Date']).agg({'cases':['sum']})
fatalities_total_date_SouthKorea = data3[data3['Territory']=='Republic of Korea'].groupby(['Date']).agg({'target':['sum']})
total_date_SouthKorea = confirmed_total_date_Singapore.join(fatalities_total_date_Singapore)


plt.figure(figsize=(15,10))
plt.subplot(2, 2, 1)
total_date_Italy.plot(ax=plt.gca(), title='Italy')
plt.ylabel("Confirmed infection cases", size=13)

plt.subplot(2, 2, 2)
total_date_Spain.plot(ax=plt.gca(), title='Spain')

plt.subplot(2, 2, 3)
total_date_Australia.plot(ax=plt.gca(), title='United Kingdom')
plt.ylabel("Confirmed infection cases", size=13)

'''plt.subplot(2, 2, 4)
total_date_Singapore.plot(ax=plt.gca(), title='Singapore')
'''
plt.subplot(2, 2, 4)
total_date_SouthKorea.plot(ax=plt.gca(), title='SouthKorea')


# In[27]:


#what type of data can we deduce from the given data
#we can get the mortality rate in the countries as of the beginning of the beginning and we will compare with other weeks
data3.head()


# In[28]:


'''calculating the difference between cases and target that will help in getting mortality rate in different weeks
and seeing among them there may be recoveries'''
data['diff']=data['cases'] - data['target']
#week one diff
data1['diff']=data1['cases'] - data1['target']
#week two diff
data2['diff']=data2['cases'] - data2['target']
#week last diff
data3['diff']=data3['cases'] - data3['target']


# In[29]:


#lets look through the three developed diff columns and see whether their are any missing values
#for the first dataset
print(data.isna().any())
print(data.isna().sum())
#for the second dataset
print(data1.isna().any())
print(data1.isna().sum())
#for the third dataset
print(data2.isna().any())
print(data2.isna().sum())
#for the last dataset
print(data3.isna().any())
print(data3.isna().sum())


# In[30]:


'''#calculating the increase in the number of cases between the weeks
data['weekoneincrease']=data1['cases'] - data['cases']
data['weektwoincreasefromweekone']=data2['cases'] - data1['cases']
this is no necessary just calculate the values in a descending order
'''
#calculate the rise in cases by subtracting the previous value of a row with another 
#data1["risen cases"] = data1["cases"].diff(-1)
#we use the +ve notation since we want o subtract one from the next
data3["risen cases"] = data3["cases"].diff(1)


# In[31]:


#replacing the first value with a zero
data3["risen cases"]=data3['risen cases'].replace(np.nan, 0.00, regex=True)


# In[32]:


#checking whether there are any zero values in our latest dataset
print(data3.isna().sum())


# In[33]:


#lets also add a column of the rise in deaths to our latest data set
data3["risen targets daily"] = data3["target"].diff(1)
#change the value of the first loc[0] to a 0
data3['risen targets daily'] = data3['risen targets daily'].replace(np.nan, 0.00, regex=True)


# In[34]:


#checking whether the difference column has been created
data3.head()


# In[35]:


#calculating the mortality rates of different Territories rounded off to two decimal places
#last week mortality rate
data3['mortality rate last week'] = round((data3['target']/data3['cases']) * 100,2)


# In[36]:


#replacing the Nans in the mortality rate with 0.00
data3['mortality rate last week'] = data3['mortality rate last week'].replace(np.nan, 0.00, regex=True)


# In[37]:


#looking at the data type for the various columns that we have
print(data3.dtypes)


# In[38]:


#checking the values for mortality rate
print("mortality rates in last week: ", data3['mortality rate last week'].nunique())


# In[39]:


#finding out the rise in mortality rate per day in each of the territories
data3["mortality rate rise per day"] = data3["mortality rate last week"].diff(1)
#change the value of the first loc[0] to a 0
data3['mortality rate rise per day'] = data3['mortality rate rise per day'].replace(np.nan, 0.00, regex=True)


# In[40]:


data3.head()


# In[41]:


'''#lets group the respective Territories to their Continents this may help in organizing per R0
import pycountry_convert as pc

country_code = pc.country_name_to_country_alpha2("China", cn_name_format="default")
print(country_code)
continent_name = pc.country_alpha2_to_continent_code(country_code)
print(continent_name)'''


# In[42]:


'''the next part is to check the modal split of the individual continents but there was lack of data for the various
continents especially Africa so lets look at sth that we have data on which is which countries have put up stringent
measures and with those we can use the R0 as a little less than others where people still move freely
'''


# In[43]:


'''
for places with high laws on covid we use 3,medium we use 2 and low we use 1 and very low 0
adapted from https://www.weforum.org/agenda/2020/03/coronavirus-this-is-how-the-world-is-responding/ and
https://www.vox.com/science-and-health/2020/3/22/21189889/coronavirus-covid-19-pandemic-response-south-korea-phillipines-italy-nicaragua-senegal-hong-kong
https://www.nation.co.ke/news/How-countries-are-battling-coronavirus/1056-5502012-147wgeoz/index.html
http://www.xinhuanet.com/english/2020-03/16/c_138883650.htm
'''
def label_race (row):
    if row['Territory'] == 'Republic of Korea (the)' :
        return 3
    if row['Territory'] == 'United States of America (the)' :
        return 2
    if row['Territory'] == 'Philippines (the)':
        return 1
    if row['Territory']  == 'Nicaragua':
        return 0
    if row['Territory'] == 'Italy':
        return 1
    if row['Territory'] == 'Senegal':
        return 3
    if row['Territory'] == 'Singapore':
        return 3
    if row['Territory'] == 'Tunisia':
        return 2
    if row['Territory'] == 'Kenya':
        return 2
    if row['Territory'] == 'France':
        return 2
    if row['Territory'] == 'Iran (Islamic Republic of)':
        return 1
    if row['Territory'] == 'Germany':
        return 2
    if row['Territory'] == 'Switzerland':
        return 2
    if row['Territory'] == 'Austria':
        return 1
    if row['Territory'] == 'China':
        return 3
    if row['Territory'] == 'Japan':
        return 2
    if row['Territory'] == 'Saudi Arabia':
        return 3
    if row['Territory'] == 'Egypt':
        return 3
    if row['Territory'] == 'United Kingdom of Great Britain and Northern Ireland (the)':
        return 2
    if row['Territory'] == 'South Africa':
        return 2
    if row['Territory'] == 'Uganda':
        return 1
    if row['Territory'] == 'Argentina':
        return 2
    if row['Territory'] == 'Serbia':
        return 3
    if row['Territory'] == 'Czechia':
        return 2
    if row['Territory'] == 'Mexico':
        return 1
    if row['Territory'] == 'Iraq':
        return 2
    if row['Territory'] == 'Astralia':
        return 2
    return 0
#data.apply (lambda row: label_race(row), axis=1)
data3['Stringent'] = data3.apply (lambda row: label_race(row), axis=1)


# In[44]:


data3.head()


# In[45]:


#checking to see if the values for the Stringent stuck
print("Number of unique values for the Stringent column: ", data3['Stringent'].nunique())


# In[46]:


#checking for the data types of all columns
print(data3.dtypes)


# In[47]:


print("Number of unique values for the Continent column: ", data3['Continent'].unique())


# In[48]:


'''looking at the epidemic a country is only as efficient as its health system and am assuming that the 
countries economic strength has a relationship with its health system'''
'''https://en.wikipedia.org/wiki/List_of_continents_by_GDP_(nominal) -->link to list of continents by their gdp
as of 2019 in billions of us dollars'''
def label_economy (row):
    if row['Continent'] == 'Asia' :
        return 31580
    if row['Continent'] == 'Europe' :
        return 21790
    if row['Continent'] == 'Africa':
        return 2450
    if row['Continent']  == 'North America':
        return 24430
    if row['Continent'] == 'South America':
        return 3640
    if row['Continent'] == 'Oceania':
        return 1630
    if row['Continent'] == 'Europe and Asia':
        return 26685
    return 0
#data.apply (lambda row: label_race(row), axis=1)
data3['continents economy'] = data3.apply (lambda row: label_economy(row), axis=1)


# In[49]:


#checking out the data
data3.head()


# In[50]:


#checking for the unique values of the continents economy 
print("Number of unique values for the Continent economy column: ", data3['continents economy'].unique())


# In[51]:


'''lets look at the countries that have had an encounter with another corona virus epidemic and thus it is 
likely that the countries would have measures put in place to deal with another such virus
this is adapted from: https://www.who.int/csr/sars/country/table2004_04_21/en/'''
def label_sars (row):
    if row['Territory'] == 'Australia' :
        return 6
    if row['Territory'] == 'Canada' :
        return 251
    if row['Territory'] == 'China':
        return 532700
    if row['Territory']  == 'Taiwan':
        return 34600
    if row['Territory'] == 'France':
        return 7
    if row['Territory'] == 'Germany':
        return 9
    if row['Territory'] == 'India':
        return 3
    if row['Territory'] == 'Indonesia':
        return 2
    if row['Territory'] == 'Italy':
        return 4
    if row['Territory'] == 'Kuwait':
        return 1
    if row['Territory'] == 'Malaysia':
        return 5
    if row['Territory'] == 'Mongolia':
        return 9
    if row['Territory'] == 'New Zealand':
        return 1
    if row['Territory'] == 'Philippines (the)':
        return 14
    if row['Territory'] == 'United Kingdom of Great Britain and Northern Ireland (the)':
        return 5
    if row['Territory'] == 'Russian Federation (the)':
        return 1
    if row['Territory'] == 'Singapore':
        return 238
    if row['Territory'] == 'South Africa':
        return 1
    if row['Territory'] == 'Spain':
        return 1
    if row['Territory'] == 'Sweden':
        return 5
    if row['Territory'] == 'Switzerland':
        return 1
    if row['Territory'] == 'Thailand':
        return 9
    if row['Territory'] == 'United States of America (the)':
        return 27
    if row['Territory'] == 'Viet Nam':
        return 63
    return 0
#data.apply (lambda row: label_race(row), axis=1)
data3['countries sars infections'] = data3.apply (lambda row: label_sars(row), axis=1)


# In[52]:


#lets view the data head
data3.head()


# In[53]:


print(data3.dtypes)


# In[54]:


'''pre processing and this will be used to make sure that you convert all the object columns into sth that can be 
used to train the model and in this we are going to be using xgboost
for the conversion from categorical to interger we are going to use a function in case we need to re use
function at a later time

from sklearn.preprocessing import OrdinalEncoder
def categoricalToInteger(data2):
    #Define Ordinal Encoder Model
    oe = OrdinalEncoder()
    data2[['Territory X Date','Territory','Continent']] = oe.fit_transform(data2.loc[:,['Territory X Date','Territory','Continent']])
    return data2
#apply the function
data2 = categoricalToInteger(data2)
'''


# In[55]:


#with the MERS epidemic it is seen to have only affected Saudi Arabia being the focal point of the disease and all


# In[56]:


'''we know that the more data we have the better our model will actually become so we can use this to our 
advantage and split the date column to have more data from it
'''
import datetime as dt
def create_features_from_date(data3):
    data3['day'] = data3['Date converted'].dt.day
    data3['month'] = data3['Date converted'].dt.month
    data3['dayofweek'] = data3['Date converted'].dt.dayofweek
    data3['dayofyear'] = data3['Date converted'].dt.dayofyear
    data3['quarter'] = data3['Date converted'].dt.quarter
    data3['weekofyear'] = data3['Date converted'].dt.weekofyear
    return data3
#apply the function
data3 = create_features_from_date(data3)


# In[57]:


data3.head()


# In[58]:


#Trying out something lets see how it works with what I already have


# In[59]:


'''
#example when using the time delta function in present time
from datetime import datetime, timedelta  
# Using current time 
ini_time_for_now = datetime.now() 
# printing initial_date 
print ("initial_date", str(ini_time_for_now))  
# Calculating future dates 
# for two years 
future_date_after_2yrs = ini_time_for_now + \ 
                        timedelta(days = 730) 
  
future_date_after_2days = ini_time_for_now + \ 
                         timedelta(days = 2) 
  
# printing calculated future_dates 
print('future_date_after_2yrs:', str(future_date_after_2yrs)) 
print('future_date_after_2days:', str(future_date_after_2days))

#another example of time delta usage in calculating the difference

from datetime import datetime, timedelta 
  
# Using current time 
ini_time_for_now = datetime.now() 
  
# printing initial_date 
print ("initial_date", str(ini_time_for_now)) 
  
# Some another datetime 
new_final_time = ini_time_for_now + \timedelta(days = 2) 
  
# printing new final_date 
print ("new_final_time", str(new_final_time)) 
  
  
# printing calculated past_dates 
print('Time difference:', str(new_final_time - \ini_time_for_now)) 
'''


# In[60]:


print(data3.dtypes)


# In[61]:


#adopted from Alchemi 
# Define function with the coefficients to estimate
def func_logistic(t, a, b, c):
    return c / (1 + a * np.exp(-b*t))


# In[62]:


#Load dependencies

import pandas as pd
import numpy as np
from fbprophet import Prophet
import pickle
import math
import scipy.optimize as optim
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from datetime import datetime, timedelta
import logging
logging.getLogger('fbprophet').setLevel(logging.WARNING)


# In[63]:


def death_cap():
    
    cap =[]
    
    for r in data3['Territory'].unique():
        data = data3[data3['Territory']==r][['target']]   
        data = data.reset_index(drop=False)
        data.columns = ['Timestep', 'Total Cases']
        if any(data['Total Cases'] > 0):
            data1 = data[data['Total Cases']>0]
            if len(data1['Total Cases'].unique()) < 5:
                cap.append(data1['Total Cases'].max()+51)
            else:
                data1['Timestep'] = range(0, len(data1['Timestep']))
        
                # Randomly initialize the coefficients
                np.random.seed(0)
                p0 = np.random.exponential(size=3)

                # Set min bound 0 on all coefficients, and set different max bounds for each coefficient
                bounds = (0, [100000., 1000., 1000000000.])

                # Convert pd.Series to np.Array and use Scipy's curve fit to find the best Nonlinear Least Squares coefficients
                x = np.array(data1['Timestep']) + 1
                y = np.array(data1['Total Cases'])
            
                try:
                    x = x.argsort()
                    (a,b,c),cov = optim.curve_fit(func_logistic, x, y, bounds=bounds, p0=p0, maxfev=1000000)
                
                    # The time step at which the growth is fastest
                    t_fastest = np.log(a) / b
                    i_fastest = func_logistic(t_fastest, a, b, c)
                
                    res_df = data1[['Timestep', 'Total Cases']].reset_index(drop=True)
                    res_df['fastest_grow_day'] = t_fastest
                    res_df['fastest_grow_value'] = i_fastest
                    res_df['growth_stabilized'] = t_fastest <= x[-1]
                    res_df['timestep'] = x
                    res_df['res_func_logistic'] = func_logistic(x, a, b, c)
            
                    if t_fastest <= x[-1]:
                        print('Death stabilized:', r, '| Fastest grow day:', t_fastest, '| Death:', i_fastest, '| Total Days:', x[-1])
                        res_df['cap'] = func_logistic(x[-1] + 60, a, b, c)
                        print(res_df['cap'][0])
                        
                    else:
                        print('Death increasing:', r, '| Fastest grow day:', t_fastest, '| Infections:', i_fastest)
                        res_df['cap'] = func_logistic(t_fastest + 60, a, b, c)
                        print(res_df['cap'][0])
                        
                    d = res_df['cap'][0]
                    cap.append(d)    
                    
                except RuntimeError:
                    print('No fit found for: ', r)
        
        else:
            cap.append(0)
         
            
    return cap


# In[64]:


cap = death_cap()


# In[65]:


uniq_terr = data3['Territory'].unique()


# In[66]:


cap_check = pd.DataFrame({'Territory':uniq_terr, 'cap': cap})


# In[67]:


data3 = data3.merge(cap_check, on='Territory', how='left')


# In[68]:


data3.head()


# In[ ]:


from tqdm import tqdm as tqdm

collect = []

for r in tqdm(data3['Territory'].unique()):
    if data3[data3['Territory']==r]['cap'].iloc[0] > 0:
        try:
            to_check = data3[data3['Territory']==r][['Date', 'target' ,'cap']]
            to_check = to_check[to_check['target']>0]
            to_check.columns = ['ds', 'y', 'cap']
            to_check['ds'] = pd.to_datetime(to_check['ds'])
            to_check['weekday'] = to_check['ds'].apply(lambda x: pd.Timestamp(x).dayofweek)
            m = Prophet(interval_width=0.95, growth='logistic')
            m.add_regressor('weekday')
            m.fit(to_check)
            future = m.make_future_dataframe(periods=51)
            future['cap'] = to_check['cap'].iloc[0]
            future['weekday'] = future['ds'].apply(lambda x: pd.Timestamp(x).dayofweek)
            forecast = m.predict(future)[['ds', 'yhat']][-51:]
            ter_targ =[]
            for d in forecast['ds']:
                a = r + ' X ' + str(d.strftime('%#m/%#d/%y'))
                ter_targ.append(a)
            forecast['Territory X Date'] = ter_targ
            forecast['target'] = forecast['yhat']
            fin_df = forecast.drop(['ds', 'yhat'], axis=1)
            
            to_targ = []
            for e in to_check['ds']:
                b = r + ' X ' + str(e.strftime('%#m/%#d/%y'))
                to_targ.append(b)
            to_check['Territory X Date'] = to_targ
            to_check['target'] = to_check['y']
            to_df = to_check[['Territory X Date', 'target']]
            final_df = pd.concat([to_df, fin_df], axis=0)
            collect.append(final_df)
            
        except:
            dates = pd.date_range(start='2020-04-19', end='2020-06-08', freq='1d')        
            exc_targ =[]
            for d in dates:
                a = r + ' X ' + str(d.strftime('%#m/%#d/%y'))
                exc_targ.append(a)
            fin_df = pd.DataFrame(exc_targ, columns=['Territory X Date'])
            fin_df['target'] = to_check['cap'].iloc[0]
            to_targ = []
            for e in to_check['ds']:
                b = r + ' X ' + str(e.strftime('%#m/%#d/%y'))
                to_targ.append(b)
            to_check['Territory X Date'] = to_targ
            to_check['target'] = to_check['y']
            to_df = to_check[['Territory X Date', 'target']]
            final_df = pd.concat([to_df, fin_df], axis=0)
            
            collect.append(final_df)
            
    else:
        to_check = data3[data3['Territory']==r][['Date', 'target']]        
        to_check.columns = ['ds', 'y']
        to_check['ds'] = pd.to_datetime(to_check['ds'])
        m = Prophet(interval_width=0.95)
        m.fit(to_check)
        future = m.make_future_dataframe(periods=51)
        forecast = future[-51:]
        ter_targ =[]
        for d in forecast['ds']:
            a = r + ' X ' + str(d.strftime('%#m/%#d/%y'))
            ter_targ.append(a)
        forecast['Territory X Date'] = ter_targ
        forecast['target'] = 0
        fin_df = forecast.drop(['ds'], axis=1)
        collect.append(fin_df)


# In[ ]:


df = collect[0]

for i in range(1,len(collect)):
     df = pd.concat([df, collect[i]], axis=0)


# In[ ]:


df = df.reset_index(drop=True)


# In[ ]:


df['Territory'] = df['Territory X Date'].apply(lambda x: x.split(' X ')[0])


# In[ ]:


new_df = []


for r in tqdm(df['Territory'].unique()):
    correct = df[df['Territory']==r][['Territory X Date', 'target', 'Territory']]
    for i in range(1, len(correct)):
        if correct['target'].iloc[i] < correct['target'].iloc[i-1]:
            correct['target'].iloc[i] = correct['target'].iloc[i] + (correct['target'].iloc[i-1] - correct['target'].iloc[i])
    new_df.append(correct)


# In[ ]:


pred = new_df[0]

for i in range(1,len(new_df)):
    pred = pd.concat([pred, new_df[i]], axis=0)


# In[ ]:


pred['target'] = pred['target'].astype('int64')


# In[ ]:


pred[['Territory X Date', 'target']].to_csv('Predictions 19-04 to 08-06 Update.csv', index=False)

