import pandas as pd
import os
import io
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords', quiet=True)

def get_dataset():

    local_files = [
        
    ]
    
    for file in local_files:
        if os.path.exists(file):
            try:
                df = pd.read_csv(file, encoding='latin-1')
                if len(df.columns) >= 2:
                    df = df.iloc[:, :2] 
                    df.columns = ['label', 'message']
                    return df
            except Exception as e:
                print(f"Error reading {file}: {e}")
                continue
    
    print("Attempting to download dataset...")
    try:
        url = "https://raw.githubusercontent.com/justmarkham/pydata-dc-2016-tutorial/master/sms.tsv"
        response = requests.get(url)
        response.raise_for_status()
        
        df = pd.read_csv(io.StringIO(response.text), sep='\t', header=None, names=['label', 'message'])
        return df
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        return None

def preprocess_text(text):
    if pd.isna(text):
        return ""
    
    stemmer = PorterStemmer()
    
    text = text.lower()
    
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    
    return ' '.join(words)

def main():
    print("SMS Spam Detection Model")
    print()
    df = get_dataset()
    
    if df is None:
        print("ERROR: Could not load the dataset.")
        print("Please try one of these solutions:")
        print("1. Download the dataset manually from:")
        print("   https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection")
        print("   and place it in this directory as 'spam.csv'")
        print(f"2. Current working directory: {os.getcwd()}")
        print("3. Check your internet connection if you want automatic download")
        return
    
    df['label'] = df['label'].map({'ham': 0, 'spam': 1, 'Ham': 0, 'Spam': 1})
    X = df['message']
    y = df['label']
    
    print("Dataset loaded successfully!")
    print(f"Total messages: {len(X)}")
    print(f"Spam messages: {sum(y)} ({sum(y)/len(y):.1%})")
    print(f"Ham messages: {len(y)-sum(y)} ({(len(y)-sum(y))/len(y):.1%})")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print("\nTraining model...")
    model = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            preprocessor=preprocess_text
        )),
        ('classifier', MultinomialNB())
    ])
    
    model.fit(X_train, y_train)
    
    print("\nEvaluating model...")
    y_pred = model.predict(X_test)
    
    print("\nModel Evaluation")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    test_messages = [
        "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005.",
        "Hi there, just checking if we're still meeting tomorrow?",
        "Congratulations! You've won a $10000 Walmart gift card! Click here to claim.",
        "Ok, see you later then."
    ]
    
    print("Example Predictions")
    for msg in test_messages:
        pred = model.predict([msg])[0]
        proba = model.predict_proba([msg])[0]
        print(f"Message: {msg}")
        print(f"Prediction: {'SPAM' if pred == 1 else 'HAM'}")
        print(f"Confidence: {max(proba):.1%}")

if __name__ == "__main__":
    main()
