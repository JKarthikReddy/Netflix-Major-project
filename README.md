import pandas as pd
import altair as alt

# Load the dataset
df = pd.read_csv("Netflix Dataset.csv")

# 1. Data Cleaning and Preparation
# Drop rows with missing Release_Date
df_cleaned = df.dropna(subset=['Release_Date']).copy()

# Strip whitespace from Release_Date
df_cleaned['Release_Date'] = df_cleaned['Release_Date'].str.strip()

# Convert Release_Date to datetime, using errors='coerce' to handle bad formats
df_cleaned['Release_Date'] = pd.to_datetime(df_cleaned['Release_Date'], format='%B %d, %Y', errors='coerce')

# Drop rows where date conversion failed (resulted in NaT)
df_cleaned.dropna(subset=['Release_Date'], inplace=True)

# Extract Release Year and convert to integer
df_cleaned['Release_Year'] = df_cleaned['Release_Date'].dt.year.astype(int)

# Rename columns for clarity
df_cleaned.rename(columns={
    'Category': 'Content_Type',
    'Type': 'Genre'
}, inplace=True)

# Define the analysis period (2008 to 2021)
START_YEAR = 2008
END_YEAR = 2021
df_filtered = df_cleaned[(df_cleaned['Release_Year'] >= START_YEAR) & (df_cleaned['Release_Year'] <= END_YEAR)].copy()


# 2. Objective 1 Analysis: Movies vs. TV Shows Distribution Over the Years
# Group by year and content type and count the entries
yearly_content_type = df_filtered.groupby(['Release_Year', 'Content_Type']).size().reset_index(name='Count')

# Create the stacked bar chart
chart_content_type = alt.Chart(yearly_content_type).mark_bar().encode(
    x=alt.X('Release_Year:O', title='Release Year'),
    y=alt.Y('Count', title='Number of Titles Added'),
    color='Content_Type',
    tooltip=['Release_Year', 'Content_Type', 'Count']
).properties(
    title='Annual Content Addition by Type (Movies vs. TV Shows): 2008-2021'
).interactive()

# Save the chart as annual_content_addition_by_type.json
chart_content_type.save('annual_content_addition_by_type.json')
