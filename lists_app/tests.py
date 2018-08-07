from django.test import TestCase
from django.urls import resolve
from .views import home_page
from django.http import HttpRequest
from .models import Item
from django.template.loader import render_to_string

class HomePageTest(TestCase):

	def test_root_url_resolves_to_homepage_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_content_homepage(self):
		request = HttpRequest()
		response = home_page(request)
		self.assertTrue(response.content.startswith(b'<html>'))
		self.assertIn(b'<title>To-Do lists</title>',response.content)
		self.assertTrue(response.content.endswith(b'</html>'))
		self.assertIn(b'</body>',response.content)
		expected_html = render_to_string('home.html')
		self.assertTrue(response.content.decode(),)

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = home_page(request)
		
		self.assertIn('A new list item',response.content.decode())

	def test_item_in_models_database(self):
		first_item = Item()
		first_item.text = 'The first list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(),2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text,'The first list item')
		self.assertEqual(second_saved_item.text,'Item the second')

	def test_home_page_can_save_a_POST_request(self):
 		request = HttpRequest()
 		request.method = 'POST'
 		request.POST['item_text'] = 'A new list item'

 		response = home_page(request)
 		
 		self.assertEqual(Item.objects.count(), 1)
 		new_item = Item.objects.first()
 		self.assertEqual(new_item.text, 'A new list item')
 		self.assertEqual(response.status_code, 302)
 		self.assertEqual(response['location'], '/')

	def test_home_page_only_save_item_when_necessary(self):
		request= HttpRequest()
		home_page(request)

		self.assertEqual(Item.objects.count(),0)


