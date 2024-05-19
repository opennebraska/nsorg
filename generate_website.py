import pandas as pd
import numpy as np
import matplotlib.pyplot as plt   # https://pandas.pydata.org/docs/user_guide/visualization.html#basic-plotting-plot
from matplotlib.ticker import FuncFormatter
# For prettier plots: https://pandas.pydata.org/community/ecosystem.html
import seaborn as sns  # https://seaborn.pydata.org
import sqlite3
# https://liquid.readthedocs.io/en/latest/
# A Python implementation of Liquid, the safe customer-facing template language for flexible web apps.
from liquid import Environment
from liquid import FileSystemLoader

env = Environment(loader=FileSystemLoader("templates/"))

con = sqlite3.connect("nsorg.sqlite3")

sqlstr = """
  SELECT count(ID) Proposals, sum(TotalBudget) Budget, sum(LB1024GrantFundingRequest) Requested
  FROM applications ap
"""
res = con.execute(sqlstr)
proposal_count, total_budget, total_requested = res.fetchone()

sqlstr = """
  SELECT sum(FundingAmount) Awarded
  FROM awards
"""
res = con.execute(sqlstr)
total_awarded = res.fetchone()[0]

sqlstr = """
  SELECT count(*)
  FROM awards
  WHERE FundingAmount = 0;
"""
res = con.execute(sqlstr)
proposals_awarded_0 = res.fetchone()[0]

df1 = pd.read_sql_query(sqlstr, con)
print(df1.head())

sqlstr = """
  SELECT Category, count(ID) Proposals, sum(TotalBudget) Budget, sum(LB1024GrantFundingRequest) Requested, sum(FundingAmount) Awarded
  FROM applications ap
  JOIN awards aw ON (aw.NSORGID = ap.ID)
  GROUP BY 1;
"""
df1 = pd.read_sql_query(sqlstr, con)
print(df1.head())

sqlstr = """
  SELECT ID, Category, OrgName Organization, ProposalTitle Title, TotalBudget Budget, LB1024GrantFundingRequest Requested, sum(FundingAmount) Awarded
  FROM applications ap
  JOIN awards aw ON (aw.NSORGID = ap.ID)
  GROUP BY 1;
"""
df2 = pd.read_sql_query(sqlstr, con)
df2['ID'] = df2['ID'].apply(lambda x: f'<a href="app/{x}.html" target="_blank">{x}</a>')
print(df2.head())

sqlstr = """
  SELECT FundingAmount Award, count(*) Count
  FROM awards
  GROUP BY 1;
"""
df10 = pd.read_sql_query(sqlstr, con)
print(df10.head())
# Sample DataFrame
data = {
    "Grant": ["Grant A", "Grant B", "Grant C", "Grant D", "Grant E"],
    "Category A": [10, 20, 30, 40, 50],
    "Category B": [5, 15, 25, 35, 45],
    "Category C": [20, 10, 30, 10, 20]
}
df = pd.DataFrame(data)

# Set the index to Grant for easy plotting
df.set_index('Grant', inplace=True)

# Plotting the stacked bar chart
ax = df.plot(kind='bar', stacked=True, figsize=(10, 7), colormap='viridis')

# Add title and labels
plt.title("Stacked Bar Chart of Grants by Category")
plt.xlabel("Grant")
plt.ylabel("Value")

# Display the legend
plt.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig('_site/d10.png', bbox_inches='tight')
plt.clf()  # https://stackoverflow.com/questions/741877/how-do-i-tell-matplotlib-that-i-am-done-with-a-plot


# Formatters for Pandas to_html() https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_html.html
def money(x): return '${:,.0f}'.format(x)
# Function to format the y-axis labels as currency
def money_formatter(x, pos): return '${:,.0f}'.format(x)
def make_zero_empty(x): return '{0:.0f}'.format(x) if x > 0 else ''
def make_zero_empty_two_digits(x): return '{0:.2f}'.format(x) if x > 0 else ''


sqlstr = """
  SELECT ID, FundingAmount Awarded
  FROM applications ap
  JOIN awards aw ON (aw.NSORGID = ap.ID)
  WHERE FundingAmount
  ORDER BY 2 DESC;
"""
df50 = pd.read_sql_query(sqlstr, con)
df50['ID'] = df50['ID'].astype(str)  # So the graph doesn't try to treat as numbers
# df10['Awarded'] = df10['Awarded'].apply(money)
print(df50.head())
sns_plot = sns.barplot(data=df50, x="ID", y="Awarded", width=1.0)
# Make the money look like money, not scientific notation.
sns_plot.yaxis.set_major_formatter(FuncFormatter(money_formatter))
# Suppress labelling the application IDs. Too messy.
sns_plot.set_xticklabels([''] * len(df50))
plt.xlabel('Awards > $0')
plt.ylabel('Award')
plt.savefig('_site/d50-1.png', bbox_inches='tight')
plt.clf()  # https://stackoverflow.com/questions/741877/how-do-i-tell-matplotlib-that-i-am-done-with-a-plot
# raw(df1.to_html(index=False))
# raw('<img src="d1.png">')

sns_plot = sns.histplot(data=df50, x="Awarded", kde=True)  # , bins=range(10000), kde=False, discrete=True)
# plt.title('Number of Employees by Salary')
plt.xlabel('Award')
plt.ylabel('Number of Awards')
sns_plot.xaxis.set_major_formatter(FuncFormatter(money_formatter))
plt.xticks(rotation=90)
plt.savefig('_site/d50-2.png', bbox_inches='tight')
plt.clf()

# award_counts = df50["Awarded"].value_counts()
# plt.pie(award_counts, labels=award_counts.index, autopct='%1.1f%%', startangle=140)
plt.pie(df50['Awarded'])
plt.title('Award distribution')
# plt.xlabel('Award')
# plt.ylabel('Number of Awards')
# sns_plot.xaxis.set_major_formatter(FuncFormatter(money_formatter))
# plt.xticks(rotation=90)
plt.savefig('_site/d50-3.png', bbox_inches='tight')
plt.clf()


sqlstr = """
  SELECT *
  FROM applications
"""
df100 = pd.read_sql_query(sqlstr, con)
print(df100.head())


site = {
  "title": "Open/Nebraska: North & South Omaha Recovery Grant Program (NSORG)",
  "df1": df1.to_html(
    # Pandas: don't show column of row number (0,1,2,...)
    index=False,
    # Pandas: format our floats
    float_format=money,
    # Datatables optionals: https://datatables.net/manual/styling/classes#Table-classes
    table_id="df1",
    classes=["display", "compact"]
  ),
  "df2": df2.to_html(
    index=False,
    float_format=money,
    # Pandas: don't escape the hyperlinks we added above
    escape=False,
    table_id="df2",
    classes=["display", "compact"]
  ),
  "df10": df10.to_html(
    index=False,
    float_format=money,
    table_id="df10",
    classes=["display", "compact"]
  ),
  "proposal_count":      proposal_count,
  "total_budget":        money(total_budget),
  "total_requested":     money(total_requested),
  "total_awarded":       money(total_awarded),
  "proposals_awarded_0": proposals_awarded_0,
}
template = env.get_template("base.liquid")
with open('_site/index.html', 'w') as f:
  f.write(
    template.render(site)
  )

site = {
  "title": site['title'],
}
template = env.get_template("application.liquid")
for index, row in df100.iterrows():
  html_file = '_site/app/%s.html' % row['ID']
  # print(row)
  site['row'] = row
  row_dict = row.to_dict()
  # Python Liquid can't handle dicts? So flatten to a list:
  site['row_items'] = [(key, value) for key, value in row_dict.items()]
  with open(html_file, 'w') as f:
    f.write(
      template.render(site)
    )
