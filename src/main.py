import flet as ft

from pose_camera_view import PoseCameraView, PoseDataEvent, PushUpState

import flet_permission_handler as fph


async def main(page: ft.Page):
    page.title = "Pose Camera View"
    page.padding = 16

    def show_snackbar(message: str):
        page.show_dialog(ft.SnackBar(ft.Text(message)))

    counter = ft.Text("0", size=48, weight=ft.FontWeight.BOLD)
    state_text = ft.Text(PushUpState.NEUTRAL.value.upper(), size=18)
    ph = fph.PermissionHandler()

    async def request_permission(e):
        status = await ph.request(fph.Permission.CAMERA)
        show_snackbar(f"Requested camera permission: {status.name}")

    def handle_pose_data(e: PoseDataEvent):
        state_text.value = e.push_up_state.value.upper()

        if e.is_completed:
            counter.value = str(int(counter.value) + 1)

        page.update()


    page.add(
        ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=0,
                            controls=[
                                ft.Text("Push-ups", size=14),
                                counter,
                            ],
                        ),
                        state_text,
                    ],
                ),
                PoseCameraView(
                    expand=True,
                    elbow_angle_min=60.0,
                    elbow_angle_max=160.0,
                    on_pose_data=handle_pose_data,
                ),
            ],
        )
    )

    await request_permission(None)

    


ft.run(main)