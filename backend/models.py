# models.py

# Model definitions for the AI Dataset Simulator

class Model:
    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.data = []

    def add_data(self, data_point):
        self.data.append(data_point)

    def get_data(self):
        return self.data

class Dataset:
    def __init__(self, model):
        self.model = model
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_records(self):
        return self.records

# Example usage:
# model = Model('MyModel', '1.0')
# dataset = Dataset(model)