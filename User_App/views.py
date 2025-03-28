from django.shortcuts import render,redirect,get_object_or_404
from Admin_App.views import *
from django.db.models import Q 
from django.utils.timezone import now
from datetime import date
from datetime import timedelta
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


# Import Q for complex queries


# Create your views here.

def user_home(request):
    movie = Movie.objects.all()
    genres = Genre.objects.all()
    recent_movies = Movie.objects.order_by('-release_date')[:4] 
    user_name = request.session.get('user_name', None)
    context={
        'user_name':user_name,
        'movie':movie,
        'genres':genres,
        'recent_movies': recent_movies
       
       
    }

    return render(request,"user_home.html",context)



def signup(request):
    if request.method == "POST":
        # Collect user inputs
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        repassword = request.POST['repassword']
        avatar = request.FILES.get('avatar')  # Fetch uploaded avatar (optional)

        # Check if username or email already exists
        if Viewers.objects.filter(Q(username__iexact=username) | Q(email__iexact=email)).exists():
            error_message = "Username or email already exists. Please choose another."
            messages.error(request, error_message)
            return render(request, "signup_error.html", {
                'username': username,
                'email': email,
                'phone': phone
            })

        # Check if passwords match
        if password != repassword:
            error_message = "Passwords do not match. Please try again."
            messages.error(request, error_message)
            return render(request, "signup_error.html", {
                'username': username,
                'email': email,
                'phone': phone
            })

        # Hash the password for security
        

        # Create the user, including avatar if provided
        Viewers.objects.create(
            username=username,
            email=email,
            phone=phone,
            password=password,
            avatar=avatar if avatar else 'avatars/default.png'  # Use default if no avatar
        )
        
        # Redirect to the user home or login page
        messages.success(request, "Signup successful! Please log in.")
        return redirect('user_home')

    # Render the signup form for GET requests
    return render(request, "signup.html")



def signup_error(request):
    return render(request, "signup_error.html")

       
def user_login(request):
    
    
    email=request.POST['email']
    password=request.POST['password']
    if email == "admin123@gmail.com" and password == "Admin@123":
        request.session['admin_id'] =16
        return redirect('admin_home')


    if Viewers.objects.filter(email=email, password=password).exists():
         data = Viewers.objects.filter(email=email, password=password).values('id','username').first()
         request.session['user_id'] = data['id']
         request.session['user_name'] = data['username']
         return redirect('user_home')
    else:
        return redirect('login_error')
    

def login_error(request):
 
 return render(request, "login_error.html")



def movie_details(request, m_id):
    if 'user_id' not in request.session:
        # Redirect to login_error page if the user is not logged in
        return redirect('login_error')

    # Fetch movie details and related data
    movie = get_object_or_404(Movie, id=m_id)
    comments = movie.comment_set.all()
    cast = Cast.objects.filter(movie=movie)
    user_name = request.session.get('user_name', None)
    user_id = request.session['user_id']
    user_favorite = Favourite.objects.filter(user=user_id, movie=movie).exists()
    data = Viewers.objects.get(id=user_id)

    try:
        user_reaction = User_like.objects.get(user_id=data, movie=movie).action
    except User_like.DoesNotExist:
        user_reaction = None

    # Update subscription status based on payment status
    subscriptions = Subscription_user.objects.filter(user_id=user_id, end_date__gte=date.today())
    for subscription in subscriptions:
        if subscription.payment_status == "paid":
            subscription.status = "active"
            subscription.save()
        else:
            subscription.status = "inactive"
            subscription.save()

    # Check if the user has a valid subscription and payment is completed
    has_valid_subscription = Subscription_user.objects.filter(
        user_id=data,
        status="active",
        end_date__gte=date.today(),
        payment_status="completed"
    ).exists()
    subscription = Subscription_user.objects.filter(user_id=user_id, status="active").first()

    # Pass payment status for frontend validation
    payment_status = subscription.payment_status if subscription else "none"

    context = {
        'details': movie,
        'cast': cast,
        'comments': comments,
        'user_reaction': user_reaction,
        'has_valid_subscription': has_valid_subscription,
        'user_name': user_name,
        'user_favorite': user_favorite,
        'subscription': subscription,
        'payment_status': payment_status,  # Pass payment status to the template
    }
    return render(request, 'movie_details.html', context)


def movie_search(request):
    query = request.GET.get('q', '')  # Get the search query
    movies = Movie.objects.all()  # Default: Get all movies

    if query:
        movies = movies.filter(
            movie_name__icontains=query
        ) | movies.filter(
            movie_genre__name__icontains=query
        )

    context = {
        'movies': movies,
        'query': query
    }
    return render(request, 'movie_search.html', context)






def user_logout(request):
   
    request.session.delete()
    return redirect('user_home')   


def update_profile(request):
    
    # Ensure the user is logged in
    if 'user_id' not in request.session:
        return redirect('user_home')
    user_id=request.session['user_id']
    user_name=request.session['user_name']
    v=get_object_or_404(Viewers,id=user_id)
    context={
        'v':v,
        'user_name':user_name
    }
    return render(request,"update_profile.html",context)

    


def profile_update(request):
    user_name = request.session.get('user_name', None)

    # Ensure the user is logged in
    if 'user_id' not in request.session:
        return redirect('user_home')

    user_id = request.session['user_id']
    viewer = Viewers.objects.get(id=user_id)

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
            avatar_file = viewer.avatar  # Keep the existing avatar if no file is uploaded

        # Handle password update
       
        if password:
            if password == repassword:
                password= password  # Replace this with `set_password()` for hashing
            else:
                # Render form with an error if passwords do not match
                return render(request, 'update_profile.html', {
                    'error': 'Passwords do not match.',
                    'viewer': viewer,
                    'user_name': user_name
                })
        else:
            password = Viewers.password  # Keep the existing password if not changed

        # Update database fields using variables
        Viewers.objects.filter(id=user_id).update(
            username=username,
            email=email,
            phone=phone,
            avatar=avatar_file,
            password=password
        )

        # Redirect to the home page after successful update
        return redirect('user_home')

    # Context for the template
    context = {
        'user_name': user_name,
        'viewer': viewer
    }

    return render(request, 'update_profile.html', context)




def add_comment(request, v_id):
    
    if 'user_id' not in request.session:  
        
        return redirect('login_error')  

    if request.method == 'POST':
        text = request.POST.get('comment_text')  
        if text:  
            movie = get_object_or_404(Movie, id=v_id)
            user_id = request.session['user_id']
            data = Viewers.objects.get(id=user_id) 
            
          
            Comment.objects.create(
                movie=movie,
                user=data,
                text=text
            )

        
        return redirect('movie_details', m_id=v_id)

    return redirect('movie_details', m_id=v_id)


def plan_details(request):
    plans=Subscription_plan.objects.all()
    user_name=request.session.get('user_name')
    context={
        'plans':plans,
        'user_name':user_name,
    }

    return render(request,"plan_details.html",context)



def add_subscription(request, plan_id):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to subscribe to a plan.")
        return redirect('login_error')

    user_id = request.session['user_id']
    data = Viewers.objects.get(id=user_id)
    plan = get_object_or_404(Subscription_plan, id=plan_id)
    
    # Check if there's an existing subscription for the user
    existing_subscription = Subscription_user.objects.filter(user=data).first()

    if existing_subscription:
        # If there's an active subscription, handle the payment status
        if existing_subscription.status == "active" and existing_subscription.end_date >= now().date():
            if existing_subscription.payment_status == "pending":
                # If payment is pending, just update the plan to the new one and redirect to confirm page
                existing_subscription.plan = plan
                existing_subscription.start_date = now().date()
                existing_subscription.end_date = now().date() + timedelta(days=int(plan.duration_days))
                existing_subscription.status = "active"  # Mark as active again after the change
                existing_subscription.payment_status = "pending"  # Keep it pending as it's not paid yet
                existing_subscription.save()
                return redirect('confirm', plan_id=plan.id)
            elif existing_subscription.payment_status == "paid":
                # If payment is completed, show a warning message for an active subscription
                messages.warning(request, "You already have an active subscription!")
                return redirect('plan_details')

        # If the subscription is inactive or expired, update it
        if existing_subscription.status == "inactive" or existing_subscription.end_date < now().date():
            existing_subscription.plan = plan
            existing_subscription.start_date = now().date()
            existing_subscription.end_date = now().date() + timedelta(days=int(plan.duration_days))
            existing_subscription.status = "active"
            existing_subscription.payment_status = "pending"  # Default to pending if it's not paid yet
            existing_subscription.save()
            return redirect('confirm', plan_id=plan.id)

    # If no existing subscription, create a new one
    Subscription_user.objects.create(
        plan=plan,
        user=data,
        start_date=now().date(),
        end_date=now().date() + timedelta(days=int(plan.duration_days)),
        status="active",
        payment_status="pending"  # Assume it's pending by default
    )

    return redirect('confirm', plan_id=plan.id)







def confirm_subscription(request, plan_id):
    # Check if the user is logged in
    if 'user_id' not in request.session:
        return redirect("login_error")

    user_id = request.session['user_id']
    user_name = request.session['user_name']
    
    # Get the subscription plan selected by the user
    subscription_plan = get_object_or_404(Subscription_plan, id=plan_id)

    # Get the subscription details for the user and selected plan
    user_subscription = get_object_or_404(Subscription_user, user_id=user_id, plan=subscription_plan)

    # Get the payment details for the user and selected plan (if exists)
    payment = Payment.objects.filter(subscription=user_subscription).last()  # Assuming the latest payment is the one you want

    # Pass the subscription and payment details to the context
    context = {
        'user_id': user_id,
        'plan': user_subscription,
        'user_name': user_name,
        'payment': payment,  # Add payment details to context
    }

    return render(request, "confirm_subscription.html", context)




def user_reaction(request, m_id, action):
    if request.method == 'POST':
       
        if action not in ['like', 'dislike']:
            messages.error(request, "Invalid action.")
            return redirect('movie_details', m_id=m_id)

        # Get the movie and user
        movie = get_object_or_404(Movie, id=m_id)
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "User not logged in.")
            return redirect('movie_details', m_id=m_id)

        # Check if the user has already reacted to this movie
        user_reaction = User_like.objects.filter(user_id=user_id, movie_id=movie.id).first()

        if user_reaction:
            # If the user is trying to change their reaction from like to dislike or vice-versa
            if user_reaction.action != action:
                # Remove the previous reaction (like or dislike)
                if user_reaction.action == 'like':
                    movie.like_count -= 1
                elif user_reaction.action == 'dislike':
                    movie.dislike_count -= 1

                # Remove the old reaction
                user_reaction.delete()

                # Create the new reaction (like or dislike)
                User_like.objects.create(user_id=user_id, movie_id=movie.id, action=action)

                if action == 'like':
                    movie.like_count += 1
                elif action == 'dislike':
                    movie.dislike_count += 1

                messages.success(request, f"Your {action} was recorded.")

            else:
                # If the user clicks the same reaction again (e.g., like to like), remove the reaction
                user_reaction.delete()
                if action == 'like':
                    movie.like_count -= 1
                elif action == 'dislike':
                    movie.dislike_count -= 1
                messages.success(request, f"Your {action} was removed.")
        else:
            
            User_like.objects.create(user_id=user_id, movie_id=movie.id, action=action)

            if action == 'like':
                movie.like_count += 1
            elif action == 'dislike':
                movie.dislike_count += 1

            messages.success(request, f"Your {action} was recorded.")

       
        movie.save()
        return redirect('movie_details', m_id=m_id)

    messages.error(request, "Invalid request method.")
    return redirect('movie_details', m_id=m_id)


def plan_history(request):
    if 'user_id' not in request.session:
      
        return redirect('login_error') 
    
    user_id = request.session['user_id']
    data = Viewers.objects.get(id=user_id) 
    user_name=request.session['user_name']
    active_plan = Subscription_user.objects.filter(user=data, status="active").first()
    plan_history = Subscription_user.objects.filter(user=data).order_by('-start_date')
    
    context = {
        'active_plan': active_plan,
        'plan_history': plan_history,
        'user_name':user_name,
    }
    return render(request, 'plan_history.html', context)


def view_profile(request):
    if 'user_id' not in request.session:
        return redirect('login_error')
    user_id=request.session['user_id']
    user_name=request.session.get('user_name')
    viewer=get_object_or_404(Viewers,id=user_id)
    context={
        'viewer':viewer,
        'user_name':user_name
   }
    return render(request,"view_profile.html",context)





def user_favourites(request):
    if 'user_id' not in request.session:
        return redirect('login_error') 

    user_id = request.session['user_id']
    fav_movies = Favourite.objects.filter(user=user_id)

    context = {
        'fav_movies': fav_movies, 
        'user_name': request.session.get('user_name'),
    }
    return render(request, "view_favourites.html", context)



def add_favourite(request, f_id, add):
    if 'user_id' not in request.session:
        return redirect('login_error')  

    user_id = request.session['user_id']
    user = get_object_or_404(Viewers, id=user_id)
    movie = get_object_or_404(Movie, id=f_id)

    if add != 'fav':
        return HttpResponse("Invalid action", status=400)  

    if Favourite.objects.filter(user=user, movie=movie).exists():
        Favourite.objects.filter(user=user, movie=movie).delete()
    else:
        Favourite.objects.create(user=user, movie=movie)

   
    return redirect(request.META.get('HTTP_REFERER', 'user_home'))


def liked_movies(request):
    if 'user_id' not in request.session:
        return redirect('login_error')
    user_id = request.session['user_id']
    like=User_like.objects.filter(user=user_id)
    context={
        'like':like,
        'user_name': request.session.get('user_name'),
    }


    return render(request,"liked_movies.html",context)





    # Fetch the subscription plan

def confirm(request, plan_id):
    if 'user_id' not in request.session:
        return redirect("login_error")
      
    user_id = request.session['user_id']
    user_name=request.session['user_name']
    
   
    subscription_plan = get_object_or_404(Subscription_plan, id=plan_id)

    user_subscription = get_object_or_404(Subscription_user, user_id=user_id, plan=subscription_plan)

    context = {
        'user_id': user_id,
        'plan': user_subscription,
        'user_name':user_name,
    }
    return render(request, "confirm.html", context)



 # Assuming 'User' is the model for the user


def process_payment(request, subscription_id):
    # Ensure the user is logged in
    if 'user_id' not in request.session:
        messages.warning(request, "You must be logged in to make a payment.")
        return redirect('login_error')

    user_id = request.session['user_id'] 
    subscription = get_object_or_404(Subscription_user, id=subscription_id, user_id=user_id)

    # Ensure the subscription is active and payment hasn't been made already
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        if payment_method not in   ['credit_card', 'paypal', 'bank_transfer']:
            messages.error(request, "Invalid payment method selected.")
            return redirect('process_payment', subscription_id=subscription_id)

        try:
            # Simulate payment creation
            payment = Payment.objects.create(
                user_id=user_id,
                subscription=subscription,
                amount=subscription.plan.price,
                status='pending',
                payment_method=payment_method,
            )

            # Simulate successful payment processing
            payment.status = 'completed'
            payment.transaction_id = f"txn_{now().strftime('%Y%m%d%H%M%S')}"
            payment.save()

            # Update subscription payment status and activate subscription
            subscription.payment_status = 'paid'
            subscription.status = 'active'
            subscription.save()

            # Send confirmation email
            user = Viewers.objects.get(id=user_id)  # Ensure using the correct model for user
            user_email = user.email  # Get the user's email directly from the User model
            if user_email:
                subject = 'Payment Successful!'
    # Render the email body from an HTML template
                message = render_to_string('mail.html', {
                'username': request.session.get('user_name', 'User'),
                'subscription': subscription,
                'transaction_id': payment.transaction_id,
                'amount': subscription.plan.price,
             })
            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user_email])
            email.content_subtype = "html"  # Specify that the content is HTML
            email.send()

            # Add success message
            messages.success(request, "Payment was successful!")
            return redirect('process_payment', subscription_id=subscription_id)

        except Exception as e:
            messages.error(request, f"Payment failed: {str(e)}")
            return redirect('process_payment', subscription_id=subscription_id)

    # Render the payment page for GET requests
    return render(request, 'payment.html', {
        'subscription': subscription,
        'confirm_url': reverse('confirm_subscription', args=[subscription.plan.id])
    })


def Films(request):
    # Check if user_id is in the session; if not, redirect to login
    if 'user_id' not in request.session:
        return redirect("login_error")  # Redirect to login page if user is not authenticated

    user_id = request.session['user_id']
    user_name = request.session['user_name']

    # Fetch the 10 most recently uploaded films
    recent_films = Movie.objects.all().order_by('-release_date')[:10]

    # Fetch all genres
    genres = Genre.objects.all()

    context = {
        'recent_films': recent_films,
        'genres': genres,
        'user_name': user_name,  # Pass the username to the template
    }

    return render(request, 'Films.html', context)

