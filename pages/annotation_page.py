from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.logger import logger
from utils.screenshot_helper import take_screenshot

class AnnotationPage(BasePage):
    def __init__(self, page: Page):
            super().__init__(page)
            

    # Web Elements
    #Page object for text highlightinh / annotation actions inside the ePub reader iframe.
    
    IFRAME_SELECTOR = "iframe[title='EPUB Book Content']"
    # epub_frame = page.frame_locator('iframe[title="EPUB Book Content"]')

    # Color Pannel Button ((aria-labels observed in DOM))
    COLOR_BUTTONS = {
        "orange": "select orange color",
        "blue": "select blue color",
        "brown": "select brown color",
        "purple": "select purple color"
    }

    ANNOTATION_LISTING_BUTTON = "annotation listing"
    ANNOTATION_CARD_SELECTOR = "div.notification-block"

    COLOR_HEX_MAP = {
        "orange": None,   # fill in after inspecting an orange annotation card
        "blue": None,
        "brown": None,
        "purple": "#bb0ebe",  # observed in your screenshot
    }
    

# Methods: 


    def _reader_frame(self):
        return self.page.locator(self.IFRAME_SELECTOR).content_frame
   # Returns the content_frame for the ePub reader iframe.

    def select_paragraph_text(self, paragraph_id: str, steps: int = 20):
        """
        Simulates a real mouse click and drag to select all text inside a paragraph
        element identified by its DOM ID (eg: 'aha1418').
        """

        frame = self._reader_frame()
        print(frame.locator("body").inner_html()[:2000])  # dump what's actually loaded
        paragraph = frame.locator(f"#{paragraph_id}")

        expect(paragraph).to_be_visible(timeout=10000)
        box = paragraph.bounding_box()

        if not box:
            raise Exception(f"Could not resolve bounding box for paragraph id={paragraph_id}")
    
        logger.info(f"Selecting text in paragraph #{paragraph_id} via mouse drag")

    # Start just inside the top-left of the paragraph (avoids clipping the first character)
        start_x, start_y = box["x"] + 2, box["y"] + 2
        end_x, end_y = box["x"] + box["width"]-2, box["y"] + box["height"] -2

        self.page.mouse.move(start_x, start_y)
        self.page.mouse.down()
        self.page.mouse.move(end_x, end_y, steps=steps)
        self.page.mouse.up()

        take_screenshot(self.page, f"text_selected_{paragraph_id}")


    def select_highlight_color(self, color: str = "orange"):
        """Clicks the given color swatch in the highlight color panel that appears after selection."""

        if color not in self.COLOR_BUTTONS:
            raise ValueError(f"Unsupported color '{color}'. Options: {list(self.COLOR_BUTTONS.keys())} ")
     
        color_button = self.page.get_by_role("button", name=self.COLOR_BUTTONS[color])
        expect(color_button).to_be_visible()
        color_button.click()

        logger.info(f"Applied '{color}' highlight color")
        take_screenshot(self.page, f"highlight_applied_{color}")

    def highlight_paragraph(self, paragraph_id: str, color: str = "orange"):
        """Convenience method: select paragraph text + apply highlight color in one call."""
        self.select_paragraph_text(paragraph_id)
        self.select_highlight_color(color)
        self.refresh()
    

    def open_annotation_listing(self):
        logger.info("Opening annoation listing page")
        self.page.get_by_role("button", name=self.ANNOTATION_LISTING_BUTTON).click()

    def get_latest_annotation_card(self):
        return self.page.locator(self.ANNOTATION_CARD_SELECTOR).first
    
    def verify_annotation_text(self, expected_text_snippet: str):
        card = self.get_latest_annotation_card()
        text_locator = card.locator("p.infodetail")
        expect(text_locator).to_contain_text(expected_text_snippet)
        logger.info(f"Annotation text confirmed: contains '{expected_text_snippet}'")
    
    def verify_annotation_color(self, expected_color: str):
        expected_hex = self.COLOR_HEX_MAP.get(expected_color)
        if not expected_hex:
            raise ValueError(f"No hex mapping defined yet for color '{expected_color}'")

        card = self.get_latest_annotation_card()
        style = card.get_attribute("style") or ""

        assert expected_hex.lower() in style.lower(), (
            f"Expected border color {expected_hex} for '{expected_color}' highlight, "
            f"but card style was: {style}"
        )
        logger.info(f"Annotation color confirmed: {expected_color} ({expected_hex})")

    def verify_annotation_date_present(self):
        card = self.get_latest_annotation_card()
        date_locator = card.locator("p.mb-0", has_text="Added:")
        expect(date_locator).to_be_visible()

    def verify_annotation_added(self, expected_text_snippet: str, expected_color: str, timeout: int = 15000):
        
        self.open_annotation_listing()
        
        card = self.get_latest_annotation_card()
        card.wait_for(state="visible", timeout=timeout)
        logger.info(f"First card content: {card.inner_text()[:200]}")


        self.verify_annotation_text(expected_text_snippet)
        self.verify_annotation_color(expected_color)
        self.verify_annotation_date_present()

        add_note_button = card.locator('#colorfilterAddNote')
        expect(add_note_button).to_be_visible()

        take_screenshot(self.page, f"annotation_listing_verified_{expected_color}")

    def refresh(self):
        logger.info("Reloading page to force fresh annotation state")
        self.page.reload()
        self.page.wait_for_load_state("networkidle")

    def get_annotation_cfi(self, card):
        return card.get_attribute("data-cfirange") or ""

    def verify_annotation_cfi_targets_paragraph(self, expected_paragraph_id: str):
        card = self.get_latest_annotation_card()
        cfi = self.get_annotation_cfi(card)

        assert expected_paragraph_id in cfi, (
        f"Expected paragraph id '{expected_paragraph_id}' in CFI range, "
        f"but got: {cfi}"
        )
        logger.info(f"CFI confirmed targeting paragraph #{expected_paragraph_id}: {cfi}")

