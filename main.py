import flet

import settings
from src.client.auth_component import AuthComponent
from src.client.tests_component import TestsComponent
from src.client.database_component import DatabaseComponent
from src.client.learning_component import LearningComponent
from src.client.settings_component import SettingsComponent
from settings import SETTINGS


def main(page: flet.Page) -> None:
    # Page settings

    page.title = "QuantumSnake"
    page.window_height = 650
    page.window_width = 450
    page.vertical_alignment = flet.MainAxisAlignment.END
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER

    # Defs

    def change_page(event: flet.ControlEvent, require_page: int = None) -> None:
        require_page = int(event.data) if not require_page else require_page

        for pg in page.controls[0].content.controls:
            pg.visible = False
            pg.content.reload()

        page.controls[0].content.controls[int(require_page)].visible = True

        page.update()

    def create_pages() -> None:
        page.controls[0].content.controls.clear()
        page.controls[1].visible = True

        page.controls[0].content.controls.extend([
            flet.Container(
                content=LearningComponent(),
                visible=True,
                expand=True,
            ),
            flet.Container(
                content=TestsComponent(),
                visible=False,
                expand=True
            ),
            flet.Container(
                content=DatabaseComponent(),
                visible=False,
                expand=True
            ),
            flet.Container(
                content=SettingsComponent(),
                visible=False,
                expand=True
            ),
        ])

        page.update()

    # Variables

    page.session.set('change_page', change_page)
    page.session.set('create_pages', create_pages)

    page.add(
        flet.Container(
            expand=True,
            content=flet.Column(
                controls=[
                    flet.Container(
                        content=AuthComponent(),
                        visible=True,
                        expand=True,
                        animate_opacity=300
                    )
                ]
            )
        ),
        flet.Container(
            visible=False,
            border_radius=10,
            content=flet.NavigationBar(
                destinations=[
                    flet.NavigationDestination(icon=flet.icons.SCHOOL, label='Обучение'),
                    flet.NavigationDestination(icon=flet.icons.OFFLINE_PIN, label='Тесты'),
                    flet.NavigationDestination(icon=flet.icons.BOOK, label='База знаний'),
                    flet.NavigationDestination(icon=flet.icons.SETTINGS, label='Настройки')
                ],
                on_change=change_page
            )
        )
    )


if __name__ == '__main__':
    flet.app(main)
