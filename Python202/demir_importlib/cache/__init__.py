



def __getattr__(name):
    print("çağrılan", name)
    return name
