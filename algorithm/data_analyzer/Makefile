AIM = sim_spot_futures

PYTHON_PATH = C:/Users/Alan/AppData/Local/Programs/Python/Python35

LD_LIBRARY_PATH+="C:/Users/Alan/AppData/Local/Programs/Python/Python35/"

ALL : sim_spot_futures.pyd binomial_amer.pyd clean

%.pyd: %.obj
	gcc -fPIC $< -Wall -O3 -shared -o $@ -L$(LD_LIBRARY_PATH) -l python35

%.obj: %.c
	gcc -c $< -o $@ -I$(PYTHON_PATH)/include

%.c: %.pyx
	cython -o $@ $<

clean:
	rm -rf *.c *.obj