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

pages = [
  "13,14,15,16,17",     # First table
  "18,19,20,21,22,23",  # Second table
  "24,25,26,27",        # Third table
  # "28,29,30,31",        # Fourth table
]
pages = ','.join(pages)

# Read tables from a PDF file
tables = camelot.read_pdf("appendix_f.pdf", pages=pages, split_text=True)
print("read_pdf() is done")
i = 0
for table in tables:
  # Kick out JSON files so we can inspect them to see how disappointed (or not) we are in Camelot.
  table.to_json("debug/" + str(i) + ".json")
  i += 1

# Convert each table into a DataFrame
dataframes = [table.df for table in tables]
print("conversion of all tables to dataframes is done")


# Function to count the number of elements in a cell
def count_elements(cell):
  if pd.isna(cell):
    return 0
  return len(cell.split('\n'))  # There's no such argument allowed here: expand=True))


# Drop columns that only have one element after we split()
def drop_columns_that_dont_split(df):
  print("Welcome to drop_columns_that_dont_split()")
  # Inspect the DataFrame and drop columns with only one element in each cell after split
  columns_to_drop = []

  for column in df.columns:
    # unique_counts = df[column].apply(lambda cell: count_elements(cell)).nunique()
    count = df[column].apply(lambda cell: count_elements(cell)).iloc[0]
    # print("=========")
    # print(count)
    # print("=========")
    # count = count_elements(column)
    # print("For column", column, "count elements is", count)
    if count == 1:
      # if unique_counts == 1:
      columns_to_drop.append(column)

  # Drop the columns
  df_cleaned = df.drop(columns=columns_to_drop)
  # Rename columns to sequential integers so the now-missing columns don't leave gaps in the column IDs
  df_cleaned.columns = range(df_cleaned.shape[1])
  # print(df_cleaned)
  return df_cleaned


# Function to split DataFrame
def split(df):

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

  # -----------------
  # Jay's helpful debugging:
  # for column in df.columns:
    # df[column] = df[column].str.split('\n', expand=True)
  #   print("------- debug 2 for column", column, "----------")
    # print(debug.iloc[0])
  #   val = df.iat[0, column]  # Leave Pandas, get back to Python str
  #   print(repr(val))  # print \n, not newline. So I can see 'em
  #   print(type(val))  # Python str
  #   print("--------------------------")
  #   debug = df[column].str.split('\n', expand=True)
  #   print(debug)
  #   print("-------- end -------------\n")
  # -----------------

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
  # Can't expand=True here either:
  # TypeError: DataFrame.explode() missing 1 required positional argument: 'column'

  # df = df.apply(lambda x: x.str.split('\n').explode()).reset_index(drop=True)
  df = df.apply(lambda x: x.str.split('\n'))
  # ValueError: cannot reindex on an axis with duplicate labels
  return df


# Function to split DataFrame
def explode(df):
  df = df.apply(lambda x: x.explode()).reset_index(drop=True)
  # ValueError: cannot reindex on an axis with duplicate labels
  return df


# Apply the function to the DataFrame
# df_expanded = split_and_expand(df)


data = {
    "Column1": ["value1\nvalue2\nvalue3", "value4\nvalue5", "value6"],
    "Column2": ["a\nb\nc", "d\ne", "f"]
}
df = pd.DataFrame(data)
# df_expanded = split_and_expand(df)
# print(df_expanded)


def clean_and_concat_dataframes(begin, end):
  df = pd.DataFrame({})
  i = begin
  while i < end:
    this_df = dataframes[i]
    print("Going to try to concat in dataframe #", i, ":")
    print("-------------------")
    print(this_df)
    print("-------------------")
    this_df = this_df.drop([0])  # Drop header row. PDF is a mess.
    this_df = drop_columns_that_dont_split(this_df)
    this_df = split_and_expand(this_df)
    df = pd.concat([df, this_df])
    i += 1
  return df


# The first actual dataframe we want to extract is 4..8 from the messy set of all dataframes extracted above
# lol, can't even do this, because it's inconsistent:
# df1 = clean_and_concat_dataframes(4, 8)
df1 = dataframes[0]
df1 = df1.drop([0])  # Drop header row. PDF is a mess.
df1 = drop_columns_that_dont_split(df1)
df1 = split(df1)
df1 = explode(df1)
# Success: we now have PDF page 13
# Where is PDF page 14??
this_df = dataframes[1]
this_df = this_df.drop([0])  # Drop header row. PDF is a mess.
this_df = drop_columns_that_dont_split(this_df)
this_df = split(this_df)
this_df = explode(this_df)
# Success: we now have PDF page 15 (fancy, this one has no header row)
# Where is PDF page 16??
df1 = pd.concat([df1, this_df])
this_df = dataframes[2]
this_df = drop_columns_that_dont_split(this_df)
this_df = split(this_df)
this_df = explode(this_df)
# Success: we now have PDF page 17
df1 = pd.concat([df1, this_df]).reset_index(drop=True)
print(df1)

# PDF page 18 begins the second set of tabular data:
df2 = dataframes[3]
df2 = df2.drop([0])  # Drop header row. PDF is a mess.
df2 = drop_columns_that_dont_split(df2)
df2 = split(df2)
# Gah, the PDF has a blank so the list is 1 element short of the length of the others.
# We need to fill that blank with None or explode() is going to explode.
# In a runtime error sort of way, not the way we want. ;)
df2.iat[0, 4].insert(30, None)
df2 = explode(df2)

# PDF page 23
this_df = dataframes[4]
this_df = this_df.drop([1])  # Drop footer row. PDF is a mess.
this_df = drop_columns_that_dont_split(this_df)
this_df = split(this_df)
this_df = explode(this_df)
df2 = pd.concat([df2, this_df]).reset_index(drop=True)
print(df2)

# PDF page 24
# OH DEAR DOG THIS IS A BLANKNESS NIGHTMARE that Camelot above detects absolutely no
# blankness in...
this_df = dataframes[5]
this_df = this_df.drop([0])  # Drop header row. PDF is a mess.
print(this_df)


# The first actual dataframe we want to extract is 4..8 from the messy set of all dataframes extracted above
# df1 = dataframes[4]
# df1 = df1.drop([0])  # Drop header row. PDF is a mess.
# df1 = drop_columns_that_dont_split(df1)
# df1 = split_and_expand(df1)
# print(df1)


# Display the DataFrames
def naively_loop_all_dataframes():
  for i, df in enumerate(dataframes):
    if i < 4:
      continue  # PDF tables we don't want
    print(f"Table {i}")
    print(df)
    df = df.drop([0])  # Drop header row. PDF is a mess.
    print(df)
    print("------ here are the index value counts: --------------------")
    print(df.index.value_counts())
    print("------ element counts ----------")
    # Apply the function to each cell in the DataFrame
    element_counts = df.applymap(count_elements)
    # Display the DataFrame with element counts
    print(element_counts)
    print("------ Drop columns ----------------")
    df = drop_columns_that_dont_split(df)
    print(df)
    print("------- split and expand -------------------")
    df = split_and_expand(df)
    print(df)
    break


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
