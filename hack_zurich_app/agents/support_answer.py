from typing import Union


class SupportAnswer:
    def __init__(self, answer: str, document_path: Union[str, None]):
        self.answer = answer
        self.document_path = document_path
