from __future__ import print_function

import argparse
import os
import pandas as pd

# from sklearn.externals import joblib
import joblib

from sklearn.neural_network import MLPRegressor as nn

# Provided model load function
def model_fn(model_dir):
    """Load model from the model_dir. This is the same model that is saved
    in the main if statement.
    """
    print("Loading model.")
    
    # load using joblib
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    print("Done loading model.")
    
    return model


if __name__ == '__main__':
    
    # All of the model parameters and training parameters are sent as arguments
    # when this script is executed, during a training job
    
    # Here we set up an argument parser to easily access the parameters
    parser = argparse.ArgumentParser()

    # SageMaker parameters, like the directories for training data and saving models; set automatically
    parser.add_argument('--output-data-dir', type=str, default=os.environ['SM_OUTPUT_DATA_DIR'])
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--data-dir', type=str, default=os.environ['SM_CHANNEL_TRAIN'])
    
    # Model parameters
    parser.add_argument('--alpha', type=int, default=1)
    parser.add_argument('--max_iter', type=int, default=1000)

    # args holds all passed-in arguments
    args = parser.parse_args()

    # Read in csv training file
    training_dir = args.data_dir
    train_data = pd.read_csv(os.path.join(training_dir, "r_train.csv"), header=None, names=None)

    # Labels are in the first column
    train_y = train_data.iloc[:,0]
    train_x = train_data.iloc[:,1:]    

    alpha = args.alpha
    max_iter = args.max_iter
    
    model = nn(alpha=alpha, max_iter=max_iter)
    
    model = model.fit(train_x, train_y)        

    # Save the trained model
    joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))
