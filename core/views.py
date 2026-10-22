from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm
from analyzer.models import Resume


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/landing.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome aboard, {user.first_name or user.username}!')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
    stats = {
        'total': resumes.count(),
        'avg_score': round(sum(r.overall_score for r in resumes) / resumes.count(), 1) if resumes else 0,
        'best_score': max((r.overall_score for r in resumes), default=0),
    }
    return render(request, 'core/dashboard.html', {'resumes': resumes[:8], 'stats': stats})
