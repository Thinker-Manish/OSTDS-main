"""
analysis.py

This module performs basic data analysis on a given dataset, including:
- Converting specified columns to numeric types.
- Generating summary statistics.
- Computing and displaying the correlation matrix.
- Visualizing the correlation matrix using a heatmap.

Author: [Aquil Iqbal]
Email : [aquiliqbal14@gmail.com]
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


def convert_columns_to_numeric(df: pd.DataFrame, column_list: list) -> pd.DataFrame:
    """
    Converts specified columns in the DataFrame to numeric data types.

    Args:
        df (pd.DataFrame): The input DataFrame.
        column_list (list): A list of column names to convert.

    Returns:
        pd.DataFrame: The DataFrame with specified columns converted to numeric values.
    """
    for column in column_list:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df


def analyze_data(file_path: str):
    """
    Loads a dataset, performs exploratory data analysis (EDA), 
    and visualizes the correlation matrix.

    Steps:
    - Reads the dataset from the specified file path.
    - Converts object-type columns to numeric where possible.
    - Removes rows with NaN values.
    - Prints summary statistics.
    - Computes and displays the correlation matrix.
    - Visualizes the correlation matrix using a heatmap.

    Args:
        file_path (str): Path to the dataset file.
    """
    # Load the dataset
    data = pd.read_csv(file_path)

    # Convert object-type columns to numeric where applicable
    columns_to_convert = data.select_dtypes(
        include=['object']).columns.tolist()
    data = convert_columns_to_numeric(data, columns_to_convert)

    # Drop rows with NaN values after conversion
    data = data.dropna()

    # Display basic statistics
    summary = data.describe()
    print("Summary Statistics:\n", summary)

    # Compute correlation matrix
    correlation = data.corr()
    print("\nCorrelation Matrix:\n", correlation)

    # Visualize correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix Heatmap")
    plt.show()


if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    analyze_data(os.path.join(base_dir, "..", "processed_data.csv")
                 )
