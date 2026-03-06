# Code du scanner de ports
import asyncio
from colorama import Fore, Style, init

init(autoreset=True) # Initialize colorama

semaphore = asyncio.Semaphore(500) # You can change it to the value you want, but not too much either
                                   # as 500 is the standart value you shouldn't have to change it

async def scan_port(ip, port):
    async with semaphore:
        try:
            conn = asyncio.open_connection(ip, port)
            reader, writer = await asyncio.wait_for(conn, timeout = 0.1)

            writer.close()
            await writer.wait_closed()
            print(f"{Fore.CYAN}[:)] Port {port:<5} : OPEN {Style.RESET_ALL}")
            return port
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            return None
        except Exception:
            return None
    
async def run_scanner(target_ip, port_range):

    tasks = []
    for port in port_range:
        tasks.append(scan_port(target_ip, port))

    print(f"Starting scan on {len(tasks)} ports...")
    results = await asyncio.gather(*tasks)

    open_ports = [port for port in results if port is not None]
    return open_ports