# -*- coding: utf-8 -*-
"""
Data loading functionality.

This module contains functions for loading and retrieving data from various sources.
"""
import os
import pandas as pd


def get_data_path(subfolder='raw'):
    """
    Get the path to the data directory.
    
    Parameters
    ----------
    subfolder : str, optional
        Subdirectory within the data directory, by default 'raw'
    
    Returns
    -------
    str
        Path to the data directory
    """
    # Get the absolute path of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate to the data directory (2 levels up from src/data)
    data_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'data', subfolder)
    
    return data_dir


def load_dataset(filename, subfolder='raw'):
    """
    Load a dataset from the data directory.
    
    Parameters
    ----------
    filename : str
        Name of the file to load
    subfolder : str, optional
        Subdirectory within the data directory, by default 'raw'
    
    Returns
    -------
    pandas.DataFrame
        Loaded dataset
    
    Example
    -------
    >>> df = load_dataset('example.csv')
    >>> print(df.head())
    """
    # Construct the full path to the file
    file_path = os.path.join(get_data_path(subfolder), filename)
    
    # Determine the file type and load accordingly
    if filename.endswith('.csv'):
        return pd.read_csv(file_path)
    elif filename.endswith('.parquet'):
        return pd.read_parquet(file_path)
    elif filename.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file_path)
    elif filename.endswith('.json'):
        return pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file format: {filename}")


def save_dataset(df, filename, subfolder='processed'):
    """
    Save a dataset to the data directory.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to save
    filename : str
        Name of the file to save
    subfolder : str, optional
        Subdirectory within the data directory, by default 'processed'
        
    Example
    -------
    >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    >>> save_dataset(df, 'example_processed.csv')
    """
    # Construct the full path to the file
    file_path = os.path.join(get_data_path(subfolder), filename)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Determine the file type and save accordingly
    if filename.endswith('.csv'):
        df.to_csv(file_path, index=False)
    elif filename.endswith('.parquet'):
        df.to_parquet(file_path, index=False)
    elif filename.endswith(('.xls', '.xlsx')):
        df.to_excel(file_path, index=False)
    elif filename.endswith('.json'):
        df.to_json(file_path, orient='records')
    else:
        raise ValueError(f"Unsupported file format: {filename}")

