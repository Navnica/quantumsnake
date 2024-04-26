import flet


class TestsComponent(flet.SafeArea):
    def reload(self) -> None:
        pass

    def build(self):
        self.content = flet.Column(
            scroll=flet.ScrollMode.ADAPTIVE,
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
                flet.GridView(
                    runs_count=2,
                    spacing=5,
                    expand=True,
                    controls=[
                        flet.ExpansionTile(
                            title=flet.Text("Эмоции"),
                            leading=flet.Icon(name=flet.icons.EMOJI_EMOTIONS),
                            collapsed_text_color=flet.colors.WHITE,
                            text_color=flet.colors.PRIMARY,
                            bgcolor=flet.colors.SURFACE_VARIANT,
                            shape=flet.RoundedRectangleBorder(radius=10),
                            collapsed_shape=flet.RoundedRectangleBorder(radius=10),
                            controls=[
                                flet.FilledButton(text="Пройти")
                            ],
                        ),

                        flet.ExpansionTile(
                            title=flet.Text("Ответы"),
                            leading=flet.Icon(name=flet.icons.QUESTION_ANSWER),
                            collapsed_text_color=flet.colors.WHITE,
                            text_color=flet.colors.PRIMARY,
                            bgcolor=flet.colors.SURFACE_VARIANT,
                            shape=flet.RoundedRectangleBorder(radius=10),
                            collapsed_shape=flet.RoundedRectangleBorder(radius=10),
                            controls=[
                                flet.FilledButton(text="Пройти")
                            ],
                        ),

                        flet.ExpansionTile(
                            title=flet.Text("Время"),
                            leading=flet.Icon(name=flet.icons.ACCESS_TIME_FILLED),
                            collapsed_text_color=flet.colors.WHITE,
                            text_color=flet.colors.PRIMARY,
                            bgcolor=flet.colors.SURFACE_VARIANT,
                            shape=flet.RoundedRectangleBorder(radius=10),
                            collapsed_shape=flet.RoundedRectangleBorder(radius=10),
                            controls=[
                                flet.FilledButton(text="Пройти")
                            ],
                        ),

                        flet.ExpansionTile(
                            title=flet.Text("Наречия"),
                            leading=flet.Icon(name=flet.icons.QUESTION_ANSWER),
                            collapsed_text_color=flet.colors.WHITE,
                            text_color=flet.colors.PRIMARY,
                            bgcolor=flet.colors.SURFACE_VARIANT,
                            shape=flet.RoundedRectangleBorder(radius=10),
                            collapsed_shape=flet.RoundedRectangleBorder(radius=10),
                            controls=[
                                flet.FilledButton(text="Пройти")
                            ],
                        ),
                    ]
                )
            ]
        )
