import camelot
import pandas as pd
import matplotlib.pyplot as plt   # https://pandas.pydata.org/docs/user_guide/visualization.html#basic-plotting-plot
from matplotlib.ticker import FuncFormatter
# For prettier plots: https://pandas.pydata.org/community/ecosystem.html
import seaborn as sns  # https://seaborn.pydata.org
import sqlite3

pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.width = 1000

# Read tables from a PDF file
# tables = camelot.read_pdf("appendix_f.pdf", pages="all")

# Convert each table into a DataFrame
# dataframes = [table.df for table in tables]


# Function to split and expand DataFrame
def split_and_expand(df):

  # Attempt 5: Nope, this explodes
  # Split each cell by '\n'
  # df = df.apply(lambda x: x.str.split('\n'))  
  # Explode the DataFrame
  # df_expanded = df.apply(lambda x: x.explode()).reset_index(drop=True)
  # ValueError: cannot reindex on an axis with duplicate labels

  # Attempt 4: Nope, this explodes
  # Split each cell by '\n'
  # for column in df.columns:
  #   df[column] = df[column].str.split('\n')
  # Explode each column individually and concatenate the results
  # df_expanded = pd.concat([df[col].explode() for col in df.columns], axis=1)
  # Reset the index to avoid duplicate labels
  # df_expanded = df_expanded.reset_index(drop=True)
  # ValueError: cannot reindex on an axis with duplicate labels

  # Attempt 3: Nope, this explodes
  # Split each cell by '\n'
  # for column in df.columns:
  #   df[column] = df[column].str.split('\n')
  # Explode the DataFrame
  # df_expanded = df.apply(pd.Series.explode)
  # Reset the index
  # df_expanded = df_expanded.reset_index(drop=True)
  # ValueError: cannot reindex on an axis with duplicate labels

  # Attempt 2: Nope, this explodes
  # Split each cell by '\n' and create a new DataFrame where each row is a value from the split
  # df_expanded = df.apply(lambda x: x.str.split('\n')).apply(pd.Series.explode).reset_index(drop=True)
  # ValueError: cannot reindex on an axis with duplicate labels

  # Attempt 1: Nope, this explodes:
  # Split each cell by '\n' and create a new DataFrame where each row is a value from the split
  df_expanded = df.apply(lambda x: x.str.split('\n').explode()).reset_index(drop=True)
  # ValueError: cannot reindex on an axis with duplicate labels

  return df_expanded

# Apply the function to the DataFrame
# df_expanded = split_and_expand(df)


data = {
    "Column1": ["value1\nvalue2\nvalue3", "value4\nvalue5", "value6"],
    "Column2": ["a\nb\nc", "d\ne", "f"]
}
df = pd.DataFrame(data)
df_expanded = split_and_expand(df)
print(df_expanded)

# Display the DataFrames
# for i, df in enumerate(dataframes):
#   if i < 4:
#     continue  # PDF tables we don't want
#   print(f"Table {i}")
#   print(df)
#   df = df.drop([0])  # Drop header row. PDF is a mess.
#   print(df)
#   df = split_and_expand(df)
#   print(df)
#   break


# con = sqlite3.connect("nsorg.sqlite3")

sqlstr = """
  SELECT
    CASE WHEN FundingAmount <= 50000 THEN FundingAmount ELSE 0 END,
    CASE WHEN FundingAmount > 50000 AND FundingAmount < 1000000 THEN FundingAmount ELSE 0 END,
    CASE WHEN FundingAmount >= 1000000 THEN FundingAmount ELSE 0 END
  FROM awards
  WHERE FundingAmount > 0;
"""
# df10 = pd.read_sql_query(sqlstr, con)
# print(df10.head())


