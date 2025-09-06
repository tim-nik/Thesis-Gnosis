from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from elearning.models import Course, Chapter, Lesson
from .models import Quiz, Question, Choice, QuizAttempt, AttemptAnswer

@login_required
def quiz_take(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    quiz = lesson.quizzes.filter(is_published=True).first()
    if not quiz:
        messages.info(request, "Δεν υπάρχει διαθέσιμο κουίζ για αυτό το μάθημα.")
        return redirect("courses:lesson_detail", lesson_id=lesson.id)

    if request.method == "POST":
        questions = list(quiz.questions.prefetch_related('choices'))
        total = len(questions)
        score = 0
        attempt = QuizAttempt.objects.create(user=request.user, quiz=quiz, total=total)
        for q in questions:
            cid = request.POST.get(f"q_{q.id}")
            selected = Choice.objects.filter(id=cid, question=q).first() if cid else None
            correct = bool(selected and selected.is_correct)
            if correct: score += 1
            AttemptAnswer.objects.create(
                attempt=attempt, question=q,
                selected_choice=selected, is_correct=correct
            )
        attempt.score = score
        attempt.save()
        return redirect("quizzes:quiz_result", attempt_id=attempt.id)

    questions = quiz.questions.prefetch_related('choices').all()
    return render(request, "quizzes/quiz_take.html", {
        "lesson": lesson, "quiz": quiz, "questions": questions,
    })

@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    return render(request, "quizzes/quiz_result.html", {
        "attempt": attempt,
        "quiz": attempt.quiz,
        "lesson": attempt.quiz.lesson,
        "answers": attempt.answers.select_related('question', 'selected_choice'),
    })
