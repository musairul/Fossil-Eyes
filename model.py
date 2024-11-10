import os
import pickle

from img2vec_pytorch import Img2Vec
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

img2vec = Img2Vec()

data_dir = './Fossils'
train_dir = os.path.join(data_dir, 'train') 
val_dir = os.path.join(data_dir, 'val')

data = {}

for j, dir_ in enumerate([train_dir, val_dir]):
    features = []
    labels = []
    for classes in os.listdir(dir_):
        for pic_path in os.listdir(os.path.join(dir_, classes)):
            pic_pathname = os.path.join(dir_, classes, pic_path)
            fossilpic = Image.open(pic_pathname)
            
            print(f"{pic_pathname}")
            fossilcharac = img2vec.get_vec(fossilpic)
            features.append(fossilcharac)
            labels.append(classes)

    data[['training_data', 'validation_data'][j]] = features
    data[['training_labels', 'validation_labels'][j]] = labels


model = RandomForestClassifier()
model.fit(data['training_data'], data['training_labels'])


y_pred = model.predict(data['validation_data'])
score = accuracy_score(y_pred, data['validation_labels'])
print(score)    

with open('./model.p', 'wb') as f:
    pickle.dump(model, f)
    f.close()