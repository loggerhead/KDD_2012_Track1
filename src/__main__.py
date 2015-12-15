#!/usr/bin/env python
# -*- coding: utf-8 -*-

import conf
import preprocess
import predict
import data_summary as summary
from gen_validation_set import *
import evaluate

if __name__ == '__main__':
    if conf.show_summary:
        print 'Getting summary of training dataset...'
        summary.summary_of_training_set(conf.paths['original_train'])
        print 'Getting summary of user profile...'
        summary.summary_of_user_profile(conf.paths['original_user_profile'])
    if conf.generate_validation_set:
        print 'Generating validation dataset...'
        gen_validation_set(conf.paths['original_train'],
                           conf.paths['train_dataset'],
                           conf.paths['validation_dataset'])
    if conf.do_preprocess:
        print 'Preprocessing...'
        preprocess.filter_by_session(conf.paths['preprocess_dataset'],
                                     conf.paths['preprocess_output'])
    if conf.do_training:
        print 'Training...'
        predict.predict(conf.paths['train_dataset'],
                        conf.paths['test_dataset'],
                        conf.paths['predict_output'])
        print 'Converting predicted result to submission format...'
        predict.to_submission_format(conf.paths['predict_output'],
                                     conf.paths['predict_submission_output'])
    if conf.do_evaluate:
        print 'Computing mAP@3...'
        evaluate.compute_mAP_and_rank(conf.paths['predict_submission_output'],
                                      conf.paths['solution_dataset'])