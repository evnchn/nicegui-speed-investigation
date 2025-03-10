from nicegui.element import Element


class MyRowSoftload(Element, component='my_row_softload.js'):

    def __init__(self, *, texts=[], bools=[]) -> None:
        super().__init__()
        self._props["texts"] = texts
        self._props["bools"] = bools
