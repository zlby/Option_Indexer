cdef char* _say_hello():
    return "hello world"

def say_hello():
    a = _say_hello()
    return a.decode("utf-8")