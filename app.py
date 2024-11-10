from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from PIL import Image
import io
import logging
from infer import infer
from analyse import analyse_fossil
import base64
import uuid
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')

# Configuration for uploads
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# In-memory storage for markers
markers = []

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/map')
def map_page():
    return send_from_directory('static', 'map.html')

@app.route('/gallery') 
def gallery():
    # Path to the 'uploads' folder
    uploads_folder = os.path.join(app.root_path, 'static', 'uploads')
    
    # Get a list of all image files in the folder
    image_files = [f for f in os.listdir(uploads_folder) if f.endswith('.jpg')]
    
    # Pass the list of image files to the template
    return render_template('gallery.html', images=image_files)


@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400
    
    image_file = request.files['image']
    
    try:
        image_data = image_file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Get initial prediction and confidence
        prediction, confidence = infer(image)
        
        result = {
            'name': prediction,
            'confidence': confidence
        }
        
        if prediction not in ["not enough confidence", "Non-Fossils", "Error"]:
            analysis = analyse_fossil(prediction)
            if analysis != "error":
                result.update(analysis)
        
        # Save the image for later use with markers
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        result['image_path'] = f'/static/uploads/{filename}'
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return jsonify({
            'name': 'Error',
            'confidence': 0
        }), 500

@app.route('/add_marker', methods=['POST'])
def add_marker():
    try:
        if 'image' not in request.files:
            return jsonify({'status': 'error', 'message': 'No image file'}), 400

        image_file = request.files['image']
        username = request.form.get('username')
        lat = float(request.form.get('lat'))
        lng = float(request.form.get('lng'))

        # Generate unique filename and save image
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(filepath)
        
        # Create marker data
        marker_data = {
            'username': username,
            'lat': lat,
            'lng': lng,
            'image_url': f'/static/uploads/{filename}',
            'timestamp': datetime.now().isoformat()
        }
        
        markers.append(marker_data)
        logger.info(f"Added new marker: {marker_data}")
        
        return jsonify({
            'status': 'success',
            'image_url': marker_data['image_url']
        })
    
    except Exception as e:
        logger.error(f"Error adding marker: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_markers')
def get_markers():
    return jsonify(markers)

if __name__ == '__main__':
    app.run(debug=False)