import pandas as pd
import numpy as np
import math
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler

# Load your dataset
url = '/content/drive/MyDrive/content/NLICx.csv'
df = pd.read_csv(url)
df = df.applymap(lambda x: str(x).replace(',', ''))

# Consider multiple features
features = ['Open', 'High', 'Low', 'Ltp', 'Qty', 'Turnover','% Change', 'Inflation Rate']
df1 = df[features]

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
df_normalized = scaler.fit_transform(df1)

# Split the data into training and test sets
training_size = int(len(df_normalized) * 0.65)
test_size = len(df_normalized) - training_size
train_data, test_data = df_normalized[0:training_size, :], df_normalized[training_size:len(df_normalized), :]

# Function to create dataset with multiple features
def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), :]
        dataX.append(a)
        dataY.append(dataset[i + time_step, :])
    return np.array(dataX), np.array(dataY)

time_step = 100
X_train, y_train = create_dataset(train_data, time_step)
X_test, y_test = create_dataset(test_data, time_step)

# Reshape the input data
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], len(features))
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], len(features))

# Build the LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_step, len(features))))
model.add(LSTM(50, return_sequences=True))
model.add(LSTM(50))
model.add(Dense(len(features)))  # Adjust the number of neurons in the Dense layer based on the number of features
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

# Convert target values to one-hot encoding for categorical crossentropy (add)
y_train_onehot = tf.keras.utils.to_categorical(y_train.argmax(axis=1), num_classes=len(features))
y_test_onehot = tf.keras.utils.to_categorical(y_test.argmax(axis=1), num_classes=len(features))

# Train the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=64, verbose=1)

model.save_weights("model_weights.h5")
print("Model weights saved.")

# Evaluate accuracy on the training dataset
train_loss, train_accuracy = model.evaluate(X_test, y_test_onehot, verbose=0)
print(f'Training Accuracy: {train_accuracy}')

# Make predictions for the next day
last_day_data = df_normalized[-time_step:, :]
last_day_data = last_day_data.reshape(1, time_step, len(features))
predicted_values = model.predict(last_day_data)

# Inverse transform the predicted values
predicted_values = scaler.inverse_transform(predicted_values)

# Print the predicted values
predicted_df = pd.DataFrame(predicted_values, columns=features)
print("Predicted Values for the Next Day:")
print(predicted_df)




predicted_df = pd.DataFrame(predicted_values, columns=features)

# Extract the last 'Ltp' value from the input dataset
last_ltp_value = float(df['Ltp'].iloc[-1])

# Extract the predicted 'Ltp' value
predicted_ltp_value = float(predicted_df['Ltp'].iloc[0])

# Print the predicted values
print("Predicted Values for the Next Day:")
print(predicted_df)

# Compare the predicted 'Ltp' with the last value in the input dataset
if predicted_ltp_value > last_ltp_value:
    print("Prediction: Increase")
else:
    print("Prediction: Decrease")