from datetime import datetime
from pathlib import Path
from utils.html_builder import build_html_content


def test_export_latest_nhk_article_to_pdf(nhk_page, page):
    nhk_page.open_first_article()
    
    # 1. Esperar a que la página original cargue imágenes y scripts por completo
    page.wait_for_load_state("networkidle")

    data = nhk_page.get_article_data_raw_html()

    assert data["title_text"], "El título no debería estar vacío"

    html_content = build_html_content(
        body_html=data["body_html"],
        image_url=data["image_url"],
        article_url=data["article_url"],
    )

    # 2. Cambiar 'load' por 'networkidle' para renderizar fuentes e imágenes del HTML generado
    page.set_content(html_content, wait_until="networkidle")
    page.emulate_media(media="screen")

    # Asegura crear la carpeta donde buscará GitHub Actions
    output_dir = Path("noticias_pdf")
    output_dir.mkdir(exist_ok=True)

    today_str = datetime.now().strftime("%Y-%m-%d")
    pdf_filename = output_dir / f"NHK_{today_str}.pdf"

    page.pdf(path=str(pdf_filename), format="A4", print_background=True)

    assert pdf_filename.exists()
    assert pdf_filename.stat().st_size > 0