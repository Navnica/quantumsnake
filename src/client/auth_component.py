import flet
import requests
import asyncio
from settings import SETTINGS


class AuthComponent(flet.SafeArea):
    def reload(self) -> None:
        pass

    def build(self) -> None:
        def set_connection_info(fail: bool) -> None:
            color: str = flet.colors.GREEN if not fail else flet.colors.RED
            text: str = 'Успешно' if not fail else 'Не удалось'

            self.content.controls[-1].color = color
            self.content.controls[-1].value = text
            self.content.controls[0].controls[-1].content = flet.Icon(
                name=flet.icons.DONE if not fail else flet.icons.PRIORITY_HIGH, color=color)
            self.content.controls[0].controls[0].value = 1

            self.content.controls[0].controls[0].color = color

        def end_animate(event: flet.ControlEvent) -> None:
            if self.page.session.get('auth'):
                self.page.session.get('create_pages')()
                return

            self.content = auth_content
            self.opacity = 1
            self.update()

        async def check_connection():
            await asyncio.sleep(3)
            if requests.get(SETTINGS.SERVER_URL).status_code == 200:
                set_connection_info(fail=False)
                self.page.loop.create_task(start_animation())

            else:
                set_connection_info(fail=True)

            self.update()

        async def start_animation() -> None:
            await asyncio.sleep(1)
            self.opacity = 0
            self.update()

        async def on_login_click(event: flet.ControlEvent) -> None:
            login_text_field: flet.TextField = auth_content.controls[0].content.controls[0]
            password_text_field: flet.TextField = auth_content.controls[0].content.controls[1]

            if login_text_field.value == '' or password_text_field.value == '':
                if login_text_field.value == '':
                    login_text_field.error_text = 'Поле пусто'

                if password_text_field.value == '':
                    password_text_field.error_text = 'Поле пусто'

            else:
                response: requests.Response = requests.post(
                    url=SETTINGS.SERVER_URL + '/user_auth/login',
                    json={
                        'username': login_text_field.value,
                        'password': password_text_field.value,
                    },
                    params={'token': SETTINGS.TOKEN}
                )

                match response.status_code:
                    case 200:
                        if response.json():
                            self.page.session.set('auth', True)
                            self.page.session.set('username', login_text_field.value)
                            self.opacity = 0

                        else:
                            login_text_field.error_text = 'Неверное имя пользователя или пароль'

                    case 401:
                        pass

            self.page.update()

        async def on_registration_click(event: flet.ControlEvent) -> None:
            if not auth_content.controls[0].content.controls[2].visible:
                auth_content.controls[0].content.controls[2].visible = True
                auth_content.controls[0].content.controls[4].visible = False
                self.update()
                return

            login_text_field: flet.TextField = auth_content.controls[0].content.controls[0]
            password_text_field: flet.TextField = auth_content.controls[0].content.controls[1]
            confirm_password_text_field: flet.TextField = auth_content.controls[0].content.controls[2]

            if (
                    login_text_field.value == '' or
                    password_text_field.value == '' or
                    confirm_password_text_field.value == '' or
                    password_text_field.value != confirm_password_text_field.value
            ):
                if login_text_field.value == '':
                    login_text_field.error_text = 'Поле пусто'

                if password_text_field.value == '':
                    password_text_field.error_text = 'Поле пусто'

                if confirm_password_text_field.value == '':
                    confirm_password_text_field.error_text = 'Поле пусто'

                elif password_text_field.value != confirm_password_text_field.value:
                    confirm_password_text_field.error_text = 'Пароли не совпадают'

            else:
                response: requests.Response = requests.post(
                    url=SETTINGS.SERVER_URL + '/user_auth/register',
                    json={
                        'username': login_text_field.value,
                        'password': password_text_field.value,
                    },
                    params={'token': SETTINGS.TOKEN}
                )

                match response.status_code:
                    case 200:
                        self.page.session.set('username', login_text_field.value)
                        self.page.session.set('auth', True)
                        self.opacity = 0

                    case 409:
                        login_text_field.error_text = 'Имя пользователя занято'

            self.page.update()

        self.animate_opacity = flet.Animation(duration=200)
        self.on_animation_end = end_animate

        start_content: flet.Column = flet.Column(
            alignment=flet.MainAxisAlignment.CENTER,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Stack(
                    width=70,
                    height=70,
                    alignment=flet.alignment.center,
                    controls=[
                        flet.ProgressRing(
                            width=70,
                            height=70
                        ),

                        flet.Container(
                            alignment=flet.alignment.center,
                            content=flet.Icon(name=flet.icons.MORE_HORIZ)
                        )
                    ]
                ),

                flet.Divider(height=20, color=flet.colors.with_opacity(0, flet.colors.GREEN)),
                flet.Text(value='Подключение к серверу')

            ]
        )

        auth_content: flet.Column = flet.Column(
            alignment=flet.MainAxisAlignment.END,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Container(
                    border_radius=10,
                    padding=10,
                    bgcolor=flet.colors.SURFACE_VARIANT,
                    content=flet.Column(
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        controls=[
                            flet.TextField(
                                label='Имя пользователя',
                                border_radius=10,
                                border_width=2,
                                border_color=flet.colors.PRIMARY,
                            ),

                            flet.TextField(
                                label='Пароль',
                                password=True,
                                can_reveal_password=True,
                                border_radius=10,
                                border_width=2,
                                border_color=flet.colors.PRIMARY
                            ),

                            flet.TextField(
                                label='Повторение пароля',
                                password=True,
                                can_reveal_password=True,
                                border_radius=10,
                                border_width=2,
                                border_color=flet.colors.PRIMARY,
                                animate_opacity=flet.Animation(duration=200),
                                visible=False
                            ),

                            flet.Divider(height=20, color=flet.colors.PRIMARY),
                            flet.FilledButton(
                                text='Войти',
                                on_click=on_login_click,
                                width=150
                            ),

                            flet.TextButton(
                                text='Регистрация',
                                on_click=on_registration_click
                            )
                        ]
                    )
                )

            ]
        )

        self.content = start_content
        self.page.loop.create_task(check_connection())
