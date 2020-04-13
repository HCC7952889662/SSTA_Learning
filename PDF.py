import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import norm
import re
from config import *

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

    #Generating the PDF function by the given mu  sigma and size
    def NORM(self, mu, sigma, sample_dist):
        range = (mu + 4 * sigma) * 2
        size = (range / sample_dist)
        k = (size) * sample_dist / 2
        x = np.around(np.arange(mu - k, mu + k, sample_dist), decimals=self.decimal_place)
        p = self.n_pdf(x, mu, sigma)
        return x, p

    def n_pdf(self, x, mean, std):
        p = (1 / (std * np.sqrt(2 * np.pi)) * np.exp(- (x - mean) ** 2 / (2 * std ** 2)))*self.sample_dist
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
        # Step0: find important parameters first
        p1_min = round(self.delay.min(), self.decimal_place)
        p1_max = round(self.delay.max(), self.decimal_place)
        p2_min = round(PDF2.delay.min(), self.decimal_place)
        p2_max = round(PDF2.delay.max(), self.decimal_place)

        # Step1 : create numpy.array of the SUM result by defining the boundary of its possible value
        min_of_sum = round(p1_min + p2_min, self.decimal_place)  # minimum boundary of SUM
        max_of_sum = round(p1_max + p2_max, self.decimal_place)  # maximum boundary of SUM
        size = int((max_of_sum - min_of_sum) / sample_dist) + 1  # the size of SUM +1
        # Initializing delay and pdf numpy.array
        sum_delay = np.around(np.linspace(min_of_sum, max_of_sum, size, endpoint=True), decimals=self.decimal_place)
        sum_pdf = np.zeros(size)

        # Step2: concatenate 0s into 2 Inputs to make them size equal to (size1+size2)
        p1_delay = np.concatenate((self.delay, np.zeros(len(PDF2.pdf))))
        p1_pdf = np.concatenate((self.pdf, np.zeros(len(PDF2.pdf))))
        p2_delay = np.concatenate((PDF2.delay, np.zeros(len(self.pdf))))
        p2_pdf = np.concatenate((PDF2.pdf, np.zeros(len(self.pdf))))

        # Step3: do pointers moving
        # when p = 0, the head of the second input is alighed with the tail of the first input
        for p in range(len(sum_delay)):  # the second input moves p sample_dist
            # these 2 pointers is used for calculation of probability
            p1_pointer = 0
            p2_pointer = p
            while (p2_pointer >= 0):
                sum_pdf[p] = p1_pdf[p1_pointer] * p2_pdf[p2_pointer] + sum_pdf[p]
                p2_pointer -= 1  # when this pointer go from p to 0, all overlapped parts are calculated
                p1_pointer += 1

        # Return the result as PDF Obj
        R1 = PDF(sample_dist=self.sample_dist, delay=sum_delay, pdf=sum_pdf, decimal_place=self.decimal_place)
        R1.data_shrink()
        #R1.pdf = R1.pdf / np.sum(R1.pdf)
        return R1
    
    def __add__(self,PDF2): ###'+' operator overloading
        return self.SUM(PDF2)
    
    def MAX(self, PDF2):
        # Step1: find important parameters first
        # print(self.delay)
        p1_min = round(self.delay.min(), self.decimal_place)
        p1_max = round(self.delay.max(), self.decimal_place)
        p2_min = round(PDF2.delay.min(), self.decimal_place)
        p2_max = round(PDF2.delay.max(), self.decimal_place)

        # Prevent access to nonexistent value
        p1_delay = self.delay
        p1_pdf = self.pdf
        p2_delay = PDF2.delay
        p2_pdf = PDF2.pdf

        # print(p1_delay)
        # print(p1_pdf)
        # print(p2_delay)
        # print(p2_pdf)

        # Step2: create numpy.array of the MAX result by defining the boundary of its possible values
        min_of_max = round(max(p1_min, p2_min), self.decimal_place)
        max_of_max = round(max(p1_max, p2_max), self.decimal_place)
        size = int(round((max_of_max - min_of_max), self.decimal_place) / sample_dist) + 1
        # Initializing the numpy array
        max_delay = np.around(np.linspace(min_of_max, max_of_max, size, endpoint=True), decimals=self.decimal_place)
        max_pdf = np.zeros(size)

        p1_pointer = 0
        p2_pointer = 0

        # See every possible value in MAX output
        for p in range(size):
            # print(str(max_delay[p])+' ###############################' )
            # Check PDF2 first, so that we just have to ensure that the value exist in p1, otherwwise it is 0.
            if max_delay[p] <= p1_max:
                while max_delay[p] > p1_delay[p1_pointer]:
                    p1_pointer += 1
                    if p1_delay[p1_pointer] == p1_max:
                        break

                # print(p1_pointer)
                # find indices of all values in p1 that its value is smaller than max value
                idx2_list = np.where((p2_delay <= max_delay[p]))[0]  # include the same value
                # print(p2_delay[idx2_list])
                for idx in idx2_list:
                    max_pdf[p] = max_pdf[p] + p2_pdf[idx] * p1_pdf[p1_pointer]
            # Check PDF1, we just have to ensure that the value exist in p1, otherwise it is 0.
            if max_delay[p] <= p2_max:
                while max_delay[p] > p2_delay[p2_pointer]:
                    p2_pointer += 1
                    if p2_delay[p2_pointer] == p2_max:
                        break
                # print(p2_pointer)
                # find indices of all values in p1 that its value is smaller than max value
                idx1_list = np.where((p1_delay < max_delay[p]))[0]  # exclude the same value
                # print(p1_delay[idx1_list])
                for idx in idx1_list:
                    max_pdf[p] = max_pdf[p] + p1_pdf[idx] * p2_pdf[p2_pointer]
            # print('###############################')
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
