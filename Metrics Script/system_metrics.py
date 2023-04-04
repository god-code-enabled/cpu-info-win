import shutil
import psutil
import pandas as pd
from time import sleep
from os import system as sys
from datetime import datetime

now = datetime.now()


# Check Disk usage function
def check_disk_usage(disk):
    """Takes a directory of a disk and calculates disk usage"""
    du= shutil.disk_usage(disk)
    free = du.free / du.total * 100
    # print ("Current disk usage for {}".format(disk))
    #print("{:.2f}% free out of {}".format(free, du.total))
    return f"{free:.2f}%" 


# Check CPU usage function
def check_cpu_usage():
    usage = psutil.cpu_percent(0.1)*10
    return usage

cpu_threshold = 50

while True:
        # Get Total CPU usage
        cpu_usage = check_cpu_usage()
        # Get CPU usage percentage for each core
        cpu_percent_per_core = psutil.cpu_percent(percpu=True)
        processes = []
        cpu_core_data = [] 
        sum_core_data = 0
        num_of_threads = 24

        # Update displayed table if usage goes above set threshold
        if cpu_usage >= cpu_threshold:   
            
            # Iterate through all running processes and append their details to the list
            for process in psutil.process_iter():
                try:
                    process_info = process.as_dict(attrs=["pid", "name", "cpu_percent"])
                    processes.append(process_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
                
            # Sort the list of processes by CPU usage
            sorted_processes = sorted(processes, key=lambda k: k["cpu_percent"], reverse=True)
        
            # Create pandas table for per core usage
            for core in cpu_percent_per_core:
                cpu_core_data.append({"Per core usage":core})
                sum_core_data += core     
                
            df_core = pd.DataFrame(cpu_core_data)
            overall_usage = sum_core_data / num_of_threads
            sys("cls") 
            
            data=[{"| Disk |": "C:", "| Disk usage |":check_disk_usage("C:"),"| Overall CPU usage |": f'{overall_usage:.2f}%'},
                {"| Disk |": "D:", "| Disk usage |":check_disk_usage("D:"),"| Overall CPU usage |": ""},
                {"| Disk |": "F:", "| Disk usage |":check_disk_usage("F:"),"| Overall CPU usage |": ""},
                {"| Disk |": "I:", "| Disk usage |":check_disk_usage("I:"),"| Overall CPU usage |": ""},
        ]   
            df_disk = pd.DataFrame(data)
            df_processes = pd.DataFrame(sorted_processes)
            with open("processes.txt", "a") as file:
                 
                for process in sorted_processes:
                    pid = process['pid']
                    name = process['name']
                    cpu_percent = process['cpu_percent']/num_of_threads
                    if cpu_percent > cpu_threshold and name != "System Idle Process":
                        file.write(f"Time: {now}, PID: {pid}, Name: {name}, CPU percent: {cpu_percent:.2f}%\n")
                    
                    
            print("System Disk and CPU usage overview:\n")
            print(df_disk)
            print("\n")
            print(df_core)
            sleep(1)
         
       