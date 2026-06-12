Flight Delay Intelligence System

A PySpark-based data analytics project that analyzes U.S. flight delays and cancellations. The project explores delay patterns across airlines, airports, routes, months, and departure times, and includes an interactive dashboard built with Dash and Plotly.

Tools & Technologies

* Python
* PySpark
* Pandas
* Matplotlib
* Seaborn
* Plotly
* Dash

Dataset

The analysis uses:

* flights.csv , Note: The original flights.csv dataset is not included in this repository due to file size limitations.
* airlines.csv
* airports.csv

Analysis Performed

* Flight cancellation analysis
* Cancellation reason distribution
* Average arrival delay by month
* Average arrival delay by departure hour
* Most delayed flight routes
* Delay causes analysis
* Airport delay geo-map

Dashboard

An interactive dashboard was built using Dash and Plotly to visualize:

* Monthly delay trends
* Cancellation reasons
* Most delayed routes

Key Insights

* Late aircraft delays were the largest contributor to overall delays.
* Early morning flights generally had lower delays.
* Some routes consistently showed much higher delays than others.
* Delay hotspots could be identified through airport geo-mapping.

Files

* report.ipynb – Complete analysis and visualizations
* main.py – PySpark analysis script
* airlines.csv, airports.csv, flights.csv – Dataset files
