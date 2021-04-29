import time


def measure_time(start):
    """
    Measure time
    :param start:
    :return:
    """
    if start is None:
        start = time.time()
        return start
    else:
        end = time.time() - start
        print("time: %f minutes" % (round(end / 60, 2)))
