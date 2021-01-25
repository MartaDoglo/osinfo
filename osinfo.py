"""
Используя configargparse и re напишите cli инструмент, выдающий информацию
об операционной системе (тип ОС, какой процессор, можно количество ОЗУ)
"""
from log import logger
import subprocess
import re
import configargparse
from tabulate import tabulate


def get_os_info():
    os_info = subprocess.Popen(['lsb_release', '-a'], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).communicate()[0].decode('ascii')
    os_r = re.findall(r"(Distributor ID|Release|Description):(.*)", os_info)
    os = {i[0]: i[1].strip() for i in os_r}
    return f"\n---===OPERATION SYSTEM INFORMATION===---\n{tabulate(os.items(), tablefmt='plain')}\n"


def get_cpu_info():
    cpu_info = subprocess.Popen(['lscpu'], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE).communicate()[0].decode('ascii')
    cpu_r = re.findall(r"(Model name|Architecture"
                       r"|CPU\(s\)|CPU MHz"
                       r"|CPU max MHz|CPU min MHz"
                       r"|Virtualization|L1d cache|"
                       r"L1i cache|L2 cache|L3 cache):(.*)", cpu_info)

    cpu = {i[0]: i[1].strip() for i in cpu_r}
    return f"\n---===CPU INFORMATION===---\n{tabulate(cpu.items(), tablefmt='plain')}\n"


def get_ram_info():
    ram_info = subprocess.Popen(['free', '-h'], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE).communicate()[0].decode('ascii')
    ram_r = re.findall(r"(Mem|Swap):(\s*\S*)", ram_info)
    ram = {i[0]: i[1].strip() for i in ram_r}
    return f"\n---===RAM INFORMATION===---\n{tabulate(ram.items(), tablefmt='plain')}\n"


def get_info(opt: configargparse):
    funcs = {'os': get_os_info, 'cpu': get_cpu_info, 'ram': get_ram_info}
    result = ""
    for i in funcs.keys():
        if vars(opt).get(i) is True:
            result += funcs.get(i)()
    print(result)


def get_configs():
    p = configargparse.ArgParser()
    p.add_argument('--cpu', '-c', action='store_true', help='Shows cpu info')
    p.add_argument('--ram', '-r', action='store_true', help='Shows ram info')
    p.add_argument('--os', '-o', action='store_true', help='Shows OS info')
    options = p.parse_args()
    logger.info(options)
    return options


if __name__ == '__main__':
    get_info(get_configs())
