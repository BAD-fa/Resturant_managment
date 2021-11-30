import pickle


class BaseQuery:

    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def load(self):
        with open(self.file_path, "rb+") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break

    def get(self, query_params, query_value):
        for elm in self.load():
            if getattr(elm, query_params) == query_value:
                return elm
        return None

    def filter(self):
        pass

    def exist(self, query_params, query_value) -> bool:
        for elm in self.load():
            if getattr(elm, query_params) == query_value:
                return True
        return False
