from django.shortcuts import render
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from app.models import *
from app.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()

    return render(request, 'registration/registration_form.html', {'form': form})

@login_required(login_url='/accounts/login/')
def index(request):

    message = "Hello World"

    nhoods = Neighborhood.objects.all()
    context ={"nhoods":nhoods,"message":message}

    return render(request,'index.html',context)

@login_required(login_url='/accounts/login/')
def profile(request, username):
    title = "Profile"
    profile = User.objects.get(username=username)
    # comments = Comments.objects.all()
    users = User.objects.get(username=username)
    id = request.user.id
    form = ProfileForm()

    try :
        profile_info = Profile.get_by_id(profile.id)
    except:
        profile_info = Profile.filter_by_id(profile.id)


    # alerts = Project.get_profile_pic(profile.id)
    return render(request, 'registration/profile.html', {'title':title,'profile':profile,'profile_info':profile_info,"form":form})

@login_required(login_url='/accounts/login/')
def update_profile(request):

    profile = User.objects.get(username=request.user)
    try :
        profile_info = Profile.get_by_id(profile.id)
    except:
        profile_info = Profile.filter_by_id(profile.id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = request.user
            update.save()
            # return HttpResponseRedirect(reverse('profile', username=request.user))
            messages.success(request,"Profile Updated")
            return redirect('profile', username=request.user)
    else:
        form = ProfileForm()

    return render(request, 'registration/update_profile.html', {'form':form, 'profile_info':profile_info})

@login_required(login_url='/accounts/login')
def new_nhood(request):
    current_user = request.user
    if request.method == 'POST':
        form = NeighborhoodForm(request.POST,request.FILES)
        if form.is_valid():
            new_nhood = form.save(commit=False)
            new_nhood.user = current_user
            new_nhood.save()
            messages.success(request,"New Hood Created")
            return redirect('index')
    else:
            form = NeighborhoodForm()
            # context= {"form":form}
    return render(request, 'new_nhood.html',{"form":form})

@login_required(login_url='/accounts/login/')
def current_hood(request):
    return render(request, 'current_hood.html')


@login_required(login_url='/accounts/login/')
def join_hood(request,id):
    hood = get_object_or_404(Neighborhood, pk=id)
    request.user.wewe.neighborhood = hood
    request.user.wewe.save()
    messages.success(request, "You Just Joined a New Hood")
    return redirect('current_hood')

@login_required(login_url='/accounts/login/')
def exit_hood(request,id):
    hood = get_object_or_404(Neighborhood, pk=id)
    if request.user.wewe.neighborhood == hood:
        # request.user.wewe.neighborhood = Null
        # request.user.wewe.neighborhood = False
        # messages.success(request, "Image uploaded!")
        request.user.wewe.neighborhood = None
        request.user.wewe.save()
        messages.success(request,"Hood Exited")
    return redirect('index')

@login_required(login_url='/accounts/login/')
def new_business(request):
    current_user = request.user
    if request.method == 'POST':
        form = BusinessForm(request.POST,request.FILES)
        if form.is_valid():
            new_business = form.save(commit=False)
            new_business.user = current_user
            new_business.neighborhood=request.user.wewe.neighborhood
            assert isinstance(new_business.save, object)
            new_business.save()
            messages.success(request, "New Business Created")
            return redirect('current_hood')
    else:
        form = BusinessForm()
        # context= {"form":form}
    return render(request, 'new_business.html',{"form":form})

@login_required(login_url='/accounts/login/')
def new_alert(request):
    current_user = request.user
    if request.method == 'POST':
        form = AlertForm(request.POST,request.FILES)
        if form.is_valid():
            new_alert = form.save(commit=False)
            new_alert.user = current_user
            new_alert.neighborhood=request.user.wewe.neighborhood
            assert isinstance(new_alert.save, object)
            new_alert.save()
            messages.success(request, "Post created successfully")
            return redirect('current_hood')
    else:
        form = AlertForm()
                # context= {"form":form}
    return render(request, 'new_alert.html',{"form":form})

@login_required(login_url='/accounts/login/')
def search_business(request):
    # profile = Profile.get_profile()

    # if 'caption' in request.GET and request.GET["caption"]:
    if 'name' in request.GET and request.GET["name"]:

        search_term = request.GET.get("name")
        found_businesses = Business.search_by_name(search_term)
        message = f"{search_term}"
        print(search_term)

        context = {"found_businesses":found_businesses,"message":message}

        return render(request, 'search.html',context)

    else:
        message = "You haven't searched for any term"
        # context={"message":message}
        return render(request, 'search.html',{"message":message})

# @login_required(login_url='/accounts/login')
# def single_post(request,id):
#     alert = Alert.objects.get(id = id)
#     comments = Comment.objects.order_by('-date_posted')
#
#     context={"alert":alert,"comments":comments}
#     return render(request, 'single_post.html',context)

@login_required(login_url='/accounts/login/')
def post_comment(request,alert_id):
    # alerts = Alert.objects.get(id = alert_id)
    alerts = get_object_or_404(Alert, pk=alert_id)

    comments = Comment.objects.order_by('-date_posted')
    # alert = get_object_or_404(Alert, pk=alert_id)
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.alert = alerts
            comment.user = current_user
            comment.save()


            # return redirect('comment')
            return HttpResponseRedirect(reverse('comment', args=(alerts.id,)))
    else:
        form = CommentForm()
    return render(request, 'single_post.html', {"user":current_user,"alerts":alerts,"comments":comments,"form":form})

# def delete_post(request, postId):
#     Posts.objects.filter(pk=postId).delete()
#     messages.error(request, 'Succesfully Deleted a Post')
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# @login_required(login_url='/accounts/login/')
# def delete_hood(request, id):
#
#     Hood.objects.filter(user=request.user, pk=id).delete()
#     messages.error(request, 'Succesfully deleted your hood')
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
