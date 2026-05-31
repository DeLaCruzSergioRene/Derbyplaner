import flet as ft

UMAS = [
    "Air_Grove.png", "El_Condor_Pasa.png", "Daiwa_Scarlet.png", "GoldShip.png", 
    "Grass_Wonder.png", "Kitasan_Black.png", "Manhattan_Cafe.png", "Mejiro_Bright.png",
    "Mejiro_Dober.png", "Mejiro_McQueen.png", "Narita_Brian.png", "Oguri_Cap.png",
    "Silence_Suzuka.png", "Special_Week.png", "Señorita_CB.png", "Still_In_Love.png",
    "Sweep_Tosho.png", "Symboli_Rudolf.png", "Tokai_Teio.png", "Vodka.png"
]

def seleccion(page: ft.Page):
    def on_click_uma(e, uma_name):
        page.current_user['uma_seleccionada'] = uma_name
        print(f"Uma seleccionada: {uma_name}")
    
    def get_uma_label(filename):
        return filename.replace("_", " ").replace(".png", "")
    
    buttons = [
        ft.Container(
            content=ft.Column([
                ft.Text(get_uma_label(uma), size=18, weight="bold", color="#E438AB", text_align="center"),
                ft.Image(
                    src=f"assets/umamusumes/{uma}",
                    width=160,
                    height=160,
                    fit="contain"
                ),
            ], spacing=3, horizontal_alignment="center"),
            ink=True,
            on_click=lambda e, u=uma: on_click_uma(e, u)
        )
        for uma in UMAS
    ]
    
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Selecciona a tu corredora:", size=28, weight="bold", color="#744BB1", text_align="center"),
                ft.GridView(
                    controls=buttons,
                    runs_count=5,
                    spacing=10,
                    run_spacing=10,
                    expand=True,
                    auto_scroll=True,
                )
            ], spacing=20, expand=True),
            padding=15,
            expand=True
        )
    )