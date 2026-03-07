# Code du scanner de ports
import asyncio
from colorama import Fore, Style, init

init(autoreset=True) # Initialize colorama



async def scan_port(ip, semaphore, port, callback=None, progress_callback=None, check_run = None):
    if check_run and not check_run():
        return "STOPPED"
    
    async with semaphore:
        try:
            if check_run and not check_run(): return "STOPPED"

            conn = asyncio.open_connection(ip, port)
            reader, writer = await asyncio.wait_for(conn, timeout = 0.3)

            if callback: callback(f"[ :D ] Port {port:<5} : OPEN", status = "open")

            writer.close()
            await writer.wait_closed()
            return port
        
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            #if callback: callback(f"[ :O ] Port {port:<5} : CLOSED", status = "closed") we don't log the closed ports because it will slow down the scan
            return None
        
        except Exception:
            if callback:
                callback(f"[ :O ] Port {port:<5} : ERROR", status = "error")
            return None
        finally:
            if progress_callback: progress_callback()
    
async def run_scanner(target_ip, port_range, callback=None, progress_callback=None, check_run = None):
    semaphore = asyncio.Semaphore(500) # You can change it to the value you want, but not too much either
                                   # as 500 is the standart value you shouldn't have to change it
    
    tasks = []
    for port in port_range:
        tasks.append(scan_port(target_ip, semaphore, port, callback, progress_callback, check_run))

    print(f"Starting scan on {len(tasks)} ports...")
    print("\n")

    results = await asyncio.gather(*tasks)
    return [port for port in results if isinstance(port,int)]