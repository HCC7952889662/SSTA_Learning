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
##class PDF
class PDF:
    def __init__(self, dict, gate, size, f):
        # Using DataFrame to create an PDF obj instead of considering GateType
        if dict is None and f is not None:
            #print('Dictionary is not complete')
            self.data = f
        # Create an PDF obj by referring to SSTALIB
        else:
            if dict[gate]['form'] is None:
                print("Format is not available now")
            else:
                self.data = self.NORM(dict[gate]["mu"], dict[gate]["sigma"], size)

    def NORM(self, mu, sigma, size):
        x = sigma * np.random.randn(size) + mu
        x = np.around(x, decimals=2)
        cx = scipy.stats.norm.cdf(x, loc=mu, scale=sigma)
        px = scipy.stats.norm.pdf(x, loc=mu, scale=sigma)
        px = px / sum(px)  ################################################################
        f = pd.DataFrame({'Data': x, 'PDF': px, 'CDF': cx})
        #print(sum(px))
        return f
        # overload the SUM (+) or max operations
    
    def SUM(self,p1):
        P = []
        M = []
        for i in range(p1.data['Data'].size):
            for j in range(self.data['Data'].size):
                value = p1.data['Data'][i]+self.data['Data'][j]
                if (value) not in M:
                    M.append(value)
                    P.append(p1.data['PDF'][i]*self.data['PDF'][j])
                else:
                    P[M.index(value)] = P[M.index(value)] + p1.data['PDF'][i]*self.data['PDF'][j]
        f = pd.DataFrame({'Data': M, 'PDF': P})
        return PDF_generator_intermediate(f)
    
    def MAX(self,p1):
        P = []
        M = []
        for i in range(p1.data['Data'].size):
            P_temp = 0
            for j in range(self.data['Data'].size):
                if (p1.data['Data'][i] >= self.data['Data'][j]):
                    P_temp = P_temp + p1.data['PDF'][i]*self.data['PDF'][j]
            if p1.data['Data'][i] not in M:
                M.append(p1.data['Data'][i])
                P.append(P_temp)
            else:
                P[M.index(p1.data['Data'][i])] = P[M.index(p1.data['Data'][i])] + P_temp

        for i in range(self.data['Data'].size):
            P_temp = 0
            for j in range(p1.data['Data'].size):
                if (self.data['Data'][i] > p1.data['Data'][j]):
                    P_temp = P_temp + self.data['PDF'][i]*p1.data['PDF'][j]
            if self.data['Data'][i] not in M:
                M.append(self.data['Data'][i])
                P.append(P_temp)
            else:
                P[M.index(self.data['Data'][i])] = P[M.index(self.data['Data'][i])] + P_temp
        f = pd.DataFrame({'Data': M, 'PDF': P})
        return PDF_generator_intermediate(f)

    def sum_probability(self):
        sum = 0.0
        for p in self.data['PDF']:
            sum = sum + p
        return sum

    #After this function, the data will be divide by N
    def data_shrink_core(self, N):
        k = 0
        P = []
        D = []
        div, mod = divmod(len(self.data), N)
        while k < div:
            a = self.data.iloc[[N*k, N*(k+1)-1], :].mean()
            P.append(a['PDF'] * N)
            D.append(a['Data'])
            k += 1
        if mod != 0:
            a = p3.data.iloc[[N*div, (N*div+mod-1)], :].mean()
            P.append(a['PDF'] * mod)
            D.append(a['Data'])
        self.data = pd.DataFrame({'Data': D, 'PDF': P})

    def data_shrink_mode(self,N,mode='fast'):
        if mode == 'fast':
            self.data_shrink_core(N)
        elif mode == 'precise': # N must be power of 2
            while N > 1:
                N, mod = divmod(N, 2)
                self.data_shrink_core(2)

    def plot(self):
        plt.figure()
        sns.scatterplot(self.data['Data'], self.data['PDF'], color="tan")
        #plt.show()

    def MAX_of_SUM(self,p2,pc):
        ps1 = self.SUM(pc)
        ps2 = p2.SUM(pc)
        pms = ps1.MAX(ps2)
        return pms

    def SUM_of_MAX(self,p2,pc):
        pm1 = self.MAX(pc)
        pm2 = p2.MAX(pc)
        psm = pm1.SUM(pm2)
        return psm

    def Result_plot(self,psm, pms):
        plt.figure()
        plt.subplot2grid((1,2), (0, 0), colspan=2)
        #######Start to plot
        SMP = plt.subplot2grid((1, 2), (0, 0))
        SMP.title.set_text('MAX_of_SUM')
        sns.scatterplot(psm.data['Data'], psm.data['PDF'], color="tan")

        MSP = plt.subplot2grid((1, 2), (0, 1))
        MSP.title.set_text('SUM_of_MAX')
        sns.scatterplot(pms.data['Data'], pms.data['PDF'], color="teal")

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
    p1 = PDF(dict = sstalib, gate = gate, size = size, f=None)
    return p1

def PDF_generator_intermediate(f):
    p1 = PDF(dict = None, gate = None, size = None, f = f)
    return p1

try:
    sstalib = read_sstalib("tech10nm.sstalib")
    p1 = PDF_generator(sstalib,'AND',50)
    #p1.plot()
    
    p2 = PDF_generator(sstalib, 'OR', 50)
    p7 = PDF_generator(sstalib, 'NOR', 50)
    
    p3 = p1.SUM(p2)
    p3.plot()
    print('before '+ str(p3.sum_probability()))
    p3.data_shrink_mode(16, mode='fast')
    print('after ' + str(p3.sum_probability()))
    p3.plot()
    plt.show()

except IOError:
    print("error in the code")
