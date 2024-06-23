import re
from tensorflow.keras.preprocessing.sequence import pad_sequences
from textblob import TextBlob
import pickle
from tensorflow.keras.models import load_model
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

contractions_dict = {
    r"don't": "do not",
    r"doesn't": "does not",
    r"didn't": "did not",
    r"haven't": "have not",
    r"hasn't": "has not",
    r"hadn't": "had not",
    r"won't": "will not",
    r"wouldn't": "would not",
    r"couldn't": "could not",
    r"shouldn't": "should not",
    r"mightn't": "might not",
    r"mustn't": "must not",
    r"weren't": "were not",
    r"wasn't": "was not",
    r"ain't": "is not",
    r"won't": "would not"
}

def expand_contractions(text):
    for contraction, expanded_form in contractions_dict.items():
        text = re.sub(contraction, expanded_form, text, flags=re.IGNORECASE)
    return text

def remove_tags(text):
    return re.sub(r'<[^>]+>', '', text)

def preprocess_text(text):
    text = remove_tags(text)
    text = expand_contractions(text)
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    tokens = [token for token in tokens if token.isalpha()]
    stop_words = set(stopwords.words('english'))
    stop_words.remove('not')
    tokens = [token for token in tokens if token not in stop_words]
    
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    text = ' '.join(tokens)
    return text

def correct_spelling(text):
    blob = TextBlob(text)
    corrected_text = str(blob.correct())
    return corrected_text

def analyze_review(review, model, tokenizer):
    corrected = correct_spelling(review.lower())
    review = preprocess_text(corrected)
    sequence = tokenizer.texts_to_sequences([review])
    padded_sequence = pad_sequences(sequence, maxlen=100, padding='post')
    prediction = model.predict(padded_sequence)
    sentiment = "positive" if prediction > 0.5 else "negative"
    stars = round(float(prediction * 5), 1)  

    departments_keywords = {
        "Customer Service": [
            "service", "support", "customer service", "help", "response", "rude", "behavior", "polite", "agent", "call", "email",
            "assistance", "aid", "care", "courtesy", "treatment", "interaction", "representative", "communication", "reply", "feedback"
        ],
        "Product Quality": [
            "product", "quality", "fabric","defective", "broken", "durable", "material", "build", "manufacture", "craftsmanship", "faulty", "not working", "difficult",
            "item", "standard", "wastage", "flawed", "damaged", "component", "construction", "production", "workmanship", "malfunctioning", "inoperative", "challenging"
        ],
        "Shipping": [
            "shipping", "delayed", "package", "sealed", "arrived", "late delivery", "courier", "tracking", "shipment", "dispatch", "fast", "slow",
            "delivery", "postponed", "parcel", "wrapped", "received", "carrier", "monitoring", "consignment", "send", "quick"
        ],
        "Technical Support": [
            "technical", "tech support", "IT", "software", "hardware", "bug", "issue", "glitch", "error", "malfunction", "install", "update",
            "technological", "technical assistance", "information technology", "program", "device", "fault", "problem", "flaw", "mistake", "breakdown", "setup", "upgrade"
        ],
        "Marketing": [
            "marketing", "advertising", "promotion", "campaign", "brand", "advertised", "strategy", "market", "target",
            "promotion", "publicity", "advertisement", "drive", "branding", "marketed"
        ],
        "Sales": [
            "sales", "purchase", "buy", "order", "pricing", "discount", "offer", "deal", "cost", "checkout", "price",
            "transactions", "acquisition", "procure", "command", "rate", "reduction", "proposal", "bargain", "expense","expensive" "payment", "value"
        ]
    }

    def assign_departments(review):
        assigned_departments = []
        for department, keywords in departments_keywords.items():
            if any(keyword in review.lower() for keyword in keywords):
                assigned_departments.append(department)
        return ', '.join(assigned_departments) if assigned_departments else "General"

    departments = assign_departments(review)

    return sentiment, departments,stars

def load_model_and_tokenizer(model_path, tokenizer_path):
    model = load_model(model_path)
    with open(tokenizer_path, 'rb') as handle:
        tokenizer = pickle.load(handle)
    return model, tokenizer
