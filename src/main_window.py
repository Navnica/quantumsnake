import flet


class MainWindow(flet.UserControl):
    def __init__(self) -> None:
        super().__init__()

    def build(self):
        self.learning_container: flet.Container = flet.Container(
            content=flet.Column(
                controls=[
                    flet.Row(
                        controls=[
                            flet.IconButton(
                                icon=flet.icons.ABC,
                                icon_size=40,
                                icon_color=flet.colors.GREY,
                                style=flet.ButtonStyle(
                                    shape=flet.RoundedRectangleBorder(radius=13),
                                    bgcolor=flet.colors.GREY_800
                                ),
                                on_click=self.on_abc_click
                            ),
                            flet.IconButton(
                                icon=flet.icons.MENU_BOOK,
                                icon_size=40,
                                icon_color=flet.colors.GREY,
                                style=flet.ButtonStyle(
                                    shape=flet.RoundedRectangleBorder(radius=13),
                                    bgcolor=flet.colors.GREY_800
                                )
                            ),
                        ],
                        alignment=flet.MainAxisAlignment.CENTER,
                    ),

                    flet.Row(
                        controls=[
                            flet.IconButton(
                                icon=flet.icons.ASSIGNMENT_RETURNED,
                                icon_size=40,
                                icon_color=flet.colors.GREY,
                                style=flet.ButtonStyle(
                                    shape=flet.RoundedRectangleBorder(radius=13),
                                    bgcolor=flet.colors.GREY_800
                                )
                            )
                        ],
                        alignment=flet.MainAxisAlignment.CENTER
                    ),
                ],
                alignment=flet.MainAxisAlignment.CENTER,
            ),
            bgcolor=flet.colors.TRANSPARENT,
            alignment=flet.alignment.center,
            border_radius=15,
        )

        self.abc_container = flet.Container(
            content=flet.Text("ABC"),
            visible=False
        )

        self.navigation_bar: flet.Container = flet.Container(
            content=flet.NavigationBar(
                destinations=[
                    flet.NavigationDestination(icon=flet.icons.SCHOOL, label='Обучение'),
                    flet.NavigationDestination(icon=flet.icons.OFFLINE_PIN, label='Тесты'),
                    flet.NavigationDestination(icon=flet.icons.BOOK, label='База знаний')
                ],
                on_change=self.on_destination_change,
                bgcolor=flet.colors.TRANSPARENT,
            ),
            bgcolor=flet.colors.GREY_900,
            border_radius=15,
            margin=flet.Margin(0, 20, 0, 0)
        )

        return (flet.Column(
            controls=[
                self.learning_container,
                self.abc_container,
                self.navigation_bar
            ],
        ))

    def on_abc_click(self, event: flet.ControlEvent) -> None:
        self.learning_container.visible = False
        self.abc_container.visible = True
        self.learning_container.update()
        self.abc_container.update()

    def on_destination_change(self, event: flet.ControlEvent) -> None:
        if int(event.data) == 0:
            if not self.learning_container.visible:
                self.learning_container.visible = True
                self.abc_container.visible = False
                self.learning_container.update()
                self.abc_container.update()
