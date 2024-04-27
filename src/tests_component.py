import flet


class TestsComponent(flet.SafeArea):
    def reload(self) -> None:
        pass

    def build(self):
        self.content = flet.Column(
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Stack(
                    width=150,
                    height=150,
                    controls=[
                        flet.ProgressRing(
                            value=1/4,
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
                flet.GridView(
                    runs_count=2,
                    max_extent=170,
                    controls=[
                        flet.Container(
                            bgcolor=flet.colors.SURFACE_VARIANT,
                            border_radius=15,
                            content=flet.Column(
                                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                alignment=flet.MainAxisAlignment.CENTER,
                                controls=[
                                    flet.Icon(name=flet.icons.EMOJI_EMOTIONS, size=55),
                                    flet.FilledButton(text='Эмоции')
                                ]
                            )
                        )
                    ]
                )
            ]
        )
