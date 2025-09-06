# In core/tests/test_database.py

from django.test import TestCase
from core.models import Course, Chapter, Lesson, Quiz, Question, Answer
from django.contrib.auth.models import User
from django.utils import timezone

class DatabaseConnectionTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create base course
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            difficulty_level="Beginner",
            learning_objectives="Test Objectives",
            estimated_duration=60
        )

    def test_course_relationships(self):
        # Create chapter
        chapter = Chapter.objects.create(
            course=self.course,
            title="Test Chapter",
            description="Test Description",
            order=1
        )
        
        # Test chapter creation
        self.assertEqual(self.course.chapters.count(), 1)
        
        # Create lesson
        lesson = Lesson.objects.create(
            chapter=chapter,
            title="Test Lesson",
            content="Test Content",
            order=1
        )
        
        # Test lesson creation
        self.assertEqual(chapter.lessons.count(), 1)

    def test_quiz_system(self):
        chapter = Chapter.objects.create(
            course=self.course,
            title="Quiz Chapter",
            description="Test Description",
            order=1
        )
        
        lesson = Lesson.objects.create(
            chapter=chapter,
            title="Quiz Lesson",
            content="Test Content",
            order=1
        )
        
        # Create quiz
        quiz = Quiz.objects.create(
            lesson=lesson,
            title="Test Quiz",
            description="Test Quiz Description",
            time_limit=30,
            passing_score=70
        )
        
        # Create questions and answers
        question = Question.objects.create(
            quiz=quiz,
            question_text="Test Question",
            order=1
        )
        
        Answer.objects.create(
            question=question,
            answer_text="Correct Answer",
            is_correct=True
        )
        
        Answer.objects.create(
            question=question,
            answer_text="Wrong Answer",
            is_correct=False
        )
        
        # Test relationships
        self.assertEqual(quiz.questions.count(), 1)
        self.assertEqual(question.answers.count(), 2)
