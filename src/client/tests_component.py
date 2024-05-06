import flet
from src.client.test_create_fragment import TestCreateFragment


class TestTile(flet.Container):
    icon_name: str
    button_text: str
    size: int

    def __init__(self, icon_name: str, button_text: str, size: int = 135) -> None:
        super().__init__()

        self.icon_name = icon_name
        self.button_text = button_text
        self.size = size

    def build(self) -> None:
        self.width = self.size
        self.height = self.size
        self.bgcolor = flet.colors.SURFACE_VARIANT
        self.border_radius = 10
        self.content = flet.Column(
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            alignment=flet.MainAxisAlignment.CENTER,
            controls=[
                flet.Icon(name=self.icon_name, size=55),
                flet.FilledButton(text=self.button_text)]
        )


class TestsComponent(flet.SafeArea):
    def __init__(self):
        super().__init__()

    def reload(self) -> None:
        pass

    def switch_container(self, container: flet.Container) -> None:
        for c in self.content.controls:
            c.visible = c == container

        self.page.update()

    def on_new_test_click(self, event: flet.ControlEvent) -> None:
        self.switch_container(self.content.controls[1])

    def build(self) -> None:
        self.content = flet.Column(
            controls=[
                flet.Container(
                    visible=True,
                    expand=True,
                    content=flet.Column(
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            flet.Stack(
                                width=150,
                                height=150,
                                controls=[
                                    flet.ProgressRing(
                                        value=0,
                                        bgcolor=flet.colors.SURFACE_VARIANT,
                                        width=150,
                                        height=150,
                                    ),
                                    flet.Container(
                                        alignment=flet.alignment.center,
                                        content=flet.Column(
                                            alignment=flet.MainAxisAlignment.CENTER,
                                            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                            controls=[
                                                flet.Text("Тестов пройдено", weight=flet.FontWeight.BOLD),
                                                flet.Text("0/4")
                                            ]
                                        ),
                                    )
                                ]
                            ),
                            flet.FilledButton(
                                text='Новый тест',
                                visible=self.page.session.get('session').Role.power_level > 1,
                                on_click=self.on_new_test_click
                            ),
                            flet.Divider(height=10),

                        ]
                    )
                ),
                flet.Container(
                    visible=False,
                    expand=True,
                    content=TestCreateFragment(par=self)
                )

            ]
        )
