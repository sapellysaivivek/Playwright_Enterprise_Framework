from venv import logger

from utils.logger import getloggings
from config.config import Base_url


class NotePage:
    def __init__(self, page ):
        self.page = page
        self.logger = getloggings(self.__class__.__name__)
    def addNewNote(self):
        self.page.get_by_test_id("add-new-note").click()
        self.logger.debug("adding new note")
    def selectcatagory(self , catagory):
        self.page.get_by_test_id("note-category").select_option(catagory)
        self.logger.debug("choosing category")
    def checkcomplete(self):
        self.page.get_by_test_id("note-completed").check()
    def addTitle(self ,title):
        self.logger.debug("filling title")
        self.page.get_by_test_id("note-title").fill(title)
    def adddesc(self , content):
        self.page.get_by_test_id("note-description").fill(content)
        self.logger.debug("filling description")
    def submitnote(self):
        self.page.get_by_test_id("note-submit").click()
        self.logger.debug("submitting this note")
    def deleteNote(self ,title):
        note = self.page.locator('[data-testid="note-card"]').filter(
        has=self.page.locator('[data-testid="note-card-title"]', has_text=title))
        delete_btn = note.get_by_text("Delete")
        self.logger.debug(f"deleting note with title: {title}")
        delete_btn.click()
        self.page.get_by_test_id("note-delete-confirm").click()
        logger.info("click delete")
          
    def addNote(self, title: str, content: str):
        self.page.goto(Base_url)
        self.addNewNote()
        self.selectcatagory("Personal")
        self.checkcomplete()
        self.addTitle(title)
        self.adddesc(content)
        self.submitnote()
        
    def is_note_present(self, title: str) -> bool:
        self.page.goto(Base_url)

        note = self.page.locator(
            '[data-testid="note-card"]'
        ).filter(
            has=self.page.locator(
                '[data-testid="note-card-title"]',
                has_text=title
            )   
        )

        return note.count() > 0
        