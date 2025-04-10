import multiprocessing
import time
import psutil
import os
from datetime import datetime

block_size = 100 * 1024 * 1024  # 100MB blocks
max_blocks = 10  # Maximum 1GB (adjust based on your system)

def cpu_stress(process_num):
    """Function to stress a single CPU core with intensive calculations"""
    print(f"Process {process_num}: Starting CPU stress")
    start_time = time.time()
    
    # manually stop this, else it'll damage your system
    while True:
        for i in range(10000000):
            x = i * i * i * i
            x = x ** 0.5
            x = x / 3.14159
        
        current_time = time.time()
        if current_time - start_time > 60:
            print(f"Process {process_num}: Still running at {datetime.now().strftime('%H:%M:%S')}")
            start_time = current_time

def memory_stress():
    """Function to consume memory gradually"""
    memory_blocks = []
    print("Starting memory consumption...")
    for i in range(max_blocks):
        try:
            memory_blocks.append(bytearray(block_size))
            print(f"Allocated block {i+1}/{max_blocks} ({(i+1)*100}MB)")
            time.sleep(5) 
        except MemoryError:
            print("Maximum memory reached!")
            break
    
    print("Keeping memory allocated...")
    while True:
        time.sleep(60)  #

def monitor_temperature():
    """Monitor system temperature if available"""
    if hasattr(psutil, "sensors_temperatures"):
        while True:
            temps = psutil.sensors_temperatures()
            if temps:
                print("\nCurrent temperatures:")
                for name, entries in temps.items():
                    for entry in entries:
                        print(f"  {name}: {entry.label or 'N/A'}: {entry.current}°C")
            else:
                print("No temperature sensors detected")
            
            time.sleep(30)  # every 30 seconds
    else:
        print("Temperature monitoring not supported on this system")

if __name__ == "__main__":
    print("=" * 50)
    print("WARNING: This program will stress your system and generate heat.")
    print("Use at your own risk and only on devices you're willing to damage.")
    print("Press Ctrl+C to stop the program.")
    print("=" * 50)
    
    num_cores = multiprocessing.cpu_count()
    print(f"Detected {num_cores} CPU cores")
    
    try:
        temp_monitor = multiprocessing.Process(target=monitor_temperature)
        temp_monitor.start()
        
        mem_process = multiprocessing.Process(target=memory_stress)
        mem_process.start()
        
        processes = []
        for i in range(num_cores):
            p = multiprocessing.Process(target=cpu_stress, args=(i,))
            processes.append(p)
            p.start()
            print(f"Started CPU stress process {i+1}/{num_cores}")
        
        for p in processes:
            p.join()
            
    except KeyboardInterrupt:
        print("\nProgram interrupted. Shutting down...")
    
    print("Program ended")