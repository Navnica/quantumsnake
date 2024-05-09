import flet
from settings import SETTINGS
import requests


class SettingsComponent(flet.SafeArea):
    def reload(self) -> None:
        pass

    def on_role_edit_click(self, event: flet.ControlEvent):
        self.content.controls[2].content.controls[1].controls[0].read_only = False
        self.content.controls[2].content.controls[1].controls[0].focus()
        self.page.update()

    async def on_submit_role_click(self, event: flet.ControlEvent):
        all_role_response: requests.Response = requests.get(
            url=f'{SETTINGS.SERVER_URL}/role/get_all',
            params={'token': SETTINGS.TOKEN}
        )

        new_role_id = 0

        for role in all_role_response.json():
            if role['access_code'] == self.content.controls[2].content.controls[1].controls[0].value:
                new_role_id = role['id']

        if new_role_id != 0:
            user_response_get: requests.Response = requests.get(
                url=f'{SETTINGS.SERVER_URL}/user/get_by_username/{self.page.session.get("session").User.username}',
                params={'token': SETTINGS.TOKEN}
            )

            data: dict = user_response_get.json()
            data['role_id'] = new_role_id

            requests.put(
                url=f'{SETTINGS.SERVER_URL}/user/update/{user_response_get.json()["id"]}',
                params={'token': SETTINGS.TOKEN},
                json=data
            )

            self.content.controls[2].content.controls[3].value = 'Роль обновлена'
            self.content.controls[2].content.controls[3].color = flet.colors.GREEN
            self.content.controls[2].content.controls[0].controls[0].read_only = True

        else:
            self.content.controls[2].content.controls[3].value = 'Роль не найдена'
            self.content.controls[2].content.controls[3].color = flet.colors.RED

        self.page.update()

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
            scroll=flet.ScrollMode.AUTO,
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
                            flet.Text(value=f'Имя: {self.page.session.get("session").User.username}'),
                            flet.Text(value=f'ID: {self.page.session.get("session").User.identification}')
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
                                    flet.Text(
                                        value="Тема приложения",
                                        color=flet.colors.PRIMARY,
                                        weight=flet.FontWeight.BOLD
                                    ),
                                    flet.Icon(name=flet.icons.PALETTE)
                                ]
                            ),
                            color_column
                        ]
                    )
                ),

                flet.Container(
                    visible=SETTINGS.DEBUG,
                    bgcolor=flet.colors.SURFACE_VARIANT,
                    border_radius=10,
                    padding=10,
                    content=flet.Column(
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        controls=[
                            flet.Row(
                                alignment=flet.MainAxisAlignment.CENTER,
                                controls=[
                                    flet.Text(
                                        value='Отладка',
                                        color=flet.colors.PRIMARY,
                                        weight=flet.FontWeight.BOLD
                                    ),
                                    flet.Icon(name=flet.icons.BUG_REPORT)
                                ]
                            ),

                            flet.Row(
                                alignment=flet.MainAxisAlignment.CENTER,
                                controls=[
                                    flet.TextField(
                                        label='Код роли',
                                        value=self.page.session.get("session").Role.access_code,
                                        read_only=True,
                                        text_align=flet.TextAlign.CENTER,
                                        can_reveal_password=True,
                                        border_radius=10,
                                        border_width=2,
                                        border_color=flet.colors.PRIMARY,
                                        height=45,
                                        dense=True
                                    ),

                                    flet.IconButton(
                                        icon=flet.icons.EDIT,
                                        icon_color=flet.colors.SURFACE_VARIANT,
                                        on_click=self.on_role_edit_click,
                                        style=flet.ButtonStyle(
                                            bgcolor=flet.colors.PRIMARY,
                                            shape=flet.RoundedRectangleBorder(radius=10),
                                        )
                                    )
                                ]
                            ),

                            flet.FilledButton(
                                text='Применить',
                                on_click=self.on_submit_role_click
                            ),

                            flet.Text(
                                value='Потребуется перезапуск'
                            )
                        ]
                    )
                ),

            ]
        )
