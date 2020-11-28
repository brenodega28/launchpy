from classes.ngrok import Ngrok


class Templates:
    ngrok = Ngrok

    @staticmethod
    def new(data):
        name = data.pop("template")

        return getattr(Templates, name)(**data)