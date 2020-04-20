import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import norm
import re
from config import *
import ssd

##class PDF
class PDF:
    def __init__(self, sample_dist, mu=None, sigma=None, delay=None, pdf=None, decimal_place= None):
        if delay is not None and pdf is not None:
            self.delay = delay
            self.pdf = pdf
            self.sample_dist = sample_dist
            self.decimal_place = decimal_place
        else:
            if mu is None or sigma is None:
                print('invalid input')
            else:
                self.sample_dist = sample_dist
                self.decimal_place = self.decimal_place_generator()
                self.delay, self.pdf = self.NORM(mu, sigma, sample_dist)
                self.data_shrink()
                # plt.figure()
                # plt.plot(self.delay, self.pdf)
                # plt.show()

    #Generating the PDF function by the given mu  sigma and size
    def NORM(self, mu, sigma, sample_dist):
        # range = (mu + 4 * sigma)*2
        range_delay = (3 * sigma)*2
        size = (range_delay/sample_dist)+1
        k = (size - 1) * sample_dist / 2
        # print(k)
        x = np.arange(mu - k, mu + k, sample_dist)
        x = np.around(x, decimals=self.decimal_place)
        # px = norm.pdf(x, loc=mu, scale=sigma)
        px = self.n_pdf(x, mu, sigma)
        # px = px / sum(px)
        size_px= len(px)
        area = 0
        for i in range(size_px):
            area = area + px[i]*self.sample_dist
        print(area)
        return x, px

    def n_pdf(self, x, mean, std):
        p = (1 / (std * np.sqrt(2 * np.pi)) * np.exp(- (x - mean) ** 2 / (2 * std ** 2))) #*self.sample_dist
        return p

    def decimal_place_generator(self):
        c = 0
        sd = self.sample_dist
        while (sd < 1):
            sd *= 10
            c += 1
        return c

    def mu(self):
        return np.mean(self.delay)

    def std(self):
        return np.std(self.delay)

    def SUM(self, PDF2):
        # Step1 : create numpy.array of the SUM result by defining the boundary of its possible values
        min_of_sum = round(self.delay.min(), self.decimal_place) + round(PDF2.delay.min(), self.decimal_place) # minimum boundary of SUM
        max_of_sum = round(self.delay.max(), self.decimal_place) + round(PDF2.delay.max(), self.decimal_place) # maximum boundary of SUM
        size = int((max_of_sum - min_of_sum) / sample_dist) + 2     #the size of SUM +1
        #Initializing delay and pdf numpy.array
        sum_delay = np.around(np.linspace(min_of_sum, max_of_sum, size, endpoint=True), decimals=self.decimal_place)
        # mu_sum = self.mu() + PDF2.mu()
        # sigma_sum = np.sqrt((self.std())**2 + (PDF2.std())**2)
        # sum_pdf = (1 / (sigma_sum * np.sqrt(2 * np.pi)) * np.exp(- (sum_delay - mu_sum) ** 2 / (2 * sigma_sum ** 2)))
        
        sum_pdf = np.zeros(size)

        # Step2: concatenate 0s into 2 Inputs to make them size equal to (size1+size2)

        p1_delay = np.concatenate((self.delay, np.zeros(len(PDF2.pdf))))
        # p1_range1 = np.arange(min(self.delay.min(),PDF2.delay.min()),self.delay.min(),sample_dist)
        # p1_range2 = np.arange(self.delay.max()+sample_dist,max(self.delay.max(),PDF2.delay.max())+sample_dist,sample_dist)
        # p1_pdf = np.concatenate((np.zeros(len(p1_range1)), self.pdf, np.zeros(len(p1_range2))))
        # print(self.delay,p1_range1,p1_range2)
        p1_pdf = np.concatenate((self.pdf, np.zeros(len(PDF2.pdf))))
        p2_delay = np.concatenate((PDF2.delay, np.zeros(len(self.pdf))))
        # p2_range1 = np.arange(min(self.delay.min(),PDF2.delay.min()),PDF2.delay.min(),sample_dist)
        # p2_range2 = np.arange(PDF2.delay.max()+sample_dist,max(self.delay.max(),PDF2.delay.max())+sample_dist,sample_dist)
        # p2_pdf = np.concatenate((np.zeros(len(p2_range1)), PDF2.pdf, np.zeros(len(p2_range2))))
        # print(PDF2.delay,p2_range1,p2_range2)
        p2_pdf = np.concatenate((PDF2.pdf, np.zeros(len(self.pdf))))
        # print(len(p1_pdf),len(p2_pdf))
        # range_delay = np.arange(min(self.delay.min(),PDF2.delay.min()),max(self.delay.max(),PDF2.delay.max())+sample_dist,sample_dist)
        # Step3: do pointers moving
        #when p = 0, the head of the second input is alighed with the tail of the first input
        for p in range(len(sum_delay)): #the second input moves p sample_dist
            # these 2 pointers is used for calculation of probability
            p1_pointer = 0
            p2_pointer = p
            while (p2_pointer >= 0):
                sum = p1_delay[p1_pointer] + p2_delay[p2_pointer]
                # sum = range_delay[p1_pointer] + range_delay[p2_pointer]
                if sum >= min_of_sum:
                    idx = int(round((sum - min_of_sum) / self.sample_dist, self.decimal_place))#find the index of that value of SUM
                    pdf_1 = (p1_pdf[p1_pointer])#*sample_dist)
                    pdf_2 = (p2_pdf[p2_pointer])#*sample_dist)
                    sum_pdf[idx] = (pdf_1*pdf_2) + sum_pdf[idx]
                p2_pointer -= 1 # when this pointer go from p to 0, all overlapped parts are calculated
                p1_pointer += 1

        #finding area under curve after sum.
        area = 0
        for i in range(len(sum_delay)):
            area = area + sum_pdf[i]*self.sample_dist
        print(area)
        sum_pdf = sum_pdf/area
        #Return the result as PDF Obj
        
        R1 = PDF(sample_dist = self.sample_dist, delay = sum_delay, pdf = sum_pdf, decimal_place= self.decimal_place)
        R1.data_shrink()
        plt.figure()
        plt.plot(R1.delay, R1.pdf)
        plt.show()
        return R1
    
    def __add__(self,PDF2): ###'+' operator overloading
        return self.SUM(PDF2)
    
    def MAX(self, PDF2):
        #Step1: find important parameters first
        p1_min = round(self.delay.min(), self.decimal_place)
        p1_max = round(self.delay.max(), self.decimal_place)
        p2_min = round(PDF2.delay.min(), self.decimal_place)
        p2_max = round(PDF2.delay.max(), self.decimal_place)

        #Prevent access to nonexistent value
        p1_delay = np.concatenate((self.delay, np.zeros(len(PDF2.pdf))))
        p1_pdf = np.concatenate((self.pdf, np.zeros(len(PDF2.pdf))))
        p2_delay = np.concatenate((PDF2.delay, np.zeros(len(self.pdf))))
        p2_pdf = np.concatenate((PDF2.pdf, np.zeros(len(self.pdf))))

        #Step2: create numpy.array of the MAX result by defining the boundary of its possible values
        min_of_max = round(max(p1_min, p2_min), self.decimal_place)
        max_of_max = round(max(p1_max, p2_max), self.decimal_place)
        size = int(round((max_of_max-min_of_max), self.decimal_place) / sample_dist) +2
        #Initializing the numpy array
        max_delay = np.around(np.linspace(min_of_max, max_of_max, size, endpoint=True), decimals=self.decimal_place)
        max_pdf = np.zeros(size)

        #See every possible value in MAX output
        for p in range(size):
            #Check PDF2 first, so that we just have to ensure that the value exist in p1, otherwwise it is 0.
            if max_delay[p] <= p1_max:
                idx1 = int(round((max_delay[p] - p1_min)/sample_dist, self.decimal_place))
                # find indices of all values in p1 that its value is smaller than max value
                idx2_list = np.where((p2_delay <= max_delay[p]))[0]   #include the same value
                sum = 0
                for idx in idx2_list:
                    sum = sum + (p2_pdf[idx]*sample_dist)
                max_pdf[p] = max_pdf[p] + p1_pdf[idx1] * sum
            # Check PDF1, we just have to ensure that the value exist in p1, otherwwise it is 0.
            if max_delay[p] <= p2_max:
                idx2 = int(round((max_delay[p] - p2_min), self.decimal_place) / sample_dist)
                #find indices of all values in p1 that its value is smaller than max value
                idx1_list = np.where((p1_delay < max_delay[p]))[0]    #exclude the same value
                sum = 0
                for idx in idx1_list:
                    sum = sum + (p1_pdf[idx]*sample_dist)
                max_pdf[p] = max_pdf[p] + p2_pdf[idx2] * sum
        area = 0
        for i in range(len(max_pdf)):
            area = area + max_pdf[i]*self.sample_dist
        print(area)
        R1 = PDF(sample_dist=self.sample_dist, delay=max_delay, pdf=max_pdf, decimal_place=self.decimal_place)
        R1.data_shrink()
        return R1

    def data_shrink(self):
        for p in self.pdf:
            if p < P_tolerance:
                self.delay = np.delete(self.delay, np.where(self.pdf == p))
                self.pdf = np.delete(self.pdf, np.where(self.pdf == p))
        # self.pdf = self.pdf / np.sum(self.pdf)

    def plot(self, color='tan'):
        plt.figure()
        sns.lineplot(self.delay, self.pdf, color=color)
        #plt.show()

#try:
    #sns.set(color_codes=True, style="white")
    # settings for seaborn plot sizes
    #sns.set(rc={'figure.figsize': (5, 5)})
    #sstalib = read_sstalib('tech10nm.sstalib')

    #PDF1 = PDF_generator(sstalib, 'TEST', sample_dist)
    #print(PDF1.std())
    #PDF2 = PDF_generator(sstalib, 'TEST1', sample_dist)
    #PDF1.plot()
    #print(len(PDF1.delay))
    #PDF1.data_shrink()
    #print(len(PDF1.delay))
    #M1 = PDF1.MAX(PDF2)
    #M1.plot()
    #print(len(M1.delay))
    #print(np.sum(M1.pdf))

    #S1 = PDF1.SUM(PDF2)
    #S1.plot()
    #python3 ckt_sim.py tech10nm.sstalib c6288.ckt658
    #plt.show()

#except IOError:
    #print("error in the code")
