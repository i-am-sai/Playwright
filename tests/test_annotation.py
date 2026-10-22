import pytest
from playwright.sync_api import expect
from pages.annotation_page import AnnotationPage
from pages.reader_page import ReaderPage
from utils.logger import logger
from datetime import datetime



class TestHighlightAnnotation:

    @pytest.mark.dev
    def test_highlight_paragraph_purple(self, reader_on_chapter, annotation_page):
        """
           TC: Select a full paragraph of reader text and apply an orange highlight.
           Paragraph under test: id='aha1418' (BLS course completion requirements).
        """

        # reader_on_chapter already gives you everything ReaderPage offers (including your new verify_chapter_content method), since it is a ReaderPage instance.
        logger.info("\nTest Case 4: Annotation Creation")    
        reader_on_chapter.open_table_of_contents()
        reader_on_chapter.capture_screenshot("TOC Loaded")
        reader_on_chapter.click_toc_chapter("Part 4")
        reader_on_chapter.capture_screenshot("TOC Chapter 4 Loaded")
        reader_on_chapter.verify_chapter_heading("Testing")
        
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
    @pytest.mark.dev
    def test_highlight_paragraph_orange(self, reader_on_chapter, annotation_page):
        """
           TC: Select a full paragraph of reader text and apply an orange highlight.
           Paragraph under test: id='aha1418' (BLS course completion requirements).
        """

        # reader_on_chapter already gives you everything ReaderPage offers (including your new verify_chapter_content method), since it is a ReaderPage instance.
        logger.info("\nTest Case 4: Annotation Creation")    
        reader_on_chapter.open_table_of_contents()
        reader_on_chapter.capture_screenshot("TOC Loaded")
        reader_on_chapter.click_toc_chapter("Part 4")
        reader_on_chapter.capture_screenshot("TOC Chapter 4 Loaded")
        reader_on_chapter.verify_chapter_heading("Testing")
        
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

class TestNoteAnnotation:

    
    @pytest.mark.dev
    def test_add_note_and_verify_in_listing(self, reader_on_chapter, annotation_page):
        logger.info("\nTest Case 4: Note Creation")    
        reader_on_chapter.open_table_of_contents()
        reader_on_chapter.capture_screenshot("TOC Loaded")
        reader_on_chapter.click_toc_chapter("Part 4")
        reader_on_chapter.capture_screenshot("TOC Chapter 4 Loaded")
        reader_on_chapter.verify_chapter_heading("Testing")
        
        paragraph_id = "aha1423"
        reader_on_chapter.verify_chapter_content(paragraph_id)
        logger.info("Chapter content 1419 present ")

        # annotation = AnnotationPage(reader_on_chapter.page)
      
        logger.info(f"Starting creating note for paragraph #{paragraph_id}")
        note_text = f"Note{datetime.now().strftime('%H%M%S')}"
        
        annotation_page.create_note(paragraph_id, note_text)
        # annotation_page.select_paragraph_text(PARAGRAPH_ID)
        # annotation_page.add_note_to_selection(note_text)
        annotation_page.verify_note_in_listing(note_text)
        annotation_page.capture_screenshot("Note Listed")


    
