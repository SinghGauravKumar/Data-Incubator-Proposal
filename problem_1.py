import numpy as np
import pylab as pl
import random

def find_difference(T,N,sample_size):
    differences=[]
    for i in range(sample_size):
        temp_list=[random.randint(1,10) for i in range(T)]
        last_register=temp_list[-N:]
        max_register=np.sort(temp_list)[-N:]
        L=np.prod(last_register)
        M=np.prod(max_register)
        differences.append(M-L)
    return differences

sample_size=1000000
T=8
N=2
differences=find_difference(T,N,sample_size)
ml_mean=np.mean(differences)
ml_std=np.std(differences)
print "For T=8, N=2, the mean of M-L is:",ml_mean,', with a standard deviation of:',ml_std, " using 1 million samples"
a=32
b=64
below_b=[item for item in differences if item<=b]
over_a_and_below_b=[item for item in below_b if item>=a]
conditional_probability=float(len(over_a_and_below_b))/len(below_b)
print "for a=32,b=64,T=32 and N=4 at 1 million samples, conditional_probability=",conditional_probability
sample_size=1000000
T=32
N=4
differences=find_difference(T,N,sample_size)
ml_mean=np.mean(differences)
ml_std=np.std(differences)
print "For T=32, N=4 and 10M samples, the mean of M-L is:",ml_mean,', with a standard deviation of:',ml_std, " using 1 million samples"
a=2048
b=4096
below_b=[item for item in differences if item<=b]
over_a_and_below_b=[item for item in below_b if item>=a]
conditional_probability=float(len(over_a_and_below_b))/len(below_b)
print "for a=2048,b=4096,T=32 and N=4 at 1 million samples, conditional_probability=",conditional_probability
