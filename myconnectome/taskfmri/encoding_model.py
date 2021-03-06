"""
do encoding model across sessions
"""

import os,glob,sys,ctypes
import nibabel.gifti.giftiio
import numpy
import sklearn.linear_model
from myconnectome.utils.array_to_gifti import array_to_gifti_32k

basedir = os.environ['MYCONNECTOME_DIR']
datadir='/corral-repl/utexas/poldracklab/data/selftracking'

def get_codes():
    f=open('contrast_annotation.txt')
    header=f.readline().strip().split('\t')
    nvars=len(header)-3

    coding={}

    lines=f.readlines()
    for l in lines:
        l_s=l.strip().split('\t')
        tasknum=int(l_s[0])
        contrastnum=int(l_s[1])
        taskname=l_s[2]
        codes=[]
        for i in range(nvars):
            try:
                codes.append(int(l_s[i+3]))
            except:
                codes.append(0)
        if not coding.has_key(tasknum):
            coding[tasknum]={}
        coding[tasknum][contrastnum]=codes
    return coding,header[3:]

def get_files(coding,datadir):

    files=[]
    taskcodes=[]
    for t in coding.keys():
        for c in coding[t].keys():
            
            tcfiles=glob.glob(os.path.join(datadir,'sub*/model/model%03d/task%03d*333.feat/stats_pipeline/zstat%03d.R.smoothed.func.gii'%(t,t,c)))

            for f in tcfiles:
                files.append(f)
                taskcodes.append([t,c])
    return files,taskcodes

def load_data(files):
    contrastdata=numpy.zeros((len(files),32492*2))

    for i in range(len(files)):
        f=files[i]
        rh=nibabel.gifti.giftiio.read(f).darrays[0].data
        lh=nibabel.gifti.giftiio.read(f.replace('.R.','.L.')).darrays[0].data
        contrastdata[i,:]=numpy.hstack((lh,rh))
    return contrastdata                      


def get_design_matrix(coding,taskcodes):
    desmtx=[]
    for t in taskcodes:
        desmtx.append(coding[t[0]][t[1]])
    desmtx=numpy.array(desmtx)
    return desmtx

if __name__=="__main__":
 
    coding,names=get_codes()

    files,taskcodes=get_files(coding,datadir)

    contrastdata=load_data(files)

    desmtx=get_design_matrix(coding,taskcodes)
    desmtx=desmtx-numpy.mean(desmtx,0)
    df = desmtx.shape[0] - desmtx.shape[1]

    tstat_lasso=numpy.zeros((desmtx.shape[1],32492*2))
    tstat=numpy.zeros((desmtx.shape[1],32492*2))

    badctr=0
    lm=sklearn.linear_model.LinearRegression()
    lr=sklearn.linear_model.Lasso(alpha=0.01)
    ctr=0
    ctr2=0
    for i in range(contrastdata.shape[1]):
        if ctr==100:
            ctr=0
            ctr2+=1
            print ctr2
        else:
            ctr+=1
            ctr2+=1
        y=contrastdata[:,i]-numpy.mean(contrastdata[:,i])
        lr.fit(desmtx,y)
        resid=y-desmtx.dot(lr.coef_)
        sse=numpy.dot(resid,resid)/float(df)
        tstat_lasso[:,i]=lr.coef_/sse

        lm.fit(desmtx,y)
        resid=y-desmtx.dot(lm.coef_)
        sse=numpy.dot(resid,resid)/float(df)
        tstat[:,i]=lm.coef_/sse

    
    tstat[numpy.isnan(tstat)]=0
    tstat_lasso[numpy.isnan(tstat_lasso)]=0
    
    
    numpy.save(os.path.join(basedir,'task/encoding_tstat_lasso.npy'),tstat_lasso)
    numpy.save(os.path.join(basedir,'task/encoding_tstat.npy'),tstat)

    
    array_to_gifti_32k(tstat_lasso,os.path.join(basedir,'task/encoding_tstat_lasso'),names)

    array_to_gifti_32k(tstat,os.path.join(basedir,'task/encoding_tstat'),names)
    
    
