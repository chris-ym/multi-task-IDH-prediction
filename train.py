import argparse
import math
import numpy as np
import pandas as pd
import tensorflow as tf
import socket
import importlib
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'models'))
sys.path.append(os.path.join(BASE_DIR, 'utils'))
import tf_util

parser = argparse.ArgumentParser()
parser.add_argument('--gpu', type=int, default=0, help='GPU to use [default: GPU 0]')
parser.add_argument('--model', default='RTNet', help='Model name: RTNet')
parser.add_argument('--num_data', type=int, default='10', help='number of balanced data')
parser.add_argument('--log_dir', default='log', help='Log dir [default: log]')
parser.add_argument('--num_trans_enc', type=int, default=2, help='Number of transformer encoder [default: 2]')
parser.add_argument('--max_epoch', type=int, default=50, help='Epoch to run [default: 50]')
parser.add_argument('--batch_size', type=int, default=64, help='Batch Size during training [default: 64]')
parser.add_argument('--learning_rate', type=float, default=0.001, help='Initial learning rate [default: 0.001]')
parser.add_argument('--decay_step', type=int, default=200000, help='Decay step for lr decay [default: 200000]') 
parser.add_argument('--loss_weight', type=int, default=1, help='Initial loss weight [default: 1]')
parser.add_argument('--optimizer', default='adam', help='adam or momentum [default: adam]')
FLAGS = parser.parse_args()

MODEL = FLAGS.model
BATCH_SIZE = FLAGS.batch_size
MAX_EPOCH = FLAGS.max_epoch
BASE_LEARNING_RATE = FLAGS.learning_rate
GPU_INDEX = FLAGS.gpu
LOSS_WEIGHT = FLAGS.loss_weight
DECAY_STEP = FLAGS.decay_step
OPTIMIZER = FLAGS.optimizer
LOG_DIR = FLAGS.log_dir

MODEL = importlib.import_module(FLAGS.model) # import network module
MODEL_FILE = os.path.join(BASE_DIR, 'models', FLAGS.model+'.py')
LOG_DIR = FLAGS.log_dir
if not os.path.exists(LOG_DIR): 
    os.mkdir(LOG_DIR)
os.system('cp %s %s' % (MODEL_FILE, LOG_DIR)) # backup of model definition
os.system('cp train.py %s' % (LOG_DIR)) # backup of train process
LOG_FOUT = open(os.path.join(LOG_DIR, 'log_train.txt'), 'w')
LOG_FOUT.write(str(FLAGS)+'\n')

#### read train & test data#############################
#### Import data (different methods)

def get_data(data_name):
    import os
    import pickle
    name, extension = os.path.splitext(path)
    if extension == ".csv":
        data=pd.read_csv("%s.csv"%data_name)
    elif extension == ".pkl":
        f=open("%s.pkl"%data_name,'rb')
        data=pickle.load(f)
        f.close()
    else:
        
    return data
#######################################################

#### definition of learning rate(lr)
def warmup_and_decay_lr(batch,warm_up=False):
    lr = tf.train.cosine_decay(BASE_LEARNING_RATE,
                         batch * BATCH_SIZE,
                         DECAY_STEP,)
    if warm_up == True:
        warmup_steps = int(batch * MAX_EPOCH * 0.2)
        warmup_lr = ( BASE_LEARNING_RATE * tf.cast(global_step, tf.float32)) / tf.cast(
            warmup_steps, tf.float32)                    
        return tf.cond( global_step < warmup_steps, lambda: warmup_lr, lambda: lr)
    
    lr = tf.maximum(lr, 0.001)
    return lr

    

def log_string(out_str):
    LOG_FOUT.write(out_str+'\n')
    LOG_FOUT.flush()
    print(out_str)
    

#### train function (version 2)####
def train():
    with tf.Graph().as_default():
        with tf.device('/gpu:'+str(GPU_INDEX)): 
            #is_training_pl = tf.placeholder(tf.bool, shape=(BATCH_SIZE))
            #print(is_training_pl)  
            batch = tf.Variable(0)
            
            if FLAGS.model == 'RTNet':      
                data1_pl, label1_pl = MODEL.input_placeholder(BATCH_SIZE, TIME_STEPS, RISK_FEATURES)                
                data2_pl, label2_pl = MODEL.input_placeholder(BATCH_SIZE, TIME_STEPS, FEATURES)
                # Get model
                pred1, pred2 = MODEL.create_model(data1_pl, data2_pl)
                
            elif FLAGS.model == 'CTNet':
                data_pl, label1_pl = MODEL.input_placeholder(BATCH_SIZE, TIME_STEPS, FEATURES)                
                data_pl, label2_pl = MODEL.input_placeholder(BATCH_SIZE, TIME_STEPS, FEATURES)                
                # Get model
                pred1, pred2 = MODEL.create_model(data_pl)
            else:
                print("Neither RTNet or CTNet couldn't be processed!!")
                
            # Get loss
            loss, loss1, loss2= MODEL.loss_def(pred1, pred2, label1_pl, label2_pl)
            tf.summary.scalar('loss1', loss1)
            tf.summary.scalar('loss2', loss2)
            tf.summary.scalar('total_loss', loss)
            
            # Multi-output calculation
            #####
            #correct_1 = pred1, tf.to_int64(label1_pl).............
            correct_2 = tf.equal(tf.argmax(pred2, 1), tf.to_int64(label2_pl))
           
            accuracy = tf.reduce_sum(tf.cast(correct, tf.float32)) / float(BATCH_SIZE)
            tf.summary.scalar('accuracy', accuracy)            
            
            
            
# next_time_pred pkgs
old_target=df[['target']]
df=df.drop(['target'],axis=1)


# Number of training samples.
sample_count = len(train_sample)
epochs = max_epoch

# Number of warmup epochs.
warmup_epoch = int(0.2*max_epoch)

# Base learning rate after warmup.
learning_rate_base = 0.001

total_steps = int(epochs * sample_count / batch_size)

# Compute the number of warmup batches.
warmup_steps = int(warmup_epoch * sample_count / batch_size)

warm_up_lr = tf_util.WarmUpCosineDecayScheduler(learning_rate_base=learning_rate_base,
                                        total_steps=total_steps,
                                        warmup_learning_rate=0.0,
                                        warmup_steps=warmup_steps,
                                        hold_base_rate_steps=0)

#### train function (version 1)####
# build training model and save
def train():
    with tf.Graph().as_default():
        i=0
        
        if MODEL == "RTNet":
            0000
        elif MODEL == "CTNet":
            0000
        else:
            "Error: Neither RTNet nor CTNet"
        
        clf=create_model()
        clf.summary()
        history=clf.fit(np.asarray(train_cb),[np.asarray(train_reg),np.asarray(train_lbl)],epochs=max_epoch,batch_size=batch_size,callbacks=[callback], validation_data=(np.asarray(val_cb),[np.asarray(val_reg),np.asarray(val_lbl)])) 
        clf.save("ensemble_2SA_eval1_%s_combinemodel_v2_0to10_loss_weight_1of5.h5" % i)
        #for i in range(num_data)
        
if __name__ == "__main__":
    train()
    LOG_FOUT.close()
