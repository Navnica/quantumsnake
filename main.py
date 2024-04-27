import flet
from src.tests_component import TestsComponent
from src.database_component import DatabaseComponent
from src.learning_component import LearningComponent
from src.settings_fragment import SettingsFragment


def main(page: flet.Page) -> None:
    # Page settings

    page.title = "QuantumSnake"
    page.window_height = 600
    page.window_width = 400
    page.vertical_alignment = flet.MainAxisAlignment.END
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER

    # Defs

    def change_page(event: flet.ControlEvent) -> None:
        for pg in pages:
            pg.visible = False
            pg.content.reload()

        pages[int(event.data)].visible = True

        page.update()

    # Variables

    pages: list = [
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
            content=SettingsFragment(),
            visible=False,
            expand=True
        )
    ]

    page.add(
        flet.Container(
            expand=True,
            content=flet.Column(
                controls=[pg for pg in pages],
            )
        ),
        flet.Container(
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
