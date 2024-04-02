import flet


class DataBaseComponent(flet.UserControl):
    def __init__(self) -> None:
        super().__init__()

    def build(self) -> None:
        self.visible = False

        self.search_bar: flet.SearchBar = flet.SearchBar()

        return flet.Column(controls=[self.search_bar], alignment=flet.MainAxisAlignment.START)

    def reload(self) -> None:
        pass