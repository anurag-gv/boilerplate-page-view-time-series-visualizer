import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import calendar

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=True, index_col=[0])

# Clean data
cond1 = df.value <= df.value.quantile(97.5/100)
cond2 = df.value >= df.value.quantile(2.5/100)
df = df[cond1 & cond2]

def draw_line_plot():
    # Draw line plot
    fig, axes = plt.subplots(figsize=(16,6))
    axes.plot(df.index, df.value, color='red')
    axes.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    axes.set_xlabel('Date')
    axes.set_ylabel('Page Views')
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.resample('MS').mean()
    missing = pd.date_range('2016-01-01', '2016-04-01', freq='MS')
    fill = pd.DataFrame(index=missing)
    fill['value'] = np.nan
    df_bar = pd.concat([df_bar, fill]).sort_index()
    df_bar['month'] = pd.Categorical(df_bar.index.month, categories=range(1,13), ordered=True)
    df_bar['year'] = df_bar.index.year
    df_bar = df_bar.pivot(index='year', columns='month', values='value')

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(14, 6))
    width = 0.5  # width of a single bar
    n_months = 12
    x = np.arange(len(df_bar.index))  # one position per year
    fig, ax = plt.subplots(figsize=(14, 6))
    width = 0.7  # width of a single bar (the year-bar; monthly=yearly/12)
    n_months = 12
    x = np.arange(len(df_bar.index))  # one position per year
    cmap = plt.get_cmap('tab20', n_months)
    for i, month in enumerate(df_bar.columns):
        ax.bar(
            x + (i - n_months / 2) * (width / n_months),  # shift bars within group
            df_bar[month],
            width=width / n_months,
            color=cmap(i),
            label=calendar.month_name[month]
        )
    ax.set_xticks(x)
    ax.set_xticklabels(df_bar.index)
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Month', loc='upper left', bbox_to_anchor=(0.01, 0.99))
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(14,6))

    sns.boxplot(data=df_box, x="year", y="value", hue="year", ax=ax1, palette='bright', legend=False, fliersize=0.5)
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")
    ax1.set_title('Year-wise Box Plot (Trend)')

    sns.boxplot(data=df_box, x="month", y="value", hue="month", ax=ax2, fliersize=0.5, order=calendar.month_abbr[1:13])
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")
    ax2.set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
