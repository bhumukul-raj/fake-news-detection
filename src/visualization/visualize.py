# -*- coding: utf-8 -*-
"""
Visualization utilities.

This module contains functions for creating visualizations.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os


def save_figure(fig, filename, dpi=300):
    """
    Save a matplotlib figure to the reports/figures directory.
    
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure to save
    filename : str
        Name of the file to save
    dpi : int, optional
        Resolution of the figure, by default 300
    """
    # Get the absolute path of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate to the reports/figures directory (2 levels up from src/visualization)
    figures_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'reports', 'figures')
    
    # Ensure the directory exists
    os.makedirs(figures_dir, exist_ok=True)
    
    # Save the figure
    fig.savefig(os.path.join(figures_dir, filename), dpi=dpi, bbox_inches='tight')
    print(f"Figure saved to {os.path.join(figures_dir, filename)}")


def plot_distribution(data, column, title=None, bins=30, figsize=(10, 6)):
    """
    Plot the distribution of a column in a dataframe.
    
    Parameters
    ----------
    data : pandas.DataFrame
        Dataframe containing the column to plot
    column : str
        Name of the column to plot
    title : str, optional
        Title of the plot, by default None
    bins : int, optional
        Number of bins for the histogram, by default 30
    figsize : tuple, optional
        Size of the figure, by default (10, 6)
        
    Returns
    -------
    matplotlib.figure.Figure
        The created figure
        
    Example
    -------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'values': np.random.normal(0, 1, 1000)})
    >>> fig = plot_distribution(df, 'values', title='Normal Distribution')
    >>> save_figure(fig, 'normal_distribution.png')
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot the histogram
    sns.histplot(data[column], bins=bins, kde=True, ax=ax)
    
    # Set the title and labels
    if title:
        ax.set_title(title)
    ax.set_xlabel(column)
    ax.set_ylabel('Frequency')
    
    plt.tight_layout()
    return fig


def plot_correlation_matrix(data, method='pearson', figsize=(12, 10), title=None):
    """
    Plot a correlation matrix for the numeric columns in a dataframe.
    
    Parameters
    ----------
    data : pandas.DataFrame
        Dataframe containing the columns to correlate
    method : str, optional
        Method of correlation, by default 'pearson'
    figsize : tuple, optional
        Size of the figure, by default (12, 10)
    title : str, optional
        Title of the plot, by default None
        
    Returns
    -------
    matplotlib.figure.Figure
        The created figure
        
    Example
    -------
    >>> import pandas as pd
    >>> import numpy as np
    >>> df = pd.DataFrame({
    ...     'A': np.random.normal(0, 1, 100),
    ...     'B': np.random.normal(0, 1, 100),
    ...     'C': np.random.normal(0, 1, 100)
    ... })
    >>> fig = plot_correlation_matrix(df, title='Correlation Matrix')
    >>> save_figure(fig, 'correlation_matrix.png')
    """
    # Calculate the correlation matrix
    corr = data.select_dtypes(include=[np.number]).corr(method=method)
    
    # Create the figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    
    # Draw the heatmap
    sns.heatmap(
        corr, 
        mask=mask, 
        cmap=cmap, 
        vmax=1, 
        vmin=-1, 
        center=0,
        square=True, 
        linewidths=.5, 
        cbar_kws={"shrink": .5},
        annot=True,
        fmt='.2f',
        ax=ax
    )
    
    # Set the title
    if title:
        ax.set_title(title)
    
    plt.tight_layout()
    return fig

