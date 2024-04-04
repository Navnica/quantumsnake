import flet


class DataBaseComponent(flet.UserControl):
    def __init__(self) -> None:
        super().__init__()

    def build(self):
        self.visible = False

        self.search_bar: flet.Container = flet.Container(
            content=flet.SearchBar(),
            padding=flet.Padding(0, 30, 0, 0)
        )

        return self.search_bar

    def reload(self) -> None:
        pass