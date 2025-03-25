"""
main.py

This script loads, cleans, and analyzes COVID-19 dataset.
It performs the following tasks:
- Loads a CSV file containing COVID-19 data
- Cleans the dataset by removing missing values and filtering for US data
- Saves the cleaned dataset
- Analyzes the dataset by generating statistical summaries
- Visualizes case fatality ratio and correlation matrix using Seaborn and Matplotlib

Author: [Aquil Iqbal]
Email : [aquiliqbal14@gmail.com]
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from logger import setup_logger
import os


def clean_data(df):
    """
    Cleans the given DataFrame by:
    - Dropping rows with missing values
    - Converting 'Last_Update' column to datetime format
    - Filtering data for the US only
    - Removing unnecessary columns ('Long_', 'Lat')

    Args:
        df (pd.DataFrame): Raw dataset

    Returns:
        pd.DataFrame: Cleaned dataset
    """
    df.dropna(inplace=True)
    df['Last_Update'] = pd.to_datetime(df['Last_Update'])
    logger.info(f"Columns in the dataset: {df.columns.tolist()}")

    if 'Country_Region' not in df.columns:
        logger.error("'Country_Region' column not found.")
        return pd.DataFrame()

    df = df[df['Country_Region'] == 'US']
    df.drop(columns=['Long_', 'Lat'], errors='ignore', inplace=True)
    return df


def load_data(file_path):
    """
    Loads data from a CSV file.

    Args:
        file_path (str): Path to the CSV file

    Returns:
        pd.DataFrame: Loaded dataset or None if loading fails
    """
    try:
        data = pd.read_csv(file_path)
        logger.info("Data successfully loaded")
        return data
    except FileNotFoundError:
        logger.error(
            f"File not found at path: {file_path}. Please check the file path.")
    except pd.errors.ParserError:
        logger.error("Error reading the CSV file. It may be malformed.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    return None


def save_cleaned_data(df, file_path):
    """
    Saves cleaned dataset to a CSV file.

    Args:
        df (pd.DataFrame): Cleaned dataset
        file_path (str): Destination path for the CSV file
    """
    try:
        df.to_csv(file_path, index=False)
        logger.info(f"Cleaned data saved to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save cleaned data: {e}")


def analyze_data(cleaned_data):
    """
    Analyzes cleaned data by:
    - Generating descriptive statistics grouped by state (if available)
    - Calculating and visualizing case fatality ratio
    - Plotting correlation matrix

    Args:
        cleaned_data (pd.DataFrame): Cleaned dataset
    """
    if cleaned_data.empty:
        logger.warning("No data available for analysis.")
        return

    if 'Province_State' in cleaned_data.columns:
        statewise_summary = cleaned_data.groupby('Province_State').describe()
        print(statewise_summary)

    if {'Deaths', 'Confirmed'}.issubset(cleaned_data.columns):
        cleaned_data['Case_Fatality_Ratio'] = cleaned_data.apply(
            lambda row: (row['Deaths'] / row['Confirmed'] *
                         100) if row['Confirmed'] > 0 else 0,
            axis=1
        )
        plot_case_fatality_ratio(cleaned_data['Case_Fatality_Ratio'])
        plot_correlation_matrix(cleaned_data)


def plot_case_fatality_ratio(case_fatality_ratio):
    """
    Plots a histogram of case fatality ratio.

    Args:
        case_fatality_ratio (pd.Series): Series containing case fatality ratios
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(case_fatality_ratio, kde=True)
    plt.title("Distribution of Case Fatality Ratio")
    plt.xlabel("Case Fatality Ratio (%)")
    plt.show()


def plot_correlation_matrix(cleaned_data):
    """
    Plots a heatmap of the correlation matrix for numerical columns.

    Args:
        cleaned_data (pd.DataFrame): Cleaned dataset
    """
    numeric_data = cleaned_data.select_dtypes(include=['float64', 'int64'])
    correlation = numeric_data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix")
    plt.show()


if __name__ == '__main__':
    # Setup logger
    logger = setup_logger(log_level="DEBUG")

    # Define file paths
    base_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(
        base_dir, "..", "01-01-2021 (1).csv")
    processed_file_path = os.path.join(
        base_dir, "..", "processed_data.csv")

    logger.warning("Running analysis on single file only")
    logger.info(f"Attempting to load data from: {csv_file_path}")

    # Load, clean, and analyze data
    df = load_data(csv_file_path)
    if df is not None:
        cleaned_data = clean_data(df)
        if not cleaned_data.empty:
            save_cleaned_data(cleaned_data, processed_file_path)
            analyze_data(cleaned_data)
        else:
            logger.error("Cleaned data is empty. Exiting the script.")
    else:
        logger.error("Data loading failed. Exiting the script.")
