import flet
from src.learnin_component import LearningComponent


def main(page: flet.Page):
    pages: dict[int, flet.UserControl] = {
        0: LearningComponent()
    }

    def open_page(page_id: int) -> None:
        for pg in pages:
            pages[pg].visible = True if pg == page_id else False
            pages[pg].reload()
            pages[pg].update()

    def on_destination_change(event: flet.ControlEvent) -> None:
        open_page(int(event.data))

    page.title = "QuantumSnake"
    page.window_height = 600
    page.window_width = 400
    page.vertical_alignment = flet.MainAxisAlignment.END
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
    page.theme_mode = flet.ThemeMode.DARK

    navigation_bar: flet.NavigationBar = flet.NavigationBar(
        destinations=[
            flet.NavigationDestination(icon=flet.icons.SCHOOL, label='Обучение'),
            flet.NavigationDestination(icon=flet.icons.OFFLINE_PIN, label='Тесты'),
            flet.NavigationDestination(icon=flet.icons.BOOK, label='База знаний')
        ],
        on_change=on_destination_change,
        bgcolor=flet.colors.TRANSPARENT
    )

    page.add(
        flet.Container(
            pages[0],
            expand=True),
        flet.Container(
            content=navigation_bar,
            bgcolor=flet.colors.GREY_900,
            border_radius=15,
            margin=flet.Margin(0, 20, 0, 0)
        )
    )


if __name__ == '__main__':
    flet.app(target=main)
