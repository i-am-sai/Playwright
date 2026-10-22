import pytest
from playwright.sync_api import expect
from pages.toc_page import TOCPage
from utils.config_reader import ConfigReader
from utils.logger import logger


class TestTableOfContents:
   
    
    def test_toc_ui_elements_present(self, reader_on_chapter, toc_page):
        logger.info("\nTest Case 4: TOC UI Elements Verified")
        reader_on_chapter.open_table_of_contents()
        toc_page.verify_all_toc_ui_elements()
    
   
    def test_toc_chapter_accordion_expands(self,reader_on_chapter, toc_page):
        reader_on_chapter.open_table_of_contents()
        toc_page.verify_toc_accordion_expands(
            "Part 1: General Concepts", "Course Equipment")

  
    def test_toc_close(self, reader_on_chapter, toc_page):
        reader_on_chapter.open_table_of_contents()
        toc_page.verify_toc_closes()


# method to verfiy number of algo and fig in TOC