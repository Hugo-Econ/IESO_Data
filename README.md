Web Scraping IESO Market Data to SQL for Grid Analysis

🧠 Project Overview
This project supports an analysis of the impact of battery energy storage on Ontario's electricity grid. To do this, I extract and structure operational and market data from Ontario's Independent Electricity System Operator (IESO).

Specifically, the workflow includes:

Scraping generator performance and price data directly from the IESO public data repository

Matching generator capabilities with actual dispatch and zonal marginal prices

Storing the processed data in a SQLite database for easy querying and analysis

The result is a clean, SQL-queryable dataset that enables deeper exploration of energy storage behavior and its market effects.

🔧 Data Sources
IESO Public Reports
https://www.ieso.ca/en/Power-Data/Data-Directory

Reports include:

Generator capability and output

Available capacity

Zonal and locational marginal prices (5-minute and hourly)

🛠️ Tools
Python 3

requests, pandas, beautifulsoup4 for scraping and parsing

sqlite3 for compact SQL storage

📁 Output
All data is stored in a SQLite file (.sqlite) with structured tables:

lmp_data – Real-time marginal prices (5-min intervals)

Additional tables can be added for generator dispatch and forecasts

✅ Status
✅ Web scraping implemented for selected hourly reports

✅ Latest file versions auto-detected

✅ Data import into SQLite working and tested

🚧 In progress: full month automation, timestamp alignment, cross-source merging

📊 Use Cases
Analyze storage dispatch vs. market signals

Compare generator performance across zones

Evaluate trends in congestion and energy loss pricing
