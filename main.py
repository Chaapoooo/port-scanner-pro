# Point d'entrée du prog
import asyncio
from src.scanner import run_scanner

async def main():
    question = input("Do you want to scan a host ? (y/n) ")

    if question.lower() == "y": 
        target_ip = input("Enter the target IP address :");

        if len(target_ip.split('.')) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in target_ip.split('.')):
            print("Invalid IP address. Please enter a valid IP address")
            exit()

        print(f"Target IP address : {target_ip}")
        print("-------------------------------")
        question = input("Do you want to scan all ports (1) or a specific range (2) ? (ex : 20-80) ")
        print("-------------------------------")
        print(len(question))
        if question.lower() == "1" and len(question) == 1: 
            return await run_scanner(target_ip, range(1, 65536))

        elif question.lower() == "2" and len(question) == 1:
            port_range = input("Enter the port range to scan (e.g., 20-80): ")
            start_port, end_port = map(int, port_range.split('-'))
            
            if start_port < 1 or end_port > 65535 or start_port > end_port:
                print("Invalid port range. Please enter a valid range (e.g., 20-80).")
                exit()
            else: return await run_scanner(target_ip, range(start_port, end_port + 1))
        else: return print("Invalid input.")

    elif question.lower() == "n": return print("Scan cancelled.")

    else: return print("Invalid input.")

if __name__ == "__main__": # sert de sécurité
    try:
        asyncio.run(main())
        input("Scan completed or cancelled. Enter to exit.")
    except KeyboardInterrupt:
        print("\nScan cancelled by User.")