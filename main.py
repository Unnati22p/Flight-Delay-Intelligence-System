from pyspark.sql import SparkSession  # Import SparkSession for creating Spark app
from pyspark.sql.functions import col, avg, hour, concat_ws, count, sum as _sum  # Import necessary PySpark SQL functions

# Step 1: Create Spark session
spark = SparkSession.builder.appName("FlightDelayAnalysis").getOrCreate()  # Initialize Spark session with app name

# Step 2: Load datasets
airlines_df = spark.read.csv("airlines.csv", header=True, inferSchema=True)  # Load airlines CSV with headers and schema inference
airports_df = spark.read.csv("airports.csv", header=True, inferSchema=True)  # Load airports CSV
flights_df = spark.read.csv("flights.csv", header=True, inferSchema=True)  # Load flights CSV

# Step 3: Rename for clarity
# Rename IATA_CODE to AIRLINE_CODE and AIRLINE to AIRLINE_NAME
airlines_df = airlines_df.withColumnRenamed("IATA_CODE", "AIRLINE_CODE") \
                         .withColumnRenamed("AIRLINE", "AIRLINE_NAME")

# Step 4: Join flights with airline names
flights_with_airlines = flights_df.join(airlines_df, flights_df.AIRLINE == airlines_df.AIRLINE_CODE, "left")  # Left join flights with airlines on code

# Step 5: Average delay by airline
# Group by airline and calculate average delay
avg_delay_by_airline = flights_with_airlines.groupBy("AIRLINE_NAME") \
    .agg(avg("ARRIVAL_DELAY").alias("AvgArrivalDelay")) \
    .orderBy(col("AvgArrivalDelay").desc())

print("\n🔴 Worst Performing Airlines by Average Arrival Delay:")  # Print section title
avg_delay_by_airline.show(10)  # Show top 10 worst performing airlines

# Step 6: Average delay by month
# Group flights by month and calculate average delay
avg_delay_by_month = flights_df.groupBy("MONTH") \
    .agg(avg("ARRIVAL_DELAY").alias("AvgArrivalDelay")) \
    .orderBy("MONTH")

print("\n📅 Average Arrival Delay by Month:")  # Print section title
avg_delay_by_month.show()  # Show results

# Step 7: Average delay by departure hour
from pyspark.sql.functions import floor  # Import floor function to truncate hours

# Extract departure hour from time
flights_df = flights_df.withColumn("DEP_HOUR", floor(col("DEPARTURE_TIME") / 100))
# Group by hour and calculate average delay
avg_delay_by_hour = flights_df.groupBy("DEP_HOUR") \
    .agg(avg("ARRIVAL_DELAY").alias("AvgArrivalDelay")) \
    .orderBy("DEP_HOUR")

print("\n⏰ Average Arrival Delay by Departure Hour:")  # Print section title
avg_delay_by_hour.show()  # Show results

# Step 8: Most delayed routes
# Create route column
flights_with_routes = flights_df.withColumn("ROUTE", concat_ws(" → ", "ORIGIN_AIRPORT", "DESTINATION_AIRPORT"))
# Group by route and calculate average delay and flight count
most_delayed_routes = flights_with_routes.groupBy("ROUTE") \
    .agg(avg("ARRIVAL_DELAY").alias("AvgArrivalDelay"), count("*").alias("FlightCount")) \
    .orderBy(col("AvgArrivalDelay").desc())

print("\n✈️ Top 5 Most Delayed Routes:")  # Print section title
most_delayed_routes.show(5)  # Show top 5 delayed routes

# Step 9: Cancellation Trends
cancelled_flights = flights_df.filter(col("CANCELLED") == 1)  # Filter only cancelled flights
# Group cancelled flights by reason
cancellation_by_reason = cancelled_flights.groupBy("CANCELLATION_REASON") \
    .count().orderBy(col("count").desc())

print("\n❌ Cancellation Reasons Count:")  # Print section title
cancellation_by_reason.show()  # Show cancellation reason counts

# Step 10: Delay Reasons Breakdown
delay_reason_cols = ["AIR_SYSTEM_DELAY", "SECURITY_DELAY", "AIRLINE_DELAY", "LATE_AIRCRAFT_DELAY", "WEATHER_DELAY"]  # List of delay reason columns
# Aggregate sum of each delay reason column
total_delay_reasons = flights_df.agg(*[_sum(col(c)).alias(c) for c in delay_reason_cols])

print("\n⏳ Total Delay Minutes by Reason:")  # Print section title
total_delay_reasons.show()  # Show total delay minutes for each reason

# Stop Spark session
spark.stop()  # Gracefully stop Spark session
