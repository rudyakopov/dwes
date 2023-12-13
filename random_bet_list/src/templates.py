def render_templates(template_name: str, context: dict = {}) -> str:
    html_str = ""
    with open(template_name, "r", encoding="utf-8") as file:
        html_str = file.read()

    html_str = html_str.format(**context)

    return html_str
