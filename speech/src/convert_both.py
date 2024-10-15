import numpy as np
import pysptk as sptk
import pyworld as pw
from scipy.io import wavfile
from train import *

import os

fs = 16000
fftlen = 512
alpha = 0.42
dim = 25
n_units = 128

model = VCDNN(dim,n_units)
_ = model.load_state_dict(torch.load("model/vcmodel.model"))

# Calculating mean/std of log_F0
datalist = []
with open("conf/train.list", "r") as f:
    for line in f:
        line = line.rstrip()
        datalist.append(line)

src_lf0 = None
tgt_lf0 = None
for i in range(0, len(datalist)):
    with open("data/SF/f0/{}.f0".format(datalist[i]), "rb") as f:
        f0 = np.fromfile(f, dtype="<f8", sep="")
    lf0 = np.log2(f0[f0 > 0.0])
    if src_lf0 is None:
        src_lf0 = lf0
    else:
        src_lf0 = np.concatenate([src_lf0, lf0])

    with open("data/TF/f0/{}.f0".format(datalist[i]), "rb") as f:
        f0 = np.fromfile(f, dtype="<f8", sep="")
    lf0 = np.log2(f0[f0 > 0.0])
    if tgt_lf0 is None:
        tgt_lf0 = lf0
    else:
        tgt_lf0 = np.concatenate([tgt_lf0, lf0])

src_lf0_mean = src_lf0.mean(axis=0)
src_lf0_std = src_lf0.std(axis=0)
tgt_lf0_mean = tgt_lf0.mean(axis=0)
tgt_lf0_std = tgt_lf0.std(axis=0)

# linear transformation of log F0
datalist = []
with open("conf/eval.list", "r") as f:
    for line in f:
        line = line.rstrip()
        datalist.append(line)

if not os.path.exists("data/SF-TF/f0"):
    os.mkdir("data/SF-TF/f0")

for i in range(0, len(datalist)):
    with open("data/SF/f0/{}.f0".format(datalist[i]), "rb") as f:
        f0 = np.fromfile(f, dtype="<f8", sep="")
        f0[f0 > 0.0] = np.power(2, (np.log2(f0[f0 > 0.0]) - src_lf0_mean) * tgt_lf0_std / src_lf0_std + tgt_lf0_mean)  # F0 = 0 は基本周波数が定義されていないことを意味する
    with open("data/SF-TF/f0/{}.f0".format(datalist[i]), "wb") as f:
        f0.tofile(f)
x = []
datalist = []
with open("conf/eval.list", "r") as f:
    for line in f:
        line = line.rstrip()
        datalist.append(line)

for d in datalist:
    with open("data/SF/mgc/{}.mgc".format(d),"rb") as f:
        dat = np.fromfile(f,dtype="<f8",sep="")
        x.append(dat.reshape(len(dat)//dim,dim))
print(datalist)
for i in range(0,len(datalist)):
    outfile = "result/wav/{}_f0_both.wav".format(datalist[i])
    with open("data/SF-TF/f0/{}.f0".format(datalist[i]),"rb") as f:
        f0 = np.fromfile(f, dtype="<f8", sep="")
    with open("data/SF/ap/{}.ap".format(datalist[i]),"rb") as f:
        ap = np.fromfile(f, dtype="<f8", sep="")
        ap = ap.reshape(len(ap)//(fftlen+1),fftlen+1)
    y = model.get_predata(x[i])
    y = y.astype(np.float64)
    sp = sptk.mc2sp(y, alpha, fftlen*2)
    owav = pw.synthesize(f0, sp, ap, fs)
    owav = np.clip(owav, -32768, 32767)
    wavfile.write(outfile, fs, owav.astype(np.int16))
print("DONE BOTH")
