import flet


class TestsComponent(flet.UserControl):
    def __init__(self) -> None:
        super().__init__()

    def build(self) -> None:
        self.visible = False
        return flet.Text("TestsComponent")

    def reload(self) -> None:
        pass