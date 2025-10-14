from bs4 import BeautifulSoup
from .ai_client import ask_ai, get_ai_client
import asyncio

async def generate_form_data(html_content: str):
    """
    Parses form HTML and uses AI to generate dummy input values.
    """
    client = get_ai_client()
    soup = BeautifulSoup(html_content, "html.parser")

    forms_data = []
    for form in soup.find_all("form"):
        inputs = form.find_all(["input", "textarea", "select"])
        input_summary = "\n".join([
            f"Name: {i.get('name')} | Type: {i.get('type')} | Placeholder: {i.get('placeholder')}"
            for i in inputs if i.get("name")
        ])

        prompt = (
            "Generate realistic dummy data for the following form fields. "
            "Use generic, safe values (e.g., name='John Doe', email='john@example.com', etc.).\n\n"
            f"{input_summary}\n\nReturn as JSON {{'field_name': 'value'}}"
        )

        try:
            ai_response = await ask_ai(client, prompt)
            forms_data.append(ai_response)
        except Exception as e:
            forms_data.append(f"[AI ERROR] {e}")

    return forms_data
