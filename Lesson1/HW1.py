import os
import platform
import subprocess
import time
import threading
from ipaddress import ip_address
from pprint import pprint

result = {'Доступные узлы': "", "Недоступные узлы": ""}

DNULL = open(os.devnull, 'w')


def check_is_ipaddress(value):
    try:
        ipv4 = ip_address(value)
    except ValueError:
        raise Exception('Некорректный ip адрес')
    return ipv4


def ping(ipv4, result, get_list):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    response = subprocess.Popen(["ping", param, '1', '-w', '1', str(ipv4)],
                                stdout=subprocess.PIPE)
    if response.wait() == 0:
        result["Доступные узлы"] += f"{ipv4}; "
        res = f"{ipv4} - Узел доступен"
        if not get_list:
            print(res)
        return res
    else:
        result["Недоступные узлы"] += f"{ipv4}; "
        res = f"{str(ipv4)} - Узел недоступен"
        if not get_list:
            print(res)
        return res


def host_ping(hosts_list, get_list=False):
    print("Начинаю проверку доступности узлов...")
    threads = []
    for host in hosts_list:
        try:
            ipv4 = check_is_ipaddress(host)
        except Exception as e:
            print(f'{host} - {e} воспринимаю как доменное имя')
            ipv4 = host

        thread = threading.Thread(target=ping, args=(ipv4, result, get_list), daemon=True)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    if get_list:
        return result


if __name__ == '__main__':
    hosts_list = ['192.168.8.1', '8.8.8.8', 'ya.ru', 'vk.com','192.168.1.1', '8.8.4.4', '192.168.0.1']
    start = time.time()
    host_ping(hosts_list)
    end = time.time()
    print(f'total time: {int(end - start)}')
    pprint(result)
