def build_html_content(body_html: str, article_url: str = "") -> str:
    """Genera la plantilla HTML formateada con furigana, enlace original e imagen."""
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
    <div>{body_html}</div>
</body>
</html>"""