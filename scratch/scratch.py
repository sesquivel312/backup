dict = {'k1':'v1', 'k2':'v2'}

def func(**kwargs):
    for key in kwargs:
        print key, kwargs[key]

func(**dict)