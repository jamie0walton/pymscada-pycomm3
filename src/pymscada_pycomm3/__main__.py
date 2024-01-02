"""Logix for pymscada."""
import asyncio
from pymscada import Config
from pymscada_pycomm3 import LogixClient


async def main():
    config = Config('config/pycomm3.yaml')
    module = LogixClient(**config)
    await module.start()
    await asyncio.get_event_loop().create_future()


if __name__=='__main__':
    asyncio.run(main())
