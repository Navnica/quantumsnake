import flet


class DictFragment(flet.Column):
    def build(self) -> None:
        self.controls.extend([
            flet.Text('Dict Fragment')
        ])
