import flet


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
    def reload(self) -> None:
        pass

    def build(self) -> None:
        self.content = flet.Column(
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                flet.Stack(
                    width=150,
                    height=150,
                    controls=[
                        flet.ProgressRing(
                            value=1 / 4,
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
                                    flet.Text("1/4")
                                ]
                            ),
                        )
                    ]
                ),
                flet.Divider(height=10),
                flet.Row(
                    alignment=flet.MainAxisAlignment.SPACE_EVENLY,
                    controls=[
                        TestTile(
                            icon_name=flet.icons.EMOJI_EMOTIONS,
                            button_text='Эмоции'
                        ),

                        TestTile(
                            icon_name=flet.icons.QUESTION_ANSWER,
                            button_text='Ответы'
                        )
                    ]
                ),

                flet.Row(
                    alignment=flet.MainAxisAlignment.SPACE_EVENLY,
                    controls=[
                        TestTile(
                            icon_name=flet.icons.TIMER,
                            button_text='Времена'
                        ),

                        TestTile(
                            icon_name=flet.icons.RECORD_VOICE_OVER,
                            button_text='Наречия'
                        )
                    ]
                )
            ]
        )
