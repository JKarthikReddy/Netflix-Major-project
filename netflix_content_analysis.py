 import pandas as pd
import altair as alt

# --- 1. DATA LOADING AND CLEANING ---

# Load the dataset
# Replace 'path/to/your/Netflix Dataset.csv' with the actual path to your file
df = pd.read_csv("/content/Netflix Dataset.csv")

# 1.1 Data Preparation for Time-Series Analysis
# Drop rows with missing Release_Date, as it's crucial for time-series analysis
df_cleaned = df.dropna(subset=['Release_Date']).copy()

# Strip whitespace from Release_Date to fix parsing issues
df_cleaned['Release_Date'] = df_cleaned['Release_Date'].str.strip()

# Convert Release_Date to datetime, using errors='coerce' to handle bad formats
df_cleaned['Release_Date'] = pd.to_datetime(df_cleaned['Release_Date'], format='%B %d, %Y', errors='coerce')

# Drop rows where date conversion failed (resulted in NaT)
df_cleaned.dropna(subset=['Release_Date'], inplace=True)

# Extract Release Year and convert to integer
df_cleaned['Release_Year'] = df_cleaned['Release_Date'].dt.year.astype(int)

# Rename columns for clarity based on the problem statement
df_cleaned.rename(columns={
    'Category': 'Content_Type', # For 'Movies vs. TV Shows'
    'Type': 'Genre'             # For genre analysis
}, inplace=True)

# Define the analysis period (2008 to 2021)
START_YEAR = 2008
END_YEAR = 2021
df_filtered = df_cleaned[(df_cleaned['Release_Year'] >= START_YEAR) & (df_cleaned['Release_Year'] <= END_YEAR)].copy()


# --- 2. OBJECTIVE 1: MOVIES VS. TV SHOWS DISTRIBUTION OVER THE YEARS ---

# Group by year and content type and count the entries
yearly_content_type = df_filtered.groupby(['Release_Year', 'Content_Type']).size().reset_index(name='Count')

# Create the stacked bar chart for content type trends
chart_content_type = alt.Chart(yearly_content_type).mark_bar().encode(
    x=alt.X('Release_Year:O', title='Release Year'),
    y=alt.Y('Count', title='Number of Titles Added'),
    color='Content_Type',
    tooltip=['Release_Year', 'Content_Type', 'Count']
).properties(
    title='Annual Content Addition by Type (Movies vs. TV Shows): 2008-2021'
).interactive()

# Save the chart
chart_content_type.save('annual_content_addition_by_type.json')
print("Generated: annual_content_addition_by_type.json")


# --- 3. OBJECTIVE 2: IDENTIFYING AND TRACKING GENRE POPULARITY ---

# 3.1 Prepare the Genre data (split comma-separated values)
genre_df = df_filtered[['Release_Year', 'Genre']].copy()
genre_df['Genre'] = genre_df['Genre'].str.split(', ')
genre_exploded = genre_df.explode('Genre').copy()
genre_exploded['Genre'] = genre_exploded['Genre'].str.strip() # Clean whitespace

# 3.2 Calculate top 10 overall genres
top_genres = genre_exploded['Genre'].value_counts().nlargest(10).index.tolist()

# Filter data to include only the top 10 genres
top_genres_yearly = genre_exploded[genre_exploded['Genre'].isin(top_genres)]

# Group by year and genre and count the titles
genre_trends = top_genres_yearly.groupby(['Release_Year', 'Genre']).size().reset_index(name='Count')

# Create the line chart for genre trends
chart_genre_trends = alt.Chart(genre_trends).mark_line(point=True).encode(
    x=alt.X('Release_Year:O', title='Release Year'),
    y=alt.Y('Count', title='Number of Titles Added'),
    color='Genre',
    tooltip=['Release_Year', 'Genre', 'Count']
).properties(
    title='Annual Content Addition for Top 10 Genres: 2008-2021'
).interactive()

# Save the chart
chart_genre_trends.save('annual_genre_trends.json')
print("Generated: annual_genre_trends.json")


# --- 4. OBJECTIVE 3: COMPARING COUNTRY-WISE CONTRIBUTIONS ---

# 4.1 Prepare the Country data (split comma-separated values)
country_df = df_cleaned[['Country']].copy() # Use the full cleaned set for overall contributions
country_df['Country'] = country_df['Country'].str.split(', ')
country_exploded = country_df.explode('Country').copy()

# 4.2 Clean and filter country data
country_exploded['Country'] = country_exploded['Country'].str.strip()
country_exploded.dropna(subset=['Country'], inplace=True)
country_exploded = country_exploded[country_exploded['Country'] != '']

# 4.3 Calculate the overall frequency of the top 10 countries
country_counts = country_exploded['Country'].value_counts().nlargest(10).reset_index()
country_counts.columns = ['Country', 'Count']

# Create the bar chart for country contributions
chart_country_contributions = alt.Chart(country_counts).mark_bar().encode(
    x=alt.X('Count', title='Number of Titles'),
    # Sort the y-axis by the count in descending order
    y=alt.Y('Country:N', sort='-x', title='Country'),
    tooltip=['Country', 'Count']
).properties(
    title='Top 10 Countries Contributing to Netflix Catalog'
)

# Save the chart
chart_country_contributions.save('top_10_country_contributions.json')
print("Generated: top_10_country_contributions.json")

# --- END OF ANALYSIS CODE ---
 import altair as alt
import json

# Load the JSON files and save them as PNG
# Load the chart specifications from the JSON files
with open('annual_content_addition_by_type.json', 'r') as f:
    chart_content_type_spec = json.load(f)

with open('annual_genre_trends.json', 'r') as f:
    chart_genre_trends_spec = json.load(f)

with open('top_10_country_contributions.json', 'r') as f:
    chart_country_contributions_spec = json.load(f)

# Create chart objects from the specifications
chart_content_type = alt.Chart.from_dict(chart_content_type_spec)
chart_genre_trends = alt.Chart.from_dict(chart_genre_trends_spec)
chart_country_contributions = alt.Chart.from_dict(chart_country_contributions_spec)


# Save the charts as PNG using altair_saver
chart_content_type.save('annual_content_addition_by_type.png')
chart_genre_trends.save('annual_genre_trends.png')
chart_country_contributions.save('top_10_country_contributions.png')

print("Generated: annual_content_addition_by_type.png")
print("Generated: annual_genre_trends.png")
print("Generated: top_10_country_contributions.png")
