import random
import json
import time
from timeit import Timer
from typing import List

from serialization_tests import __version__
from serialization_tests.request_type import InputRequest


def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap

@timing
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


def json_parsing(reqs: List[InputRequest]):
    for req in reqs:
        parsed = json.dumps(req.dict())
        reparsed = InputRequest(**json.loads(parsed))
        assert reparsed == req


def test_version():
    assert __version__ == "0.1.0"


def test_json_parsing():
    """
    Serialization-Test 1
    """
    vals: List[InputRequest] = generate_input_requests()
    json_parsing(vals)
