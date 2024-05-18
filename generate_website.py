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

site = {
  "title": "howdy howdy howdy",
  "df1":   df1.to_html(
    # Pandas: don't show column of row number (0,1,2,...)
    index=False,
    # https://datatables.net/manual/styling/classes#Table-classes
    table_id="myTable",
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
