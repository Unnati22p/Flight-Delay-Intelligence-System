import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load data
flights = pd.read_csv('data/flights.csv')
airlines = pd.read_csv('data/airlines.csv')
airports = pd.read_csv('data/airports.csv')

# Preprocess
flights['ROUTE'] = flights['ORIGIN_AIRPORT'].astype(str) + " → " + flights['DESTINATION_AIRPORT'].astype(str)
avg_delay_by_month = flights.groupby('MONTH')['ARRIVAL_DELAY'].mean().reset_index()
cancellation_reasons = flights['CANCELLATION_REASON'].value_counts().reset_index()
cancellation_reasons.columns = ['Reason', 'Count']
delayed_routes = flights.groupby('ROUTE')['ARRIVAL_DELAY'].mean().reset_index().sort_values(by='ARRIVAL_DELAY', ascending=False).head(5)

# Initialize app
app = dash.Dash(__name__)
app.title = "Flight Delay Dashboard"

# Layout
app.layout = html.Div([
    html.H1("✈️ Flight Delay Dashboard", style={'textAlign': 'center'}),

    dcc.Graph(
        figure=px.bar(
            avg_delay_by_month,
            x='MONTH',
            y='ARRIVAL_DELAY',
            title="Average Arrival Delay by Month",
            labels={'ARRIVAL_DELAY': 'Avg Arrival Delay (min)'}
        )
    ),

    dcc.Graph(
        figure=px.pie(
            cancellation_reasons,
            names='Reason',
            values='Count',
            title="Flight Cancellation Reasons"
        )
    ),

    dcc.Graph(
        figure=px.bar(
            delayed_routes,
            x='ARRIVAL_DELAY',
            y='ROUTE',
            orientation='h',
            title="Top 5 Most Delayed Routes",
            labels={'ARRIVAL_DELAY': 'Avg Delay (min)', 'ROUTE': 'Route'}
        )
    )
])

# Run server
if __name__ == '__main__':
    app.run(debug=True)


