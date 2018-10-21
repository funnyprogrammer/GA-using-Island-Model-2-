import matplotlib.pyplot as plt
from ast import literal_eval

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line


def plotter2dALL(num_threads,x_var,timing):
    #for isl in range(num_threads):
        #with open('verify_{0}'.format(isl), 'r')
    for i in range(num_threads):
        x = []
        y = []
        with open('plot_{0}.csv'.format(i), 'r') as pl:
            for line in nonblank_lines(pl):
                y.append(literal_eval(line))

        for asi in range(x_var * 3):
            x.append(asi)

        plt.plot(x, y)

    plt.axis([0, x_var * 3, 0, 1000])
    plt.title('Average fitness in every islands',loc='left')
    plt.title('Time = ' + str(timing),loc='right')
    plt.show()
    for i in range(num_threads):
        x = []
        y2 = []
        with open('plot2_{0}.csv'.format(i), 'r') as pl:
            for line in nonblank_lines(pl):
                y2.append(literal_eval(line))
        for i in range(x_var * 3):
            x.append(i)
        plt.plot(x, y2)
        plt.axis([0, x_var * 3, 0, 1000])
        plt.title('Maximum fitness in every islands')
    plt.show()

def plotter2dSEP(num_threads,x_var,time):
    for i in range(num_threads):
        x = []
        y = []
        with open('plot_{0}.csv'.format(i), 'r') as pl:
            for line in nonblank_lines(pl):
                y.append(literal_eval(line))
        for i in range(x_var * 3):
            x.append(i)

        plt.plot(x, y)
        plt.axis([0, x_var * 3, 0, 10000])
        plt.title('Island ' + str(i), loc= 'left')
        plt.title('Time = ' + str(time[i]), loc='right')
        plt.show()