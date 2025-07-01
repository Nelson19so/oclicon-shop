from django.test import TestCase
from apps.public.models import FrequentlyAskedQuestions

# frequently asked question test
class FrequentlyAskedQuestionsTest(TestCase):
    def test_frequently_asked_questions_str(self):
        faq = FrequentlyAskedQuestions.objects.create(
            email='test@gmail.com', subject='testCase',
            description='TestCase description'
        )
        self.assertEqual(str(faq), 'test@gmail.com')
