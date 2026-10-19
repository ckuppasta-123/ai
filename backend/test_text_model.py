from app.text_classifier import text_classifier


print("Loading DistilBERT sentiment model...")

text_classifier.load()

print("\nModel information:")
print(text_classifier.get_info())

print("\nDistilBERT loaded successfully!")

test_sentences = [
    "This application is excellent and very easy to use.",
    "The deployment failed and the application is not working.",
    "The project is okay, but it needs some improvements.",
]

print("\nRunning test predictions...")

for sentence in test_sentences:
    result = text_classifier.predict(sentence)

    print("\nText:", sentence)
    print("Result:", result)