import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import norm
import re
sns.set(color_codes=True,style="white")
# settings for seaborn plot sizes
sns.set(rc={'figure.figsize':(5,5)})

##class PDF
class PDF:
    def __init__(self, sample_dist, mu=None, sigma=None, size= 101, delay=None, pdf=None, decimal_place= None):
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
                self.delay, self.pdf = self.NORM(mu, sigma, sample_dist, size)

    #Generating the PDF function by the given mu  sigma and size
    def NORM(self, mu, sigma, sample_dist, size):
        k = (size - 1) * sample_dist / 2
        # print(k)
        x = np.arange(mu - k, mu + k, sample_dist)
        x = np.around(x, decimals=self.decimal_place)
        px = norm.pdf(x, loc=mu, scale=sigma)
        px = px / sum(px)
        return x, px

    def decimal_place_generator(self):
        c = 0
        sd = self.sample_dist
        while (sd < 1):
            sd *= 10
            c += 1
        return c

    def SUM(self, PDF2):
        # Step1 : create numpy.array of the sum result and the size is from sum of min to sum of max
        # also initialize the sum
        min_of_sum = round(self.delay.min() + PDF2.delay.min(), self.decimal_place)
        max_of_sum = round(self.delay.max() + PDF2.delay.max(), self.decimal_place)
        size = int((max_of_sum - min_of_sum) / sample_dist) + 1
        sum_delay = np.around(np.linspace(min_of_sum, max_of_sum, size, endpoint=True), decimals=self.decimal_place)
        sum_pdf = np.zeros(size)

        # Step2: concatenate 0s into 2 numpy
        p1_delay = np.concatenate((self.delay, np.zeros(len(PDF2.pdf))))
        p1_pdf = np.concatenate((self.pdf, np.zeros(len(PDF2.pdf))))
        p2_delay = np.concatenate((PDF2.delay, np.zeros(len(self.pdf))))
        p2_pdf = np.concatenate((PDF2.pdf, np.zeros(len(self.pdf))))

        # Step3: do pointers moving
        for p in range(len(sum_delay)):
            p1_pointer = 0
            p2_pointer = p
            while (p2_pointer >= 0):
                sum = p1_delay[p1_pointer] + p2_delay[p2_pointer]
                if sum >= min_of_sum:
                    idx = int(round((sum - min_of_sum) / self.sample_dist, self.decimal_place))
                    sum_pdf[idx] = p1_pdf[p1_pointer] * p2_pdf[p2_pointer] + sum_pdf[idx]
                p2_pointer -= 1
                p1_pointer += 1

        R1 = PDF(sample_dist = self.sample_dist, delay = sum_delay, pdf = sum_pdf, decimal_place= self.decimal_place)
        return R1

    def MAX(self, PDF2):
        p1_min = round(self.delay.min(), 2)
        p1_max = round(self.delay.max(), 2)
        p2_min = round(PDF2.delay.min(), 2)
        p2_max = round(PDF2.delay.max(), 2)

        min_of_max = round(max(p1_min, p2_min), 2)
        max_of_max = round(max(p1_max, p2_max), 2)
        size = int((max_of_max - min_of_max) / sample_dist) + 1
        max_delay = np.around(np.linspace(min_of_max, max_of_max, size, endpoint=True), decimals=2)
        max_pdf = np.zeros(size)

        for p in range(size):
            if max_delay[p] <= p1_max:
                idx1 = int(round((max_delay[p] - p1_min) / sample_dist, 2))
                # looking for PDF2 first
                print(p1_max)
                idx2_list = np.where((PDF2.delay <= max_delay[p]))[0]
                print(idx2_list)
                sum = 0
                for idx in idx2_list:
                    sum = sum + PDF2.pdf[idx]
                max_pdf[p] = max_pdf[p] + self.pdf[idx1] * sum

            if max_delay[p] <= p2_max:
                idx2 = int(round((max_delay[p] - p2_min) / sample_dist, 2))
                idx1_list = np.where((self.delay < max_delay[p]))[0]
                sum = 0
                for idx in idx1_list:
                    sum = sum + self.pdf[idx]
                max_pdf[p] = max_pdf[p] + PDF2.pdf[idx2] * sum

        R1 = PDF(sample_dist=self.sample_dist, delay=max_delay, pdf=max_pdf, decimal_place=self.decimal_place)
        return R1

    def plot(self):
        plt.figure()
        sns.lineplot(self.delay, self.pdf, color="tan")
        #plt.show()

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
    #{'IPT': {'form': 'normal', 'mu': '2', 'sigma': '0.5'},  'NOT': {'form': 'normal', 'mu': '4', 'sigma': '0.5'},
    # 'NAND': {'form': 'normal', 'mu': '6', 'sigma': '0.8'}, 'AND': {'form': 'normal', 'mu': '6.5', 'sigma': '0.8'},
    # 'NOR': {'form': 'normal', 'mu': '7', 'sigma': '0.8'},  'OR': {'form': 'normal', 'mu': '7.5', 'sigma': '0.8'},
    # 'XOR': {'form': 'normal', 'mu': '12', 'sigma': '1.5'}, 'BUFF': {'form': 'normal', 'mu': '2.5', 'sigma': '0.5'},
    # 'XNOR': {'form': 'normal', 'mu': '12', 'sigma': '1.5'}}
    return sstalib

def PDF_generator(sstalib, gate, size, sample_dist):
    if size != None:
        p1 = PDF(sample_dist = sample_dist, mu = sstalib[gate]['mu'], sigma = sstalib[gate]['sigma'], size = size)
    else:
        p1 = PDF(sample_dist = sample_dist, mu=sstalib[gate]['mu'], sigma=sstalib[gate]['sigma'])
    return p1


try:
    sstalib = read_sstalib('tech10nm.sstalib')
    sample_dist = 0.01

    PDF1 = PDF_generator(sstalib, 'TEST', 201, sample_dist)
    PDF2 = PDF_generator(sstalib, 'TEST1', 201, sample_dist)


    M1 = PDF1.MAX(PDF2)
    M1.plot()

    S1 = PDF1.SUM(PDF2)
    S1.plot()

    plt.show()


except IOError:
    print("error in the code")
