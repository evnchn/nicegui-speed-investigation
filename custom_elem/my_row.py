from nicegui.element import Element


class MyRow(Element, component='my_row.js'):

    def __init__(self, *, texts=[], bools=[]) -> None:
        super().__init__()
        self._props["texts"] = texts
        self._props["bools"] = bools
