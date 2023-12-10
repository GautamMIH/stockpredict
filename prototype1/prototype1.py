import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

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


import numpy as np

# Define the sigmoid and tanh activation functions
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)

# Initialize weights and biases
input_size = len(features)
hidden_size = 50
output_size = len(features)

weights_input = np.random.randn(input_size, hidden_size)
weights_hidden = np.random.randn(hidden_size, hidden_size)
weights_output = np.random.randn(hidden_size, output_size)

bias_hidden = np.zeros((1, hidden_size))
bias_output = np.zeros((1, output_size))

# Training hyperparameters
learning_rate = 0.001
epochs = 100

# Training the LSTM
for epoch in range(epochs):
    for i in range(len(X_train)):
        # Forward pass
        inputs = X_train[i]
        targets = y_train[i]

        hidden_state = np.zeros((1, hidden_size))
        cell_state = np.zeros((1, hidden_size))

        loss = 0

        for t in range(time_step):
            # Update hidden state
            combined = np.dot(inputs[t], weights_input) + np.dot(hidden_state, weights_hidden) + bias_hidden
            hidden_state = tanh(combined)

        # Output layer
        output = np.dot(hidden_state, weights_output) + bias_output

        # Backward pass
        output_error = output - targets
        loss += np.sum(output_error ** 2)

        # Update weights and biases
        weights_output -= learning_rate * np.dot(hidden_state.T, output_error)
        hidden_error = np.dot(output_error, weights_output.T)
        hidden_error = hidden_error * (1 - hidden_state ** 2)

        for t in reversed(range(time_step)):
            # Update hidden state
            combined = np.dot(inputs[t], weights_input) + np.dot(hidden_state, weights_hidden) + bias_hidden
            hidden_state = tanh(combined)

            # Update weights and biases
            weights_input -= learning_rate * np.dot(inputs[t].reshape(-1, 1), hidden_error)
            weights_hidden -= learning_rate * np.dot(hidden_state.T, hidden_error)
            bias_hidden -= learning_rate * hidden_error

# # Make predictions for the next day
# last_day_data = df_normalized[-time_step:, :]
# hidden_state = np.zeros((1, hidden_size))
# cell_state = np.zeros((1, hidden_size))

# predicted_values = []

# for t in range(time_step):
#     # Update hidden state
#     combined = np.dot(last_day_data[t], weights_input) + np.dot(hidden_state, weights_hidden) + bias_hidden
#     hidden_state = tanh(combined)

# # Output layer
# output = np.dot(hidden_state, weights_output) + bias_output
# predicted_values.append(output)

# # Inverse transform the predicted values
# predicted_values = np.array(predicted_values).reshape(-1, len(features))
# predicted_values = scaler.inverse_transform(predicted_values)

# # Print the predicted values
# predicted_df = pd.DataFrame(predicted_values, columns=features)
# print("Predicted Values for the Next Day:")
# print(predicted_df)





import numpy as np
import pandas as pd


# Save the trained weights and biases to separate CSV files
np.savetxt("weights_input.csv", weights_input, delimiter=",")
np.savetxt("weights_hidden.csv", weights_hidden, delimiter=",")
np.savetxt("weights_output.csv", weights_output, delimiter=",")
np.savetxt("bias_hidden.csv", bias_hidden, delimiter=",")
np.savetxt("bias_output.csv", bias_output, delimiter=",")

# Print a message indicating that training is complete
print("Training complete. Weights and biases saved.")





import pandas as pd
import numpy as np

input_size = len(features)
hidden_size = 50
output_size = len(features)
# # Load the saved weights from the CSV file
# saved_weights = np.loadtxt("lstm_weights.csv", delimiter=",")

# Load the saved weights and biases from separate CSV files
weights_input = np.loadtxt("weights_input.csv", delimiter=",")
weights_hidden = np.loadtxt("weights_hidden.csv", delimiter=",")
weights_output = np.loadtxt("weights_output.csv", delimiter=",")
bias_hidden = np.loadtxt("bias_hidden.csv", delimiter=",")
bias_output = np.loadtxt("bias_output.csv", delimiter=",")


# Load input data for prediction
# Replace this with your own input data
url = '/content/drive/MyDrive/content/NLICx.csv'
input_df = pd.read_csv(url)
input_df = input_df.applymap(lambda x: str(x).replace(',', ''))

# Consider the same features used during training
input_features = ['Open', 'High', 'Low', 'Ltp', 'Qty', 'Turnover', '% Change', 'Inflation Rate']
input_data = input_df[input_features]

# Normalize the input data using the same scaler used during training
input_normalized = scaler.transform(input_data)

# Reshape the input data to match the model's expected input shape
input_sequence = np.array([input_normalized[-time_step:, :]])
input_sequence = input_sequence.reshape(1, time_step, len(features))

# Make predictions
hidden_state = np.zeros((1, hidden_size))
predicted_values = []

for t in range(time_step):
    # Update hidden state
    combined = np.dot(input_sequence[0, t], weights_input) + np.dot(hidden_state, weights_hidden) + bias_hidden
    hidden_state = np.tanh(combined)

# Output layer
output = np.dot(hidden_state, weights_output) + bias_output
predicted_values.append(output)

# Inverse transform the predicted values
predicted_values = np.array(predicted_values).reshape(-1, len(features))
predicted_values = scaler.inverse_transform(predicted_values)

# Print the predicted values
predicted_df = pd.DataFrame(predicted_values, columns=features)
print("Predicted Values for the Next Day:")
print(predicted_df)
