import flet
import json


class Test(flet.SafeArea):
    def __init__(self, test_data: dict) -> None:
        super().__init__()
        self.test_data = test_data

    def on_test_finish_click(self, event: flet.ControlEvent) -> None:
        self.page.controls[1].visible = True
        self.parent.parent.parent.destroy_create_page()

    def build(self) -> None:
        self.content = flet.Column(
            controls=[
                flet.Text(str(self.test_data)),
                flet.TextButton(
                    text='Завершить тест',
                    on_click=self.on_test_finish_click
                )
            ],
        )
