# -*- coding: utf-8 -*-
import os
import pandas as pd
import matplotlib.pyplot as plt

# change directory to where dataset is and take a look at what data is like
os.chdir('/Users/Suyang/GitHub/fivethirtyeight-data/police-killings')
police_killings = pd.read_csv("police_killings.csv", encoding="ISO-8859-1")
police_killings.head(5)

"""
Problem 1: California, Texas, and Florida have the most killings but have a much higher 
population. What are some ways you can calibrate for the difference in population?
"""

# Calculate the ratio(killings per people) 
# The chance of being killed by police if you live in CA, TX and FL
# Searching wikipedia for information about population and population denstyof these states

# People killed by police divided by the population of that state
# People killed by poluce divided by the population density of that state
state_count = police_killings.groupby('state').size() # Series object
killings_sort_by_state = state_count.sort_index(ascending = True).to_frame() # Series object

# According to results of killings_sort_by_state, we can see the top three state
# with most people killed by police are California, Texas and Florida.


# Data Source: https://en.wikipedia.org/wiki/List_of_U.S._states_by_population_density
# 2013 population and population density(/sqmi)
population_and_density = pd.read_csv('/Users/Suyang/Documents/population and density.csv', thousands = ',')
states_abbr = pd.read_csv('/Users/Suyang/Documents/us_states.csv')
# Very important to specify the thousands is seperated by comma

population_and_density = population_and_density.sort_values(by=['State']).reset_index(drop=True)
# The North Dakota is the last one, it is not correct order, do the following to move
# the North Dakota to row 33, and move rows below that one row down

population_middle = population_and_density[33:]
population_last= population_and_density.iloc[-1]
population_middle = population_middle.shift()
population_middle.iloc[0] = population_last.squeeze()
population_and_density.iloc[33:] = population_middle

population_and_density['Abbr'] = states_abbr['Abbr']
killings_sort_by_state.index.names = ['Abbr']
killings_sort_by_state.reset_index(level = 0, inplace= True)
killings_sort_by_state = killings_sort_by_state.rename(columns={0:'killings'})
# change index name so we can merge it later on common name
# merge these two dataframes
killings_population_density = population_and_density.merge(killings_sort_by_state, on = 'Abbr',
how = 'left')
killings_population_density['killings'].fillna(0, inplace=True)

killings_population_density['killings/population'] = killings_population_density['killings'].astype(float) / killings_population_density['population']
killings_population_density['killings/density'] = killings_population_density['killings'].astype(float) / killings_population_density['density/sqmi']
# change str with ',' to numeric value

def killings_rate_list(column):
    killings_sort = killings_population_density.sort_values([column], ascending = False)
    killings_list = killings_sort.State.tolist()
    killings_list = [state.replace(u'\xa0', u'').strip('\n') for state in killings_list]
    return killings_list

killings_rate_population = killings_rate_list('killings/population')
killings_rate_density = killings_rate_list('killings/density')
# Don't repeat self(DRY), design a function
# Therefore, if we base on the chance of killings per people, the highest rate is in Oklahoma, Arizona and Nebraska 
# if we base on the change of killings per density, the highest rate is in Alaska, Texas, and Arizona



"""
Problem 2: What general racial leanings do the killings have? At first glance, 
there were more killings of white civilians than both black and hispanic combined. 
How complete of a picture does this provide?
"""
# Generate a histgram of racial distribution of the deceased 
racial_killings = police_killings['raceethnicity'].value_counts()
racial_killings.plot(kind="bar")
black_killings_rate = racial_killings['Black']/racial_killings.sum()
# 28.9 percent of the deceased-135 of the 467-are African-Americans, much higher 
# than 14.3 percent, the national rate for black population estimated by 2014 US Census Bureau.

police_killings[['share_black']] = police_killings[['share_black']].apply(pd.to_numeric, errors='coerce')
# Convert type of 'share_black' from object to float,[[]], [] will not convert the type

killings_share_black_50 = len(police_killings[police_killings['share_black']>=50.0])
# Count the number of killings occured in regions with black population more than 50 percent
# 55, out of 467, killings took place in tracts with more than 50 percent of black population 


"""
Problem 3: While it's well known that lower income areas tend to have more crime, 
does the data refute or support that general claim? Did you find any links between 
features you didn't feel were related?
"""
nat_house_income_count = police_killings.groupby(['nat_bucket']).size().to_frame()
nat_house_income_count['percent'] = nat_house_income_count[0]/467
plt.hist(police_killings['nat_bucket'], range=(0.5,5.5))
police_killings[['nat_bucket']].boxplot()
# 30 percent of the killings—139 of the 467—took place in census tracts that are 
# in the bottom 20 percent nationally in terms of household income
# Percentage of killings decrease as household income increases. 
# Only 8 percent of the killings happened in the population that are in top 20 
# percent nationally in terms of household income

# To conclude, the data supports the statement that lower income areas tend to 
# have more crimes.







