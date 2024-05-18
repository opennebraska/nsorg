import pandas as pd
import numpy as np
import matplotlib.pyplot as plt   # https://pandas.pydata.org/docs/user_guide/visualization.html#basic-plotting-plot
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
print(df2.head())

sqlstr = """
  SELECT *
  FROM applications
"""
df100 = pd.read_sql_query(sqlstr, con)
print(df100.head())


# Formatters for Pandas to_html() https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_html.html
def money(x): return '${:,.0f}'.format(x)
def make_zero_empty(x): return '{0:.0f}'.format(x) if x > 0 else ''
def make_zero_empty_two_digits(x): return '{0:.2f}'.format(x) if x > 0 else ''


site = {
  "title": "Open/Nebraska: North & South Omaha Recovery Grant Program (NSORG)",
  "df1":   df1.to_html(
    # Pandas: don't show column of row number (0,1,2,...)
    index=False,
    # Pandas: format our floats
    float_format=money,
    # Datatables optionals: https://datatables.net/manual/styling/classes#Table-classes
    table_id="df1",
    classes=["display", "compact"]
  ),
  "df2":   df2.to_html(
    index=False,
    float_format=money,
    table_id="df2",
    classes=["display", "compact"]
  ),
  "proposal_count":  proposal_count,
  "total_budget":    money(total_budget),
  "total_requested": money(total_requested),
  "total_awarded":   money(total_awarded),
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


# sns_plot = sns.barplot(data=df1, x="students", y="RaceEthnicity")
# plt.savefig('d1.png', bbox_inches='tight')
# plt.clf()  # https://stackoverflow.com/questions/741877/how-do-i-tell-matplotlib-that-i-am-done-with-a-plot
# raw(df1.to_html(index=False))
# raw('<img src="d1.png">')


# with open('index.html', 'w') as f:
#   f.write(doc.render())
