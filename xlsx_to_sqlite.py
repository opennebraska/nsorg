import pandas as pd
import sqlite3

# pd.options.display.max_columns = None
# pd.options.display.max_rows = None
# pd.options.display.width = 1000

# https://stackoverflow.com/a/61473956/4656035
conn = sqlite3.connect("data/nsorg.sqlite3")

df1 = pd.read_excel('data/public_records_request/Grant Application.xlsx', sheet_name=0)
print(df1.head())
print('----------------------')
# print(df1.columns.tolist())
# print(df1.loc[0, :])
# Drop row 2
df1.drop(df1.index[0], inplace=True)
# Provide new column names to be database friendly
df1.columns = [
  "ID",
  "OrgName",
  "PhysicalAddress",
  "MailingAddress",
  "Website",
  "SocialMediaAccounts",
  "Name",
  "Title",
  "EmailAddress",
  "Phone",
  "Team",
  "TeamExplanation",
  "OrganizationalChart",
  "OtherCompletedProjects",
  "ProposalTitle",
  "TotalBudget",
  "LB1024GrantFundingRequest",
  "ProposalType",
  "BriefProposalSummary",
  "Timeline",
  "PercentageCompletedByJuly2025",
  "FundingGoals",
  "Community Needs",
  "OtherExplanation",
  "ProposalDescriptionAndNeedsAlignment",
  "VisioningWorkshopFindingsAlignment",
  "PrioritiesAlignment",
  "EconomicImpact",
  "EconomicImpactPermanentJobsCreated",
  "EconomicImpactTemporaryJobsCreated",
  "EconomicImpactWageLevels",
  "EconomicImpactAlignProposedJobs",
  "CommunityBenefit",
  "CommunityBenefitSustainability",
  "BestPracticesInnovation",
  "OutcomeMeasurement",
  "OutcomeMeasurementHow",
  "OutcomeMeasurementCoinvestment",
  "Partnerships",
  "PartnershipsOrgs",
  "PartnershipsMOU",
  "Displacement",
  "DisplacementExplanation",
  "PhysicalLocation",
  "QualifiedCensusTract",
  "AdditionalLocationDocuments",
  "PropertyZoning",
  "ConnectedToUtilities",
  "ConnectedToUtilitiesConnected",
  "ConnectedToUtilitiesUpgradesNeeded",
  "DesignEstimatingBidding",
  "DesignEstimatingBiddingPackageDeveloped",
  "DesignEstimatingBiddingCostsDetermined",
  "GeneralContractor",
  "GeneralContractorPublicCompetitiveBid",
  "GeneralContractorPublicCompetitiveBidWhyNot",
  "RequestRationale",
  "GrantFundsUsage",
  "ProposalFinancialSustainability",
  "ProposalFinancialSustainabilityOperations",
  "FundingSources",
  "FundingSourcesPendingDecisions",
  "FundingSourcesCannotContinue",
  "Scalability",
  "ScalabilityComponents",
  "FinancialCommitment",
  "ARPAComplianceAcknowledgment",
  "ARPAReportingMonitoringProcessAck",
  "LB1024FundingSourcesAck",
  "PublicInformation",
  "FileUploads"
]
# Change to Pandas int to get rid of all the ".0"s
df1["ID"] = df1["ID"].astype('Int64')  # capital I

print(df1.head())
# df2 = df2[~df2["school"].str.contains("Total", na=False)]

# Create a database table and write all the dataframe data into it
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
df1.to_sql("applications", conn, if_exists="replace", index=False)
conn.execute('CREATE INDEX "ix_applications_index" ON "applications" ("ID")')


"""
df2 = pd.read_excel(
  'data/SchoolLevel_RaceGenderGradeMembership_1718to1920.xlsx',
  sheet_name=1,
  usecols="A:W",
  header=None,
  skiprows=3,    # Drop the 3 header rows, the human-friendly formatting is confusing
  skipfooter=1,  # Also drop grand total row at the bottom
)
"""
df2 = pd.read_excel('data/public_records_request/NSORG Awards Data.xlsx', sheet_name=0)
print(df2.head())
# Provide new column names to be database friendly
df2.columns = [
  "DropMe",
  "Category",
  "ProposalName",
  "OrganizationName",
  "NSORGID",
  "FundingAmount",
]
# Drop column A
df2 = df2.drop(["DropMe"], axis=1)
# Drop row 1
df2.drop(df2.index[0], inplace=True)
# Drop all rows with "Total" in the Category column
df2 = df2[~df2["Category"].str.contains("Total", na=False)]

# They didn't re-state the Category every time, which is convenient for humans, but terrible
# for data processing. Luckily Pandas can fill the missing data back in for us:
df2["Category"] = df2["Category"].ffill()
# Change to Pandas float so we don't end up with SQLite TEXT
df2["FundingAmount"] = df2["FundingAmount"].astype('float')

print("Final dataframe:")
print(df2.head())

# Create a database table and write all the dataframe data into it
df2.to_sql("awards", conn, if_exists="replace")


conn.commit()
conn.close()
