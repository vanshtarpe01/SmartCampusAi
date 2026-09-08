with open("app.py", "r") as f:
    content = f.read()

content = content.replace('''    from pages.career_analysis import render_career_analysis
        "💼 Career Analysis": render_career_analysis,''', '''        "💼 Career Analysis": render_career_analysis,''')

content = content.replace('''else:
    # Student Navigation Mapping''', '''else:
    # Student Navigation Mapping
    from pages.career_analysis import render_career_analysis''')

with open("app.py", "w") as f:
    f.write(content)
