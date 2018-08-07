import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Chrome()
		# self.browser.implicitly_wait(3)
	# def tearDown(self):
	# 	self.browser.quit()
	def check_text_in_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')

		self.assertIn(row_text, [row.text for row in rows])

	def test_Home_page(self):
		self.browser.get('http://localhost:8000')
		self.assertIn('To-Do',self.browser.title)
		
		head_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-do',head_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a to-do item')

		inputbox.send_keys('Eating something...')
		inputbox.send_keys(Keys.ENTER)

		self.check_text_in_table('Eating something...')



if __name__=='__main__':
	unittest.main(warnings= 'ignore')

