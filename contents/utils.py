import os 
from pathlib import Path
from datetime import datetime
import markdown
from flask import flash

BASE_DIR = Path(__file__).resolve().parent

def get_env_vars(name, default):
    env = os.getenv(name)
    if not env:
        if not default:
            raise ValueError(f"{name} is not set")
        return default
    return env


def get_form_errors(form):
    for _, errors in form.errors.items():
        for error in errors:
            flash(error, "danger")


def inject_current_year():
    return {"year": datetime.now().year}


def format_markdown(content):
    html_content = markdown.markdown(content)
    styled_content = html_content.replace("<h1>", '<h1 class="text-3xl font-bold text-cyan-600 py-3">')
    styled_content = styled_content.replace("<h2>", '<h2 class="text-2xl font-bold text-cyan-600 py-3">')
    styled_content = styled_content.replace("<h3>", '<h3 class="text-xl font-bold text-cyan-600 py-3">')
    styled_content = styled_content.replace("<h4>", '<h4 class="text-lg font-bold text-cyan-600 py-3">')
    styled_content = styled_content.replace("<h5>", '<h5 class="text-md font-bold text-cyan-600 py-3">')
    styled_content = styled_content.replace("<h6>", '<h6 class="text-sm font-bold text-cyan-600 py-3">')
    styled_content = styled_content.replace("<ul>", '<ul class="list-disc list-inside pl-4 ml-4">')
    styled_content = styled_content.replace("<ol>", '<ol class="list-decimal list-inside pl-4">')
    styled_content = styled_content.replace("<li>", '<li class="my-2">')
    styled_content = styled_content.replace("<p>", '<p class="my-3">')
    styled_content = f'<div class="prose lg:prose-xl">{styled_content}</div>'
    return styled_content


