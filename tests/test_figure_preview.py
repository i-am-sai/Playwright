import pytest
from utils.logger import logger
from pages.toc_page import TOCPage
from pages.figure_page import FigurePage

class TestFigurePreview:

    
    def test_figure_preview_flow(self, toc_page, figure_page):
        logger.info("\nTest Case 7: Figure Preview Verified")

        toc_page.open_table_of_contents()
        expected_count = toc_page.get_figures_count()
        toc_page.toc_figures_link.click()
        figure_page.verify_listing_heading(expected_count)
        figure_page.open_first_figure()
        figure_page.verify_go_to_content_and_next()
        figure_page.click_next_and_verify_previous()
        figure_page.verify_zoom_controls()
