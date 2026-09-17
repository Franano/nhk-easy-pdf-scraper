from urllib.parse import urljoin
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage


class NHKHomePage(BasePage):
    URL = "https://www3.nhk.or.jp/news/easy/"

    # --- LOCATORS ---
    ABROAD_DISCLAIMER_BTN = "text=確認しました / I understand"
    FIRST_ARTICLE_LINK = "#js-news-list article a[href*='/news/easy/']"
    ARTICLE_TITLE = "h1.article-title"
    ARTICLE_BODY = "#js-article-body, .article-body, article.easy-article"


    # --- MÉTODOS DE ACCIÓN ---
    def open(self):
        """Navega a la URL principal."""
        self.navigate_to(self.URL)
        self.dismiss_abroad_disclaimer()

    def dismiss_abroad_disclaimer(self):
        """Maneja el aviso internacional si aparece."""
        btn = self.page.locator(self.ABROAD_DISCLAIMER_BTN)
        try:
            btn.wait_for(state="visible", timeout=4000)
            btn.click()
        except PlaywrightTimeoutError:
            pass

    def open_first_article(self):
        """Abre la primera noticia y espera la carga del título."""
        first_article = self.page.locator(self.FIRST_ARTICLE_LINK).first
        first_article.wait_for(state="visible", timeout=5000)
        first_article.click()

        self.page.locator(self.ARTICLE_TITLE).first.wait_for(
            state="visible", timeout=10000
        )

    def get_article_data_raw_html(self) -> dict:
        """Extrae los elementos de la noticia limpiando reproductores y herramientas."""
        title_locator = self.page.locator(self.ARTICLE_TITLE).first
        body_locator = self.page.locator(self.ARTICLE_BODY).first

        body_html = ""
        if body_locator.count() > 0:
            body_html = self.page.evaluate(
                """(selector) => {
                const el = document.querySelector(selector);
                if (!el) return '';
                const clone = el.cloneNode(true);
                
                // Remueve reproductores, iframes y las herramientas de audio/furigana
                const selectorsToRemove = 'video, iframe, .video-player, #js-article-video, .article-main__tools, #js-article-tools, .player-button';
                clone.querySelectorAll(selectorsToRemove).forEach(v => v.remove());
                
                return clone.innerHTML;
            }""",
                self.ARTICLE_BODY,
            )

        return {
            "title_html": title_locator.inner_html().strip()
            if title_locator.count() > 0
            else "",
            "title_text": title_locator.inner_text().strip()
            if title_locator.count() > 0
            else "",
            "body_html": body_html.strip(),
            "article_url": self.page.url,
        }