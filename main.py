from src.main_window import MainWindow
import flet


def main(page: flet.Page):
    page.title = "QuantumSnake"
    page.window_height = 600
    page.window_width = 400
    page.vertical_alignment = flet.MainAxisAlignment.END
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
    main_window: MainWindow = MainWindow()
    page.add(main_window)

if __name__ == '__main__':
    flet.app(target=main)
