import flet


class GrammarFragment(flet.Column):
    def build(self) -> None:
        self.controls.extend([
            flet.Text('Grammar Fragment')
        ])
