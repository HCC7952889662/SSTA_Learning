from PDF import *
from ckt_sim import PDF_generator,read_sstalib
import math
import sys


try:
    gate_type=sys.argv[2]
    rows=2
    cols=3
    sstalib = read_sstalib(sys.argv[1])
    plt.figure()
    plt.subplot2grid((rows,cols),(0,0),colspan=3)

    ip1 = PDF_generator(sstalib,'IPT',sample_dist)
    plt.subplot2grid((rows,cols),(0,0))
    plt.title("plot for ip1, mean=%s ,std=%s"%((sstalib['IPT'])['mu'],(sstalib['IPT'])['sigma']))
    plt.xlabel('Delay(ns)')
    plt.ylabel('Probability')
    sns.lineplot(ip1.delay, ip1.pdf, color='black')
    

    ip2 = PDF_generator(sstalib,'IPT',sample_dist)
    plt.subplot2grid((rows,cols),(0,1))
    plt.title("plot for ip2, mean=%s ,std=%s"%((sstalib['IPT'])['mu'],(sstalib['IPT'])['sigma']))
    plt.xlabel('Delay(ns)')
    plt.ylabel('Probability')
    sns.lineplot(ip2.delay, ip2.pdf, color='black')

    g1 = PDF_generator(sstalib,gate_type,sample_dist)
    plt.subplot2grid((rows,cols),(0,2))
    plt.title("plot for gate(%s), mean=%s ,std=%s"%(gate_type,(sstalib[gate_type])['mu'],(sstalib[gate_type])['sigma']))
    plt.xlabel('Delay(ns)')
    plt.ylabel('Probability')
    sns.lineplot(g1.delay, g1.pdf, color='black')
    
    moi=ip1.MAX(ip2)
    som = moi.SUM(g1)
    plt.subplot2grid((rows,cols),(1,0),colspan=3)
    plt.title("plot for Sum of Max")
    plt.xlabel('Delay(ns)')
    plt.ylabel('Probability')
    sns.lineplot(som.delay, som.pdf, color='black', label="Sum of Max")

    # soi_1 = ip1.SUM(g1)
    # soi_2 = ip2.SUM(g1)
    # mos = soi_1.MAX(soi_2)
    # # plt.subplot2grid((3,3),(1,0),colspan=3)
    # # plt.title("plot for Max of Sum")
    # # plt.xlabel('Delay(ns)')
    # # plt.ylabel('Probability')
    # sns.lineplot(mos.delay, mos.pdf, color='red', label="Max of Sum")

    plt.subplots_adjust(wspace=0.5,hspace=0.7)
    plt.legend(loc="upper left")
    plt.autoscale()
    plt.show()
    print("simulation ends.")
except IOError:
    print("error in the code")
