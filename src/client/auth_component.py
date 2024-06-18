import flet
import requests
import asyncio
from src.tools.session import Session
from settings import SETTINGS


class AuthComponent(flet.SafeArea):
    def reload(self) -> None:
        pass

    def build(self) -> None:
        def set_session(username: str) -> None:
            response_user = requests.get(
                url=f'{SETTINGS.SERVER_URL}/user/get_by_username/{username}',
                params={'token': SETTINGS.TOKEN}
            )

            response_role = requests.get(
                url=f'{SETTINGS.SERVER_URL}/role/get/{response_user.json()["role_id"]}',
                params={'token': SETTINGS.TOKEN}
            )

            files = [
                Session.VideoFiles.VideoFile(name=file['name'], tag=file['tag'])
                for file in requests.get(
                    url=f'{SETTINGS.SERVER_URL}/video_file/get_all',
                    params={'token': SETTINGS.TOKEN}
                ).json()
            ]

            session = Session(
                user=response_user.json(),
                role=response_role.json(),
                video_files=files
            )

            self.page.session.set('session', session)
            self.page.session.set('auth', True)
            self.opacity = 0

        def set_connection_info(fail: bool) -> None:
            color = flet.colors.GREEN if not fail else flet.colors.RED
            text = 'Успешно' if not fail else 'Не удалось'

            self.content.controls[2].color = color
            self.content.controls[2].value = text
            self.content.controls[0].controls[-1].content = flet.Icon(
                name=flet.icons.DONE if not fail else flet.icons.PRIORITY_HIGH, color=color)
            self.content.controls[0].controls[0].value = 1
            self.content.controls[4].visible = fail and SETTINGS.DEBUG

            self.content.controls[0].controls[0].color = color

        async def check_connection():
            await asyncio.sleep(3)
            response_status_code = 0

            try:
                response_status_code = requests.get(SETTINGS.SERVER_URL).status_code
            except requests.exceptions.ConnectionError:
                pass

            if response_status_code == 200:
                set_connection_info(fail=False)
                self.page.loop.create_task(start_animation())
            else:
                set_connection_info(fail=True)

            self.update()

        async def start_animation() -> None:
            await asyncio.sleep(1)
            self.opacity = 0
            self.update()

        def end_animation(event: flet.ControlEvent) -> None:
            if self.page.session.get('auth'):
                self.page.session.get('create_pages')()
                return

            self.content = auth_content
            self.opacity = 1
            self.update()

        async def on_login_click(event: flet.ControlEvent) -> None:
            login_text_field = auth_content.controls[0].content.controls[0]
            password_text_field = auth_content.controls[0].content.controls[1]

            if not login_text_field.value or not password_text_field.value:
                if not login_text_field.value:
                    login_text_field.error_text = 'Поле пусто'

                if not password_text_field.value:
                    password_text_field.error_text = 'Поле пусто'
            else:
                response = requests.post(
                    url=SETTINGS.SERVER_URL + '/user_auth/login',
                    json={
                        'username': login_text_field.value,
                        'password': password_text_field.value,
                    },
                    params={'token': SETTINGS.TOKEN}
                )

                if response.status_code == 200 and response.json():
                    set_session(login_text_field.value)
                else:
                    login_text_field.error_text = 'Неверное имя пользователя или пароль'

            self.page.update()

        async def on_registration_click(event: flet.ControlEvent) -> None:
            if not auth_content.controls[0].content.controls[2].visible:
                auth_content.controls[0].content.controls[2].visible = True
                auth_content.controls[0].content.controls[4].visible = False
                self.update()
                return

            login_text_field = auth_content.controls[0].content.controls[0]
            password_text_field = auth_content.controls[0].content.controls[1]
            confirm_password_text_field = auth_content.controls[0].content.controls[2]

            if (
                not login_text_field.value or
                not password_text_field.value or
                not confirm_password_text_field.value or
                password_text_field.value != confirm_password_text_field.value
            ):
                if not login_text_field.value:
                    login_text_field.error_text = 'Поле пусто'

                if not password_text_field.value:
                    password_text_field.error_text = 'Поле пусто'

                if not confirm_password_text_field.value:
                    confirm_password_text_field.error_text = 'Поле пусто'
                elif password_text_field.value != confirm_password_text_field.value:
                    confirm_password_text_field.error_text = 'Пароли не совпадают'
            else:
                response = requests.post(
                    url=SETTINGS.SERVER_URL + '/user_auth/register',
                    json={
                        'username': login_text_field.value,
                        'password': password_text_field.value,
                    },
                    params={'token': SETTINGS.TOKEN}
                )

                if response.status_code == 200:
                    set_session(login_text_field.value)
                elif response.status_code == 409:
                    login_text_field.error_text = 'Имя пользователя занято'

            self.page.update()

        async def on_connection_setting_click(event: flet.ControlEvent) -> None:
            def save_settings(event: flet.ControlEvent) -> None:
                SETTINGS.SERVER_URL = server_address_text_field.value
                SETTINGS.TOKEN = token_text_field.value

                self.page.dialog.open = False
                self.page.update()
                self.page.loop.create_task(check_connection())

            server_address_text_field = flet.TextField(
                label='Адрес сервера',
                value=SETTINGS.SERVER_URL,
                border_radius=10,
                border_width=2,
                border_color=flet.colors.PRIMARY,
            )

            token_text_field = flet.TextField(
                label='Токен',
                value=SETTINGS.TOKEN,
                border_radius=10,
                border_width=2,
                border_color=flet.colors.PRIMARY,
            )

            self.page.dialog = flet.AlertDialog(
                open=True,
                shape=flet.RoundedRectangleBorder(radius=10),
                content=flet.Column(
                    height=250,
                    alignment=flet.MainAxisAlignment.CENTER,
                    horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                    controls=[
                        server_address_text_field,
                        token_text_field,
                        flet.FilledButton(text='Сохранить', on_click=save_settings)
                    ]
                )
            )
            self.page.update()

        self.animate_opacity = flet.Animation(duration=200)
        self.on_animation_end = end_animation

        start_content = flet.Column(
            alignment=flet.MainAxisAlignment.CENTER,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Stack(
                    width=70,
                    height=70,
                    alignment=flet.alignment.center,
                    controls=[
                        flet.ProgressRing(width=70, height=70),
                        flet.Container(
                            alignment=flet.alignment.center,
                            content=flet.Icon(name=flet.icons.MORE_HORIZ)
                        )
                    ]
                ),
                flet.Divider(height=20, color=flet.colors.with_opacity(0, flet.colors.GREEN)),
                flet.Text(value='Подключение к серверу'),
                flet.Divider(height=20, color=flet.colors.with_opacity(0, flet.colors.GREEN)),
                flet.FilledButton(
                    text='Настройки подключения',
                    visible=False,
                    on_click=on_connection_setting_click
                )
            ]
        )

        auth_content = flet.Column(
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
