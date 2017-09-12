import os
<<<<<<< HEAD

ext = ["calculate_hedge_cost", "sim_spot_futures"]
=======
ext=["calculate_hedge_cost", "sim_spot_futures.pyx"]
>>>>>>> a8b8f2e1c441519f6dfca5902eacc0d62dc5c2cc
ls = os.listdir(".")

for i in ext:
    if i not in [x.split(".")[0] for x in ls if x.endswith(".pyd")]:
        os.system("python setup.py build_ext --inplace")
        break
for i in ls:
    if i.endswith(".c"):
<<<<<<< HEAD
        os.chdir(".")
        os.remove(i)

del os
=======
        os.remove(i)
del os

# fixme : 基本上弄完了 你CYTHON 没装
>>>>>>> a8b8f2e1c441519f6dfca5902eacc0d62dc5c2cc
