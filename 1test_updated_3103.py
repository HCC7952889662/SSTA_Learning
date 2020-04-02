import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import random
import scipy
import seaborn as sns
from scipy import stats
import pdb
import re
sns.set(color_codes=True,style="white")
# settings for seaborn plot sizes
sns.set(rc={'figure.figsize':(10,10)})


def read_sstalib(filename):
    sstalib = {}
    infile = open(filename)
    count = 0
    #condition on cell form to how to read it.
    for line in infile:  
        if line != "":
            if re.match(r'^#', line):
                pass
            else:
                #print(line)
                line_syntax =  re.match(r'cell (.*):',line, re.IGNORECASE)
                if line_syntax:
                    print(line_syntax.group(1))
                    gate = line_syntax.group(1)
                    count+=1

                line_syntax = re.match(r'.*form = (.*)', line, re.IGNORECASE)
                if line_syntax:
                    print(line_syntax.group(1))
                    form = line_syntax.group(1)
                    count += 1

                line_syntax = re.match(r'.*mu = (.*)', line, re.IGNORECASE)
                if line_syntax:
                    print(line_syntax.group(1))
                    mu = line_syntax.group(1)
                    count += 1

                line_syntax = re.match(r'.*sigma = (.*)', line, re.IGNORECASE)
                if line_syntax:
                    print(line_syntax.group(1))
                    sigma = line_syntax.group(1)
                    count += 1

                if count == 4:
                    sstalib[gate] = {'form': form, 'mu': mu, 'sigma': sigma}
                    count = 0
    # it should return an object of Dict
        # it should return an object of Dict
    #{'IPT': {'form': 'normal', 'mu': '2n', 'sigma': '0.5n'}, 'NOT': {'form': 'normal', 'mu': '4n', 'sigma': '0.5n'}, 
    # 'NAND': {'form': 'normal', 'mu': '6n', 'sigma': '0.8n'}, 'AND': {'form': 'normal', 'mu': '6.5n', 'sigma': '0.8n'}, 
    # 'NOR': {'form': 'normal', 'mu': '7n', 'sigma': '0.8n'}, 'OR': {'form': 'normal', 'mu': '7.5n', 'sigma': '0.8n'}, 
    # 'XOR': {'form': 'normal', 'mu': '12n', 'sigma': '1.5n'}, 'BUFF': {'form': 'normal', 'mu': '2.5n', 'sigma': '0.5n'}, 'XNOR': {'form': 'normal', 'mu': '12n', 'sigma': '1.5n'}}
    return sstalib

#print(read_sstalib("tech10nm.sstalib"))

class PDF:

    def __init__(self, form=None, args):
        if form is None:
            print("Format is not available now")
        elif form == "norm":
            self.data = NORM(args["mu"], args["sigma"], args["size"])

        # overload the SUM (+) or max operations

def NORM(mu, sigma, size):
        x = sigma * np.random.randn(size) + mu
        x = np.around(x, decimals=2)
        cx = scipy.stats.norm.cdf(x, loc=mu, scale=sigma)
        px = scipy.stats.norm.pdf(x, loc=mu, scale=sigma)
        px = px/sum(px)################################################################
        f = pd.DataFrame({'Data': x, 'PDF': px, 'CDF': cx})
        print(sum(px))
        return f

class node:
    # def __init__(self,f1,f2,fc):
    #     self.f1=f1
    #     self.f2=f2
    #     self.fc=fc

    def SUM(self,f1,f2):
        P = []
        M = []
        for i in range(f1['Data'].size):
            for j in range(f2['Data'].size):
                value = f1['Data'][i]+f2['Data'][j]
                if (value) not in M:
                    M.append(value)
                    P.append(f1['PDF'][i]*f2['PDF'][j])
                else:
                    P[M.index(value)] = P[M.index(value)] + f1['PDF'][i]*f2['PDF'][j]
        f = pd.DataFrame({'Data': M, 'PDF': P})
        return f

    def MAX(self,f1,f2):
        P = []
        M = []
        for i in range(f1['Data'].size):
            P_temp = 0
            for j in range(f2['Data'].size):
                if (f1['Data'][i] >= f2['Data'][j]):
                    P_temp = P_temp + f1['PDF'][i]*f2['PDF'][j]
            if f1['Data'][i] not in M:
                M.append(f1['Data'][i])
                P.append(P_temp)
            else:
                P[M.index(f1['Data'][i])] = P[M.index(f1['Data'][i])] + P_temp

        for i in range(f2['Data'].size):
            P_temp = 0
            for j in range(f1['Data'].size):
                if (f2['Data'][i] > f1['Data'][j]):
                    P_temp = P_temp + f2['PDF'][i]*f1['PDF'][j]
            if f2['Data'][i] not in M:
                M.append(f2['Data'][i])
                P.append(P_temp)
            else:
                P[M.index(f2['Data'][i])] = P[M.index(f2['Data'][i])] + P_temp
        f = pd.DataFrame({'Data': M, 'PDF': P})
        return f

    def MAX_of_SUM(self,f1,f2,fc):
        fs1 = self.SUM(f1,fc)
        fs2 = self.SUM(f2,fc)
        fms = self.MAX(fs1,fs2)
        return fms

    def SUM_of_MAX(self,f1,f2,fc):
        fm1 = self.MAX(f1,fc)
        fm2 = self.MAX(f2,fc)
        fsm = self.SUM(fm1,fm2)
        return fsm


    def Result_plot(self,fsm, fms):
        plt.figure()
        plt.subplot2grid((1,2), (0, 0), colspan=2)
        #######Start to plot
        SMP = plt.subplot2grid((1, 2), (0, 0))
        SMP.title.set_text('MAX_of_SUM')
        sns.scatterplot(fsm['Data'], fsm['PDF'], color="tan")

        MSP = plt.subplot2grid((1, 2), (0, 1))
        MSP.title.set_text('SUM_of_MAX')
        sns.scatterplot(fms['Data'], fms['PDF'], color="teal")





try:
    read_sstalib("tech10nm.sstalib")
    mu1 = 0
    sigma1 = 1
    size1 = 20
    f1 = NORM(mu1, sigma1, size1)
    pdb.set_trace()
    mu2 = 5
    sigma2 = 1
    size2 = 20
    f2 = NORM(mu2, sigma2, size2)

    mu3 = 2
    sigma3 = 1
    size3 = 50
    fc = NORM(mu3, sigma3, size3)

    N = node()
    
    a = [2,3,4,5]
    pa = [0.25,0.25,0.25,0.25]
    b = [1,2,3,4,5]
    pb = [0.2,0.2,0.2,0.2,0.2]
    c = [6,7,8,1,2]
    pc = [0.2,0.2,0.2,0.2,0.2]
    f1 = pd.DataFrame({'Data': a, 'PDF': pa})
    f2 = pd.DataFrame({'Data': b, 'PDF': pb})
    fc = pd.DataFrame({'Data': c, 'PDF': pc})
    
    #fsum = SUM(f1,f2)
    #print(fsum['PDF'].sum())

    fsm = N.SUM_of_MAX(f1,f2,fc)
    print(fsm)
    print("finish SUM of MAX part")
    fms = N.MAX_of_SUM(f1,f2,fc)
    print(fms)
    print("mean of sum of max",np.mean(fsm['Data']))
    print("std of sum of max",np.std(fsm['Data']))
    print("mean of max of sum",np.mean(fms['Data']))
    print("std of max of sum",np.std(fms['Data']))
    m1=np.mean(fsm['Data'])
    m2=np.mean(fms['Data'])
    s1=np.std(fsm['Data'])
    s2=np.std(fms['Data'])
    t=(m1-m2)/np.sqrt(((s1**2)/len(fsm['Data']))+((s2**2)/len(fms['Data'])))
    print("value of t statistics:",t)
    t2, p2 = stats.ttest_ind(fsm['Data'],fms['Data'])
    print("t = " + str(t2))
    print("p = " + str(p2))
    N.Result_plot(fsm,fms)
    plt.show()


    fmax = MAX(f1,f2)
    print(fmax)
    sns.scatterplot(fmax['Data'],fms['PDF'], color = "green")
    plt.show()


except IOError:
    print("error in the code")
