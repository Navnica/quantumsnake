import flet


class SettingsFragment(flet.SafeArea):
    def reload(self) -> None:
        pass

    def build(self):
        color_seeds: dict[str, str] = {
            'deeppurple': 'Фиолетовый',
            'indigo': 'Индиго',
            'blue': 'Голубой',
            'teal': 'Бирюзовый',
            'green': 'Зелёный',
            'yellow': 'Жёлтый',
            'orange': 'Оранжевый',
            'deeporange': 'Закат',
            'pink': 'Розовый'
        }

        self.content = flet.Column(
            controls=[
                flet.Container(
                    bgcolor=flet.colors.SURFACE_VARIANT,
                    border_radius=10,
                    padding=10,
                    content=flet.Column(
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        controls=[
                            flet.Text(value="Тема приложения"),
                            flet.Divider(height=10),
                            flet.GridView(
                                runs_count=3,
                                expand=False,
                                controls=[
                                    flet.FilledButton(
                                        width=10,
                                        style=flet.ButtonStyle(
                                            bgcolor=color_key,
                                            shape=flet.RoundedRectangleBorder(radius=10)
                                        )
                                    ) for color_key in color_seeds
                                ]
                            )
                        ]
                    )
                )
            ]
        )