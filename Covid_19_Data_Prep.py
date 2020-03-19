
# coding: utf-8

# # Zindi Covid-19 Contest - Data Prep
# 
# This notebook shows how the data for the Zindi contest - Predicting the Global Spread of COVID-19 is derived. As this is an evolving situation, the dataset is not fixed at the start of the contest. Instead, you may use all available data at a given time, and are encouraged to keep incorporating new data as it becomes available. Each week, the leaderboard wil reset and a new submission file will be shared covering the most recent test period. The ultimate goal is to make predictions fo the time following the CLOSE of the competition - more info on the competition page.
# 
# In this notebook, we download the latest figures from https://github.com/CSSEGISandData/COVID-19, add some additional information, group by Country/Region, re-shape into the format required for submission and show how you can score your model on the latest data without needing to upload submissions to Zindi. 

# ## Downloading the Data
# 
# The data has been curated by the Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE), and is pubically available on their GitHub repository. We clone the repository to get the data.
# 

# In[ ]:


# Get the latest data
get_ipython().system('git clone https://github.com/CSSEGISandData/COVID-19')


# ## Loading the Data

# In[ ]:


import pandas as pd


# In[ ]:


cases = pd.read_csv('/content/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
cases.head()


# In[ ]:


deaths = pd.read_csv('/content/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
deaths.head()


# ## Adding Population info
# 
# This is optional, but this section adds population info.

# In[ ]:


get_ipython().system('pip install countryinfo # Run if needed')


# In[ ]:


from countryinfo import CountryInfo

pops = {}
fails = []

regions = sorted(deaths['Country/Region'].unique())
for r in regions:
  try:
    country = CountryInfo(r)
    pops[r] = country.info()['population']
  except:
    fails.append(r)
    print('No pop data for', r)


# In[ ]:


# Manual fixes
pops['Andorra'] = 76965
pops['Congo (Kinshasa)'] = 81340000
pops["Cote d'Ivoire"] = 24290000
pops['Cruise Ship'] = 2670 # Not included in competition
pops['Czechia'] = 10650000
pops['Holy See'] = 1000 # Also excluded since it's small and unique.
pops['Korea, South'] = 51470000
pops['North Macedonia'] = 2077000
pops['Reunion'] = 859959
pops['Serbia'] = 7022000
pops['Taiwan*'] = 23780000
pops['US'] = 372200000


# In[ ]:


# Adding in population as a column
cols = list(deaths.columns)
deaths['Population'] = deaths['Country/Region'].map(pops)
deaths = deaths[cols[:2]+['Population']+cols[2:]] # Nice ordering
deaths.head()


# ## Some Quick Visualizations

# In[ ]:


# Cases for mainland China (note - data is cumulative)
cases.groupby('Country/Region').sum().loc['China'][3:].plot()


# In[ ]:


# Deaths in Italy
deaths.groupby('Country/Region').sum().loc['Italy'][3:].plot()


# In[ ]:


# Looking at raw numbers vs pop adjusted figures
grouped = deaths.groupby('Country/Region').sum()
# grouped['3/12/20'].sort_values(ascending=False).head(20) # Raw numbers
(grouped['3/12/20']*1e7/deaths.groupby('Country/Region').mean()['Population']).sort_values(ascending=False).head(20) # Scaled by population (deaths/10M people)


# ## Dropping rows to match Zindi
# 
# We exclude unusual entries like the cruise ship data, to focus on large regions

# In[ ]:


deaths = deaths.loc[deaths.Population >10000] # Drops Cruise ship and Holy See
cases = cases.loc[cases['Country/Region'].isin(deaths['Country/Region'].unique())]
deaths.shape, cases.shape


# ## Preparing a 'sample submission' file and scoring locally
# 
# This will mimic the way submissions to Zindi will work. We'll generate an example submission file along with a reference file (the correct answers, used for scoring). 
# 
# Dates for the submission will change as the competition goes on. Here, we'll use the last available week of data for local testing. The next section shows how to create a submission file that can be uploaded to Zindi for scoring.

# In[ ]:


# Creating the 'reference' file

TEST_PERIOD = 7 # In days

test_dates = deaths.columns[-TEST_PERIOD:] # The last two weeks worth of data
countries = deaths.groupby('Country/Region').sum()[test_dates] # Group by country/region, and select only the columns for the test_period

# Create a new dataframe, with a Region X Date column. 
reference = pd.DataFrame({
    'Region X Date':list(map((lambda x: ' X '.join(x)), list(countries.stack().index.to_flat_index()))), # Check output to see what this is doing
    'target':countries.stack() # The target we'll be predicting: cumulative number of cases for a given region at a given date.
}).reset_index(drop=True) # Don't need the multiIndex created with Stack
reference.to_csv('reference.csv', index=False)
reference.head()


# In[ ]:


# Sample submission is the same as the reference file, just with target set to 0
print(reference.target.sum())
ss = reference.copy()
ss['target'] = 0
print(ss.target.sum())
ss.to_csv('SampleSub.csv', index=False)


# In[ ]:


# Scoring
from sklearn.metrics import mean_absolute_error

# Create some 'predictions
predictions = ss.copy()
predictions['target'] = 42 # These would be your actual predictions

# Calculate MAE
print('MAE: ', mean_absolute_error(reference['target'], predictions['target']))


# # Matching the Zindi Submission File
# 
# The competition requires that you submit a file containing predictions for the whole of the time period between March 6 and June 7. The way it works is that only the relevant week's worth of predictions will be evaluated. Let's create an appropriate file.

# In[ ]:


dates = pd.date_range(start='2020-03-06', end='2020-06-07', freq='1d')
ids = []
for c in sorted(deaths['Country/Region'].unique()):
  for d in dates:
    ids.append(c + ' X ' + d.strftime('%m/%d/%y'))
ss = pd.DataFrame({
    'Region X Date':ids,
    'target':0
})
ss.to_csv('SampleSubmission.csv', index=False)
ss.head()


# In[ ]:


ss.tail()


# # Creating 'Train.csv'
# 
# You can shape your training data in any way you want, **provided that it does not include data from the test period**. The goal is to predict into the future. While the competition is open, you could simply use all the available data for training and get a near-perfect score. However, this won't represent how well your model will do in the future. The final score will be based on new, unseen data based on events after the competition closes. 
# 
# This is how the 'train.csv' file available from Zindi is generated:

# In[ ]:


train_dates = deaths.columns[5:-TEST_PERIOD]
country_deaths = deaths.groupby('Country/Region').sum()[train_dates] 
country_cases = cases.groupby('Country/Region').sum()[train_dates] 

train = pd.DataFrame({
    'Region X Date':list(map((lambda x: ' X '.join(x)), list(country_deaths.stack().index.to_flat_index()))), 
    'target':country_deaths.stack(),
    'cases':country_cases.stack() # Added as they may be useful
}).reset_index(drop=True)
train.to_csv('train.csv', index=False)
train.head()


# Zindi will update the training data weekly, but you are also encouraged to use the data from JH as shown in this notebook to keep up with the latest information.
