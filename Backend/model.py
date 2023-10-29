import cv2
import numpy as np
from tensorflow import keras
from keras.models import Sequential
from keras.layers import GlobalAveragePooling2D, Dense
from keras.applications.xception import Xception, preprocess_input
import keras.utils as image
from tqdm import tqdm
from glob import glob

dog_names = [item[20:-1] for item in sorted(glob("dogImages/train/*/"))]

network = "DogXceptionData.npz"
bottleneck_features = np.load(f'bottleneck_features/{network}')
train_features = bottleneck_features['train']
valid_features = bottleneck_features['valid']
test_features = bottleneck_features['test']


def create_model():
    model = Sequential()
    model.add(GlobalAveragePooling2D(input_shape=train_features.shape[1:]))
    model.add(Dense(133, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model


def path_to_tensor(img_path):
    # loads RGB image as PIL.Image.Image type
    img = image.load_img(img_path, target_size=(224, 224))
    # convert PIL.Image.Image type to 3D tensor with shape (224, 224, 3)
    x = image.img_to_array(img)
    # convert 3D tensor to 4D tensor with shape (1, 224, 224, 3) and return 4D tensor
    return np.expand_dims(x, axis=0)


def extract_Xception(tensor):
    return Xception(weights='imagenet', include_top=False).predict(preprocess_input(tensor))


# def predict_dog_breed(img_path):
#     model = create_model()
#     model.load_weights('best_model.hdf5')
#     bottleneck_feature = extract_Xception(path_to_tensor(img_path))
#     predicted_vector = model.predict(bottleneck_feature)
#     return dog_names[np.argmax(predicted_vector)]

# def predict_dog_breed(img_path):
#     model = create_model()
#     model.load_weights('best_model.hdf5')
#     bottleneck_feature = extract_Xception(path_to_tensor(img_path))
#     predicted_vector = model.predict(bottleneck_feature)

#     threshold = 0.4

#     high_prob_indices = np.where(predicted_vector >= threshold)[1]

#     if len(high_prob_indices) == 0:
#         return dog_names[np.argmax(predicted_vector)]

#     elif len(high_prob_indices) == 1:
#         return dog_names[high_prob_indices[0]]

#     else:
#         return ', '.join([dog_names[idx] for idx in high_prob_indices])

def predict_dog_breed(img_path):
    model = create_model()
    model.load_weights('best_model.hdf5')
    bottleneck_feature = extract_Xception(path_to_tensor(img_path))
    predicted_vector = model.predict(bottleneck_feature)

    threshold = 0.1

    high_prob_indices = np.where(predicted_vector >= threshold)[1]
    high_prob_values = predicted_vector[0][high_prob_indices]

    if len(high_prob_indices) == 0:
        max_idx = np.argmax(predicted_vector)
        return f"{dog_names[max_idx]} with confidence {predicted_vector[0][max_idx]:.2f}"

    elif len(high_prob_indices) == 1:
        return f"{dog_names[high_prob_indices[0]]} with confidence {high_prob_values[0]:.2f}"

    else:
        return ', '.join([f"{dog_names[idx]} ({predicted_vector[0][idx]:.2f})" for idx in high_prob_indices])


def yolo(image_path):

    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

    image = cv2.imread(image_path)
    # h, w = image.shape[:2]

    cv_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # plt.imshow(cv_rgb)
    # plt.show()

    blob = cv2.dnn.blobFromImage(
        image, 1/255, (416, 416), swapRB=True, crop=False)

    # Perform detection
    net.setInput(blob)
    layer_names = net.getLayerNames()
    output_layer_names = [layer_names[i - 1]
                          for i in net.getUnconnectedOutLayers()]
    detections = net.forward(output_layer_names)

    # print("Manual forward pass output:", output)

    human_detected = False
    dog_detected = False

    # print("A single detection:", detections[0][0])

    # print(net.getLayerNames())
    # print(net.getUnconnectedOutLayers())

    for output in detections:
        for detection in output:
            # print("detect jaa:",    detection)
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                # print(class_id, confidence)
                if class_id == 0:
                    human_detected = True
                elif class_id == 16:
                    dog_detected = True

        if human_detected and dog_detected:
            return "Both human and dog detected!", predict_dog_breed(image_path)
        elif human_detected:
            return "Hello, human!", predict_dog_breed(image_path)
        elif dog_detected:
            return "Hello, dog!", predict_dog_breed(image_path)
        else:
            return "Error: No human or dog detected in the image.", None

    # result, breed = yolo(image_path)
    # if breed:
    #     print(f"{result} You look like a {breed}.")
    # else:
    #     print(result)
