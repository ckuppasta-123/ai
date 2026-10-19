from pathlib import Path

from app.image_classifier import image_classifier


print("Loading MobileNetV2...")
image_classifier.load()

print("\nModel information:")
print(image_classifier.get_info())

print("\nMobileNetV2 loaded successfully!")

test_image = Path("test.jpg")

if test_image.exists():
    print("\nRunning prediction on test.jpg...")

    result = image_classifier.predict(
        test_image.read_bytes(),
        top_k=3,
    )

    print("\nPrediction result:")
    print(result)
else:
    print("\nNo test.jpg found.")
    print("Model loading test completed successfully.")