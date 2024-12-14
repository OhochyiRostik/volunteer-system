import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Input, Embedding, Flatten, Concatenate, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import mean_absolute_error

class NeuralCF:
    def __init__(self, num_users, num_items, embedding_dim=10, hidden_layers=[64, 32], activation='relu', learning_rate=0.001):
        self.num_users = num_users
        self.num_items = num_items
        self.embedding_dim = embedding_dim
        self.hidden_layers = hidden_layers
        self.activation = activation
        self.learning_rate = learning_rate
    def _build_model(self):
        user_input = Input(shape=(1,))
        item_input = Input(shape=(1,))
        user_embedding = Embedding(self.num_users, self.embedding_dim)(user_input)
        user_embedding = Flatten()(user_embedding)
        item_embedding = Embedding(self.num_items, self.embedding_dim)(item_input)
        item_embedding = Flatten()(item_embedding)
        vector = Concatenate()([user_embedding, item_embedding])
        for units in self.hidden_layers:
            vector = Dense(units, activation=self.activation)(vector)
        output = Dense(1, activation='sigmoid')(vector)
        model = Model(inputs=[user_input, item_input], outputs=output)
        return model
    def train(self, X_train, y_train, epochs=2, batch_size=10, validation_split=0.1):
        X_train = [X_train[:, 0], X_train[:, 1]]
        y_train = np.array(y_train)
        model = self._build_model()
        model.compile(optimizer=Adam(learning_rate=self.learning_rate), loss='mean_squared_error')
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=validation_split)
        self.model = model
    def predict(self, X_test):
        X_test = [X_test[:, 0], X_test[:, 1]]
        return self.model.predict(X_test)
# Hyperparameters that could be tuned
embedding_dim = 10
hidden_layers = [64, 32]
activation = 'relu'
learning_rate = 0.001
df = pd.read_csv("Dataset.csv").iloc[:30000,:]
X = df[['User_ID','Event_ID']].to_numpy()
y = df['Rating'].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
num_users = df['User_ID'].max() + 1
num_items = df['Event_ID'].max() + 1
# Train and predict using NeuralCF
print("------------------------------")
ncf = NeuralCF(num_users, num_items, embedding_dim, hidden_layers, activation, learning_rate)
ncf.train(X_train, y_train, epochs=2)
y_pred = ncf.predict(X_test)
# Evaluate using Mean Squared Error
mse = mean_absolute_error(y_test, y_pred)

ncf.model.save('ncf_model.h5')

print("Mean Absolute Error:", mse)