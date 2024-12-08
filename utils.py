import uuid

class Utils:
    @staticmethod
    def generate_key(prefix: str = "chart"):
        return f"{prefix}_{uuid.uuid4().hex}"
