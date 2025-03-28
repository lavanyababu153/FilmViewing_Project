from django.shortcuts import render,redirect,get_object_or_404
from Admin_App.models import *
from User_App.models import *
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.
def admin_home(request):
    if 'admin_id' not in request.session:
        return redirect('user_home')
    
      # Redirect to user home if not logged in as admin
    total_movies = Movie.objects.count()

    # Get total genres count
    total_genres = Genre.objects.count()

    # Get the most liked movies (Top 5 movies by like_count)
    most_liked_movies = Movie.objects.order_by('-like_count')[:5]

    # Get the most disliked movies (Top 5 movies by dislike_count)
    most_disliked_movies = Movie.objects.order_by('-dislike_count')[:5]

    # Get subscription plans count
    total_plans = Subscription_plan.objects.count()

    # Get total cast count
    total_cast = Cast.objects.count()
    # Context for the template
    context = {
        'total_movies': total_movies,
        'total_genres': total_genres,
        'most_liked_movies': most_liked_movies,
        'most_disliked_movies': most_disliked_movies,
        'total_plans': total_plans,
        'total_cast': total_cast,
    }

    return render(request, 'admin_home.html',context)  


def admin_logout(request):
   
    request.session.delete()
    return redirect('user_home')   
 

def add_film(request):
    genres = Genre.objects.all()
    context = {
        'genres':genres
    }
    if request.method=="POST":

        movie_name =request.POST['title']
        movie_genre  =request.POST['genre']
        movie_file  =request.FILES['movie_file']
        movie_poster  =request.FILES['movie_poster']
        director_name  =request.POST['director']
        duration  =request.POST['duration']
        release_date  =request.POST['release_date']
        description = request.POST['description']

        Movie.objects.create(

            movie_name = movie_name,
            movie_genre  = Genre.objects.get(id=movie_genre),
            movie_file  =  movie_file,
            movie_poster  = movie_poster,
            director_name  = director_name,
            duration  = duration,
            release_date  = release_date,
            description= description


        )

    return render(request,"add_film.html", context)



def manage_film(request):
    r=Movie.objects.all()
    context={
        'r':r
    }

    return render(request,"manage_film.html",context)



def view_film(request):
    f=Movie.objects.all()
    context={
        'f':f

    }
    return render(request,"view_film.html",context)



def film_delete(request,f_id):

    Movie.objects.filter(id=f_id).delete()
    return redirect("manage_film")



def film_update(request,c_id):
    t=Movie.objects.filter(id=c_id)
    n = Genre.objects.all()
    context ={
        't':t,
        'n':n
    }
    return render(request,"film_update.html",context)



def update_movie(request, l_id):
    n = Genre.objects.all()
    context = {'n': n}

    if request.method == "POST":
        movie_name = request.POST['title']
        movie_genre = request.POST['genre']
        director_name = request.POST['director']
        duration = request.POST['duration']
        release_date = request.POST['release_date']
        description = request.POST['description']

        try:
            movie_poster = request.FILES['movie_poster']
            fs = FileSystemStorage()
            file = fs.save(movie_poster.name, movie_poster)
        except MultiValueDictKeyError:
            file = Movie.objects.get(id=l_id).movie_poster

        try:
            movie_file = request.FILES['movie_file']
            fv = FileSystemStorage()
            video = fv.save(movie_file.name, movie_file)
        except MultiValueDictKeyError:
            video = Movie.objects.get(id=l_id).movie_file

        Movie.objects.filter(id=l_id).update(
            movie_name=movie_name,
            movie_genre=Genre.objects.get(id=movie_genre),
            director_name=director_name,
            duration=duration,
            release_date=release_date,
            description=description,
            movie_poster=file,
            movie_file=video
        )

        return redirect("view_film")

    return render(request, "film_update.html", context)




def genre_add(request):
    if request.method=="POST":
        name =request.POST['name']
        image = request.FILES['image']
        Genre.objects.create(
            name=name,
            image=image
        )
    return render(request,"genre_add.html")



def manage_genre(request):
    m=Genre.objects.all()
    context={
        'm': m

    }
    return render(request,"manage_genre.html",context)



def genre_view(request):
    g=Genre.objects.all()
    context={
        'g':g

    }

    return render(request,"genre_view.html",context)


def genre_delete(request,gd_id):
    Genre.objects.filter(id=gd_id).delete() 
    return redirect("manage_genre")



def genre_update(request,u_id):
    u= Genre.objects.filter(id=u_id)
    context = {
        'u':u
    }
    return render(request,"genre_update.html",context)



def update_genre(request,p_id):
    if request.method=="POST":
        name=request.POST['name']
        try:
            image=request.FILES['image']
            fs=FileSystemStorage()
            file=fs.save(image.name,image)
        except MultiValueDictKeyError:
            file=Genre.objects.get(id=p_id).image
        Genre.objects.filter(id=p_id).update(
            name=name,
            image=file
        )

        return redirect("genre_view")
    return render(request,"genre_update.html")



 
def view_user(request):
    j=Viewers.objects.all()
    context={
        'j':j
    }

    return render(request,"view_user.html",context)


def add_cast(request):
   
       
    movie = Movie.objects.all()
    context = {
        'movie':movie
    }

    if request.method=="POST":

        movie_name =request.POST['movie_name']
        name = request.POST['name']
        role = request.POST['role']
        image = request.FILES['image']

        Cast.objects.create(

            movie = Movie.objects.get(id=movie_name),
            name= name,
            role = role,
            image = image
        )




    return render(request,"add_cast.html",context)


def view_cast(request):
    h=Cast.objects.all()
    context={
        'h':h
    }

    return render(request,"view_cast.html",context)

def manage_cast(request):
    j=Cast.objects.all()
    context={
        'j':j
    }
    return render(request,"manage_cast.html",context)

def cast_delete(request,c_id):
    Cast.objects.filter(id=c_id).delete()
    return redirect ("manage_cast")


def update_cast(request,s_id):
    g=Movie.objects.all()
    d=Cast.objects.filter(id=s_id)
    context={
        'd':d,
        'g':g
    }
    return render(request,"cast_update.html",context)



def cast_update(request,cast_id):
    if request.method=="POST":
        movie_name =request.POST['movie_name']
        name = request.POST['name']
        role = request.POST['role']
        try:
            image=request.FILES['image']
            fs=FileSystemStorage()
            file=fs.save(image.name,image)
        except MultiValueDictKeyError:
            file=Cast.objects.get(id=cast_id).image
        
        Cast.objects.filter(id=cast_id).update(
            movie = Movie.objects.get(id=movie_name),
            name= name,
            role = role,
            image = file
        )
        return redirect('manage_cast')
    return render(request,"cast_update.html")



def add_plan(request):
    if request.method == "POST":
        name=request.POST['name']
        duration_days=request.POST['duration_days']
        price=request.POST['price']
        advertisements=request.POST['advertisements']
        streaming_quality=request.POST['streaming_quality']
        Subscription_plan.objects.create(
            name=name,
            duration_days=duration_days,
            price=price,
            advertisements=advertisements,
            streaming_quality=streaming_quality


        )
    
    return render(request,"add_plan.html")


def manage_plan(request):
    p=Subscription_plan.objects.all()
    context={
        'p':p
    }
    return render(request,"manage_plan.html",context)

def delete_plan(request,p_id):
    Subscription_plan.objects.filter(id=p_id).delete()
    return redirect("manage_plan")



def update_plan(request,u_id):
    u=Subscription_plan.objects.filter(id=u_id)
    context={
        'u':u
    }
    return render(request,"update_plan.html",context)

def plan_update(request,b_id):
    if request.method == "POST":
        name=request.POST['name']
        duration_days=request.POST['duration_days']
        price=request.POST['price']
        advertisements=request.POST['advertisements']
        streaming_quality=request.POST['streaming_quality']
        Subscription_plan.objects.filter(id=b_id).update(
            name=name,
            duration_days=duration_days,
            price=price,
            advertisements=advertisements,
            streaming_quality=streaming_quality


        )
        return redirect("manage_plan")
    return render(request,"update_plan.html")

def view_plan(request):
    w=Subscription_plan.objects.all()
    context={
        'w':w
    }
    return render(request,"view_plan.html",context)




def view_comment(request,m_id):
    film=Comment.objects.filter(movie=m_id)
    films=get_object_or_404(Movie,id=m_id)
    context={
        'film':film,
        'films':films
    }
    return render(request,"view_comment.html",context)



def view_subscription(request):
    sub=Subscription_user.objects.all()
    context={
        'sub':sub
    }
    return render(request,"view_subscription.html",context)

def view_payment(request, sub_id):  # Ensure the parameter matches your URL pattern
    # Fetch the subscription record
    subscription = get_object_or_404(Subscription_user, id=sub_id)

    # Fetch the payment record associated with the subscription
    payment = get_object_or_404(Payment, subscription=subscription, user=subscription.user)

    # Pass the subscription and payment details to the template
    context = {
        'subscription': subscription,
        'payment': payment,
    }

    return render(request, "view_payment.html", context)


def admin_profile(request):
    try:
        # Manually fetch the Viewer with ID 0 (since that's what exists in your database)
        customer = Viewers.objects.get(id=0)
    except Viewers.DoesNotExist:
        # If the object does not exist, redirect to a safe page
        return redirect('user_home')

    # Prepare context with the customer's data
    context = {
        'customer': customer
    }

    # Render the admin profile page with the context
    return render(request, "admin_profile.html", context)



def admin_update(request):
    # Ensure the user is logged in as an admin
      # Redirect to the home page if not logged in as admin
    
    admin_id = 16
    admin = get_object_or_404(Viewers, id=admin_id)

    context = {
        'admin': admin
       
    }

    return render(request, "admin_profile_update.html", context)


def profile_update(request):
    # Hardcode the admin_id as 16 for demonstration
    admin_id = 16
    admin = get_object_or_404(Viewers, id=admin_id)

    if request.method == 'POST':
        # Extract form data
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        repassword = request.POST['repassword']

        # Handle avatar update
        try:
            avatar = request.FILES['avatar']
            fs = FileSystemStorage()
            avatar_file = fs.save(avatar.name, avatar)
        except MultiValueDictKeyError:
            avatar_file = admin.avatar  # Keep the existing avatar if no file is uploaded

        # Handle password update
        if password:
            if password == repassword:
                admin.password = password  # Save the plain password (not hashed)
            else:
                return render(request, 'admin_profile_update.html', {
                    'error': 'Passwords do not match.',
                    'admin': admin
                })
        else:
            # Keep the existing password if no new password is provided
            admin.password = admin.password

        # Update admin profile information
        admin.username = username
        admin.email = email
        admin.phone = phone
        admin.avatar = avatar_file
        admin.save()  # Save the updated admin data

        # Redirect to the admin profile page after successful update
        return redirect('admin_profile') 
    
    
     # Make sure 'admin_profile' is a valid URL

















 