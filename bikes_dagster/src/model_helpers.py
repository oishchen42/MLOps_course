from sklearn.inspection import permutation_importance
import pandas as pd

def analyze_feature_importance(model, X_test: pd.DataFrame, y_test: pd.Series) -> pd.DataFrame:
    """Compute permutation-based feature importances.

    Parameters
    ----------
    model : estimator
        Fitted estimator with a `predict` method.
    X_test : pandas.DataFrame
        Test features used to compute importances.
    y_test : array-like
        True target values for `X_test`.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns `Feature` and `Importance_Score`, sorted by importance descending.
    """

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