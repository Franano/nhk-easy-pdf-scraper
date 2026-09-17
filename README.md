# NHK News Easy - Daily PDF Scraper & Exporter

[![NHK Scraper CI](https://github.com/TU_USUARIO/TU_REPOSITORIO/actions/workflows/nhk_daily_pdf.yml/badge.svg)](https://github.com/TU_USUARIO/TU_REPOSITORIO/actions/workflows/nhk_daily_pdf.yml)

Un pipeline automatizado de Web Scraping y Testing diseñado con Playwright y Pytest bajo el patrón Page Object Model (POM). Extrae diariamente la última noticia en japonés simplificado de NHK News Easy, sanitiza el contenido HTML (furigana y estilos) y genera un documento PDF de lectura optimizado listo para descargar.

---

## Arquitectura y Tecnologías

* Lenguaje: Python 3.11+
* Automatización Web: Playwright (Python)
* Testing Framework: Pytest + Pytest-Playwright
* Patrón de Diseño: Page Object Model (POM)
* CI/CD: GitHub Actions (Scheduled Workflows)
* Renderizado de PDF: CSS Print Media Queries + Font Injection (CJK)

### Flujo del Pipeline

```text
[ GitHub Actions (Cron Job / Manual) ]
                  │
                  ▼
   [ Ubuntu Runner + Japanese CJK Fonts ]
                  │
                  ▼
   [ Pytest Execution (Headless Chromium) ]
                  │
                  ├── NHKHomePage (POM) ──► Navega y extrae HTML/Furigana
                  │
                  ├── HTML Builder ─────► Sanitiza CSS y elimina UI inútil
                  │
                  └── Playwright PDF ───► Genera PDF limpio en /noticias_pdf
                  │
                  ▼
[ Upload Artifact: nhk-daily-pdf ]

```

---

## Instalación y Ejecución Local

### Prerrequisitos

* Python 3.10 o superior
* Git

### Pasos

1. Clonar el repositorio:
   git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   cd TU_REPOSITORIO

2. Crear y activar entorno virtual:
   python -m venv venv
   # En Linux/macOS:
   source venv/bin/activate
   # En Windows:
   .\venv\Scripts\activate

3. Instalar dependencias y navegadores de Playwright:
   pip install -r requirements.txt
   playwright install chromium

4. Ejecutar las pruebas y generar el PDF:
   pytest tests/

   El PDF resultante se guardará en la carpeta noticias_pdf/.

---

## CI/CD y Automatización en GitHub Actions

El proyecto cuenta con un workflow de GitHub Actions (.github/workflows/nhk_daily_pdf.yml) configurado para:

* Ejecutarse de forma programada (Cron) diariamente o bajo demanda (workflow_dispatch).
* Instalar la suite de fuentes japonesas fonts-noto-cjk en el entorno virtual de Ubuntu para garantizar que el texto en Kanji e Hiragana no sufra distorsiones.
* Generar y publicar el PDF como un Artefacto de GitHub descargable en cada ejecución exitosa.

---

## Estructura del Proyecto
```text
.
├── .github/
│   └── workflows/
│       └── nhk_daily_pdf.yml    # Pipeline de CI/CD
├── pages/
│   ├── base_page.py             # Clase base con interacciones genéricas
│   └── nhk_page.py              # Page Object de NHK News Easy
├── utils/
│   └── html_builder.py          # Formateador de HTML/CSS para PDF
├── tests/
│   └── test_nhk_exporter.py     # Test funcional y generador de artefacto
├── pytest.ini                   # Configuración global de Pytest
├── requirements.txt             # Dependencias del proyecto
└── README.md

```
