# imports
import tensorflow as tf
import keras
import pandas as pd
import numpy as np

# loading a dataset function
def load_dataset(path):
    df = pd.read_csv(path)
    df = df.drop("Strategy", axis=1)
    df_labels = df.pop("Move5A")
    return df, df_labels

# loading training data
ipd_train = pd.read_csv("train.csv")
ipd_features = ipd_train.copy().drop("Strategy", axis=1)
ipd_labels = ipd_features.pop("Move5A")
ipd_features = np.array(ipd_features)

# defining noise levels for testing
noise_levels = [0, 0.1, 0.3, 0.5, 0.7, 0.9, 1]

# defining a sequential model
model = keras.models.Sequential(
    [
        tf.keras.layers.Dense(8, activation="relu"),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(3, activation="softmax")
    ]
)

# compiling model with optimizer and training
model.compile(optimizer="nadam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(ipd_features, ipd_labels, epochs=5, validation_split=0.2, batch_size=128)

# saving model
model.save("model.h5")

# testing model
results_dict = {"Noise": [], "Accuracy": [], "Loss": []}
for noise in noise_levels:
    df_features, df_labels = load_dataset(f"test_noise_{noise}.csv")
    results = model.evaluate(df_features, df_labels)
    print(f"Test Accuracy: {results[1]*100}%")
    results_dict["Noise"].append(noise)
    results_dict["Accuracy"].append(results[1]*100)
    results_dict["Loss"].append(results[0])

# saving test results
results_df = pd.DataFrame(results_dict)
results_df.to_csv("results.csv", index=False)

