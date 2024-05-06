import flet


class TestCreateFragment(flet.SafeArea):
    def __init__(self, par: flet.SafeArea) -> None:
        super().__init__()
        self.par = par

    def build(self):
        self.content = flet.Column(
            controls=[
                flet.Row(
                    alignment=flet.MainAxisAlignment.START,
                    controls=[
                        flet.IconButton(
                            icon=flet.icons.ARROW_BACK,
                            on_click=lambda _: self.par.switch_container(self.par.content.controls[0])
                        )
                    ]
                )
            ]
        )
