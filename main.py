import flet
from flet import (
    Page, TextField, Text, Column, Container, Card,
    Colors, border_radius, Row, Icon, Icons, TextStyle
)
import re



def has_repeated_chars(password):
    return bool(re.search(r"(.)\1{2,}", password))

def has_sequential_chars(password):
    for i in range(len(password) - 2):
        if ord(password[i]) + 1 == ord(password[i + 1]) and ord(password[i + 1]) + 1 == ord(password[i + 2]):
            return True
    return False

def evaluate_password(password):
    return {
        "Length ≥ 12": len(password) >= 12,
        "Has Uppercase Letter": bool(re.search(r"[A-Z]", password)),
        "Has Lowercase Letter": bool(re.search(r"[a-z]", password)),
        "Has Digit": bool(re.search(r"\d", password)),
        "Has Special Character": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)),
        "No Repeated Characters": not has_repeated_chars(password),
        "No Sequential Characters": not has_sequential_chars(password)
    }


def main(page: Page):
    page.title = "Password Strength Checker"
    page.bgcolor = Colors.BLACK
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    
    password_input = TextField(
    label="Enter your password",
    password=True,
    can_reveal_password=True,
    border_radius=8,
    width=350,
    text_style=TextStyle(color=Colors.BLACK),
    label_style=TextStyle(color=Colors.BLACK),
    cursor_color=Colors.BLACK
)


    strength_feedback = Text("", size=18, weight="bold", color=Colors.BLACK)
    criteria_list = Column(spacing=5)

    # Password input logic
    def on_password_change(event):
        password = password_input.value
        criteria_results = evaluate_password(password)

        criteria_list.controls.clear()
        passed_count = 0

        for description, is_valid in criteria_results.items():
            icon = Icons.CHECK_CIRCLE if is_valid else Icons.CANCEL
            color = Colors.GREEN if is_valid else Colors.RED
            criteria_list.controls.append(
                Row([
                    Icon(name=icon, color=color),
                    Text(description, color=Colors.BLACK)
                ], spacing=10)
            )
            if is_valid:
                passed_count += 1

        
        total = len(criteria_results)
        if passed_count == total:
            strength_feedback.value = "✅ Strong Password"
            strength_feedback.color = Colors.GREEN
        elif passed_count >= total - 2:
            strength_feedback.value = "🟠 Medium Strength"
            strength_feedback.color = Colors.ORANGE
        else:
            strength_feedback.value = "❌ Weak Password"
            strength_feedback.color = Colors.RED

        page.update()

    password_input.on_change = on_password_change

  
    card_layout = Card(
        content=Container(
            content=Column([
                Text("Password Strength Checker", size=22, weight="bold", color=Colors.BLACK),
                password_input,
                strength_feedback,
                Text("Password must meet the following criteria:", weight="bold", size=16, color=Colors.BLACK),
                criteria_list
            ], spacing=20),
            padding=30,
            width=400,
            bgcolor=Colors.WHITE,
            border_radius=border_radius.all(12)
        ),
        elevation=12
    )

    page.add(card_layout)
    page.update()

flet.app(target=main)
