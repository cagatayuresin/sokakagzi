import random
from .models import Explanation, UserVote, UserFavorite, Topic
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, ExplanationForm, RegisterForm, UserProfileForm, UserForm, TopicForm
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator



@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    explanations = Explanation.objects.filter(topic=topic).order_by('-created_at')
    paginator = Paginator(explanations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user_votes = UserVote.objects.filter(user=request.user, explanation__topic=topic).values_list('explanation_id', 'vote_type')
    user_favorites = UserFavorite.objects.filter(user=request.user, explanation__topic=topic).values_list('explanation_id', flat=True)
    user_votes = dict(user_votes)  # Dictionary format for easier lookup in template
    return render(request, 'topic_detail.html', {
        'topic': topic,
        'page_obj': page_obj,
        'user_votes': user_votes,
        'user_favorites': user_favorites,
    })


@login_required
def favorites(request):
    user_favorites = UserFavorite.objects.filter(user=request.user).order_by('-created_at')
    explanation_ids = [fav.explanation.id for fav in user_favorites]
    explanations = Explanation.objects.filter(id__in=explanation_ids).order_by('-created_at')
    paginator = Paginator(explanations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user_votes = UserVote.objects.filter(user=request.user).values_list('explanation_id', 'vote_type')
    user_favorites_ids = UserFavorite.objects.filter(user=request.user).values_list('explanation_id', flat=True)
    user_votes = dict(user_votes)  # Dictionary format for easier lookup in template
    return render(request, 'favorites.html', {
        'page_obj': page_obj,
        'user_votes': user_votes,
        'user_favorites': user_favorites_ids,
    })


@login_required
def user_explanations(request):
    explanations = Explanation.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(explanations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user_votes = UserVote.objects.filter(user=request.user).values_list('explanation_id', 'vote_type')
    user_favorites = UserFavorite.objects.filter(user=request.user).values_list('explanation_id', flat=True)
    user_votes = dict(user_votes)  # Dictionary format for easier lookup in template
    return render(request, 'explanations.html', {
        'page_obj': page_obj,
        'user_votes': user_votes,
        'user_favorites': user_favorites,
    })

@login_required
def edit_explanation(request, explanation_id):
    explanation = get_object_or_404(Explanation, id=explanation_id, user=request.user)
    if request.method == 'POST':
        form = ExplanationForm(request.POST, instance=explanation)
        if form.is_valid():
            form.save()
            return redirect('user_explanations')
    else:
        form = ExplanationForm(instance=explanation)
    return render(request, 'edit_explanation.html', {'form': form, 'explanation': explanation})


@login_required
def delete_explanation(request, explanation_id):
    explanation = get_object_or_404(Explanation, id=explanation_id, user=request.user)
    if request.method == 'POST':
        explanation.delete()
        return redirect('user_explanations')
    return render(request, 'confirm_delete.html', {'explanation': explanation})


@login_required
def upvote_explanation(request, explanation_id):
    explanation = get_object_or_404(Explanation, id=explanation_id)
    if explanation.user == request.user:
        return JsonResponse({'status': 'self_vote', 'message': 'You cannot vote for your own explanation.'}, status=400)
    vote, created = UserVote.objects.get_or_create(user=request.user, explanation=explanation)
    if vote.vote_type == 'up':
        vote.delete()
        status = 'removed'
    else:
        vote.vote_type = 'up'
        vote.save()
        status = 'added'
    return JsonResponse({
        'status': status,
        'total_up_votes': explanation.total_up_votes,
        'total_down_votes': explanation.total_down_votes,
        'total_favorites': explanation.total_favorites
    })


@login_required
def downvote_explanation(request, explanation_id):
    explanation = get_object_or_404(Explanation, id=explanation_id)
    if explanation.user == request.user:
        return JsonResponse({'status': 'self_vote', 'message': 'You cannot vote for your own explanation.'}, status=400)
    vote, created = UserVote.objects.get_or_create(user=request.user, explanation=explanation)
    if vote.vote_type == 'down':
        vote.delete()
        status = 'removed'
    else:
        vote.vote_type = 'down'
        vote.save()
        status = 'added'
    return JsonResponse({
        'status': status,
        'total_up_votes': explanation.total_up_votes,
        'total_down_votes': explanation.total_down_votes,
        'total_favorites': explanation.total_favorites
    })


@login_required
def favorite_explanation(request, explanation_id):
    explanation = get_object_or_404(Explanation, id=explanation_id)
    if explanation.user == request.user:
        return JsonResponse({'status': 'self_favorite', 'message': 'You cannot favorite your own explanation.'}, status=400)
    favorite, created = UserFavorite.objects.get_or_create(user=request.user, explanation=explanation)
    if created:
        status = 'added'
    else:
        favorite.delete()
        status = 'removed'
    return JsonResponse({
        'status': status,
        'total_up_votes': explanation.total_up_votes,
        'total_down_votes': explanation.total_down_votes,
        'total_favorites': explanation.total_favorites
    })


def home(request):
    topics = list(Topic.objects.all())
    random_topics = random.sample(topics, min(len(topics), 5))

    if request.user.is_authenticated:
        user_votes = UserVote.objects.filter(user=request.user).values_list('explanation_id', 'vote_type')
        user_favorites = UserFavorite.objects.filter(user=request.user).values_list('explanation_id', flat=True)
        user_votes = dict(user_votes)  # Dictionary format for easier lookup in template
    else:
        user_votes = {}
        user_favorites = []

    return render(request, 'home.html', {
        'random_topics': random_topics,
        'user_votes': user_votes,
        'user_favorites': user_favorites,
    })


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('home')
    template_name = 'register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def new_topic(request):
    if request.method == 'POST':
        topic_form = TopicForm(request.POST)
        explanation_form = ExplanationForm(request.POST)
        if topic_form.is_valid() and explanation_form.is_valid():
            topic = topic_form.save()
            explanation = explanation_form.save(commit=False)
            explanation.topic = topic
            explanation.user = request.user
            explanation.save()
            return redirect('topic_detail', topic_id=topic.id)
    else:
        topic_form = TopicForm()
        explanation_form = ExplanationForm()
    return render(request, 'new_topic.html', {
        'topic_form': topic_form,
        'explanation_form': explanation_form
    })


@login_required
def add_explanation(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        form = ExplanationForm(request.POST)
        if form.is_valid():
            explanation = form.save(commit=False)
            explanation.user = request.user
            explanation.topic = topic
            explanation.save()
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = ExplanationForm()
    return render(request, 'new_explanation.html', {'form': form, 'topic': topic})


def logout_view(request):
    logout(request)
    return redirect("/")


def search(request):
    query = request.GET.get('q')
    if query:
        # Büyük/küçük harf duyarsız arama
        results = Topic.objects.filter(Q(title__icontains=query)).distinct()

        # Eğer tam eşleşen bir başlık varsa, direkt o başlığın sayfasına yönlendirme
        exact_match = results.filter(title__iexact=query).first()
        if exact_match:
            return redirect('topic_detail', topic_id=exact_match.id)

        return render(request, 'search_results.html', {'query': query, 'results': results})
    else:
        return render(request, 'search_results.html', {'query': '', 'results': []})

