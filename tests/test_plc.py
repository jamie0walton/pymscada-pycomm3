"""Just test connections to a real PLC."""
import asyncio
import pytest
from time import time
from pymscada import Tag
from pymscada_pycomm3 import LogixClient

CLIENT = {
    'bus_ip': None,
    'bus_port': None,
    'rtus': [
        {
            'name': 'Ani',
            'ip': '172.26.7.196',
            'rate': '0.1',
            'read': [
                {'addr': 'Fout', 'type': 'REAL[]', 'start': 0, 'end': 99},
                {'addr': 'Iout', 'type': 'DINT[]', 'start': 0, 'end': 99},
                # {'addr': 'SomeVar', 'type': 'REAL'}
            ],
            'writeok': [
                {'addr': 'Fin', 'type': 'REAL[]', 'start': 0, 'end': 99},
                {'addr': 'Iin', 'type': 'DINT[]', 'start': 0, 'end': 99},
                # {'addr': 'AnotherVar', 'type': 'REAL'}
            ]
        }
    ],
    'tags': {
        'Ani_Fin_20': {'type': 'float32', 'addr': 'Ani:Fin:20'},
        'Ani_Fout_20': {'type': 'float32', 'addr': 'Ani:Fout:20'},
        'Ani_Iin_20': {'type': 'int32', 'addr': 'Ani:Iin:20'},
        'Ani_Iout_20': {'type': 'int32', 'addr': 'Ani:Iout:20'}
    }
}
queue = asyncio.Queue()


def tag_callback(tag: Tag):
    """Pipe all async messages through here."""
    global queue
    queue.put_nowait(tag)


LOGIX_TEST = [
    (float, '', '', 123.456, -987.654)
]


@pytest.mark.asyncio
async def test_connect():
    """Test Logix."""
    global queue
    lc = LogixClient(**CLIENT)
    # await lc.start()
    s1 = Tag('Ani_Fin_20', float)
    s2 = Tag('Ani_Iin_20', int)
    g1 = Tag('Ani_Fout_20', float)
    g2 = Tag('Ani_Iout_20', int)
    g1.add_callback(tag_callback)
    g2.add_callback(tag_callback)
    start = time()
    await lc._poll()
    x1, x2 = await queue.get(), await queue.get()
    assert x1.value is not None
    assert x2.value is not None
    for v in range(-50, 50):
        if v == x1.value:
            continue
        s1.value = v
        await lc._poll()
        x1 = await queue.get()
        assert x1.value == pytest.approx(v)
    duration = time() - start
    assert duration < 1
