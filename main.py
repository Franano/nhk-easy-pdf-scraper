import os
from playwright.sync_api import sync_playwright
from pages.nhk_home_page import NHKHomePage


def build_html_content(body_html: str, image_url: str = "", article_url: str = "") -> str:
    """Genera una plantilla HTML limpia usando el cuerpo del artículo y agregando el botón y la imagen."""
    image_element = f'<div style="text-align: center; margin: 20px 0;"><img src="{image_url}" style="max-width: 100%; height: auto; border-radius: 8px;"></div>' if image_url else ""

    link_element = ""
    if article_url:
        link_element = f"""
        <div style="margin: 15px 0; text-align: center;">
            <a href="{article_url}" target="_blank" style="
                display: inline-block;
                background-color: #e60012;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 20px;
                font-weight: bold;
                font-size: 14px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            ">ニュースのページを開く (Ver Noticia Original y Audio)</a>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>NHK Easy News Article</title>
    <style>
        body {{
            font-family: 'Hiragino Sans', 'Meiryo', sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            line-height: 2.2;
            color: #333;
        }}
        h1, h1.article-main__title {{
            border-bottom: 2px solid #e60012;
            padding-bottom: 10px;
            line-height: 2.5;
            font-size: 24px;
        }}
        ruby rt {{
            font-size: 0.65em;
            color: #666;
        }}
    </style>
</head>
<body>
    {link_element}
    {image_element}
    <div>{body_html}</div>
</body>
</html>"""


def export_to_html(html_content: str, filename: str = "article.html"):
    """Genera el archivo HTML."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Archivo HTML generado exitosamente en: {os.path.abspath(filename)}")


def run():
    print("Accediendo a NHK Easy News...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1. Scraping con Page Object
        nhk_page = NHKHomePage(page)
        nhk_page.open()
        nhk_page.open_first_article()

        # Extrae contenido con etiquetas <ruby>, imagen y URL de la noticia
        data = nhk_page.get_article_data_raw_html()

        print("\n--- DATOS EXTRAÍDOS ---")
        print(f"Título: {data['title_text']}")
        print(f"Imagen: {data['image_url'] if data['image_url'] else 'Sin imagen'}")
        print(f"URL Noticia: {data['article_url']}")

        # 2. Construir HTML
        html_str = build_html_content(
            data["body_html"],
            data["image_url"],
            data["article_url"]
        )

        # 3. Guardar archivo HTML
        export_to_html(html_str, "article.html")

        # 4. Cargar nuestro HTML formateado en la página y generar el PDF limpio
        page.set_content(html_str, wait_until="load")
        page.emulate_media(media="screen")
        page.pdf(path="article.pdf", format="A4", print_background=True)

        print(f"Archivo PDF generado exitosamente en: {os.path.abspath('article.pdf')}")

        browser.close()


if __name__ == "__main__":
    run()