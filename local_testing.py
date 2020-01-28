import os

from taggy import Core
import timeit

core = Core()

def run(paths, core):
    for item in paths:
        core.add_document(path=item)
    res = core.most_common()
    return res

paths = [os.path.abspath(os.path.join('tests', 'docs', item)) for item in os.listdir(os.path.join('tests','docs'))] 
times = []
for i in range(len(paths)): 
    paths_to_use = paths[:i+1] 
    times.append(timeit.timeit(stmt='run(paths_to_use, core=core)', setup="from __main__ import run", number=1, globals=globals()))
print(times)


# run(paths, core)