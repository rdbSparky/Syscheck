# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 09:57:43 2021

@author: Sparky
"""

"""
pip install psutil
pip install gputil
pip install tabulate

"""

import psutil
import platform
from datetime import datetime
import GPUtil
from tabulate import tabulate


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
        
def syinfo():
    #System info
    file1 = open("MyFile.txt","w")
    file1.write("="*40 + "System Information" + "="*40)
    uname = platform.uname()
    file1.write(f"\nSystem: {uname.system}")
    file1.write(f"\nNode Name: {uname.node}")
    file1.write(f"\nRelease: {uname.release}")
    file1.write(f"\nVersion: {uname.version}")
    file1.write(f"\nMachine: {uname.machine}")
    file1.write(f"\nProcessor: {uname.processor}\n")
    # Boot Time
    file1.write("="*40 + "Boot Time" + "="*40)
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    file1.write(f"\nBoot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n")
    #CPU information
    file1.write("="*40 + "CPU Info" + "="*40)
    file1.write(f"\nPhysical cores: {psutil.cpu_count(logical=False)}")
    file1.write(f"\nTotal cores:{psutil.cpu_count(logical=True)}")
    cpufreq = psutil.cpu_freq()
    file1.write(f"\nMax Frequency: {cpufreq.max:.2f}Mhz")
    file1.write(f"\nMin Frequency: {cpufreq.min:.2f}Mhz")
    file1.write(f"\nCurrent Frequency: {cpufreq.current:.2f}Mhz")
    file1.write("\nCPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        file1.write(f"\nCore {i}: {percentage}%")
    file1.write(f"\nTotal CPU Usage: {psutil.cpu_percent()}%\n")
    # Memory Information
    file1.write("="*40 + "Memory Information" + "="*40)
    svmem = psutil.virtual_memory()
    file1.write(f"\nTotal: {get_size(svmem.total)}")
    file1.write(f"\nAvailable: {get_size(svmem.available)}")
    file1.write(f"\nUsed: {get_size(svmem.used)}")
    file1.write(f"\nPercentage: {svmem.percent}%\n")
    file1.write("="*20 + "SWAP" + "="*20)
    swap = psutil.swap_memory()
    file1.write(f"\nTotal: {get_size(swap.total)}")
    file1.write(f"\nFree: {get_size(swap.free)}")
    file1.write(f"\nUsed: {get_size(swap.used)}")
    file1.write(f"\nPercentage: {swap.percent}%\n")
    # GPU information
    file1.write("="*40 + "GPU Details" + "="*40+"\n")
    gpus = GPUtil.getGPUs()
    list_gpus = []
    for gpu in gpus:
        # get the GPU id
        gpu_id = gpu.id
        # name of GPU
        gpu_name = gpu.name
        # get % percentage of GPU usage of that GPU
        gpu_load = f"{gpu.load*100}%"
        # get free memory in MB format
        gpu_free_memory = f"{gpu.memoryFree}MB"
        # get used memory
        gpu_used_memory = f"{gpu.memoryUsed}MB"
        # get total memory
        gpu_total_memory = f"{gpu.memoryTotal}MB"
        # get GPU temperature in Celsius
        gpu_temperature = f"{gpu.temperature} °C"
        gpu_uuid = gpu.uuid
        list_gpus.append((
            gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
            gpu_total_memory, gpu_temperature, gpu_uuid
        ))

    file1.write(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                           "temperature", "uuid")))
    file1.close()
    f = open('MyFile.txt', 'r')
    s= "".join(f.read()).split('\n')
    return s