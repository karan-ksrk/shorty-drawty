import flet as ft
import socket

server_address = ('192.168.1.10', 5000)

# Function to be called when the custom button is clicked
def custom_button_click(e, macro_input):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)
        client_socket.sendall(macro_input.encode('utf-8'))
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")

# Function to handle delete button click
def delete_button_click(e, button, button_grid, cupertino_alert_dialog):
    button_row = button.parent
    button_row.controls.remove(button)
    # Remove empty rows if any
    if not button_row.controls:
        button_grid.controls.remove(button_row)
    cupertino_alert_dialog.open = False
    e.control.page.update()

def dismiss_dialog(e, cupertino_alert_dialog):
    cupertino_alert_dialog.open = False
    e.control.page.update()

def show_dialog_action(e, button, button_grid):
    cupertino_alert_dialog = ft.CupertinoAlertDialog(
        # title=ft.Text("Cupertino Alert Dialog"),
        # content=ft.Text("Do you want to delete this file?"),
        actions=[
            ft.CupertinoDialogAction(
                "Delete", is_destructive_action=True, on_click=lambda e: delete_button_click(e, button, button_grid, cupertino_alert_dialog)
            ),
            ft.CupertinoDialogAction(
                text="Cancel", on_click=lambda e: dismiss_dialog(e, cupertino_alert_dialog),
            ),
        ],
    )
    e.control.page.dialog = cupertino_alert_dialog
    cupertino_alert_dialog.open = True
    e.control.page.update()


# Function to create a new custom button with specified properties
def add_custom_button(e, page, macro_input, color_input, button_grid):
    button_color = color_input.value
    macro_keys = macro_input.value

    if not macro_input and not button_color:
        print("Please provide macro and color for the button.")
        return
    
    new_button = ft.TextButton(
       text="",
       width=100,
       height=100,
       on_click=lambda e: custom_button_click(e, macro_keys),
       on_long_press=lambda e: show_dialog_action(e, new_button, button_grid),
       style=ft.ButtonStyle(
           bgcolor=button_color,
           shape=ft.RoundedRectangleBorder(radius=2),
       )
       
    )
    last_row = button_grid.controls[-1] if  button_grid.controls else None

    if last_row and len(last_row.controls) < 3:
        last_row.controls.append(new_button)
    else:
        new_row = ft.Row(controls=[new_button], alignment=ft.MainAxisAlignment.SPACE_AROUND)
        button_grid.controls.append(new_row)

    page.update()



# Main function to create the Flet app
def main(page: ft.Page):
    page.title = "Shorty Drawty"

    macro_input = ft.TextField(
        hint_text="Enter macro (e.g., 'ctr + l')",
        width=100
    )
    color_input = ft.TextField(
        hint_text="Enter button color (e.g., 'red')",
        width=100
    )
    
    add_button = ft.IconButton(
        icon=ft.icons.ADD_CIRCLE_ROUNDED,
        icon_color="blue400",
        icon_size=50,
        tooltip="Pause record",
        on_click=lambda e: add_custom_button(e, page, macro_input,  color_input, button_grid),
    )

    button_grid = ft.Column()
    
    # Layout the input fields and the "Add Custom Button" button vertically
    input_row =  ft.Row(
        controls=[macro_input, color_input, add_button],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.END,
        expand=True
        )

    # page.add(input_row, button_grid)


    # Create a column to hold the input row at the top and the button grid below
    layout = ft.Column(
        controls=[button_grid, input_row],
        alignment=ft.MainAxisAlignment.START,
        expand=True
    )

    page.add(layout)

# Run the Flet app
ft.app(target=main)
