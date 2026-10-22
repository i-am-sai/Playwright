import pytest
from utils.logger import logger
from pages.toc_page import TOCPage
from pages.algorithm_page import AlgorithmPage


class TestAlgorithmPreview:

    def test_algorithm_preview_flow(self, reader_on_chapter, toc_page, algorithm_page):
        logger.info("\nTest Case 6: Algorithm Preview Verified")

        toc_page.open_table_of_contents()
        expected_count = toc_page.get_algorithms_count()
        toc_page.toc_algorithms_link.click()
        
        algorithm_page.verify_listing_heading(expected_count)
        algorithm_page.open_first_algorithm()
        algorithm_page.verify_go_to_content_and_next()
        algorithm_page.click_next_and_verify_previous()
        algorithm_page.verify_zoom_controls()
        algorithm_page.verify_description_and_image()