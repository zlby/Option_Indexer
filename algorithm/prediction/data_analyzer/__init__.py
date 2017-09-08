import os
ext=["calculate_hedge_cost", "sim_spot_futures.pyx"]
ls = os.listdir(".")

for i in ext:
    if i not in [x.split(".")[0] for x in ls if x.endswith(".pyd")]:
        os.system("python setup.py build_ext --inplace")
        break
for i in ls:
    if i.endswith(".c"):
        os.remove(i)
del os

# fixme : 基本上弄完了 你CYTHON 没装