#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 09:31:37 2018

@author: A153722
"""


import numpy as np
import pandas as pd
import scipy.stats as sci
import re
#import matplotlib as mpl 
from matplotlib import pyplot as plt 
import seaborn as sns
#import pandas_profiling as pp

# velger hvor mange kolonner som vises i oppsummeringer:
pd.set_option('display.max_columns', 23)

jobs = pd.DataFrame()

for year in range(2002, 2018):
    #print(year)
    file = '/Users/A153722/Documents/apne data/data/Ledigestillinger_'+str(year)+'.csv'
    yearly = pd.read_csv(file, sep=';', na_values='*')
    jobs = jobs.append(yearly, ignore_index=True)
    # feilmelding for 2005 og 2011. 2011 fikses med na_values. 2005 faar feil
    # fordi det finnes en string i forste og andre kolonne (egentlig int)



#legg til kolonne med aarstall
jobs['aarstall'] = jobs.statistikk_aar_mnd//100

#sjekk at 2005 og 2011 er med
#jobs['aarstall'].value_counts(sort=False)


#Kategorisk
jobs.iloc[:, 0:2]  = jobs.iloc[:, 0:2].astype(str)
jobs.nav_enhet_kode = jobs.nav_enhet_kode.astype('category')




#Skrive ut ugyldige nummer:
#fylkesnr = jobs['arbeidssted_fylkesnummer'].value_counts()
#fylkesnr = list(np.unique(kilde.index))
#fylkesnr[:5]
#fylkesnr[-5:]

ranges = {'arbeidssted_fylkesnummer': range(1, 23), 'arbeidssted_kommunenummer': range(101, 2400), 'yrkeskode': range(1, 10000)}

for column in ranges:
    a = -jobs[column].isin(ranges[column])  # All values outside the range is True (- negates)
    jobs.loc[a, column] = np.nan


#Datetime
jobs.iloc[:, 2:4] = jobs.iloc[:, 2:4].apply(pd.to_datetime, errors='coerce', format='%d.%m.%Y')
#Dårlig kvalitet på sistepubl_dato
#jobs.iloc[:, 2:4].head()


np.unique(jobs.stillingsnummer).size
jobs['yrke_grovgruppe'].value_counts()
jobs['yrke_grovgruppe'].value_counts()


# ---------------------------------------------------------
# proving og feiling med å legge til kolonne med aarstall
#dato
#jobs['aarstall'] = pd.to_datetime(jobs.statistikk_aar_mnd, format='%Y%m').dt.year

# int -> str -> int
#a = list(jobs.statistikk_aar_mnd.astype(str))
#jobs['aarstall'] = list(map(lambda yyyymm: yyyymm[0:4], a))
#jobs['aarstall'] = jobs['aarstall'].astype(int)


# ---------------------------------------------------------
# sjekk at årene er med, funker ogsaa:
#copy = np.array(jobs['aarstall'])
#unique, counts = np.unique(copy, return_counts=True)
#print(np.asarray((unique, counts)).T)




# ---------------------------------------------------------
# fikse 2005 - finne stringene i kolonne 0 og 1

#Source: https://stackoverflow.com/questions/1323364/in-python-how-to-check-if-a-string-only-contains-certain-characters
# og: https://stackoverflow.com/questions/21800169/python-pandas-get-index-of-rows-which-column-matches-certain-value


#sok i en-og-en string
#def special_match(strg, search=re.compile(r'[^0-9]').search):
#    return bool(search(strg))
#
#def special_match2(strg):
#    return bool(re.compile(r'[^0-9]').search(strg))
#
#ix_list = []
#for col in jobs.iloc[:, 0:2]:
#    a = jobs[col][[special_match(str(nr)) for nr in jobs.stillingsnummer]].index.tolist()
#    ix_list.extend(a)
#
#
#
##sok i hel dataframe (virker ikke paa enkeltkolonne/series)
#def special_match3(df, regex=r'[^0-9]'):
#    ix_list = []
#    
#    for col in df.columns:
#        a = df[col].str.contains(regex, regex=True)
#        ix_list.extend(a[a > 0].index.tolist())
#        
#        #ix_list.append(df.col[list(map(search, col))].index.tolist())
#        
#    return sorted(set(ix_list))
#
#
## sok i enkeltkolonner/series
#def regex_search(col, regex=r'[^0-9]'):
#    a = col.str.contains(regex, regex=True)
#    return a[a > 0].index.tolist()
#
#
##funker ikke
#def regex_search2(col, regex=r'[^0-9]'):
#    col = col.astype(str)
#    search = re.compile(regex).search
#    a = col[list(map(search, col))].index.tolist()
#    return a[a > 0].index.tolist()
#
#
#%timeit regex_search(jobs.stillingsnummer)  # 2.62 s ± 23.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
#%timeit a = jobs.stillingsnummer[[special_match(str(nr)) for nr in jobs.stillingsnummer]]
## 1.76 s ± 32.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
#%timeit jobs.stillingsnummer[list(map(special_match, jobs.stillingsnummer.astype(str)))]
##1.7 s ± 18.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


#%timeit jobs.stillingsnummer[[special_match(str(nr)) for nr in jobs.stillingsnummer]]
#%timeit jobs.stillingsnummer[[special_match2(str(nr)) for nr in jobs.stillingsnummer]]
#
#jobs.nav_enhet_kode[[special_match(str(kode)) for kode in jobs.nav_enhet_kode]]
#   
#jobs.nav_enhet_kode[bool([re.search(r'[^0-9]', str(kode)) for kode in jobs.nav_enhet_kode])]
#
#jobs.nav_enhet_kode[jobs['nav_enhet_kode'].apply(re.search(pattern = r'[^0-9]'))]
# ---------------------------------------------------------


# tester
#jobs[jobs.aarstall == 2005].tail(n=5)
#jobs.dtypes # stillingsnummer er object, men..
#sum(jobs.stillingsnummer == '2041200512000000') #fra 2005, treff kun med string
#sum(jobs.stillingsnummer == 2041200211000000)  #fra 2002, treff kun med tall
#
#
#jobs.iloc[:, 0:2]  = jobs.iloc[:, 0:2].astype(str)
#sum(jobs.stillingsnummer == 2041200211000000) # ikke treff lenger
#sum(jobs.stillingsnummer == '2041200211000000')  # treff 
#sum(jobs.stillingsnummer == '3000200501000005')  # 0
#sum(jobs.nav_enhet_kode == '3000')  # 0


#jobs = jobs.replace({'stillingsnummer': r'^aetat', 'nav_enhet_kode': r'^aetat'}, 
#                        value='3000', regex=True)


#jobs.iloc[:, 0:2]  = jobs.iloc[:, 0:2].astype(int)
#jobs[jobs.aarstall == 2005].tail(n=5)

# ---------------------------------------------------------
#Datetime
#jobs[jobs.sistepubl_dato == '28.01.5002']
#jobs.loc[122673, 'sistepubl_dato'] = '28.01.2002'
#a = pd.to_datetime(jobs.sistepubl_dato, format='%d.%m.%Y')
#
#a = []
#for i in range(len(jobs.sistepubl_dato)):
#    date = pd.to_datetime(jobs.loc[i, 'sistepubl_dato'], format='%d.%m.%Y')
#    a.append(date)
#    
#a = []
#for date in jobs.sistepubl_dato:
#    a.append(pd.to_datetime(date, format='%d.%m.%Y'))
#
#jobs.iloc[len(a),:]
#jobs.loc[len(a), 'sistepubl_dato'] = '01.10.2010'
#
#    
#jobs[jobs.sistepubl_dato == '30.10.1010']
#jobs.loc[1539397, 'sistepubl_dato'] = '30.10.2010'
#
#
#jobs[jobs.sistepubl_dato == '26.06.1010']
#jobs.loc[1565331, 'sistepubl_dato'] = '26.06.2010'
#
#
#jobs[jobs.sistepubl_dato == '30.05.0011']
#jobs.loc[1607446, 'sistepubl_dato'] = '30.05.2011'
#
#jobs[jobs.sistepubl_dato == '01.01.9999']
#jobs.loc[[1617643, 1795008], 'sistepubl_dato'] = pd.NaT
#
#jobs[jobs.sistepubl_dato == '15.12.0710']
#jobs.loc[1607446, 'sistepubl_dato'] = '30.05.2011'


#Oppsummeringer
jobs.info(null_counts=True)
jobs.describe()

# Function to calculate missing values by column
# Source: https://github.com/WillKoehrsen/machine-learning-project-walkthrough/blob/master/Machine%20Learning%20Project%20Part%201.ipynb
def missing_values_table(df):
        # Total missing values
        mis_val = df.isnull().sum()
        
        # Percentage of missing values
        mis_val_percent = 100 * mis_val / len(df)
        
        # Make a table with the results
        mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        
        # Rename the columns
        mis_val_table_ren_columns = mis_val_table.rename(
        columns = {0 : 'Missing Values', 1 : '% of Total Values'})
        
        # Sort the table by percentage of missing descending
        mis_val_table_ren_columns = mis_val_table_ren_columns[
            mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
        
        # Print some summary information
        print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
            "There are " + str(mis_val_table_ren_columns.shape[0]) +
              " columns that have missing values.")
        
        # Return the dataframe with missing information
        return mis_val_table_ren_columns
    
 

missing_values_table(jobs)
#sistepubl_dato går fra 31 til 75 missing



#EDA
len(jobs.groupby(['stilling_kilde']))
jobs.groupby(['stilling_kilde']).groups.keys()




sns.set()
#plotte ulike kategirske var over tid i density plots
#kilde = jobs.dropna(subset=['stilling_kilde']) # ikke vits, ingen missing
kilde = jobs['stilling_kilde'].value_counts()
kilde = list(kilde[kilde.values > 10].index)

# Plot of distribution of scores for building categories

# Plot each building
for kat in kilde:
    # Select the building type
    subset = jobs[jobs['stilling_kilde'] == kat]
    
    # Density plot of Energy Star scores
    sns.kdeplot(subset['statistikk_aar_mnd'],
               label = kat, shade = False, alpha = 0.8);


    
# label the plot
plt.xlabel('Energy Star Score', size = 20); plt.ylabel('Density', size = 20); 
plt.title('Density Plot of Energy Star Scores by Building Type', size = 28);
plt.show()
plt.ylim(0, 20)

jobs.groupby(['statistikk_aar_mnd','stilling_kilde'])['antall_stillinger'].sum().unstack('stilling_kilde').plot();






sns.lmplot(x='statistikk_aar_mnd', y='antall_stillinger', data=jobs)


# Remove outliers
jobs['antall_stillinger_u_outl'] = jobs['antall_stillinger'][jobs['antall_stillinger'] < 200]
antall_stillinger_u_outl = jobs.loc[jobs['antall_stillinger'] < 15, 'antall_stillinger']


sns.lmplot(x='statistikk_aar_mnd', y='antall_stillinger_u_outl', data=jobs)


plt.hist(antall_stillinger_u_outl, edgecolor = 'black');

sns.stripplot(x=jobs.statistikk_aar_mnd, y=antall_stillinger_u_outl);
sns.swarmplot(x=jobs.statistikk_aar_mnd, y=antall_stillinger_u_outl);
