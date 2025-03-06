import os
import argparse
import numpy as np
import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from sklearn.metrics import confusion_matrix

IMG_SIZE = (128, 128)
BATCH_SIZE = 32
TRAIN_DIR = "data/train"
TEST_DIR = "data/test"
MODEL_PATH = "cat_dog_classifier.h5"

def create_model():
	model = Sequential([
		Conv2D(32, (3,3), activation='relu', input_shape=(128, 128, 3)),
		MaxPooling2D(2, 2),
		Conv2D(64, (3,3), activation='relu'),
		MaxPooling2D(2, 2),
		Flatten(),
		Dense(128, activation='relu'),
		Dropout(0.5),
		Dense(1, activation='sigmoid')
	])
	model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
	return model

def train_model():
	print("Loading dataset...")
	train_datagen = ImageDataGenerator(rescale=1./255, horizontal_flip=True)
	train_gen = train_datagen.flow_from_directory(TRAIN_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='binary')

	print("Building model...")
	model = create_model()

	print("Training model...")
	model.fit(train_gen, epochs=10)

	print("Saving model...")
	model.save(MODEL_PATH)
	print(f"Model saved at {MODEL_PATH}")

def evaluate_model():
	if not os.path.exists(MODEL_PATH):
		print("No trained model found. Train the model first.")
		return

	print("Loading model...")
	model = load_model(MODEL_PATH)

	print("Loading test dataset...")
	test_datagen = ImageDataGenerator(rescale=1./255)
	test_gen = test_datagen.flow_from_directory(TRAIN_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='binary', shuffle=False)

	print("Evaluating model")
	predictions = (model.predict(test_gen) > 0.5).astype("int32")
	cm = confusion_matrix(test_gen.classes, predictions)
	print("Confusion Matrix:\n", cm)

def run_ui():
	if not os.path.exists(MODEL_PATH):
		st.error("No trained model found! Train the model first.")
		return
	
	st.title("🐶🐱 Cat vs. Dog Classifier")
	model = load_model(MODEL_PATH)

	uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])
	if uploaded_file:
		img = load_img(uploaded_file, target_size=IMG_SIZE)
		img_array = img_to_array(img) / 255.0
		img_array = np.expand_dims(img_array, axis=0)

		prediction = model.predict(img_array)
		label = "Dog 🐶" if prediction[0][0] > 0.5 else "Cat 🐱"

		st.image(uploaded_file, caption=f"Prediction: {label}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--train", action="store_true", help="Train the model")
	parser.add_argument("--evaluate", action="store_true", help="Evaluate the model")
	parser.add_argument("--ui", action="store_true", help="Run the user interface")

	args =  parser.parse_args()

	if args.train:
		train_model()
	elif args.evaluate:
		evaluate_model()
	else:
		run_ui()