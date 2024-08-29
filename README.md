# Global Flight Price Prediction

The Global Flight Price Prediction project aims to predict flight prices based on various inputs such as origin, destination, budget, expected travel date, and the date of query. This involves collecting and analyzing data related to airports, airlines, global flight data, and price information. The predictive model will be deployed on a website for user interaction.

## Project Overview

### Purpose

The primary goal of this project is to build a machine learning model that can accurately predict flight prices. The model will assist users in finding the best flight deals by providing price predictions based on their input criteria.

### Key Components

1. **Data Collection:**
   - Collect detailed information about airports and airlines.
   - Gather global flight data, including schedules and routes.
   - Scrape and store flight price data for analysis.

2. **Data Processing:**
   - Clean and preprocess the collected data.
   - Store the data in a structured format in a MySQL database.

3. **Model Training:**
   - Use the processed data to train machine learning models.
   - Evaluate and select the best-performing model for price prediction.

4. **Deployment:**
   - Deploy the trained model on a website.
   - Provide a user-friendly interface for inputting flight search criteria.
   - Display predicted flight prices based on user inputs.

## Folder Structure

- `data-management/`
  - **Purpose:** Contains scripts and resources for the initial development cycle focused on loading and scraping data related to airlines, airports, flights, routes, and prices.
  - Subfolders:
    - `configuration/`: Controls data storage method: Database or `CSV` file.
    - `data-visualization/`: Stores data as CSV file for visualization if cannot connect to database.
    - `loading-scripts/`: Contains scripts that directly load `.dat` file into database.
    - `scraping-scripts/`: Contains scripst that scrapes website and load information to the database or as `CSV`.
