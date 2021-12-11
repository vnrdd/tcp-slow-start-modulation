import config
from random import random


class Receiver:

    success_probability = config.SUCCESS_PROBABILITY

    def __init__(self) -> None:
        pass

    def generate_receipt(self) -> bool:
        return random() <= self.success_probability

    def proceed(self, packages) -> list:
        proceeded_packages = []
        
        for package in packages:
            package.fill_receipt(self.generate_receipt())
            proceeded_packages.append(package)
            
        return proceeded_packages
