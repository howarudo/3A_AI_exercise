import os
import sys
import glob

from scipy.io import wavfile # for wavfile I/O
import pyworld as pw
import numpy as np
import pysptk as sptk

spklist = ["SF", "TF"]  # speaker list [source female speaker, target female speaker]
featlist = ["mgc","f0","ap"]

# Making directories for speech features
for s in spklist:
    for f in featlist:
        if not os.path.exists("data/{}/{}".format(s,f)):
            os.mkdir("data/{}/{}".format(s,f))

for s in spklist:
    wavlist = os.listdir("data/{}/wav".format(s))
    for wf in wavlist:
        # WORLD analysis for each file
        print("speaker: {} file: {}".format(s,wf))
        fs, data = wavfile.read("data/{}/wav/{}".format(s,wf))
        data = data.astype(np.float64)

        f0, t = pw.harvest(data, fs)
        sp = pw.cheaptrick(data, f0, t, fs)
        ap = pw.d4c(data, f0, t, fs)

        alpha = 0.42
        dim = 24
        mgc = sptk.sp2mc(sp, dim, alpha)

        bn, _ = os.path.splitext(wf)

        with open("data/{}/mgc/{}.mgc".format(s,bn),"wb") as f:
            mgc.tofile(f)
        with open("data/{}/f0/{}.f0".format(s,bn),"wb") as f:
            f0.tofile(f)
        with open("data/{}/ap/{}.ap".format(s,bn),"wb") as f:
            ap.tofile(f)
