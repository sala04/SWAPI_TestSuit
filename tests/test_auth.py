import json
from pathlib import Path
from conftest import app

def test_audit_credentials(app):
    users_to_test = ["standard_user", "locked_out_user", "problem_user", "performance_glitch_user", "error_user", "visual_user"]
    password_to_test = "secret_sauce"

    MainPath = Path(__file__).resolve().parent.parent
    FolderJson = MainPath / "test_data/auth.json"

    # Estructura del reporte
    report = {
        "username_ok": [],
        "username_nok": [],
        "password_used": password_to_test
    }

    for user in users_to_test:
        app.login.navigation()
        app.login.login(user, password_to_test)

        if "inventory.html" in app.page.url:
            report["username_ok"].append(user)
            app.page.goto("https://www.saucedemo.com/")
        else:
            report["username_nok"].append(user)

    with open(FolderJson, "w") as f:
        json.dump(report, f, indent=4)

    print("\n✅ Auditoría completada. Archivo 'auth.json' generado.")
