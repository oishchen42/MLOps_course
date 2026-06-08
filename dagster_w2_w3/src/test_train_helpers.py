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
    
    # 1. Optional: Apply Cyclical Time (For Linear Models)
    if apply_cyclical:
        # Assuming apply_cyclical_time is accessible here
        train_df = lh.apply_cyclical_time(train_df)
        test_df = lh.apply_cyclical_time(test_df)
        
    # 2. Separate Features (X) and Target (y)
    columns_to_drop = ['datetime', 'direct_count', 'registered_count', 'total_rentals']
    
    y_train = train_df['total_rentals']
    X_train = train_df.drop(columns=columns_to_drop)
    
    y_test = test_df['total_rentals']
    X_test = test_df.drop(columns=columns_to_drop)
    
    # 3. Optional: Scale Continuous Features (For Linear Models)
    scaler = None
    if features_to_scale is not None:
        scaler = StandardScaler()
        # Fit ONLY on train data, transform both
        X_train[features_to_scale] = scaler.fit_transform(X_train[features_to_scale])
        X_test[features_to_scale] = scaler.transform(X_test[features_to_scale])
        
    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "scaler": scaler
    }