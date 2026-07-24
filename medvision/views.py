from django.shortcuts import render
from .forms import ImageUploadForm
from tensorflow.keras.utils import load_img, img_to_array
from .ml_model import model
import numpy as np


def predict(request):
    prediction = None
    confidence = None

    classes = ["Normal", "Pneumonia"]

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                # Uploaded image
                image = request.FILES["image"]

                # Load image
                img = load_img(image.file, target_size=(124, 124))
                img_array = img_to_array(img)

                # Add batch dimension
                img_array = np.expand_dims(img_array, axis=0)

                # Prediction
                preds = model.predict(img_array, verbose=0)

                print("Prediction Probabilities:", preds)

                predicted_index = np.argmax(preds[0])

                prediction = classes[predicted_index]
                confidence = float(preds[0][predicted_index] * 100)

            except Exception as e:
                prediction = f"Error: {str(e)}"
                confidence = None

    else:
        form = ImageUploadForm()

    return render(request, "home.html", {
        "form": form,
        "prediction": prediction,
        "confidence": round(confidence, 2) if confidence is not None else None,
    })