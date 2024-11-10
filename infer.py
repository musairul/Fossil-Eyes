import pickle

from img2vec_pytorch import Img2Vec
from PIL import Image

def infer(image_file):
    with open('./model.p', 'rb') as f:
        model = pickle.load(f)
    img2vec = Img2Vec()

    confidence_threshold = 0.4

    #img = Image.open("fossil.jpg")
    img = image_file

    features = img2vec.get_vec(img)
    
    probabilities = model.predict_proba([features])
    
    max_confidence = max(probabilities[0])
    predicted_class = model.classes_[probabilities[0].argmax()]
    
    
    if max_confidence < confidence_threshold:
        return ['not enough confidence',max_confidence]
    else:
        return [predicted_class,max_confidence]

    
