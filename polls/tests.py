import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question

class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        # Create your tests here.
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_datE
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_datE
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTest(TestCase):

    def test_no_questions(self):
        """
        If no questions exist should return appropriate error
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_questions(self):
        """
        Questions with a pub date in the past are displayed
        """

        create_question(question_text='Past Question.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question.>'])

    def test_future_questions(self):
        """
        Questions with a pub date in the future are not displayed
        """

        create_question(question_text='Future Question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_questions(self):
        """
        Questions with a pub date in the future are not displayed and questions in the past are displayed
        """
        create_question(question_text='Past Question.', days=-30)
        create_question(question_text='Future Question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question.>'])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past Question 1.", days=-30)
        create_question(question_text="Past Question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past Question 2.>', '<Question: Past Question 1.>'])

class QuestionDetailViewTest(TestCase):

    def test_future_question(self):

        """
        Detail view of a future question returns 404 not found
        """
        future_question = create_question(question_text="Future Question.", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):

        """
        Detail view of a past question return text of the past question
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionResultslViewTest(TestCase):

    def test_future_question(self):

        """
        Detail view of a future question returns 404 not found
        """
        future_question = create_question(question_text="Future Question.", days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):

        """
        Detail view of a past question return text of the past question
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

