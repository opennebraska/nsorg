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
  SELECT Category, sum(FundingAmount)
  FROM awards
  GROUP BY 1;
"""
df1 = pd.read_sql_query(sqlstr, con)
print(df1.head())

sqlstr = """
  SELECT ID, Category, OrgName, ProposalTitle, TotalBudget, LB1024GrantFundingRequest, sum(FundingAmount)
  FROM applications ap
  JOIN awards aw ON (aw.NSORGID = ap.ID)
  GROUP BY 1;
"""
df2 = pd.read_sql_query(sqlstr, con)
print(df2.head())


site = {
  "title": "howdy howdy howdy",
  "df1":   df1.to_html(
    # Pandas: don't show column of row number (0,1,2,...)
    index=False,
    # https://datatables.net/manual/styling/classes#Table-classes
    table_id="df1",
    classes=["display", "compact"]
  ),
  "df2":   df2.to_html(
    # Pandas: don't show column of row number (0,1,2,...)
    index=False,
    # https://datatables.net/manual/styling/classes#Table-classes
    table_id="df2",
    classes=["display", "compact"]
  ),
}
template = env.get_template("base.liquid")
with open('_site/index.html', 'w') as f:
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
