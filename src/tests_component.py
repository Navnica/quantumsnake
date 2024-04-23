import flet


class TestsComponent(flet.Column):
    def reload(self) -> None:
        pass

    def build(self):
        self.controls.append(
            flet.Text('TestsComponent')
        )
