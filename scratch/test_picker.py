import flet as ft
import os

def main(page: ft.Page):
    page.title = "FilePicker Test"
    
    # Let's test different ways of registering FilePicker
    picker = ft.FilePicker()
    
    # Option 1: Append to overlay immediately before page is shown
    page.overlay.append(picker)
    
    def on_click(e):
        picker.get_directory_path()
        
    btn = ft.ElevatedButton("Pick Directory", on_click=on_click)
    page.add(btn)

if __name__ == "__main__":
    os.environ["FLET_WEB_PORT"] = "8560"
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8560)
