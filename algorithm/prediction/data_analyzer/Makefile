ifdef OS
EXC= pyd
ifeq ($(USERNAME), Alan)
SHELL= powershell.exe
PYTHON_INCLUDE = C:/Users/Alan/AppData/Local/Programs/Python/Python35/include
LD_LIBRARY_PATH+="C:/Users/Alan/AppData/Local/Programs/Python/Python35/"
endif
else
EXC= so
endif

all:sim_spot_futures.$(EXC) calculate_hedge_cost.$(EXC)

%.pyd: %.obj
	gcc -fPIC $< -Wall -O3 -shared -o $@ -L$(LD_LIBRARY_PATH) -lpython35

%.so: %.obj
	gcc -fPIC $< -Wall -O3 -shared -o $@ -l python35

%.obj: %.c
ifndef PYTHON_INCLUDE
	@echo "未定义环境变量PYTHON_INCLUDE"
else
	gcc -fPIC -c $< -o $@ -I$(PYTHON_INCLUDE)
endif

%.c: %.pyx
	cython -o $@ $<