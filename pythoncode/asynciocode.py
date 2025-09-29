# parallel processing using asyncio or multiprocessing 
import asyncio
import aiohttp  # parallel http requests
import threading


async def func1():
    print("async io started")

asyncio.run(func1())


async def func2():  # it dont do the handshake with event loop
    print("select * from table")
    #await asyncio.sleep(30)
    print("data has been fetched from table")
    

asyncio.run(func2())

url =["https://google.com", "https://yahoo.com", "https://bing.com"]

async def fetch(session, url):
    async with session.get(url) as response:
        return await asyncio.sleep(30).response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(*[fetch(session, url) for url in url])
        result1 = await asyncio.wait_for(asyncio.gather(*[fetch(session, url) for url in url]), timeout=30)
        for content in result:
            print(content[:100])
            print(f"Fetched {len(content)} characters")

asyncio.run(main())
# multiprocessing 
# 200( orphane process) -- ( 201,202,203(hung))

# multithreading   -- java 
# 200-- (thread1, thread2, thread3) lightweight process









# async def async_task(name, duration):
#     print(f"Task {name} starting")
#     await asyncio.sleep(duration)
#     print(f"Task {name} completed after {duration} seconds")
#     return f"Result of {name}"


# async def main():
#     tasks = [
#         async_task("A", 2),
#         async_task("B", 3),
#         async_task("C", 1)
#     ]
#     results = await asyncio.gather(*tasks)
#     print("All tasks completed")
#     for result in results:
#         print(result)