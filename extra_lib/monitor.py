import psutil
import os


# Retorna o uso de CPU, Memória, Swap e quantidade de processos em execução

def monitor():
    p = psutil.Process(os.getpid())
    cpu = psutil.cpu_percent(interval=0.0)
    mem = (p.memory_percent())

    pid = len(psutil.pids())
    return mem, cpu
