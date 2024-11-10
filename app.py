from flask import Flask, request, jsonify
import os
from PIL import Image
import io
import logging

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
        
        # Log image details
        logger.info(f"Received image: size={image.size}, mode={image.mode}")
        
        # Here you would typically do your fossil analysis
        # This is a placeholder response
        result = {
            'status': 'success',
            'image_dimensions': {
                'width': image.size[0],
                'height': image.size[1]
            },
            'preliminary_analysis': {
                'possible_type': 'Unknown Fossil',
                'confidence': 'Further analysis needed',
                'suggestions': [
                    'Ensure good lighting',
                    'Try multiple angles',
                    'Include scale reference'
                ]
            }
        }
        
        logger.info("Analysis completed successfully")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':

    
    # Start the server
    logger.info("Starting Flask server")
    app.run(debug=True)
