import asyncio
import aiohttp
import time
import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

async def make_requests(session, base_url, counter):
    # Register
    counter += 1
    register_url = f"{base_url}/api/v1/register"
    user = generate_random_string(8)
    password = generate_random_string(8)
    async with session.post(register_url, json={"username": user, "password": password}) as response:
        await response.read()

    time.sleep(0.5)
    # Login and save JWT
    login_url = f"{base_url}/api/v1/login"
    async with session.post(login_url, json={"username": user, "password": password}) as response:
        jwt = (await response.json()).get('token', '')

    time.sleep(0.5)

    # Create a task using the JWT from login
    task_url = f"{base_url}/api/v1/tasks"
    async with session.post(task_url, json={"title": "Do something"}, cookies={"token": jwt}) as response:
        await response.read()
    
    time.sleep(0.5)

async def run_sequence(url, n_groups):
    counter = 0
    async with aiohttp.ClientSession() as session:
        tasks = [make_requests(session, url, counter) for _ in range(n_groups)]
        start_time = time.time()
        await asyncio.gather(*tasks)
        total_time = time.time() - start_time
        return total_time / n_groups  # Calculate average time per group

async def main():
    URL1 = "http://localhost:3000"
    URL2 = "http://localhost:8000"
    N_GROUPS = 4


    print("Starting the requests...")
    start_time = time.time()

    # Run the sequences for both servers
    average_time1, average_time2 = await asyncio.gather(run_sequence(URL1, N_GROUPS), run_sequence(URL2, N_GROUPS))

    total_duration = time.time() - start_time
    print(f"Total time for all request groups: {total_duration:.2f} seconds")
    print(f"Average time per group for Server 1: {average_time1:.4f} seconds")
    print(f"Average time per group for Server 2: {average_time2:.4f} seconds")

    if average_time1 < average_time2:
        print("Server 1 is faster.")
    elif average_time1 > average_time2:
        print("Server 2 is faster.")
    else:
        print("Both servers have the same average response time per group.")

if __name__ == "__main__":
    asyncio.run(main())
