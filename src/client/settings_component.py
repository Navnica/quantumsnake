import flet
from src.database.models import UserAuth


class SettingsComponent(flet.SafeArea):
    def reload(self) -> None:
        pass

    def build(self):
        def on_theme_click(event: flet.ControlEvent) -> None:
            self.page.theme = flet.Theme(color_scheme_seed=event.control.data)
            self.page.update()

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

        color_column: flet.Column = flet.Column()
        new_row: flet.Row = flet.Row(alignment=flet.MainAxisAlignment.CENTER)

        for color in color_seeds:
            new_row.controls.append(
                flet.FilledButton(
                    width=50,
                    height=50,
                    data=color,
                    on_click=lambda _: on_theme_click(_),
                    style=flet.ButtonStyle(
                        bgcolor=color,
                        shape=flet.RoundedRectangleBorder(radius=10),
                    )
                )
            )

            if len(new_row.controls) == 3:
                color_column.controls.append(new_row)
                new_row: flet.Row = flet.Row(alignment=flet.MainAxisAlignment.CENTER)

        color_column.controls.append(new_row)

        self.content = flet.Column(
            controls=[
                flet.Container(
                    bgcolor=flet.colors.SURFACE_VARIANT,
                    border_radius=10,
                    padding=10,
                    content=flet.Column(
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        controls=[
                            flet.Row(
                                alignment=flet.MainAxisAlignment.CENTER,
                                controls=[
                                    flet.Text(value="Аккаунт", color=flet.colors.PRIMARY,
                                              weight=flet.FontWeight.BOLD),
                                    flet.Icon(name=flet.icons.ACCOUNT_CIRCLE)
                                ]
                            ),
                            flet.Text(value=self.page.session.get('username')),
                            flet.Text(color='red', value='Ошибка загрузки')
                        ]
                    )
                ),

                flet.Container(
                    bgcolor=flet.colors.SURFACE_VARIANT,
                    border_radius=10,
                    padding=10,
                    content=flet.Column(
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        controls=[
                            flet.Row(
                                alignment=flet.MainAxisAlignment.CENTER,
                                controls=[
                                    flet.Text(value="Тема приложения", color=flet.colors.PRIMARY,
                                              weight=flet.FontWeight.BOLD),
                                    flet.Icon(name=flet.icons.PALETTE)
                                ]
                            ),
                            color_column
                        ]
                    )
                ),

            ]
        )
