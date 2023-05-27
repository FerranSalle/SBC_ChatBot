laptops = []


class Laptop:
    def __init__(self, manufacture, model, category, price, processor, ram, screen_size, storage, graphics, os, weight):
        self.manufacture = manufacture
        self.model = model
        self.category = category
        self.price = float(price.replace(",", ".")) if price != "N/A" else 0
        self.processor = processor
        self.ram = float(ram.replace("GB", ""))
        self.screen_size = float(screen_size.replace("\"", ""))
        if 'MB' in storage.split(" ")[0]:
            self.storage = float(storage.split(" ")[0].replace("MB", "")) * 1000.0
        elif 'TB' in storage.split(" ")[0]:
            self.storage = float(storage.split(" ")[0].replace("TB", "")) * 1000000.0
        else:
            self.storage = float(storage.split(" ")[0].replace("GB", ""))
        self.storage_type = storage.split(" ")[1]
        self.graphics = graphics
        self.os = os
        self.weight = weight.replace('kgs', '').replace('kg', '')

    def __str__(self):
        if self.storage >= 1000000.0:
            show_storage = str(self.storage / 1000000.0) + "TB"
        elif self.storage >= 1000.0:
            show_storage = str(self.storage / 10000.0) + "MB"
        else:
            show_storage = str(self.storage) + "GB"
        return "Manufacture: " + self.manufacture + "\nModel: " + self.model + "\nCategory: " + self.category + "\nPrice: " + str(
            self.price) + "\nProcessor: " + self.processor + "\nRAM: " + str(self.ram) + "GB\nScreen Size: " + str(
            self.screen_size) + "\nStorage: " + show_storage + " type: " + self.storage_type + "\nGraphics: " + self.graphics + "\nOS: " + self.os + "\nWeight: " + self.weight


def create_list_of_laptops(dataset):
    for index, row in dataset.iterrows():
        laptops.append(Laptop(row['Manufacturer'], row['Model Name'], row['Category'], row['Price (Euros)'], row['CPU'],
                              row['RAM'], row['Screen Size'], row[' Storage'], row['GPU'], row['Operating System'],
                              row['Weight']))
