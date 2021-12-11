import config
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from package import Package
from receiver import Receiver

packages = [Package(data=f'test{id}', id=id)
            for id in range(config.PACKAGES_COUNT)]

receiver = Receiver()

def is_all_packages_success(packages):
    for package in packages:
        if package.receipt == False:
            return False
    return True

# modulation #
if __name__ == '__main__':
    current_window_size = config.START_WINDOW_SIZE
    window_size_history = []
    packages_proceeded = 0

    current_stage = 'EXP'
    end_of_exp_stage = 0
    
    while packages:
        window_size_history.append(current_window_size)
        upper_border_prediction = current_window_size
        
        real_upper_border = upper_border_prediction
        
        if real_upper_border >= len(packages):
            real_upper_border = len(packages)
        

        packages_to_proceed = [
            packages.pop(0)
            for _ in range(0, real_upper_border)
        ]
    
        packages_to_proceed = receiver.proceed(packages=packages_to_proceed)
        packages_proceeded += len(packages_to_proceed)

        if current_stage == 'EXP':
            if is_all_packages_success(packages_to_proceed) and current_window_size != config.OVERFLOW_WINDOW_SIZE:
                current_window_size *= 2
            else:
                current_window_size //= 2
                end_of_exp_stage = current_window_size
                current_stage = 'ADD'
                
        elif current_stage == 'ADD':
            if is_all_packages_success(packages_to_proceed) and current_window_size != config.OVERFLOW_WINDOW_SIZE:
                current_window_size += 1
            else:
                current_window_size //= 2
    

    # plotting #
    sns.set_style("whitegrid")
    plt.xlabel('Timeline (RTT)')
    plt.ylabel('Congestion window size')
    plt.axhline(y=end_of_exp_stage, color='r', linestyle='--')
    plt.axhline(y=config.OVERFLOW_WINDOW_SIZE, color='g', linestyle='--')
    plt.legend(['End of exp. stage / Start of add. stage', 'Capacity'])
    plt.plot(window_size_history, 'b')
    plt.title('TCP Slow start modulation')
    plt.show()