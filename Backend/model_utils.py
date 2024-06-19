import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

contractions_dict = {
    r"don": "do not",
    r"doesn": "does not",
    r"didn": "did not",
    r"haven": "have not",
    r"hasn": "has not",
    r"hadn": "had not",
    r"won": "will not",
    r"wouldn": "would not",
    r"couldn": "could not",
    r"shouldn": "should not",
    r"mightn": "might not",
    r"mustn": "must not",
    r"weren": "were not",
    r"wasn": "was not",
    r"ain": "is not",
    r"won": "would not"
}
def expand_contractions(text):
    for contraction, expanded_form in contractions_dict.items():
        text = re.sub(contraction, expanded_form, text, flags=re.IGNORECASE)
    return text

def preprocess_text(sen):

    sentence = sen.lower()

    sentence = re.sub('[^a-zA-Z]', ' ', sentence)

    # Single character removal
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)  # When we remove apostrophe from the word "Mark's", the apostrophe is replaced by an empty space. Hence, we are left with single character "s" that we are removing here.

    # Remove multiple spaces
    sentence = re.sub(r'\s+', ' ', sentence)  # Next, we remove all the single characters and replace it by a space which creates multiple spaces in our text. Finally, we remove the multiple spaces from our text as well.

    #expanded forms
    sentence = expand_contractions(sentence)

    with open('stopwords.txt', 'r') as file:
      stopwords = {line.strip() for line in file}

    # Remove Stopwords
    pattern = re.compile(r'\b(' + r'|'.join(stopwords) + r')\b\s*')
    sentence = pattern.sub('', sentence)

    return sentence


def analyze_review(review, model):
  # Perform sentiment analysis
  # Preprocess the review text
  preprocessed_text = preprocess_text(review)

  word_tokenizer = Tokenizer()

  # Convert the preprocessed text to a sequence of integers
  sequence = word_tokenizer.texts_to_sequences([preprocessed_text])
  # Pad the sequence to a fixed length
  padded_sequence = pad_sequences(sequence, maxlen=100, padding='post')

  # Predict the sentiment using the model
  prediction = model.predict(padded_sequence)[0][0]

  # Determine the sentiment based on the prediction threshold
  sentiment = "positive" if prediction > 0.5 else "negative"  # Assuming model.predict returns the sentiment label

  # Dummy department classification based on keywords
  departments_keywords = {
    "Customer Service": [
      "service", "support", "customer service", "help", "response", "rude", "behavior", "polite", "agent", "call", "email",
      "assistance", "aid", "care", "courtesy", "treatment", "interaction", "representative", "communication", "reply", "feedback"
    ],
    "Product Quality": [
      "product", "quality", "defective", "broken", "durable", "material", "build", "manufacture", "craftsmanship", "faulty", "not working", "difficult",
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
      "transactions", "acquisition", "procure", "command", "rate", "reduction", "proposal", "bargain", "expense", "payment", "value"
    ]
  }

  # Function to assign departments based on keywords
  def assign_departments(review):
    assigned_departments = []
    for department, keywords in departments_keywords.items():
      if any(keyword in review.lower() for keyword in keywords):
        assigned_departments.append(department)
    return ', '.join(assigned_departments) if assigned_departments else "General"

  # Call the department assignment function
  departments = assign_departments(review)

  return sentiment, departments
