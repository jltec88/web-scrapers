# unicef-scrapper.py
import asyncio
import os
import unicodedata
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from fpdf import FPDF
from bs4 import BeautifulSoup

load_dotenv()
URL = os.getenv("LANDING_URL")


def sanitize(text: str) -> str:
    """
    Normaliza caracteres Unicode a su forma decomposed y droppea
    todos los que no quepan en Latin-1.
    """
    nkfd = unicodedata.normalize("NFKD", text)
    return nkfd.encode("latin-1", "ignore").decode("latin-1")


class PDFGenerator:
    def __init__(self, title="Reporte UNICEF"):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_title(title)
        self.pdf.set_font("Arial", size=12)

    def add_heading(self, text):
        self.pdf.set_font("Arial", 'B', 14)
        self.pdf.cell(0, 10, txt=text, ln=True)
        self.pdf.ln(2)
        self.pdf.set_font("Arial", size=12)

    def add_paragraph(self, text):
        self.pdf.multi_cell(0, 10, txt=text)
        self.pdf.ln(1)

    def output(self, filename):
        self.pdf.output(filename)


async def extract_text(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(3000)
        html = await page.content()
        await browser.close()

    with open("debug_landing.html", "w", encoding="utf-8") as f:
        f.write(html)
        print("[DEBUG] HTML guardado en debug_landing.html")

    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main") or soup

    elements = main.find_all(['h1', 'h2', 'h3', 'h4', 'p'])
    return [(el.name, el.get_text(strip=True)) for el in elements if el.get_text(strip=True)]


async def main():
    if not URL:
        print("No URL provided in .env file")
        return

    print(f"Scraping desde {URL}...")
    content = await extract_text(URL)
    if not content:
        print("No se encontró texto en la página.")
        return

    pdf = PDFGenerator()
    for tag, raw in content:
        text = sanitize(raw)
        if tag.startswith('h'):
            pdf.add_heading(text)
        else:
            pdf.add_paragraph(text)

    pdf.output("unicef_landing_report.pdf")
    print("PDF generado exitosamente como 'unicef_landing_report.pdf'")


if __name__ == "__main__":
    asyncio.run(main())
