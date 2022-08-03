import aiohttp
import asyncio
import timeit

FILE_PATH = 'lines.txt'
SERVER_URL_8080 = 'http://localhost:8080'
SERVER_URL_8081 = 'http://localhost:8081'

async def compare_strings(word: str,session: aiohttp.ClientSession(),session2: aiohttp.ClientSession()) -> bool:
    """This function sends a word(string) to both servers via HTTP GET requests,
        compares the results and returns True/False accordingly.
    Args:
        word: (str) A word from the local FILE_PATH file.
        session: a ClientSession for SERVER_URL_8080
        session2: a ClientSession for SERVER_URL_8081
    Returns:
        True if both servers returned the same word, False otherwise.
    """
    async with session.get(f"{SERVER_URL_8080}/{word}") as response:
        res1 = await response.text()

    async with session2.get(f"{SERVER_URL_8081}/{word}") as response2:
        res2 = await response2.text()

    if word == res1 and res1 == res2:
        return True
    return False

async def gather_coroutines(words: list) -> asyncio.Future:
    """This function creates a coroutine for each word in words,
        each coroutine running the fetch() function with a word.
    Args:
        words: (list) A list of words(strings)
    Returns:
        Future instance
    """
    async with aiohttp.ClientSession() as session, aiohttp.ClientSession() as session2:
        return await asyncio.gather(*[
            compare_strings(word,session,session2) for word in words
        ])

def request_servers(words: list) -> list:
    """This function creates and runs coroutines,
        Eventually returns the results for all coroutines
    Args:
        words: (list) A list of words(strings)
    Returns:
        results
    """
    tasks = gather_coroutines(words)
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(tasks)
    loop.close()
    
    return results

def main():
    start = timeit.default_timer()
    
    # read all words from local file
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        words = f.read().split('\n')
    results = request_servers(words[0:10000])
    
    # write results to local file
    with open('output.txt', 'w', encoding='utf-8') as fp:
        fp.write("\n".join(str(result) for result in results))
    print('Time: ', timeit.default_timer() - start) 


if __name__ == '__main__':
    main()