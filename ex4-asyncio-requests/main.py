import aiohttp
import asyncio
import timeit

FILE_PATH = 'lines.txt'
SERVER_URL_8080 = 'http://localhost:8080'
SERVER_URL_8081 = 'http://localhost:8081'

def get_lines_from_file():
    return open(FILE_PATH,'r').read().split('\n')

async def fetch(word,session,session2):
    async with session.get(f"{SERVER_URL_8080}/{word}") as response:
        res1 = await response.text()

    async with session2.get(f"{SERVER_URL_8081}/{word}") as response2:
        res2 = await response2.text()

    if word == res1 and res1 == res2:
        return True
    return False

async def gather_coroutines(words):
    async with aiohttp.ClientSession() as session, aiohttp.ClientSession() as session2:
        return await asyncio.gather(*[
            fetch(word,session,session2) for word in words
        ])

def request_servers(words):
    tasks = gather_coroutines(words)
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(tasks)
    loop.close()
    
    return results

def write_output(results):
    with open('output.txt', 'w') as fp:
        fp.write("\n".join(str(result) for result in results))


def main():
    words = get_lines_from_file()
    start = timeit.default_timer()
    results = request_servers(words)
    write_output(results)
    stop = timeit.default_timer()
    print('Time: ', stop - start) 

main()