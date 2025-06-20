import pandas as pd
import os
import requests
from io import StringIO
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

def download_sample_data():
    urls = [
        "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv",
        "https://raw.githubusercontent.com/sahilpatni95/Telecom-Churn-Prediction/main/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    ]
    
    for url in urls:
        try:
            print(f"Attempting download from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = pd.read_csv(StringIO(response.text))
            if not data.empty:
                print("Download successful!")
                return data
        except Exception as e:
            print(f"Download attempt failed: {e}")
    
    print("\nAll download attempts failed. Please:")
    print("1. Check your internet connection")
    print("2. Download manually from:")
    print("https://www.kaggle.com/datasets/blastchar/telco-customer-churn")
    print("3. Place the CSV file in this folder:", os.getcwd())
    return None

def locate_data_file():
    filenames = [
        'Telco-Customer-Churn.csv',
        'customer_churn.csv',
        'churn_data.csv',
        'WA_Fn-UseC_-Telco-Customer-Churn.csv',
        'Telco-Customer-Churn-1.csv'
    ]
    
    directories = [
        os.getcwd(),
        os.path.join(os.getcwd(), 'data'),
        os.path.expanduser('~'),
        os.path.join(os.path.expanduser('~'), 'Downloads'),
        os.path.join(os.path.expanduser('~'), 'Documents'),
        r'C:\Users\Public\Downloads',
        r'C:\Users\KIIT\CodSoft'
    ]
    
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        
        # Basic validation
        if data.empty:
            raise ValueError("File is empty")
        if len(data) < 10:
            raise ValueError("Insufficient data (less than 10 rows)")
        
        print("Data loaded successfully!")
        print(f"Shape: {data.shape}")
        print("First 2 rows:")
        print(data.head(2))
        return data
    
    except Exception as e:
        print(f"Error loading file: {e}")
        print("Please ensure:")
        print("1. File is a valid CSV")
        print("2. File contains sufficient data")
        print("3. You have read permissions")
        return None

def run_analysis(data):
    try:
        churn_col = next((col for col in data.columns if 'churn' in col.lower()), None)
        if not churn_col:
            available = "\n- ".join(data.columns)
            raise ValueError(f"No 'Churn' column found. Available columns:\n- {available}")
        
        # Convert target
        y = data[churn_col].astype(str).str.lower().map({'yes':1, 'no':0, '1':1, '0':0})
        if y.isna().any():
            invalid = data[churn_col][y.isna()].unique()
            raise ValueError(f"Invalid Churn values: {invalid}. Expected: Yes/No/1/0")
        
        # Prepare features
        X = data.drop([churn_col], axis=1)
        if 'customerid' in X.columns.str.lower():
            X = X.drop('customerid', axis=1)
        
        # Auto preprocessing
        numeric_cols = X.select_dtypes(include=['number']).columns
        categorical_cols = X.select_dtypes(include=['object', 'category']).columns
        
        preprocessor = ColumnTransformer([
            ('num', Pipeline([
                ('imputer', SimpleImputer(strategy='median')), 
                ('scaler', StandardScaler())
            ]), numeric_cols),
            ('cat', Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
            ]), categorical_cols)
        ])
        
        # Model pipeline
        model = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                class_weight='balanced',
                verbose=1
            ))
        ])
        
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Training
        print("\nTraining model...")
        model.fit(X_train, y_train)
        
        # Evaluation
        y_pred = model.predict(X_test)
        print("\nModel Performance:")
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
    except Exception as e:
        print(f"\nAnalysis failed: {e}")
        print("\nDebug Info:")
        print(f"- Columns: {list(data.columns)}")
        print(f"- Shape: {data.shape}")
        print(f"- Churn values: {data[churn_col].unique() if 'churn_col' in locals() else 'N/A'}")

def main():
    print("Customer Churn Analysis:")
    
    
    data_path = locate_data_file()
    if data_path:
        data = load_data(data_path)
        if data is not None:
            run_analysis(data)
            return 0
    
    print("Attempting to use sample data...")
    data = download_sample_data()
    if data is not None:
        run_analysis(data)
    else:
        print("Analysis cannot proceed without data.")
        print("Please place a valid CSV file in this folder:")
        print(os.getcwd())

if __name__ == "__main__":
    main()
    print("\nScript execution completed.")
