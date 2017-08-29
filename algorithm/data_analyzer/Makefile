
SHELL= powershell.exe

PYTHON_PATH = C:/Users/Alan/AppData/Local/Programs/Python/Python35

NUMPY_INCLUDE = "C:\Users\Alan\AppData\Local\Programs\Python\Python35\Lib\site-packages\numpy\core\include\"

LD_LIBRARY_PATH+="C:/Users/Alan/AppData/Local/Programs/Python/Python35/"

ALL :sim_spot_futures.pyd

%.pyd: %.obj
	gcc -fPIC $< -Wall -O3 -shared -o $@ -L$(LD_LIBRARY_PATH) -l python35

%.obj: %.c
	gcc -c $< -o $@ -I$(PYTHON_PATH)/include -I$(NUMPY_INCLUDE)

%.c: %.pyx
	cython -o $@ $<

#clean:
#	@rm *.c
#	@rm *.obj