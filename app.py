from flask import Flask, request, jsonify
import os
from PIL import Image
import io
import logging
from infer import infer
from analyse import analyse_fossil

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Serve the static HTML file
@app.route('/')
def index():
    logger.info("Serving index page")
    return app.send_static_file('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    logger.info("Received image analysis request")
    
    if 'image' not in request.files:
        logger.error("No image file in request")
        return jsonify({'error': 'No image file'}), 400
    
    image_file = request.files['image']
    
    try:
        # Read and process the image
        image_data = image_file.read()
        image = Image.open(io.BytesIO(image_data))
        
        logger.info(f"Received image: size={image.size}, mode={image.mode}")
        
        # Get initial prediction and confidence
        prediction, confidence = infer(image)
        logger.info(f"Prediction: {prediction}, Confidence: {confidence}")
        
        # Initialize basic result structure
        result = {
            'name': prediction,
            'confidence': confidence
        }
        
        # Only proceed with detailed analysis if it's a valid fossil prediction
        if prediction not in ["not enough confidence", "Non-Fossils", "Error"]:
            analysis = analyse_fossil(prediction)
            print("anlysis app",analysis)
            
            if analysis != "error":
                # Add detailed analysis to result
                result.update({
                    'Age': analysis['Age'],
                    'Confidence': confidence,
                    'Location': analysis['Location'],
                    'Fact_1': analysis['Fact_1'],
                    'Fact_2': analysis['Fact_2'],
                    'Fact_3': analysis['Fact_3']
                })
            else:
                logger.error("Error in fossil analysis")
                result = {
                    'name': 'Error',
                    'confidence': confidence
                }
        
        logger.info("Analysis completed successfully")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return jsonify({
            'name': 'Error',
            'confidence': 0
        }), 500

if __name__ == '__main__':
    logger.info("Starting Flask server")
    app.run(debug=True)