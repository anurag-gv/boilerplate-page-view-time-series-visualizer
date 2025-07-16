import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
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
    df_bar = df.resample('MS').sum()
    df_bar['month'] = df_bar.index.month
    df_bar['year'] = df_bar.index.year

    # Draw bar plot
    fig = sns.catplot(data = df_bar, x='year', y='value', kind='bar', hue='month', palette='muted', height=7, aspect=1, width=0.7)
    fig._legend.remove()
    ax = fig.ax
    handles, labels = ax.get_legend_handles_labels()
    month_labels = [calendar.month_name[int(label)] for label in labels]
    ax.legend(handles=handles, labels=month_labels, title='Month')
    fig.set_axis_labels("Years", "Average Page Views")
    plt.ticklabel_format(style='plain', axis='y')
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

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
    ax1.set_xlabel("year")
    ax1.set_ylabel("Page Views")
    ax1.set_title('Year-wise Box Plot (Trend)')

    sns.boxplot(data=df_box, x="month", y="value", hue="month", ax=ax2, fliersize=0.5, order=calendar.month_abbr[1:13])
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")
    ax2.set_title('Year-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
