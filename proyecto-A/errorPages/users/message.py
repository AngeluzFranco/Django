class Message:
    def __init__(self, type: str, message: str, code: int, img: str = None):
        self.type = type
        self.message = message
        self.code = code
        self.img = img

    def __str__(self):
        img_info = f"(Imagen: {self.img})" if self.img else "(Sin imagen)"
        return f"[{self.type.upper()}] Código {self.code}: {self.message} {img_info}"

    def to_dict(self):
        return {
            "tipo": self.type,
            "mensaje": self.message,
            "codigo": self.code,
            "imagen": self.img
        }
