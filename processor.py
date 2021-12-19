import config
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math 

from package import Package
from receiver import Receiver

packages = [Package(data=f'test{id}', id=id)
            for id in range(config.PACKAGES_COUNT)]

receiver = Receiver()

def is_all_packages_success(packages):
    success_sent = 0
    for package in packages:
        if package.receipt == False:
            continue
        success_sent += 1

    return success_sent, success_sent == len(packages)

# modulation #
if __name__ == '__main__':
    current_window_size = config.START_WINDOW_SIZE
    window_size_history = []
    add_stage_window_size_history = []
    packages_sent = 0

    timeline = 0

    current_stage = 'EXP'
    end_of_exp_stage = 0
    
    while timeline < 110:
        #print(timeline)
        window_size_history.append(current_window_size)
        add_stage_window_size_history.append(current_window_size)
        
        # calculate valid count of packages to send #
        real_upper_border = current_window_size
        
        if real_upper_border >= len(packages):
            real_upper_border = len(packages)
        
        # collecting packages to send #
        packages_to_proceed = [
            packages.pop(0)
            for _ in range(0, real_upper_border)
        ]
    
        # proceeding packages and getting receipts #
        packages_to_proceed = receiver.proceed(packages=packages_to_proceed)
        
        # configuring window size / switching stages #
        if current_stage == 'EXP':
            success_sent, all_success = is_all_packages_success(packages_to_proceed)
            packages_sent += success_sent
            if all_success and current_window_size < config.CAPACITY:
                current_window_size *= 2
            else:
                #RTT = current_window_size
                current_window_size //= 2
                end_of_exp_stage = current_window_size
                current_stage = 'ADD'
                add_stage_window_size_history.clear()
                
        elif current_stage == 'ADD':
            success_sent, all_success = is_all_packages_success(packages_to_proceed)
            packages_sent += success_sent
            if all_success and current_window_size < config.CAPACITY:
                current_window_size += 1
                timeline += 1
            else:
                current_window_size //= 2
    
    print(f"Usage coeff: {packages_sent / (timeline * (config.CAPACITY))}")
    #print(f"Theoretical coeff: {math.sqrt(3/2)*(1/(math.sqrt(1 - config.SUCCESS_PROBABILITY)*config.CAPACITY))}")

    # plotting #
    # sns.set_style("whitegrid")
    plt.xlabel('RTT')
    plt.ylabel('Размер окна перегрузки')
    #plt.axhline(y=end_of_exp_stage, color='pink', linestyle='--')
    #plt.axhline(y=config.CAPACITY, color='purple', linestyle='--')
    #plt.legend(['End of exp. stage / Start of add. stage', 'Пропу'])
    plt.plot(window_size_history, 'purple')
    plt.title('TCP Модуляция медленного старта')
    plt.show()