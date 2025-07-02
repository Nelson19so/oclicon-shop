from django.test import TestCase, Client
from apps.public.models import FrequentlyAskedQuestions, BlogPost
from django.contrib.auth import get_user_model
from apps.products.models import Category

User = get_user_model()

# frequently asked question test
class FrequentlyAskedQuestionsTest(TestCase):
    def test_frequently_asked_questions_str(self):
        faq = FrequentlyAskedQuestions.objects.create(
            email='test@gmail.com', subject='testCase',
            description='TestCase description'
        )
        self.assertEqual(str(faq), 'test@gmail.com')

# test blog post
class BlogPostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='tesUser', email='testemail@gmail.com', password='testpassword_12.'
        )
        self.category = Category.objects.create(name='testCategory')

    def test_blog_post_str(self):
        blog = BlogPost.objects.create(
            author=self.user,
            category=self.category,
            title='testBlogPostTitle',
            content='test blog post content'
        )
        self.assertEqual(str(blog), f'{blog.title} by {'tesUser'}')
