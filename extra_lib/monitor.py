import psutil
import os

# Retorna o uso de CPU, Memória, Swap e quantidade de processos em execução

def monitor():
    #### CPU #####
    print()
    # Captura o processo que representa o Pacman no SO
    p = psutil.Process(os.getpid())
    print("Uso de CPU: ", end='')
    cpu = psutil.cpu_percent(interval=0.0)
    print((f"{cpu:0.2f}%"))
    #write_text(f"Uso de CPU: {cpu:0.2f}%")
    print()

    ##### Memory ####

    mem = (p.memory_percent())
    #write_text(f"Uso de memoria: {mem}%")
    print()

    print(f"Uso de swap: {p.memory_full_info().swap}%")
    #write_text(f"Uso de swap: {p.memory_full_info().swap}%")
    print()

    #### Processos ####

    pid = len(psutil.pids())
    print(f"PIDS (processos rodando no sistema): {pid}")
    #write_text(f"PIDS (processos rodando no sistema): {pid}")
    print()

