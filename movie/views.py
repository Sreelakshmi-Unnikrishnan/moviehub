from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from .forms import *
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden,HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test



def index(request):
    movies = Movie.objects.all()
    return render(request, 'index.html',{'movies': movies})

def logout_view(request):
    logout(request)
    return redirect('login')
@login_required(login_url="login")
def profile(request):
    user = request.user
    movies = Movie.objects.all()
    return render(request, 'profile.html', {'user': user,'movies': movies})

def register(request):
    
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exist")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already registered")
                return redirect("register")
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password1,
                )
               
                user.save()
                messages.success(request, "welcome user,your registration was successfull")

                return redirect("login")
        else:
            messages.info(request, "Password not matches")
            return redirect("register")
    else:
        return render(request, "register.html")

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                
                return redirect("profile")
        else:
            
            messages.info(request, "Invalid Credential")
            return redirect("login")
    else:
        return render(request, "login.html")
    
@login_required
def view_profile(request,pk):
    user = User.objects.get(pk=pk)
    return render(request, 'view_profile.html', {'user': user})

@login_required
def edit_profile(request,pk):
    if request.method == 'POST':
           user = User.objects.get(pk=pk)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.save()
        return redirect('view_profile', pk=pk)
    else:
        user = request.user
        return render(request, 'edit_profile.html', {'user': user})
    
@login_required
def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        poster = request.FILES.get('poster')
        description = request.POST.get('description')
        release_date = request.POST.get('release_date')       
        actors = request.POST.get('actors')
        trailer_link = request.POST.get('trailer_link')
        categories = request.POST.getlist('category')

        if title and description and release_date and actors and trailer_link:
            movie = Movie(title=title, poster=poster, description=description, release_date=release_date, actors=actors, trailer_link=trailer_link, added_by=request.user)
            movie.save()
            movie.category.set(categories)
            return redirect('view_movie', movie_id=movie.id)
        else:
            return HttpResponseBadRequest('Please fill in all required fields.')

    categories = Category.objects.all()
    return render(request, 'add_movie.html', {'categories': categories})

@login_required
def view_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    return render(request, 'view_movie.html', {'movie': movie})

@login_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if movie.added_by != request.user:
        return HttpResponseForbidden()
    categories = Category.objects.all()
    selected_categories = movie.category.all()

    if request.method == 'POST':
        movie.title = request.POST.get('title')
        movie.description = request.POST.get('description')
        movie.release_date = request.POST.get('release_date')
        movie.actors = request.POST.get('actors')
        movie.category.set(request.POST.getlist('category'))
        movie.trailer_link = request.POST.get('trailer_link')
        
        if 'poster' in request.FILES:
            movie.poster = request.FILES['poster']
        
        movie.save()
        return redirect('view_movie', movie_id=movie.id)

    categories = Category.objects.all()
    return render(request, 'edit_movie.html', {'movie': movie, 'categories': categories,  'selected_categories': selected_categories})

@login_required
def delete_movies(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if movie.added_by != request.user:
        return HttpResponseForbidden("You do not have permission to delete this movie.")
    
    if request.method == 'POST':
        movie.delete()
        return redirect('profile') 
    
    return render(request, 'confirm_delete.html', {'movie': movie})
@login_required
def submit_review(request, movie_id):
    if request.method == 'POST':
        movie = Movie.objects.get(pk=movie_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError("Rating must be between 1 and 5.")
                Review.objects.create(movie=movie, user=request.user, rating=rating, comment=comment)
                return redirect('profile')
            except ValueError as e:
                return HttpResponseBadRequest("Invalid rating value.")
        else:
            return HttpResponseBadRequest("Rating and comment are required.")
    else:
        return render(request, 'submit_review.html', {'movie_id': movie_id})
    

def view_reviews(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie)
    return render(request, 'view_reviews.html', {'movie': movie, 'reviews': reviews})

def search_movies(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    movies = Movie.objects.all()
    
    if query:
        movies = movies.filter(title__icontains=query)
    
    if category_id:
        movies = movies.filter(category__id=category_id)
    
    categories = Category.objects.all()
    return render(request, 'search_movies.html', {'movies': movies, 'categories': categories, 'query': query, 'selected_category': category_id})

def genres_list(request):
    genres = Category.objects.all()
    return render(request, 'genres_list.html', {'genres': genres})

def movies_by_genre(request, category_id):
    genre = get_object_or_404(Category, id=category_id)
    movies = Movie.objects.filter(category=genre)
    return render(request, 'movies_by_genre.html', {'genre': genre, 'movies': movies})


def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all()
    movies = Movie.objects.all()
    genres = Category.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users, 'movies': movies, 'genres': genres})

@user_passes_test(is_admin)
def add_genre(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('admin_dashboard')
    return render(request, 'add_genre.html')

@user_passes_test(is_admin)
def add_movies(request):
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        release_date = request.POST.get('release_date')
        actors = request.POST.get('actors')
        trailer_link = request.POST.get('trailer_link')
        categories = request.POST.getlist('category')
        poster = request.FILES.get('poster')

        movie = Movie.objects.create(
            title=title,
            description=description,
            release_date=release_date,
            actors=actors,
            trailer_link=trailer_link,
            poster=poster,
            added_by=request.user
        )
        movie.category.set(categories)
        movie.save()
        return redirect('admin_dashboard')
    categories = Category.objects.all()
    return render(request, 'add_movies.html', {'categories': categories})

@user_passes_test(is_admin)
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_dashboard')
