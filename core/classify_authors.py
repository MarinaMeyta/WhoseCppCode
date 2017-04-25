import whose_cpp_code

import time

path_to_data = "data"

start_time = time.time()
whose_cpp_code.classify_authors(path_to_data, loop=10)

run_time = round(time.time() - start_time, 2)
print('run time: ', run_time)
