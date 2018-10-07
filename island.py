island_lock = [0, 0, 0, 0, 0]

def check(island_number):
    return island_lock[island_number]

def lock(island_number):
    island_lock[island_number] = 1

def unlock(island_number):
    island_lock[island_number] = 0

def wait():
    print("Wait")