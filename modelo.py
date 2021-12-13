from re import M
from typing import Dict, Text

import numpy as np
import tensorflow as tf

import tensorflow_recommenders as tfrs

import os
import pprint
import tempfile

import pandas as pd
import matplotlib.pyplot as plt
import crudrating
import crudlibros

print("Creando dataset")
masterdf = pd.read_csv('ratings.csv')
masterdf.head(3)
masterdf = masterdf[['userId', 'movieId', 'rating']]
masterdf.head(3)
masterdf[['userId', 'movieId',]] = masterdf[['userId', 'movieId']].astype(str)
masterdf['rating'] = masterdf['rating'].astype(float)

interactions_dict = masterdf.groupby(['userId', 'movieId'])[ 'rating'].sum().reset_index()

interactions_dict = {name: np.array(value) for name, value in interactions_dict.items()}
interactions = tf.data.Dataset.from_tensor_slices(interactions_dict)

items_dict = masterdf[['movieId']].drop_duplicates()
items_dict = {name: np.array(value) for name, value in items_dict.items()}
items = tf.data.Dataset.from_tensor_slices(items_dict)

interactions = interactions.map(lambda x: {
    'userId' : x['userId'], 
    'movieId' : x['movieId'], 
    'rating' : float(x['rating']),
})

items = items.map(lambda x: x['movieId'])

unique_item_titles = np.unique(np.concatenate(list(items.batch(1000))))
unique_user_ids = np.unique(np.concatenate(list(interactions.batch(1_000).map(lambda x: x["userId"]))))

unique_item_titles = np.unique(np.concatenate(list(items.batch(1000))))
unique_user_ids = np.unique(np.concatenate(list(interactions.batch(1_000).map(lambda x: x["userId"]))))

tf.random.set_seed(42)
shuffled = interactions.shuffle(100_000, seed=42, reshuffle_each_iteration=False)

train = shuffled.take(60_000)
test = shuffled.skip(60_000).take(20_000)

# libros = crudlibros.administrar_libros()
# rating = crudratings.administrar_rating()
# Conseguir todos los libros y todos los ratings
class RetailModel(tfrs.Model):
    def __init__(self, user_model, item_model):
        super().__init__()
        item_model = tf.keras.Sequential([
                                        tf.keras.layers.experimental.preprocessing.StringLookup(
                                        vocabulary=unique_item_titles, mask_token=None),
                                        tf.keras.layers.Embedding(len(unique_item_titles) + 1, embedding_dimension)
                                        ])
        self.item_model: tf.keras.Model = item_model

        user_model = tf.keras.Sequential([
                                        tf.keras.layers.experimental.preprocessing.StringLookup(
                                        vocabulary=unique_user_ids, mask_token=None),
                                        tf.keras.layers.Embedding(len(unique_user_ids) + 1, embedding_dimension)
                                        ])
        self.user_model: tf.keras.Model = user_model

        metrics = tfrs.metrics.FactorizedTopK(
                                            candidates=items.batch(128).map(item_model)
        )
        task = tfrs.tasks.Retrieval(
                                    metrics=metrics
                                    )
    
        self.task: tf.keras.layers.Layer = task

    def compute_loss(self, features: Dict[Text, tf.Tensor], training=False) -> tf.Tensor:
        user_embeddings = self.user_model(features["userId"])
        positive_movie_embeddings = self.item_model(features["movieId"])

        return self.task(user_embeddings, positive_movie_embeddings)

embedding_dimension = 32

item_model = tf.keras.Sequential([
                                tf.keras.layers.experimental.preprocessing.StringLookup(
                                vocabulary=unique_item_titles, mask_token=None),
                                tf.keras.layers.Embedding(len(unique_item_titles) + 1, embedding_dimension)
                                ])

user_model = tf.keras.Sequential([
                                tf.keras.layers.experimental.preprocessing.StringLookup(
                                vocabulary=unique_user_ids, mask_token=None),
                                tf.keras.layers.Embedding(len(unique_user_ids) + 1, embedding_dimension)
                                ])

model = RetailModel(user_model, item_model)

model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))

cached_train = train.shuffle(100_000).batch(8192).cache()
cached_test = test.batch(4096).cache()

model_hist = model.fit(cached_train, epochs=10)

model.evaluate(cached_test, return_dict=True)

epochs = [i for i in range(10)]

plt.plot(epochs, model_hist.history["factorized_top_k/top_100_categorical_accuracy"], label="accuracy")
plt.title("Accuracy vs epoch")
plt.xlabel("epoch")
plt.ylabel("Top-100 accuracy")
plt.legend()

print("Prediciendo")
brute_force  = tfrs.layers.factorized_top_k.BruteForce(model.user_model)

brute_force.index_from_dataset(items.batch(100).map(lambda items: (items, model.item_model(items))))

j = str(40)
_, titles = brute_force(tf.constant([j]))
print(f"Recommendations for user %s: {titles[0]}" %(j))