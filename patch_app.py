with open("app.py", "r") as f:
    content = f.read()
content = content.replace('    from pages.notifications import render_notifications', '    from pages.notifications import render_notifications\\n    from pages.career_analysis import render_career_analysis')
with open("app.py", "w") as f:
    f.write(content)
