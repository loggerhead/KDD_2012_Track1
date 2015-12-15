#!/usr/bin/env python
# -*- coding: utf-8 -*-

show_summary            = True
generate_validation_set = False
do_preprocess           = True
do_training             = True
do_evaluate             = True

paths = {
    'original_train': 'data/rec_log_train.csv',
    'original_test': 'data/rec_log_test.csv',
    'original_solution': 'data/KDD_Track1_solution.csv',
    'original_user_profile': 'data/user_profile.csv',
    # =============== below files will be created when running ===============
    # generate from original training dataset
    'validation_dataset': 'data/validation_dataset.csv',
    'preprocess_output': 'data/preprocessed.csv',
    # file which saves predicted result
    'predict_output': 'data/predicted.csv',
    # predicted result => submission format
    'predict_submission_output': 'data/predicted_submission.csv',
}
# dataset used for preprocessing
paths['preprocess_dataset'] = paths['original_train']
# dataset used for training
paths['train_dataset'] = paths['preprocess_output']
# dataset used for predicting
paths['test_dataset'] = paths['original_test']
# dataset used for computing mAP@3
paths['solution_dataset'] = paths['original_solution']

# parameters used in Latent Factor Model
# the number of lines of random sampling in each iteration
SAMPLES_NUMBER = 1212765
# maximum number of iterations
TRAIN_REPEAT   = 600
# dimension of the feature vectors (`p` and `q`)
DIMENSION      = 64
# η  -- formula between formulas (3) and (4)
# learning rate
ETA    = 0.22
# λ  -- formula between formulas (3) and (4)
# used for avoiding overfitting
LAMBDA = 0.04

# parameters used in preprocess
# τ0 -- formula (6)
TAU0     = 90
# π- -- formula (7)
PI_MINUS = 0
# π+ -- formula (8)
PI_PLUS  = 3
# ε  -- formula (9)
EPSILON  = 0.86