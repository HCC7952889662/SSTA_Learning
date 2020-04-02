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
sns.set(rc={'figure.figsize':(5,5)})

class PDF:
    def __init__(self, dict, gate, size):
        if dict is None:
            print('Dictionary is not complete')
        if dict[gate]['form'] is None:
            print("Format is not available now")
        else:
            self.data = self.NORM(dict[gate]["mu"], dict[gate]["sigma"], size)
            self.gate = gate

    def NORM(self, mu, sigma, size):
        x = sigma * np.random.randn(size) + mu
        x = np.around(x, decimals=2)
        cx = scipy.stats.norm.cdf(x, loc=mu, scale=sigma)
        px = scipy.stats.norm.pdf(x, loc=mu, scale=sigma)
        px = px / sum(px)  ################################################################
        f = pd.DataFrame({'Data': x, 'PDF': px, 'CDF': cx})
        print(sum(px))
        return f
        # overload the SUM (+) or max operations
    
    def SUM(self,f1):
        P = []
        M = []
        for i in range(f1['Data'].size):
            for j in range(self.data['Data'].size):
                value = f1['Data'][i]+self.data['Data'][j]
                if (value) not in M:
                    M.append(value)
                    P.append(f1['PDF'][i]*self.data['PDF'][j])
                else:
                    P[M.index(value)] = P[M.index(value)] + f1['PDF'][i]*self.data['PDF'][j]
        f = pd.DataFrame({'Data': M, 'PDF': P})
        return f
    
    def MAX(self,f1):
        P = []
        M = []
        for i in range(f1['Data'].size):
            P_temp = 0
            for j in range(f2['Data'].size):
                if (f1['Data'][i] >= self.data['Data'][j]):
                    P_temp = P_temp + f1['PDF'][i]*self.data['PDF'][j]
            if f1['Data'][i] not in M:
                M.append(f1['Data'][i])
                P.append(P_temp)
            else:
                P[M.index(f1['Data'][i])] = P[M.index(f1['Data'][i])] + P_temp

        for i in range(self.data['Data'].size):
            P_temp = 0
            for j in range(f1['Data'].size):
                if (self.data['Data'][i] > f1['Data'][j]):
                    P_temp = P_temp + self.data['PDF'][i]*f1['PDF'][j]
            if self.data['Data'][i] not in M:
                M.append(self.data['Data'][i])
                P.append(P_temp)
            else:
                P[M.index(self.data['Data'][i])] = P[M.index(f2['Data'][i])] + P_temp
        f = pd.DataFrame({'Data': M, 'PDF': P})
        return f

    def plot(self):
        plt.figure()
        sns.scatterplot(self.data['Data'], self.data['PDF'], color="tan")
        plt.show()

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
                    gate = line_syntax.group(1)
                    count+=1

                line_syntax = re.match(r'.*form = (.*)', line, re.IGNORECASE)
                if line_syntax:
                    form = line_syntax.group(1)
                    count += 1

                line_syntax = re.match(r'.*mu = (.*)', line, re.IGNORECASE)
                if line_syntax:
                    mu = float(line_syntax.group(1))
                    count += 1

                line_syntax = re.match(r'.*sigma = (.*)', line, re.IGNORECASE)
                if line_syntax:
                    sigma = float(line_syntax.group(1))
                    count += 1

                if count == 4:
                    sstalib[gate] = {'form': form, 'mu': mu, 'sigma': sigma}
                    count = 0
    # it should return an object of Dict
    #{'IPT': {'form': 'normal', 'mu': '2n', 'sigma': '0.5n'}, 'NOT': {'form': 'normal', 'mu': '4n', 'sigma': '0.5n'},
    # 'NAND': {'form': 'normal', 'mu': '6n', 'sigma': '0.8n'}, 'AND': {'form': 'normal', 'mu': '6.5n', 'sigma': '0.8n'},
    # 'NOR': {'form': 'normal', 'mu': '7n', 'sigma': '0.8n'}, 'OR': {'form': 'normal', 'mu': '7.5n', 'sigma': '0.8n'},
    # 'XOR': {'form': 'normal', 'mu': '12n', 'sigma': '1.5n'}, 'BUFF': {'form': 'normal', 'mu': '2.5n', 'sigma': '0.5n'}, 'XNOR': {'form': 'normal', 'mu': '12n', 'sigma': '1.5n'}}
    return sstalib

def PDF_generator(sstalib, gate,size):
    p1 = PDF(dict = sstalib, gate = gate, size = size)
    return p1


try:
    sstalib = read_sstalib("tech10nm.sstalib")
    p1 = PDF_generator(sstalib,'AND',50)
    p1.plot()
 

except IOError:
    print("error in the code")
