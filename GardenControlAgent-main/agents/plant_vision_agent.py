Generated python
      import base64
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

# --- Configuration (Move to a config file or environment variables ideally) ---
PROJECT_ID = "29067641139"
REGION = "us-central1"  # e.g., "us-central1"
ENDPOINT_ID = "1529936345189842944" # Just the number part

def predict_plant_health(image_file_path):
    """
    Sends an image to the Vertex AI endpoint for classification.
    Args:
        image_file_path (str): The local path to the image file.
    Returns:
        dict: The prediction results (e.g., {"status": "healthy", "confidence": 0.95})
              or None if prediction fails.
    """
    aiplatform.init(project=PROJECT_ID, location=REGION)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"
    )

    try:
        with open(image_file_path, "rb") as f:
            image_bytes = f.read()
        encoded_content = base64.b64encode(image_bytes).decode("utf-8")

        # The format of the instances will depend on the model's input expectations.
        # For AutoML Image Classification, it's typically:
        instances = [
            {
                "content": encoded_content
            }
        ]
        # If your model expects a different format, you might need to adjust.

        prediction = endpoint.predict(instances=instances)
        # print("Raw prediction:", prediction) # For debugging

        # Process the prediction response
        # The response structure can vary slightly. Inspect 'prediction.predictions[0]'
        # It usually contains 'displayNames' and 'confidences'
        if prediction.predictions:
            # Assuming single-label classification, take the top prediction
            top_prediction = prediction.predictions[0]
            # Check actual keys in your response, might be 'displayNames' or similar
            predicted_class = top_prediction.get('displayNames', [None])[0] 
            confidence = top_prediction.get('confidences', [0.0])[0]

            if predicted_class and confidence > 0: # Basic check
                return {
                    "status": predicted_class,
                    "confidence": float(confidence)
                }
        return None

    except Exception as e:
        print(f"Error during Vertex AI prediction: {e}")
        return None

# --- Example Usage (within your PlantVisionAgent) ---
if __name__ == "__main__":
    # This is a sample image path, replace with how your agent gets images
    # For the hackathon, you'll likely have a list of test images.
    test_image = "path/to/your/test_image.jpg" # e.g., from your plant_health_dataset/healthy/
    
    # Ensure the test_image path is correct and accessible
    import os
    if not os.path.exists(test_image):
        print(f"Test image not found at: {test_image}")
    else:
        result = predict_plant_health(test_image)
        if result:
            print(f"Plant Health Assessment:")
            print(f"  Status: {result['status']}")
            print(f"  Confidence: {result['confidence']:.2f}")
            # Here your agent would publish this result to ADK
            # e.g., publish_to_adk({ "timestamp": "...", "plant_id": "Plant X", "image_ref": test_image, **result })
        else:
            print("Failed to get prediction.")
