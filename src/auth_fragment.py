import flet
import requests
import time
import asyncio
from settings import SETTINGS


class AuthFragment(flet.SafeArea):
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

        async def check_connection():
            await asyncio.sleep(2)
            if requests.get(SETTINGS.SERVER_URL).status_code == 200:
                set_connection_info(fail=False)

            else:
                set_connection_info(fail=True)

            self.update()

        self.content = flet.Column(
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

        self.page.loop.create_task(check_connection())
