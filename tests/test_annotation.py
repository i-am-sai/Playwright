import pytest
from playwright.sync_api import expect
from pages.annotation_page import AnnotationPage
from pages.reader_page import ReaderPage
from utils.logger import logger

# @pytest.fixture
# def annotation_page(reader_on_chapter):
#     return AnnotationPage(reader_on_chapter.page)

class TestHighlightAnnotation:

    
    def test_highlight_paragraph_purple(self, reader_on_chapter, annotation_page):
        """
           TC: Select a full paragraph of reader text and apply an orange highlight.
           Paragraph under test: id='aha1418' (BLS course completion requirements).
        """

        # reader_on_chapter already gives you everything ReaderPage offers (including your new verify_chapter_content method), since it is a ReaderPage instance.
        logger.info("\nTest Case 4: Annotation Creation")    
    
        
        paragraph_id = "aha1418"
        reader_on_chapter.verify_chapter_content(paragraph_id)
        logger.info("Chapter content 1418 present ")

        # annotation = AnnotationPage(reader_on_chapter.page)
      
        logger.info(f"Starting highlight test for paragraph #{paragraph_id}")

        annotation_page.highlight_paragraph(paragraph_id, color="purple")
        annotation_page.capture_screenshot("Highlight Created")
        
        annotation_page.verify_annotation_added(
            expected_text_snippet="To receive a course completion card",
            expected_color="purple"
        )
        annotation_page.capture_screenshot("Highlight Present")

        annotation_page.verify_annotation_cfi_targets_paragraph(paragraph_id)

    def test_highlight_paragraph_orange(self, reader_on_chapter, annotation_page):
        """
           TC: Select a full paragraph of reader text and apply an orange highlight.
           Paragraph under test: id='aha1418' (BLS course completion requirements).
        """

        # reader_on_chapter already gives you everything ReaderPage offers (including your new verify_chapter_content method), since it is a ReaderPage instance.
        logger.info("\nTest Case 4: Annotation Creation")    
    
        
        paragraph_id = "aha1419"
        reader_on_chapter.verify_chapter_content(paragraph_id)
        logger.info("Chapter content 1419 present ")

        # annotation = AnnotationPage(reader_on_chapter.page)
      
        logger.info(f"Starting highlight test for paragraph #{paragraph_id}")

        annotation_page.highlight_paragraph(paragraph_id, color="orange")
        annotation_page.capture_screenshot("Highlight Created")
        
        annotation_page.verify_annotation_added(
            expected_text_snippet="To successfully complete the BLS course",
            expected_color="orange"
        )
        annotation_page.capture_screenshot("Highlight Present")

        annotation_page.verify_annotation_cfi_targets_paragraph(paragraph_id)
