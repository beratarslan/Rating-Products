###################################################
# Rating Products
###################################################

# - Average
# - Time-Based Weighted Average
# - User-Based Weighted Average
# - Weighted Rating


############################################
# User and Time Weighted Course Score Calculation
############################################

import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)



# Loading dataset
df = pd.read_csv("datasets/course_reviews.csv")

# Displaying first few rows
df.head()

# Checking dataset shape
df.shape

# Rating distribution
df["Rating"].value_counts()

# Questions Asked distribution
df["Questions Asked"].value_counts()

# Aggregating ratings based on questions asked
df.groupby("Questions Asked").agg({"Questions Asked": "count",
                                   "Rating": "mean"})

# Displaying first few rows after analysis
df.head()

####################
# Average
####################

# Average Rating
df["Rating"].mean()

####################
# Time-Based Weighted Average
####################

# Display dataset information
df.head()
df.info()

# Converting Timestamp column to datetime format
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Defining a reference date
current_date = pd.to_datetime('2021-02-10 0:0:0')

# Calculating days since the rating was given
df["days"] = (current_date - df["Timestamp"]).dt.days

# Calculating average ratings based on time intervals
rating_30 = df.loc[df["days"] <= 30, "Rating"].mean()
rating_90 = df.loc[(df["days"] > 30) & (df["days"] <= 90), "Rating"].mean()
rating_180 = df.loc[(df["days"] > 90) & (df["days"] <= 180), "Rating"].mean()
rating_older = df.loc[(df["days"] > 180), "Rating"].mean()

# Weighted rating calculation
weighted_rating = (rating_30 * 28/100 + 
                   rating_90 * 26/100 + 
                   rating_180 * 24/100 + 
                   rating_older * 22/100)

def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    """
    Computes time-based weighted average rating based on predefined time intervals.
    
    Parameters
    ----------
    dataframe : pd.DataFrame
        The dataset containing rating and timestamp columns.
    w1 : int, optional (default=28)
        Weight for ratings in the last 30 days.
    w2 : int, optional (default=26)
        Weight for ratings between 30 and 90 days.
    w3 : int, optional (default=24)
        Weight for ratings between 90 and 180 days.
    w4 : int, optional (default=22)
        Weight for ratings older than 180 days.
    
    Returns
    -------
    float
        Time-based weighted average rating.
    """
    return dataframe.loc[dataframe["days"] <= 30, "Rating"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["days"] > 30) & (dataframe["days"] <= 90), "Rating"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["days"] > 90) & (dataframe["days"] <= 180), "Rating"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["days"] > 180), "Rating"].mean() * w4 / 100

# Calculating time-based weighted average rating
time_based_weighted_average(df)
time_based_weighted_average(df, 30, 26, 22, 22)



####################
# User-Based Weighted Average
####################

# Displaying first few rows
df.head()

# Calculating average rating for each progress level
df.groupby("Progress").agg({"Rating": "mean"})

# Weighted rating calculation based on user progress
weighted_rating = (df.loc[df["Progress"] <= 10, "Rating"].mean() * 22 / 100 + 
                   df.loc[(df["Progress"] > 10) & (df["Progress"] <= 45), "Rating"].mean() * 24 / 100 + 
                   df.loc[(df["Progress"] > 45) & (df["Progress"] <= 75), "Rating"].mean() * 26 / 100 + 
                   df.loc[(df["Progress"] > 75), "Rating"].mean() * 28 / 100)

def user_based_weighted_average(dataframe, w1=22, w2=24, w3=26, w4=28):
    """
    Computes user-based weighted average rating based on course progress percentages.
    
    Parameters
    ----------
    dataframe : pd.DataFrame
        The dataset containing rating and progress columns.
    w1 : int, optional (default=22)
        Weight for users with progress ≤ 10%.
    w2 : int, optional (default=24)
        Weight for users with progress between 10% and 45%.
    w3 : int, optional (default=26)
        Weight for users with progress between 45% and 75%.
    w4 : int, optional (default=28)
        Weight for users with progress > 75%.
    
    Returns
    -------
    float
        User-based weighted average rating.
    """
    return dataframe.loc[dataframe["Progress"] <= 10, "Rating"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 10) & (dataframe["Progress"] <= 45), "Rating"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 45) & (dataframe["Progress"] <= 75), "Rating"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 75), "Rating"].mean() * w4 / 100

# Calculating user-based weighted average rating
user_based_weighted_average(df, 20, 24, 26, 30)


####################
# Weighted Rating
####################
def course_weighted_rating(dataframe, time_w=50, user_w=50):
    """
    Computes the overall weighted rating for a course by combining time-based and user-based weighted averages.
    
    Parameters
    ----------
    dataframe : pd.DataFrame
        The dataset containing rating, timestamp, and progress columns.
    time_w : int, optional (default=50)
        Weight assigned to the time-based weighted rating.
    user_w : int, optional (default=50)
        Weight assigned to the user-based weighted rating.
    
    Returns
    -------
    float
        The final course rating based on both time-based and user-based weights.
    """
    return time_based_weighted_average(dataframe) * time_w / 100 + user_based_weighted_average(dataframe) * user_w / 100

# Calculating weighted course rating
course_weighted_rating(df)

# Adjusting weights for time-based and user-based ratings
course_weighted_rating(df, time_w=40, user_w=60)








