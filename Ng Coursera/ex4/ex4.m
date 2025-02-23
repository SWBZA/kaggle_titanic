% Using Andrew Ng course neural network to predict Titanic survival

%% Initialization
clear ; close all; clc

%% Setup the parameters you will use for this exercise
input_layer_size  = 7;  % 7 chosen features
hidden_layer_size = 2;   % number of hidden units
num_labels = 2;          % survive / not-survive

% Load Training Data
fprintf('Loading Data ...\n')

input_data=csvread("train.csv");
y = input_data(2:end,1);
X = input_data(2:end,2:end);
m = size(X, 1);

%% ================ Part 6: Initializing Pameters ================
fprintf('\nInitializing Neural Network Parameters ...\n')

initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size);
initial_Theta2 = randInitializeWeights(hidden_layer_size, num_labels);

% Unroll parameters
initial_nn_params = [initial_Theta1(:) ; initial_Theta2(:)];


%% =================== Training NN ===================
%  To train your neural network, we will now use "fmincg", which
%  is a function which works similarly to "fminunc". Recall that these
%  advanced optimizers are able to train our cost functions efficiently as
%  long as we provide them with the gradient computations.
%
fprintf('\nTraining Neural Network... \n')

%  After you have completed the assignment, change the MaxIter to a larger
%  value to see how more training helps.
options = optimset('MaxIter', 1000);

%  You should also try different values of lambda
lambda = 0.3;

% Create "short hand" for the cost function to be minimized
costFunction = @(p) nnCostFunction(p, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, X, y, lambda);

% Now, costFunction is a function that takes in only one argument (the
% neural network parameters)
[nn_params, cost] = fmincg(costFunction, initial_nn_params, options);

% Obtain Theta1 and Theta2 back from nn_params
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));


%% ================= Part 10: Implement Predict =================
%  After training the neural network, we would like to use it to predict
%  the labels. You will now implement the "predict" function to use the
%  neural network to predict the labels of the training set. This lets
%  you compute the training set accuracy.

pred = predict(Theta1, Theta2, X);
pred = pred -1;

fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == y)) * 100);

%% ================= Predict for Titanic test set ================

% Load test data
input_test_data=csvread("test.csv");
X_predict = input_test_data(2:end,2:end);


% Make prediction on test data set
pred = predict(Theta1, Theta2, X_predict);
pred = pred -1;

% Add passenger number from test data set to upload to Kaggle
prediction_out = [input_test_data(2:end, 1)  pred(:,:)];

% Output data - REMEMBER, NO HEADER IN FILE
csvwrite("Ng_NN.csv", prediction_out);
