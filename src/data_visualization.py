"""
Data Visualization for the datasets of Wikpedia timeseries
    Works on the _cleaned.csv file created in the Wikipedia_DataCleaning.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import def_language as language

# Uncomment the file path you need
data_path = "../data/clean/train_1_cleaned.csv"
# data_path = "../data/clean/train_2_cleaned.csv"
# data_path = "../data/clean/key_1_cleaned.csv"
# data_path = "../data/clean/key_2_cleaned.csv"

train_data = pd.read_csv(data_path)

# Transforming the Date column to a datetime format
train_data['Date'] = pd.DatetimeIndex(train_data['Date'])

# Average number of views per day
temp = train_data.groupby('Date')['Visits'].mean()
plt.figure(figsize=(15,4))
plt.xlabel('Date', fontsize=8)
plt.ylabel('Avg views',fontsize=8)
plt.title('Average number of views per day', fontsize=12)
plt.plot(temp,label='Visits')
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.legend()
plt.tight_layout()
plt.show()

# Median number of views per day
temp = train_data.groupby('Date')['Visits'].median()
plt.figure(figsize=(15,4))
plt.xlabel('Date')
plt.ylabel('Median views', fontsize=8)
plt.title('Median number of views per day', fontsize=8)
plt.plot(temp,label='Visits')
plt.legend()
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.tight_layout()
plt.show()

# Creating new columns for year, month, and day after extracting from Date column
train_data['year']=train_data.Date.dt.year
train_data['month']=train_data.Date.dt.month
train_data['day']=train_data.Date.dt.day

# Creating new column and replacing month with encoded value
train_data['month_num'] = train_data['month']
train_data['month'].replace('1', '1 - January', inplace=True)
train_data['month'].replace('2', '2 - February', inplace=True)
train_data['month'].replace('3', '3 - March', inplace=True)
train_data['month'].replace('4', '4 - April', inplace=True)
train_data['month'].replace('5', '5 - May', inplace=True)
train_data['month'].replace('6', '6 - June', inplace=True)
train_data['month'].replace('7', '7 - July', inplace=True)
train_data['month'].replace('8', '8 - August', inplace=True)
train_data['month'].replace('9','9 - September',inplace=True)
train_data['month'].replace('10','10 - October',inplace=True)
train_data['month'].replace('11','11 - November',inplace=True)
train_data['month'].replace('12','12 - December',inplace=True)

# Creating a new column weekday and applying lambda function to extract from date column
train_data['weekday'] = train_data['Date'].apply(lambda x: x.weekday())

# Creating new column and encoding weekday
train_data['weekday#'] = train_data['weekday']
train_data['weekday'].replace(0,'01 - Monday',inplace=True)
train_data['weekday'].replace(1,'02 - Tuesday',inplace=True)
train_data['weekday'].replace(2,'03 - Wednesday',inplace=True)
train_data['weekday'].replace(3,'04 - Thursday',inplace=True)
train_data['weekday'].replace(4,'05 - Friday',inplace=True)
train_data['weekday'].replace(5,'06 - Saturday',inplace=True)
train_data['weekday'].replace(6,'07 - Sunday',inplace=True)

#train_data.head()

# Creating copy of the dataframe and grouping by month and weekday and looking at the mean of the visits
train_group = train_data.groupby(["month", "weekday"])['Visits'].mean().reset_index()
train_group = train_group.pivot(index='weekday', columns='month', values='Visits')
train_group.sort_index(inplace=True)

# Plotting web traffic over days of month using heatmap
sns.set(font_scale=3.5)
f, ax = plt.subplots(figsize=(60, 40))
sns.heatmap(train_group, annot=False, ax=ax, fmt="d", linewidths=2)
plt.title('Web Traffic of various months(9-12) across weekdays')
plt.show()

###
# Dropping columns previously created for new visualization
cols_to_drop = ['year','month','day','month_num','weekday','weekday','weekday#']
train_data.drop(cols_to_drop,axis=1,inplace=True)
train_data

# Top 5 pages with maximum number of views
top_pages = train_data.groupby('Page')['Visits'].sum().reset_index()
top_pages_list = top_pages.nlargest(5,'Visits')['Page'].tolist()

# Filtering the DataFrame for only the pages in the top_pages_list
top5_pages_df = train_data[train_data['Page'].isin(top_pages_list)]
top5_pages_df

# Detecting page language from URL code
temp1 = train_data
temp1['Wikipedia_page'] = temp1.Page.apply(language.detect_language)

# Creating a new column for detecting the language from the page title
temp1['Page_language'] = temp1.Wikipedia_page.apply(language.lang_code)

# Total number of views based on language of Wikipedia webpage
fig,ax = plt.subplots(figsize=(30,6))
lang_df = temp1.groupby('Page_language')['Visits'].sum().reset_index()
lang_df = lang_df[lang_df['Page_language']!='None']
lang_df['Visits'] = round(lang_df['Visits']/1000000,0)

bar_graph = lang_df.plot.bar(x='Page_language',y='Visits',rot=30,ax=ax)
bar_graph.set_ylabel('Total views (in millions)')
bar_graph.set_title('Total number of views based on language of webpage')

for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x(), p.get_height()+1000))
ax.legend()
plt.show()

###
# Identifying the top 5 pages per number of visits
top_pages = train_data.groupby('Page')['Visits'].sum().reset_index()
top_pages_list = top_pages.nlargest(5,'Visits')['Page'].tolist()
print(top_pages_list)

top5_pages_df = train_data[train_data['Page'].isin(top_pages_list)]
top5_pages_df

# Time-series of page with maximum views

top_page_df = train_data[train_data.Page == top_pages_list[0]]
#top_page_df = top_page_df['Visits']

# Making number of visits smaller to ease visualization
top_page_df['Visits'] = top_page_df['Visits'].div(1000000).round(2)

# Drop columns not used in next plots
top_page_df.drop(['Page','Wikipedia_page','Page_language'],axis=1,inplace=True)
top_page_df.head()

# Resetting index
top_page_df.reset_index(inplace=True)
top_page_df.head()

top_page_df.plot()
plt.xticks(fontsize=8)
plt.yticks(fontsize=8) 