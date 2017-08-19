AIM = sim_spot_futures

PYTHON_PATH = C:/Users/Alan/AppData/Local/Programs/Python/Python35

LD_LIBRARY_PATH+="C:/Users/Alan/AppData/Local/Programs/Python/Python35/"

ALL : $(AIM).pyd

$(AIM).pyd: $(AIM).obj
	gcc -fPIC $(AIM).obj -Wall -O3 -shared -o $(AIM).pyd -L$(LD_LIBRARY_PATH) -l python35
	rm $(AIM).c
	rm $(AIM).obj

$(AIM).obj: $(AIM).c
	gcc -c $(AIM).c -o $(AIM).obj -I$(PYTHON_PATH)/include

$(AIM).c: $(AIM).pyx
	cython -o $(AIM).c $(AIM).pyx