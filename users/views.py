from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserUpdateForm, JoinDoctorForm
from .models import DoctorApplication
from articles.models import Article  # Import the Article model
from .models import Review  # Import the Review model
from .forms import ReviewForm
import json


# Signup view
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}, your account has been created!")
            return redirect('home')
        else:
            messages.error(request, "Signup failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    return render(request, 'users/login.html')

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')

@login_required
def user_dashboard(request):
    application_status = None
    articles = None

    try:
        application = DoctorApplication.objects.get(user=request.user)
        if application.is_approved:
            application_status = "Approved"
            if request.user.is_doctor:
                from articles.models import Article
                articles = Article.objects.filter(author=request.user)
        else:
            application_status = "Pending"
    except DoctorApplication.DoesNotExist:
        application_status = None

    return render(request, 'users/user_dashboard.html', {
        'username': request.user.username,
        'application_status': application_status,
        'articles': articles,
    })


# Edit profile view
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('user_dashboard')
    else:
        form = CustomUserUpdateForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(participants=request.user).prefetch_related('participants', 'messages')
    formatted_conversations = []
    
    for conversation in conversations:
        # Find the other participant
        other_participant = conversation.participants.exclude(id=request.user.id).first()
        if other_participant:
            profile_picture_url = other_participant.profile_picture.url if other_participant.profile_picture else 'https://via.placeholder.com/40'
            last_message = conversation.messages.order_by('-timestamp').first()
            formatted_conversations.append({
                'id': conversation.id,
                'username': other_participant.username,
                'profile_picture_url': profile_picture_url,
                'last_message': last_message.content if last_message else "No messages yet"
            })
    
    return render(request, 'users/inbox.html', {'conversations': formatted_conversations})



from django.http import JsonResponse

from django.core.paginator import Paginator

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    if request.method == 'POST':
        # Handle sending a message
        data = json.loads(request.body)
        text = data.get('text')
        if text:
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=text,
            )
            return JsonResponse({
                'success': True,
                'message': {
                    'id': message.id,
                    'content': message.content,
                    'sender_id': message.sender.id,
                    'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                }
            })

    # Handle GET request for conversation details
    messages = conversation.messages.order_by('timestamp').values(
        'id', 'content', 'sender_id', 'timestamp'
    )
    # Safely fetch the other participant
    other_participant = (
        conversation.participants.exclude(id=request.user.id).first()
        if conversation.participants.count() > 1 else None
    )
    
    return JsonResponse({
        'other_participant': {
            'id': other_participant.id if other_participant else None,
            'username': other_participant.username if other_participant else None,
        },
        'messages': list(messages),
        'current_user_id': request.user.id,
    })



@login_required
def start_conversation(request, user_id):
    recipient = get_object_or_404(User, id=user_id)

    # Find an existing conversation between the two users
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=recipient).distinct().first()

    # If no conversation exists, create a new one
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, recipient)

    # Redirect to the conversation detail page
    return redirect('conversation_detail', conversation_id=conversation.id)



from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

@login_required
def search_users(request):
    query = request.GET.get('query', '')
    results = User.objects.filter(username__icontains=query).exclude(id=request.user.id)

    for user in results:
        # Ensure fallback URL for users without a profile picture
        user.profile_picture_url = (
            user.profile_picture.url if user.profile_picture else 'https://via.placeholder.com/40'
        )

    return render(request, 'users/search_users.html', {'results': results, 'query': query})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def send_message(request, conversation_id):
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        text = request.POST.get('text')
        if text:
            message = Message.objects.create(conversation=conversation, sender=request.user, content=text)
            return JsonResponse({
                                'success': True,
                                'message': {
                                    'id': message.id,
                                    'content': message.content,
                                    'sender_id': request.user.id,
                                    'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                }
                            })
        
    return JsonResponse({'success': False, 'error': 'Invalid request'})


# Join as a doctor view
@login_required
def join_as_doctor(request):
    if request.method == "POST":
        form = JoinDoctorForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if a DoctorApplication already exists for the user
            if DoctorApplication.objects.filter(user=request.user).exists():
                messages.error(request, "You have already submitted an application.")
                return redirect("user_dashboard")
            
            # Create a new DoctorApplication
            DoctorApplication.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                specialization=form.cleaned_data['specialization'],
                pmdc_number=form.cleaned_data['pmdc_number'],
                experience=form.cleaned_data['experience'],
                clinic_address=form.cleaned_data['clinic_address'],
                medical_certificate=form.cleaned_data['medical_certificate'],
            )
            messages.success(request, "Your application has been submitted successfully!")
            return redirect("user_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JoinDoctorForm()

    return render(request, "users/join_as_doctor.html", {"form": form})


# Approve doctor application view (for admin)
@login_required
def approve_doctor_application(request, application_id):
    if request.user.is_staff:  # Ensure only staff can approve
        try:
            application = DoctorApplication.objects.get(id=application_id, is_approved=False)
            application.is_approved = True
            application.save()
            application.user.is_doctor = True
            application.user.save()
            messages.success(request, f"Application for {application.full_name} has been approved!")
        except DoctorApplication.DoesNotExist:
            messages.error(request, "Application does not exist or has already been approved.")
    else:
        messages.error(request, "You do not have permission to perform this action.")
    return redirect("admin_dashboard")  # Redirect to admin dashboard or another admin page

from .forms import ReviewForm  # Replace with your actual form import



@login_required
def add_review(request):
    stars_range = range(1, 6)  # Define stars range
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)  # Don't save to database yet
            review.user = request.user  # Assign the logged-in user
            review.save()  # Now save to the database
            messages.success(request, "Your review has been submitted!")
            return redirect('review_list')  # Redirect to the review list page
        else:
            messages.error(request, "There was an error submitting your review. Please try again.")
            return render(request, 'users/add_review.html', {'form': form, 'stars_range': stars_range})
    else:
        form = ReviewForm()
        return render(request, 'users/add_review.html', {'form': form, 'stars_range': stars_range})



def review_list(request):
    reviews = Review.objects.order_by("-created_at")  # Recent reviews first
    return render(request, "users/review_list.html", {"reviews": reviews})
