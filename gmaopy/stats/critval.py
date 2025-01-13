from scipy.special import stdtr

def critval(confidence,size):
    "It calculates the value of a t-student with (size-1) degrees of freedom corresponding to       \
     a given confidence interval. (ie. it returns t such as P(-t<T<=t)=confidence where t~t_(n-1))  \
     The t-value is computed by using the bisection method. "
    if confidence>1:
        raise Exception("Confidence has to be between zero and one.")
    thigh=1.0
    chigh=stdtr(size-1,thigh)-stdtr(size-1,-thigh)
    while chigh<confidence:
        thigh*=2
        chigh=stdtr(size-1,thigh)-stdtr(size-1,-thigh)
    tlow=0
    tcrit=0.5*(thigh+tlow)
    for i in range(20):
        c=stdtr(size-1,tcrit)-stdtr(size-1,-tcrit)
        if c<confidence:
            tlow=tcrit
        else:
            thigh=tcrit
        tcrit=0.5*(thigh+tlow)
    return tcrit
