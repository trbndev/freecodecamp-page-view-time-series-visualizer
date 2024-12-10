import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("./fcc-forum-pageviews.csv", index_col="date", parse_dates=True)

# Clean data
lower_quantile = df["value"].quantile(0.025)
upper_quantile = df["value"].quantile(0.975)
df = df[(df["value"] >= lower_quantile) & (df["value"] <= upper_quantile)]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df.index, df["value"], color="firebrick")

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month_name()

    df_pivot = df_bar.groupby(["year", "month"])["value"].mean().unstack()
    months_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    df_pivot = df_pivot[months_order]

    # Draw bar plot
    fig = df_pivot.plot(kind="bar", figsize=(8, 6)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")

    # Save image and return fig (don't change this part)
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = [d.year for d in df_box.date]
    df_box["month"] = [d.strftime("%b") for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(ncols=2, figsize=(16, 5))
    sns.boxplot(
        x="year",
        y="value",
        data=df_box,
        ax=ax[0],
        palette="muted",
    )
    ax[0].set_title("Year-wise Box Plot (Trend)")
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page Views")

    sns.boxplot(
        x="month",
        y="value",
        data=df_box,
        ax=ax[1],
        order=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        palette="muted",
    )
    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig("box_plot.png")
    return fig
