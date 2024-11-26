import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D, Dense, ReLU, BatchNormalization
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model, Sequential

class ResNetBlock(Layer):
    def __init__(self, out_channels, first_stride=1):
        super().__init__()
        first_padding = 'same'
        if first_stride != 1:
            first_padding = 'valid'

        self.conv_sequence = Sequential([
            Conv2D(out_channels, 3, first_stride, padding=first_padding),
            BatchNormalization(),
            ReLU(),
            Conv2D(out_channels, 3, 1, padding='same'),
            BatchNormalization(),
            ReLU()
        ])

    def call(self, inputs):
        x = self.conv_sequence(inputs)
        if x.shape == inputs.shape:
            x = x + inputs
        return x

class ResNet(Model):
    def __init__(self):
        super(ResNet, self).__init__()
        self.conv_1 = Sequential([Conv2D(64, 7, 2), ReLU(), MaxPooling2D(3, 2)])
        self.resnet_chains = Sequential([ResNetBlock(64), ResNetBlock(64)] +
                                        [ResNetBlock(128, 2), ResNetBlock(128)] +
                                        [ResNetBlock(256, 2), ResNetBlock(256)] +
                                        [ResNetBlock(512, 2), ResNetBlock(512)] +
                                        [ResNetBlock(1024, 2), ResNetBlock(1024)])
        self.out = Sequential([GlobalAveragePooling2D(), Dense(2, activation='softmax')])

    def call(self, x):
        x = self.conv_1(x)
        x = self.resnet_chains(x)
        x = self.out(x)
        return x

# Initialize the model
model = ResNet()

# Create a dummy input to initialize the model's variables
dummy_input = tf.random.normal([16, 224, 224, 3])  # Adjust to your input shape
model(dummy_input)  # Call the model to create variables

# Load the saved weights
# Load the entire model if it was saved with model.save
model = tf.keras.models.load_weights('D:\Coding\React\Project UI\LearnScope\VerdictIQ\server\Respira\ml\model_weights.keras')


def load_and_preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # Load image
    img_array = image.img_to_array(img)  # Convert to array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array/ 255.0  # Normalize the image
    return img_array

image_path = r'D:\Coding\React\Project UI\LearnScope\VerdictIQ\public\image.png'  # Change this to your image path

# Load and preprocess the image
# img = load_and_preprocess_image(image_path)