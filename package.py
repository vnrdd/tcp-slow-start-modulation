class Package:

    def __init__(self, data, id) -> None:
        self.id = id
        self.data = data
        self.receipt = False
        
    def fill_receipt(self, receipt) -> None:
        self.receipt = receipt
    
    