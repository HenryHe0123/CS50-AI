import pickle

import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split
from tensorflow.keras import layers

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():
    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test, y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    # Check if saved data file exists
    saved_data_file = "saved_data.pkl"
    if os.path.exists(saved_data_file):
        print("Loading saved data...")
        with open(saved_data_file, "rb") as f:
            saved_data = pickle.load(f)
        print("Data loaded successfully.")
        return saved_data

    # Load data from directory
    images, labels = [], []
    completed_folders = 0
    total_folders = NUM_CATEGORIES
    bar_length = 43
    print("Loading data from directory...")

    for category in range(NUM_CATEGORIES):
        path = os.path.join(data_dir, str(category))

        # Progress bar
        progress = int(bar_length * completed_folders / total_folders)
        print('\r[{}>{}] {}%'.format('=' * progress, '.' * (bar_length - progress),
                                     int(100 * completed_folders / total_folders)), end='')

        for file in os.listdir(path):
            img = cv2.imread(os.path.join(path, file))
            img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
            images.append(img)
            labels.append(category)

        completed_folders += 1

    print('\r[{}] 100%'.format('=' * (bar_length + 1)))

    # Save the loaded data to file
    data = (images, labels)
    with open(saved_data_file, "wb") as f:
        pickle.dump(data, f)
    print("Data loaded successfully.")
    return data


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.Sequential([
        layers.Conv2D(128, (4, 4), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(256, (2, 2), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    main()
