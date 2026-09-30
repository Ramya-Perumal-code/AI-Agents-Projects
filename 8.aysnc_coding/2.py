import asyncio


async def hello():
    print("Hello")

    await asyncio.sleep(2)

    print("World")

async def main():
    await hello()

asyncio.run(main())
