ifdef OS
PLATFORM = WINDOWS_NT
ifeq (${USERNAME}, Alan)
SHELL = powershell.exe
endif
else
PLATFORM = LINUX
endif

ALL:
	echo ${SHELL}
ifeq (${PLATFORM}, WINDOWS_NT)
	rm ./ext/*.pyd
	python setup.py build_ext --inplace
	mv *.pyd ./ext
	make clear
endif

clear:
ifeq (${PLATFORM}, WINDOWS_NT)
	$$a = $$(ls);$$a
endif