"""
Data Visualization for the datasets of Wikipedia timeseries
    Downloads data from SQLite and through pandas reads it into a DataFrame
    the download function presents a select_statement argument in which
    a desired select statement can be inputted.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import def_language as language
from loadsql import download_data_from_sqlite as dwnld

""" We need to import the data from the SQL database"""


select_statement = """SELECT Page, SUM(Visits)
from page_visits
group by Page
order by SUM(Visits) desc
limit 100;
"""


dwnld(select_statement=select_statement)



data_path = ...
train_data = pd.read_csv(data_path)

# Transforming the Date column to a datetime format
train_data['Date'] = pd.DatetimeIndex(train_data['Date'])


def plot_avg_views_per_day(ax, train_data):
    # Calculate the average number of views per day
    temp = train_data.groupby('Date')['Visits'].mean()

    # Set up the plot
    ax.figure(figsize=(15, 4))
    ax.xlabel('Date', fontsize=8)
    ax.ylabel('Avg views', fontsize=8)
    ax.title('Average number of views per day', fontsize=12)

    # Plot the average views per day

    # # Set up the ticks
    # plt.xticks(fontsize=8)
    # plt.yticks(fontsize=8)
    #
    # # Show legend
    # plt.legend()
    #
    # # Adjust layout and show the plot
    # plt.tight_layout()

    return ax.plot(temp, label='Visits')

fig, ax = plt.subplots(1, 1)
plot_avg_views_per_day(ax, train_data)


def plot_median_views_per_day(ax, train_data):
    # Calculate the median number of views per day
    temp = train_data.groupby('Date')['Visits'].median()

    # Set up the plot
    ax.figure(figsize=(15, 4))
    ax.xlabel('Date', fontsize=8)
    ax.ylabel('Median views', fontsize=8)
    ax.title('Median number of views per day', fontsize=8)

    # Plot the median views per day

    # # Customize and show the plot
    # ax.legend()
    # ax.xticks(fontsize=8)
    # ax.yticks(fontsize=8)
    # ax.tight_layout()

    return ax.plot(temp, label='Visits')


plot_median_views_per_day(plt, train_data)


def extract_date_components(df, date_column):
    """
    Extracts year, month, and day from a date column in a DataFrame and creates new columns for each.

    Parameters:
    - df: pandas DataFrame containing the date column.
    - date_column: The name of the column in df that contains date values.
    """
    # Ensure the date column is in datetime format
    df[date_column] = pd.to_datetime(df[date_column])

    # Create new columns for year, month, and day
    df['year'] = df[date_column].dt.year
    df['month'] = df[date_column].dt.month
    df['day'] = df[date_column].dt.day

extract_date_components(train_data, 'Date')


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