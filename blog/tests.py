from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post


class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # get post list page
        response = self.client.get('/blog/')
        # load page successfully
        self.assertEqual(response.status_code, 200)
        # the title is named 'Blog'
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        # navbar exists
        navbar = soup.nav
        # 'Blog', 'About Me' is in navbar
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # if there is no single post,
        self.assertEqual(Post.objects.count(), 0)
        # '아직 게시물이 없습니다' appears in main area
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

        # if there are two posts,
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
        )
        post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
        )
        self.assertEqual(Post.objects.count(), 2)

        # page refreshed
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        # there are two posts in main area
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # '아직 게시물이 없습니다.' doesn't appear no longer
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

    def test_post_detail(self):
        # there is a post
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
        )
        # the post's url is '/blog/1'
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # test for the first post detail page
        # load page successfully
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # the same navbar with post list page exists
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # the web browser tab's title has the first post's title
        self.assertIn(post_001.title, soup.title.text)

        # the first post's title is in post area
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)

        # the author of the first post is in post area (To be implemented)
        # TBI

        # the content of the first post is in post area
        self.assertIn(post_001.content, post_area.text)
