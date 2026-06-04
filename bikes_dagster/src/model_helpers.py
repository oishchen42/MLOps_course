from sklearn.inspection import permutation_importance
import pandas as pd

def analyze_feature_importance(model, X_test: pd.DataFrame, y_test: pd.Series) -> pd.DataFrame:
    """Calculates feature importance without printing to the console."""
    
    result = permutation_importance(
        model, 
        X_test, 
        y_test, 
        scoring='neg_root_mean_squared_error', 
        n_repeats=10, 
        random_state=42
    )
    
    importance_df = pd.DataFrame({
        'Feature': X_test.columns,
        'Importance_Score': result.importances_mean
    })
    
    importance_df = importance_df.sort_values(by='Importance_Score', ascending=False)
    importance_df = importance_df.reset_index(drop=True)
    
    return importance_df