import pandas as pd
from sklearn.preprocessing import StandardScaler
import linear_helpers as lh

def preprocess_train_test(
    chronological_data_split: dict, 
    apply_cyclical: bool = False, 
    features_to_scale: list = None
) -> dict:
    """
    Unpacks train/test data, splits X and y, and optionally applies scaling and cyclical time.
    """
    train_df = chronological_data_split["train"].copy()
    test_df = chronological_data_split["test"].copy()
    
    # If we're training a linear model, convert cyclical features (hour, month) into sine/cosine
    if apply_cyclical:
        train_df = lh.apply_cyclical_time(train_df)
        test_df = lh.apply_cyclical_time(test_df)
        
    # Split features and target. Remove identifiers and the target variable from features.
    columns_to_drop = ['datetime', 'direct_count', 'registered_count', 'total_rentals']
    
    y_train = train_df['total_rentals']
    X_train = train_df.drop(columns=columns_to_drop)
    
    y_test = test_df['total_rentals']
    X_test = test_df.drop(columns=columns_to_drop)
    
    # Normalize numerical features if requested (typically for linear models)
    scaler = None
    if features_to_scale is not None:
        scaler = StandardScaler()
        # Important: Learn scaling params from training data only, then apply to both
        X_train[features_to_scale] = scaler.fit_transform(X_train[features_to_scale])
        X_test[features_to_scale] = scaler.transform(X_test[features_to_scale])
        
    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "scaler": scaler
    }