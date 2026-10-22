from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .forms import ResumeUploadForm
from .models import Resume
from .ml.extractor import extract_text
from .ml.analyzer import analyze_resume


@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.original_filename = request.FILES['file'].name
            resume.save()

            try:
                text = extract_text(resume.file.path)
                resume.parsed_text = text
                result = analyze_resume(text, resume.job_description)

                resume.overall_score = result['overall_score']
                resume.keyword_score = result['keyword_score']
                resume.section_score = result['section_score']
                resume.contact_score = result['contact_score']
                resume.readability_score = result['readability_score']
                resume.sections = result['sections']
                resume.skills_found = result['all_skills_found']
                resume.matched_skills = result['matched_skills']
                resume.missing_skills = result['missing_skills']
                resume.suggestions = result['suggestions']
                resume.word_count = result['word_count']
                resume.save()
            except Exception as exc:
                resume.delete()
                messages.error(request, f"Couldn't analyze that file: {exc}")
                return redirect('upload_resume')

            return redirect('result', pk=resume.pk)
    else:
        form = ResumeUploadForm()
    return render(request, 'analyzer/upload.html', {'form': form})


@login_required
def result(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if resume.user != request.user:
        return HttpResponseForbidden("You don't have access to this resume analysis.")

    skills_by_category = {}
    from .ml.skills_data import ALL_SKILLS
    for skill in resume.skills_found:
        category = ALL_SKILLS.get(skill, 'Other')
        skills_by_category.setdefault(category, []).append(skill)

    return render(request, 'analyzer/result.html', {
        'resume': resume,
        'skills_by_category': skills_by_category,
    })


@login_required
def history(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'analyzer/history.html', {'resumes': resumes})


@login_required
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        resume.file.delete(save=False)
        resume.delete()
        messages.success(request, 'Analysis deleted.')
    return redirect('history')
