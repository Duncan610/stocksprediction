from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import lightgbm as lgb
import xgboost as xgb
from statsmodels.tsa.arima.model import ARIMA
import pickle

class ModelTrainer:
    def __init__(self, model_type):
        self.model_type = model_type

    def train(self, X_train, y_train, X_test, y_test, model_path=None):
        if self.model_type == "lightgbm":
            model = lgb.LGBMRegressor()
            param_grid = {
                'num_leaves': [31, 50],
                'learning_rate': [0.01, 0.1],
                'n_estimators': [100, 200]
            }
            grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error')
            grid_search.fit(X_train, y_train)
            best_model = grid_search.best_estimator_
        
        elif self.model_type == "random_forest":
            model = RandomForestRegressor()
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5]
            }
            grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error')
            grid_search.fit(X_train, y_train)
            best_model = grid_search.best_estimator_
        
        elif self.model_type == "xgboost":
            model = xgb.XGBRegressor()
            param_grid = {
                'n_estimators': [100, 200],
                'learning_rate': [0.01, 0.1],
                'max_depth': [3, 6]
            }
            grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error')
            grid_search.fit(X_train, y_train)
            best_model = grid_search.best_estimator_
        
        elif self.model_type == "arima":
            
            model = ARIMA(y_train, order=(5, 1, 0))
            fitted_model = model.fit()
            train_pred = fitted_model.fittedvalues
            test_pred = fitted_model.forecast(steps=len(y_test))
            train_mse = mean_squared_error(y_train, train_pred)
            test_mse = mean_squared_error(y_test, test_pred)
            train_r2 = r2_score(y_train, train_pred)
            test_r2 = r2_score(y_test, test_pred)
            metrics = {
                "train_mse": train_mse,
                "test_mse": test_mse,
                "train_r2": train_r2,
                "test_r2": test_r2
            }
            if model_path:
                with open(model_path, 'wb') as f:
                    pickle.dump(fitted_model, f)
            return fitted_model, metrics
        
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

        # Common evaluation for tree-based models
        train_pred = best_model.predict(X_train)
        test_pred = best_model.predict(X_test)
        train_mse = mean_squared_error(y_train, train_pred)
        test_mse = mean_squared_error(y_test, test_pred)
        train_r2 = r2_score(y_train, train_pred)
        test_r2 = r2_score(y_test, test_pred)
        
        metrics = {
            "train_mse": train_mse,
            "test_mse": test_mse,
            "train_r2": train_r2,
            "test_r2": test_r2
        }
        
        if model_path:
            with open(model_path, 'wb') as f:
                pickle.dump(best_model, f)
        
        return best_model, metrics