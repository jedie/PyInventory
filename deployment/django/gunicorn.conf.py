import multiprocessing


workers = multiprocessing.cpu_count() * 2 + 1
access_logfile = '-'  # log to stdout

