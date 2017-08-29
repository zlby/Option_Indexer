AIM = kkk
SHELL = powershell.exe
PYTHON_PATH = C:/Users/Alan/AppData/Local/Programs/Python/Python35
LD_LIBRARY_PATH ="C:/Users/Alan/AppData/Local/Programs/Python/Python35/"
NUMPY_INCLUDE = "C:\Users\Alan\AppData\Local\Programs\Python\Python35\Lib\site-packages\numpy\core\include\"

ALL : $(AIM).pyd

$(AIM).pyd: $(AIM).obj
	gcc -fPIC $(AIM).obj -Wall -O3 -shared -o $(AIM).pyd -L$(LD_LIBRARY_PATH)  -l python35
	rm $(AIM).c
	rm $(AIM).obj

$(AIM).obj: $(AIM).c
	gcc -c $(AIM).c -o $(AIM).obj -I$(PYTHON_PATH)/include -I$(NUMPY_INCLUDE)

$(AIM).c: $(AIM).pyx
	cython -o $(AIM).c $(AIM).pyx