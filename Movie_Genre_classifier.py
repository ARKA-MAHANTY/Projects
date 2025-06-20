import os
import re
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

class MovieGenreClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2),
            stop_words='english'
        )
        self.label_binarizer = MultiLabelBinarizer()
        self.model = None
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.genre_mapping = {
            'sci-fi': 'scifi',
            'science fiction': 'scifi',
            'sci fi': 'scifi',
            'sf': 'scifi',
            'rom-com': 'romance',
            'romantic comedy': 'romance'
        }

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        words = text.split()
        words = [self.lemmatizer.lemmatize(word) for word in words 
                if word not in self.stop_words and len(word) > 2]
        return ' '.join(words)

    def normalize_genres(self, genres):
        if not isinstance(genres, list):
            return []
            
        cleaned = []
        for genre in genres:
            genre = genre.lower().strip()
            genre = self.genre_mapping.get(genre, genre)
            if genre and genre not in cleaned:
                cleaned.append(genre)
        return cleaned

    def load_data(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Data file not found at: {os.path.abspath(filepath)}")
        
        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = re.split(r':{2,3}', line.strip())
                if len(parts) >= 4:
                    genres = self.normalize_genres(parts[2].split('|'))
                    if genres:  
                        data.append({
                            'id': parts[0],
                            'title': parts[1],
                            'genres': genres,
                            'description': self.clean_text(parts[3])
                        })
        return data

    def train(self, data):
        if not data:
            raise ValueError("No training data available")
            
        descriptions = [item['description'] for item in data]
        genres = [item['genres'] for item in data]
        
        self.label_binarizer.fit(genres)
        print(f"Found genres: {', '.join(self.label_binarizer.classes_)}")
        
        X = self.vectorizer.fit_transform(descriptions)
        y = self.label_binarizer.transform(genres)
        
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model = OneVsRestClassifier(LogisticRegression(
            max_iter=1000,
            solver='saga',
            random_state=42
        ))
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_val)
        print("\nValidation Report:")
        print(classification_report(
            y_val, y_pred,
            target_names=self.label_binarizer.classes_,
            zero_division=0
        ))

    def predict(self, description):
        if not self.model:
            raise RuntimeError("Model not trained yet")
        
        cleaned = self.clean_text(description)
        X = self.vectorizer.transform([cleaned])
        y_pred = self.model.predict(X)
        return self.label_binarizer.inverse_transform(y_pred)[0]

def create_sample_data(filepath):
    sample_data = [
        "1::Inception::Sci-Fi|Action::A thief steals secrets through dream-sharing technology",
        "2::The Shawshank Redemption::Drama::Two imprisoned men bond over several years",
        "3::The Dark Knight::Action|Crime|Drama::Batman faces the Joker in Gotham City",
        "4::Pulp Fiction::Crime|Drama::Interconnected stories of criminals in Los Angeles",
        "5::Forrest Gump::Drama|Romance::A simple man witnesses key events in 20th century America"
    ]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sample_data))

def main():
    print("Movie Genre Classifier")
        
    os.makedirs('data', exist_ok=True)
    data_file = 'data/train_data.txt'
    
    if not os.path.exists(data_file):
        print("\nCreating sample data file...")
        create_sample_data(data_file)
        print(f"Sample data created at: {os.path.abspath(data_file)}")
        print("You can replace this with your own data")
    
    try:
        classifier = MovieGenreClassifier()
        
        # Load data
        print("\nLoading training data...")
        data = classifier.load_data(data_file)
        print(f"Loaded {len(data)} movie records")
        
        if not data:
            raise ValueError("No valid movie records found in the data file")
        
        # Train model
        print("\nTraining model...")
        classifier.train(data)
        print("Training completed!")
        
        # Test predictions
        test_cases = [
            "A space adventure with aliens and robots exploring distant galaxies",
            "A heartwarming story about childhood friends falling in love",
            "A detective investigates a series of mysterious murders in London"
        ]
        
        print("\nTest Predictions:")
        for desc in test_cases:
            genres = classifier.predict(desc)
            print(f"\nDescription: {desc[:80]}...")
            print(f"Predicted genres: {', '.join(genres)}")
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting:")
        print(f"1. Ensure {data_file} exists")
        print("2. Verify format: ID::Title::Genre1|Genre2::Description")
        print("3. Check file contains at least one valid record with genres")

if __name__ == "__main__":
    main()
