from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .models import Question, Choice


def _is_active(question: Question) -> bool:
    today = date.today()
    if not question.is_active:
        return False
    if question.start_date and today < question.start_date:
        return False
    if question.end_date and today > question.end_date:
        return False
    return True


def poll_list(request):
    questions = Question.objects.order_by("-create_ts")
    # Optional: split active/inactive for UI highlighting
    active_questions = [q for q in questions if _is_active(q)]
    inactive_questions = [q for q in questions if not _is_active(q)]
    return render(
        request,
        "poll/poll_list.html",
        {"active_questions": active_questions, "inactive_questions": inactive_questions},
    )


@login_required
def poll_detail(request, pk: int):
    question = get_object_or_404(Question, pk=pk)
    choices = Choice.objects.filter(question=question).order_by("create_ts")

    if request.method == "POST":
        # NOTE: No Answer/Vote model exists yet in this project.
        # We accept the submission and show a flash message for now.
        choice_id = request.POST.get("choice")
        try:
            choice = choices.get(pk=choice_id)
            messages.success(request, f"Vote submitted for: {choice.text}")
        except (Choice.DoesNotExist, ValueError, TypeError):
            messages.error(request, "Please select a valid choice.")
            return render(request, "poll/poll_detail.html", {"question": question, "choices": choices, "active": _is_active(question)})

        return redirect("poll_detail", pk=question.pk)

    return render(request, "poll/poll_detail.html", {"question": question, "choices": choices, "active": _is_active(question)})


def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)


@login_required
@staff_required
def poll_create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        is_active = request.POST.get("is_active") == "on"
        start_date = request.POST.get("start_date") or None
        end_date = request.POST.get("end_date") or None

        if not title:
            messages.error(request, "Title is required.")
            return render(request, "poll/poll_create.html")

        try:
            q = Question.objects.create(
                title=title,
                is_active=is_active,
                start_date=start_date or None,
                end_date=end_date or None,
                create_user=request.user,
            )
            messages.success(request, "Poll created.")
            return redirect("poll_detail", pk=q.pk)
        except Exception as exc:
            messages.error(request, f"Could not create poll: {exc}")

    return render(request, "poll/poll_create.html")


@login_required
@staff_required
def choice_create(request):
    questions = Question.objects.order_by("-create_ts")
    if request.method == "POST":
        question_id = request.POST.get("question")
        text = (request.POST.get("text") or "").strip()

        if not question_id or not text:
            messages.error(request, "Both question and text are required.")
            return render(request, "poll/choice_create.html", {"questions": questions})

        try:
            question = questions.get(pk=question_id)
            Choice.objects.create(question=question, text=text)
            messages.success(request, "Choice created.")
            return redirect("poll_detail", pk=question.pk)
        except Question.DoesNotExist:
            messages.error(request, "Selected question does not exist.")
        except Exception as exc:
            messages.error(request, f"Could not create choice: {exc}")

    return render(request, "poll/choice_create.html", {"questions": questions})
