def build_html_content(body_html: str, image_url: str, article_url: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 20mm 15mm 20mm 15mm;
            }}
            body {{
                font-family: "Hiragino Sans", "Meiryo", "Noto Sans CJK JP", sans-serif;
                line-height: 1.8;
                color: #222222;
                max-width: 800px;
                margin: 0 auto;
                padding: 10px;
            }}
            /* Ocultar elementos flotantes y botones multimedia que ensucian el PDF */
            .article-main__tools,
            .player,
            #js-article-tools,
            .dicWin,
            button {{
                display: none !important;
            }}
            .main-image {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .main-image img {{
                max-width: 100%;
                height: auto;
                border-radius: 8px;
            }}
            .article-body {{
                font-size: 16px;
                word-wrap: break-word;
            }}
            /* Estilo nativo para el Furigana (Ruby) */
            ruby {{
                ruby-align: center;
            }}
            rt {{
                font-size: 0.65em;
                color: #555555;
            }}
            .footer-link {{
                margin-top: 30px;
                padding-top: 10px;
                border-top: 1px solid #eeeeee;
                font-size: 12px;
                color: #0066cc;
            }}
        </style>
    </head>
    <body>
        {"<div class='main-image'><img src='" + image_url + "' /></div>" if image_url else ""}
        <div class="article-body">
            {body_html}
        </div>
        <div class="footer-link">
            <a href="{article_url}">Ver noticia original en NHK Easy News</a>
        </div>
    </body>
    </html>
    """