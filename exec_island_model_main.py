import exec_create_island as eci
import exec_migration_island as emi
import exec_island_checker as eic
import helloWorld as hW
from multiprocessing import Pool
import time
import os
from ast import literal_eval

if __name__ == '__main__':
    mig_policy_time = time.time()  # current time
    mig_policy_freq = 0.3  # frequency
    num_islands = [0, 1, 2, 3, 4]
    num_threads = 5
    keep_rolling = True

    eci.create_island(num_islands, num_threads)  # create islands
    m = Pool(num_threads)
    m.map(hW.initializePopulationParallel, num_islands)
    m.close()

    while keep_rolling:
        print("distribution time")
        #function distribution between islands
        p = Pool(num_threads)
        p.map(hW.initializeGA, num_islands)
        p.close()
        #reuniao dos broadcasters
        for each in range(num_threads):
            allBests = []
            with open('broadcast_{0}.txt'.format(each), 'r') as broad1:
                for line in hW.nonblank_lines(broad1):
                    allBests.append(literal_eval(line))
            broad1.close()
            prevBests = []
            with open('broadcast.txt', 'r') as broad2:
                for line in hW.nonblank_lines(broad2):
                    prevBests.append(literal_eval(line))
            broad2.close()
            prevBests.extend(allBests)
            with open('broadcast.txt', 'w') as broad:
                for ini in range(len(prevBests)):
                    broad.write(str(prevBests[ini]) + '\n')
            broad.close()

        #migration time
        print("migration time")
        moment = time.time()
        if moment > mig_policy_time + mig_policy_freq:  # FREQUENCY
            print("foi")
            mig_policy_time = time.time()
            var_random = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
            if var_random >= mig_policy_freq:
                p = Pool(num_threads)
                p.map(emi.do_migration, num_islands)
                p.close()
        elif moment > mig_policy_time + mig_policy_freq:
            print("nao foi")
        #reset broadcasters
        broad = open('broadcast.txt', 'w')
        broad.close()
        for i in range(num_threads):
            broad = open('broadcast_{0}.txt'.format(i), 'w')
            broad.close()

        #checker
        print("check time")
        for i in range(num_threads):
            keep_rolling = eic.check(i)
    print("terminou")

