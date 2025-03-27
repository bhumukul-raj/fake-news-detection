# -*- coding: utf-8 -*-
"""
Model training functionality.

This module contains functions for training and saving models.
"""
import os
import pickle
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def get_models_path():
    """
    Get the path to the models directory.
    
    Returns
    -------
    str
        Path to the models directory
    """
    # Get the absolute path of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate to the models directory (2 levels up from src/models)
    models_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'models')
    
    # Ensure the directory exists
    os.makedirs(models_dir, exist_ok=True)
    
    return models_dir


def save_model(model, model_name, method='pickle'):
    """
    Save a trained model to the models directory.
    
    Parameters
    ----------
    model : object
        Trained model object
    model_name : str
        Name to use for the saved model file
    method : str, optional
        Method to use for saving the model, by default 'pickle'
        Valid options: 'pickle', 'joblib'
        
    Returns
    -------
    str
        Path to the saved model
        
    Example
    -------
    >>> from sklearn.ensemble import RandomForestClassifier
    >>> from sklearn.datasets import make_classification
    >>> X, y = make_classification(n_samples=1000, n_features=20, n_classes=2)
    >>> model = RandomForestClassifier().fit(X, y)
    >>> save_model(model, 'random_forest_classifier')
    """
    # Get the path to the models directory
    models_dir = get_models_path()
    
    # Construct the full path for the model
    if not model_name.endswith(('.pkl', '.joblib')):
        if method == 'pickle':
            model_name += '.pkl'
        elif method == 'joblib':
            model_name += '.joblib'
    
    model_path = os.path.join(models_dir, model_name)
    
    # Save the model using the specified method
    if method == 'pickle':
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
    elif method == 'joblib':
        joblib.dump(model, model_path)
    else:
        raise ValueError(f"Unsupported method: {method}. Use 'pickle' or 'joblib'.")
    
    print(f"Model saved to {model_path}")
    return model_path


def load_model(model_name, method=None):
    """
    Load a model from the models directory.
    
    Parameters
    ----------
    model_name : str
        Name of the model file to load
    method : str, optional
        Method to use for loading the model, by default None (auto-detect)
        Valid options: None, 'pickle', 'joblib'
        
    Returns
    -------
    object
        Loaded model object
        
    Example
    -------
    >>> model = load_model('random_forest_classifier.pkl')
    >>> predictions = model.predict(X_test)
    """
    # Get the path to the models directory
    models_dir = get_models_path()
    
    # Ensure the model name has the correct extension
    if not (model_name.endswith('.pkl') or model_name.endswith('.joblib')):
        if method == 'pickle':
            model_name += '.pkl'
        elif method == 'joblib':
            model_name += '.joblib'
        else:
            # Try to find the model with either extension
            if os.path.exists(os.path.join(models_dir, model_name + '.pkl')):
                model_name += '.pkl'
                method = 'pickle'
            elif os.path.exists(os.path.join(models_dir, model_name + '.joblib')):
                model_name += '.joblib'
                method = 'joblib'
            else:
                raise FileNotFoundError(f"Model not found: {model_name}")
    
    model_path = os.path.join(models_dir, model_name)
    
    # Auto-detect the method if not specified
    if method is None:
        if model_name.endswith('.pkl'):
            method = 'pickle'
        elif model_name.endswith('.joblib'):
            method = 'joblib'
        else:
            raise ValueError("Could not determine the loading method from the filename.")
    
    # Load the model using the specified method
    if method == 'pickle':
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
    elif method == 'joblib':
        model = joblib.load(model_path)
    else:
        raise ValueError(f"Unsupported method: {method}. Use 'pickle' or 'joblib'.")
    
    print(f"Model loaded from {model_path}")
    return model


def evaluate_model(model, X_test, y_test, average='weighted'):
    """
    Evaluate a model on test data.
    
    Parameters
    ----------
    model : object
        Trained model object with a predict method
    X_test : array-like
        Test features
    y_test : array-like
        True test labels
    average : str, optional
        Averaging method for precision, recall, and f1 score, by default 'weighted'
        
    Returns
    -------
    dict
        Dictionary of evaluation metrics
        
    Example
    -------
    >>> from sklearn.ensemble import RandomForestClassifier
    >>> from sklearn.datasets import make_classification
    >>> from sklearn.model_selection import train_test_split
    >>> X, y = make_classification(n_samples=1000, n_features=20, n_classes=2)
    >>> X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    >>> model = RandomForestClassifier().fit(X_train, y_train)
    >>> metrics = evaluate_model(model, X_test, y_test)
    >>> print(metrics)
    """
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average=average, zero_division=0),
        'recall': recall_score(y_test, y_pred, average=average, zero_division=0),
        'f1': f1_score(y_test, y_pred, average=average, zero_division=0)
    }
    
    # Print metrics
    print("Model Evaluation Metrics:")
    for metric, value in metrics.items():
        print(f"{metric.capitalize()}: {value:.4f}")
    
    return metrics

