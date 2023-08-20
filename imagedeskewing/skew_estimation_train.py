import os
import tensorflow as tf
import numpy as np
import cv2
import math

RVl_CDIP_IMAGES_DIR = "/scratch/gpfs/RUSTOW/rvl_cdip_images/labels"
ROOT_DIR = "/scratch/gpfs/RUSTOW/rvl_cdip_images/images"
BATCH_SIZE = 128
EPOCHS = 10
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)


def read_file(file_path):
    with open(file_path, "r") as f:
        return [x.split(" ")[0].strip() for x in f.readlines()]


def load_and_preprocess(file_list):
    dataset = tf.data.Dataset.from_tensor_slices(file_list)
    dataset = dataset.map(load_image, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    dataset = dataset.map(preprocess, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    return dataset


def load_image(path):
    image = tf.io.read_file(path)
    image = tf.image.decode_jpeg(image, channels=3)
    return image


def rotatedRectWithMaxArea(w, h, angle):
    if w <= 0 or h <= 0:
        return 0, 0

    width_is_longer = w >= h
    side_long, side_short = (w, h) if width_is_longer else (h, w)

    sin_a, cos_a = abs(math.sin(angle)), abs(math.cos(angle))
    if side_short <= 2.*sin_a*cos_a*side_long or abs(sin_a-cos_a) < 1e-10:
        x = 0.5*side_short
        wr, hr = (x/sin_a, x/cos_a) if width_is_longer else (x/cos_a, x/sin_a)
    else:
        cos_2a = cos_a*cos_a - sin_a*sin_a
        wr, hr = (w*cos_a - h*sin_a)/cos_2a, (h*cos_a - w*sin_a)/cos_2a

    return wr, hr


def random_rotation(image):
    def rotate_fn(image_np):
        image_np = np.array(image_np)

        h, w, _ = image_np.shape
        center = (w / 2, h / 2)
        min_angle_rad, max_angle_rad = -math.pi / 8, math.pi / 8
        angle_rad = np.random.uniform(min_angle_rad, max_angle_rad)
        angle_deg = math.degrees(angle_rad)

        M = cv2.getRotationMatrix2D(center, angle_deg, 1.0)
        rotated_image_np = cv2.warpAffine(image_np, M, (w, h))

        wr, hr = rotatedRectWithMaxArea(w, h, angle_rad)

        # Get the starting and ending coordinates for the crop
        x1 = int(center[0] - wr // 2)
        x2 = int(center[0] + wr // 2)
        y1 = int(center[1] - hr // 2)
        y2 = int(center[1] + hr // 2)

        cropped_image_np = rotated_image_np[y1:y2, x1:x2]

        return cropped_image_np, np.array(angle_deg, dtype=np.float32)

    cropped_image, angle = tf.py_function(rotate_fn, [image], [tf.float32, tf.float32])
    cropped_image.set_shape([None, None, 3])
    return cropped_image, angle

def preprocess(image):
    rotated_image, angle = random_rotation(image)
    rotated_image = tf.image.resize(rotated_image, [224, 224])
    rotated_image = rotated_image / 255.0

    return rotated_image, angle


def create_model():
    base_model = tf.keras.applications.MobileNetV3Large(input_shape=(224, 224, 3), include_top=False,
                                                        weights="imagenet")

    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalMaxPool2D(),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(1, activation="linear")
    ])

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), loss="mse", metrics=["mae"])
    return model


if __name__ == '__main__':
    # Read and preprocess datasets
    train_file_list = [os.path.join(ROOT_DIR, x) for x in read_file(os.path.join(RVl_CDIP_IMAGES_DIR, "train.txt"))]
    test_file_list = [os.path.join(ROOT_DIR, x) for x in read_file(os.path.join(RVl_CDIP_IMAGES_DIR, "test.txt"))]
    val_file_list = [os.path.join(ROOT_DIR, x) for x in read_file(os.path.join(RVl_CDIP_IMAGES_DIR, "val.txt"))]

    train_dataset = load_and_preprocess(train_file_list)
    test_dataset = load_and_preprocess(test_file_list)
    val_dataset = load_and_preprocess(val_file_list)

    # Model creation
    model = create_model()

    # Callbacks
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=1e-6)
    checkpoint = tf.keras.callbacks.ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True)
    tensorboard = tf.keras.callbacks.TensorBoard(log_dir='./logs')

    # Training the model
    history = model.fit(train_dataset, epochs=EPOCHS, validation_data=val_dataset,
                        callbacks=[early_stopping, reduce_lr, checkpoint, tensorboard])
