This is a simple solution of [2012 KDD Cup Track 1](http://www.kddcup2012.org/c/kddcup2012-track1), which implemented Latent Factor Model by using Stochastic Gradient Descent algorithm, and most idea is came from `2.2` and `3.1` sections of paper [Context-aware Ensemble of Multifaceted Factorization Models for Recommendation Prediction in Social Networks](https://kaggle2.blob.core.windows.net/competitions/kddcup2012/2748/media/Shanda3.pdf). 

#Run
For saving your time, I strongly recommend you to install `PyPy` which is roughly three times faster than `CPython` in my test.

1. Change `config.py` file to tell the program where to find the datasets.
2. `./run.sh`
3. Press `Ctrl-C` in terminal whenever you want to end the training loop.

#Dataset
There are four datasets needed for running:

* [rec_log_train](https://coding.net/u/loggerhead/p/KDD_2012_Track1/git/raw/master/data/rec_log_train.csv.lrz)
* [rec_log_test](https://coding.net/u/loggerhead/p/KDD_2012_Track1/git/raw/master/data/rec_log_test.csv.lrz)
* [KDD_Track1_solution](https://coding.net/u/loggerhead/p/KDD_2012_Track1/git/raw/master/data/KDD_Track1_solution.csv)
* [user_profile](https://coding.net/u/loggerhead/p/KDD_2012_Track1/git/raw/master/data/user_profile.csv.lrz)

I have made some little changes to the orignal datasets:

* remove header from each file
* replace separator from `\t` (tab) to `,` (comma)

If you download datasets from above links, you will found some `.lrz` files and you need use [lrzip](https://github.com/ckolivas/lrzip) to uncompress.

```bash
# install `lrzip`
apt-get install lrzip 
# if you are OSX user, run below command to install `lrzip`
# brew install lrzip

lrzip -d *.lrz
```

#Running log
```
Getting summary of training dataset...
======================== Summary of 'rec_log_train.csv' ========================
Users: 1392873  Items: 4710     Users/Items: 295.73
+1: 5253828     -1: 67955449    +1/-1: 0.08
Begin time: 1318348785  End time:1321027199     Interval: 2678414s = 744.00 h = 31.00 d
================== Distribution of user active time (in hour) ==================
 00: |
 01: |
 07: |
 08: ||
 09: |||
 10: |||
 11: |||
 12: |||
 13: |||
 14: |||
 15: |||
 16: |||
 17: |||
 18: |||
 19: |||
 20: |||
 21: |||
 22: |||
 23: ||
Getting summary of user profile...
============================= Distribution of age ==============================
  0: |
  1: |
  2: |
  3: |
 12: |
 13: |
 14: ||
 15: ||
 16: ||
 17: ||
 18: ||
 19: ||
 20: |||
 21: |||
 22: ||||
 23: |||
 24: |||
 25: |||
 26: ||
 27: ||
 28: |
 29: |
 30: |
 31: |
 32: |
 33: |
============================ Distribution of gender ============================
  0: |
  1: |||||||||||||||||||||||||
  2: ||||||||||||||||||||||||
============================ Distribution of tweet =============================
  0: ||||
  1: |
  2: |
  3: |
  4: |
  5: |
  6: |
  7: |
  8: |
  9: |
 10: |
 11: |
 12: |
 13: |
 14: |
============================= Distribution of tags =============================
  1: ||||||||||||||||||||||||||||||||||||
  2: |
  3: |
  4: |
  5: |
  6: |
  7: |
  8: |
  9: ||
 10: ||||
Preprocessing...
Training...
init LFM...             26.158s
408th trainning used 21.1ss     |e[u][i]| = 0.251114^C
Exit program after finish current work!
409th trainning used 22.6s      |e[u][i]| = 0.251115
predict and write result...             500.564s
Converting predicted result to submission format...
convert predict result to dict...               155.102s
convert to submission format...                 50.497s
Computing mAP@3...
 Public rank: 412       mAP@3: 0.31774
Private rank: 422       mAP@3: 0.30857
```