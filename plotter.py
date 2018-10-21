from ast import literal_eval
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy import interpolate as spint

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def plot(data_points):
    X = np.linspace(min(data_points[:, 0]), max(data_points[:, 0]))
    Y = np.linspace(min(data_points[:, 1]), max(data_points[:, 1]))
    X, Y = np.meshgrid(X, Y)
    interp = spint.LinearNDInterpolator(data_points[:,:2], data_points[:,2])
    Z0 = interp(X, Y)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_trisurf(data_points[:,0], data_points[:,1], data_points[:,2])
    #ax.set_xlabel(X_FIELD)
    #ax.set_ylabel(Y_FIELD)
    #ax.set_zlabel(Z_FIELD)
    #fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

if __name__ == '__main__':
    for i in range(5):
        #fig = plt.figure()
        #ax = Axes3D(fig)
        value = []
        x = []
        y = []
        z = []
        with open('plot_{0}.csv'.format(i), 'r') as pl:
            for line in nonblank_lines(pl):
                value.append(literal_eval(line))
        #for line in range(len(value)):
            #x.append(value[line][0])
            #y.append(value[line][1])
            #z.append(value[line][2])
        #ax.plot_wireframe(x, y, z)
        #ax.plot(x, y, z)
        plot(np.array(value))
    #plt.show()