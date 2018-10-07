escores_lock = 0

def lock():
    escores_lock = 1

def unlock():
    escores_lock = 0

def check():
    return escores_lock