import pandas as pd
import matplotlib.pyplot as plt

snowfall = pd.read_html("https://www.extremeweatherwatch.com/cities/fort-wayne/snowiest-winter-season")[0]

# Calculate rolling averages
snowfall['R5'] = snowfall['Snow (inches)'].rolling(5).mean()
snowfall['R10'] = snowfall['Snow (inches)'].rolling(10).mean()

# Plot
snowfall.drop(columns='Rank').sort_values('Year').plot(x='Year')
plt.show()