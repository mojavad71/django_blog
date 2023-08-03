from django.test import TestCase
from .models import Post
from django.contrib.auth.models import User
from django.shortcuts import reverse


# Create your tests here.
class BlogPostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1')
        self.post1 = Post.objects.create(
            title='Post1',
            text="i am javad",
            status=Post.STATUS_CHOICES[0][0],
            author=self.user,
        )
        self.post2 = Post.objects.create(
            title='Post2',
            text='my nanme is javad',
            status=Post.STATUS_CHOICES[1][0],
            author=self.user,
        )

    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_title_on_blog_list_page(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, 'Post1')

    def test_post_details_on_blog_detail_page(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_post_detail_url(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url_by_name(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_status_404_if_post_id_no_exist(self):
        response = self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_draft_post_not_show_posts_list(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    def test_post_model_str(self):
        post= self.post1
        self.assertEqual(str(post), post.title)

    def test_post_detail(self):
        self.assertEqual(self.post1.title, 'Post1')
        self.assertEqual(self.post1.text, 'i am javad')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'some title',
            'text': 'hello',
            'status': 'pub',
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'some title')
        self.assertEqual(Post.objects.last().text, 'hello')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_update', args=[self.post2.id]), {
            'title': 'some11 title',
            'text': 'hello12121',
            'status': 'pub',
            'author': self.post2.author.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'some11 title')
        self.assertEqual(Post.objects.last().text, 'hello12121')

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args=[self.post2.id]), )
        self.assertEqual(response.status_code, 302)
