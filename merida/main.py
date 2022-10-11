import json
import random
import time
from typing import List

import msgpack
from serialization_tests.request_type import InputRequest


def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print(
            "{:s} function took {:.3f} ms".format(f.__name__, (time2 - time1) * 1000.0)
        )

        return ret

    return wrap


def generate_input_requests() -> List[InputRequest]:
    vals: List[InputRequest] = []
    for _ in range(100_000):
        vals.append(
            InputRequest(
                ttype=random.randint(0, 3),
                icode=random.randint(0, 256),
                itype=random.randint(0, 256),
                ivalue=random.randint(-16384, 16383),
            )
        )
    return vals

@timing
def json_parsing(reqs: List[InputRequest]):
    """
    Parse to and from json, and then assert equality.
    """
    f_time: float = 0.0
    for req in reqs:
        stime = time.process_time()
        parsed = json.dumps(req.dict())
        reparsed = json.loads(parsed)
        etime = time.process_time()
        f_time += (etime - stime)
        req_re = InputRequest(**reparsed)
        assert req_re == req
    return f_time

@timing
def msgpack_parsing(reqs: List[InputRequest]):
    """
    Parse to and from msgpack, and then assert equality, for correctness
    """
    f_time: float = 0.0
    for req in reqs:
        stime = time.process_time()
        parsed = msgpack.dumps(req.dict())
        reparsed = msgpack.loads(parsed)
        etime = time.process_time()
        f_time += (etime - stime)
        req_re = InputRequest(**reparsed)
        assert req_re == req
    return f_time

def test_parsing():
    """
    Serialization-Test 1
    """
    print("Preparing dummy data...")
    vals: List[InputRequest] = generate_input_requests()
    results = []
    for _ in range(10):
        print("Testing JSON (TOTAL)")
        json_time = json_parsing(vals)
        print("Testing Msgpack (TOTAL)")
        msgpack_time = msgpack_parsing(vals)
        print(f"Json time = {json_time}, Msgpack time = {msgpack_time}")
        results.append((json_time, msgpack_time))
    # Aggregate all values
    print("Tests ended. Aggregating")
    json_total, msgpack_total = 0.0, 0.0
    for json_time, msgpack_time in results:
        json_total += json_time
        msgpack_total += msgpack_time
    if json_total > msgpack_total:
        print(f"Msgpack is {json_total/msgpack_total:.3f} times faster than JSON")
    elif json_total < msgpack_total:
        print(f"JSON is {msgpack_total/json_total} times faster than Msgpack")
    else:
        print(f"Msgpack and JSON took the same time")
test_parsing()