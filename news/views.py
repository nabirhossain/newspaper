from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, Http404, HttpResponseRedirect
from .models import author, Category,  Post, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateForm, CommentForm, registerUser, createAuthor
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q, Count, Max
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
#password change import
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


## registration with email imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
# close registration import
# token import
from .token import activation_token
# close token

# Create your views here.

def index(request):
    post = Post.published_objects.all().order_by('-posted')[0]                              ## SHOW POST FOR FIRST GRID
    post1 = Post.published_objects.all().order_by('-posted')[1:3]                           ## SHOW POST FOR SECOND GRID
    post2 = Post.published_objects.all().order_by('-posted')[3:9]                           ## SHOW POST FOR THIRD GRID
    all_post = Post.published_objects.all().order_by('-posted')                             ## SHOW ALL POSTS
    most_popular = Post.published_objects.all().order_by('-views')[:4]                      ## SHOW MOST POULAR NEWS
    recent = Post.published_objects.filter().order_by('-posted')[0:4]                       ## SHOW FOUR MOST RECENT NEWS
    search = request.GET.get('q')
    if search:
        all_post = all_post.filter(
            Q(title__icontains = search)|
            Q(body__icontains = search)
        )
    topic_cricket = get_object_or_404(Category, name='Cricket')                                          ## show some post for selected categories in home page
    cricket = Post.published_objects.all().filter(category=topic_cricket).order_by('-posted')[:4]
    cricket1 = Post.published_objects.all().filter(category=topic_cricket).order_by('-posted')[0]
    topic_tech = get_object_or_404(Category, name='Tech')
    tech = Post.published_objects.all().filter(category=topic_tech).order_by('-posted')[:7]
    tech1 = Post.published_objects.all().filter(category=topic_tech).order_by('-posted')[0]
    topic_world = get_object_or_404(Category, name='Worlds')
    worlds = Post.published_objects.all().filter(category=topic_world).order_by('-posted')[:3]
    worlds1 = Post.published_objects.all().filter(category=topic_world).order_by('-posted')[0]
    topic_opinion = get_object_or_404(Category, name='Opinion')
    opinion = Post.published_objects.all().filter(category=topic_opinion).order_by('-posted')[:3]
    opinion1 = Post.published_objects.all().filter(category=topic_opinion).order_by('-posted')[0]
    topic_health = get_object_or_404(Category, name='Health')
    health = Post.published_objects.all().filter(category=topic_health).order_by('-posted')[:3]
    health1 = Post.published_objects.all().filter(category=topic_health).order_by('-posted')[0]
    topic_entertainment = get_object_or_404(Category, name='Entertainment')
    entertainment = Post.published_objects.all().filter(category=topic_entertainment).order_by('-posted')[:4]
    entertainment1 = Post.published_objects.all().filter(category=topic_entertainment).order_by('-posted')[0]
    topic_business = get_object_or_404(Category, name='Business')
    business = Post.published_objects.all().filter(category=topic_business).order_by('-posted')[:3]
    business1 = Post.published_objects.all().filter(category=topic_business).order_by('-posted')[0]
    topic_bd = get_object_or_404(Category, name='Bangladesh')
    bangladesh = Post.published_objects.all().filter(category=topic_bd).order_by('-posted')[:4]
    bangladesh1 = Post.published_objects.all().filter(category=topic_bd).order_by('-posted')[0]
    bangladesh2 = Post.published_objects.all().filter(category=topic_bd).order_by('-posted')[1:3]
    topic_finance = get_object_or_404(Category, name='Finance')
    finance = Post.published_objects.all().filter(category=topic_finance).order_by('-posted')[:4]
    finance1 = Post.published_objects.all().filter(category=topic_finance).order_by('-posted')[0]

    context = {
        'post':post,
        'post1':post1,
        'post2':post2,
        'all_post' : all_post,
        'most_popular':most_popular,
        'tech':tech,
        'tech1':tech1,
        'recent':recent,
        'cricket': cricket,
        'cricket1': cricket1,
        'worlds' : worlds,
        'worlds1' : worlds1,
        'opinion':opinion,
        'opinion1':opinion1,
        'health' : health,
        'health1' : health1,
        'entertainment' : entertainment,
        'entertainment1' : entertainment1,
        'business' : business,
        'business1' : business1,
        'bangladesh' : bangladesh,
        'bangladesh1' : bangladesh1,
        'bangladesh2' : bangladesh2,
        'finance' : finance,
        'finance1' : finance1,


    }
    return render(request,'news/index.html', context)



def post_create(request):
    if request.user.is_authenticated:
        u = get_object_or_404(author, auth_name=request.user.id)
        form = CreateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = u
            instance.save()
            return redirect('news:index')
        return render(request, 'news/post_create.html', {"form": form,})
    else:
        return redirect('news:index')

@login_required
def PostUpdate(request, id):
    if request.user.is_authenticated:
        u = get_object_or_404(author, auth_name= request.user.id)
        post = get_object_or_404(Post, id=id)
        form = CreateForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = u
            instance.save()
            messages.success(request, "Post updated successfully")
            return redirect('news:CreateProfile')
        return render(request, 'news/post_create.html', {"form": form})
    else:
        return redirect('news:login')

@login_required
def PostDelete(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=id)
        post.delete()
        messages.warning(request, 'post deleted successfully')
        return redirect('news:CreateProfile')
    else:
        return redirect('news:login')


def PostDetail(request, id, tag_slug=None):
    post = get_object_or_404(Post, pk=id)
    post2 = Post.published_objects.all().order_by('-posted')[:5]
    most_popular = Post.published_objects.all().order_by('-views')[:5]  ## SHOW MOST POULAR NEWS
    recent = Post.published_objects.filter().order_by('-posted')[0:5]
    first = Post.published_objects.first()
    last = Post.published_objects.last()
    related = Post.published_objects.filter(category=post.category).exclude(id=id)[:6]
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post = post.filter(tags__in=[tag])
    if post.status == 'published':
        post.views += 1  # clock up the number of post views
        post.save()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post,  name=name, email=email, content=content, reply=comment_qs)
            comment.save()
    else:
        comment_form = CommentForm()

    context ={
        'post': post,
        'post2': post2,
        'tag' : tag,
        'first':first,
        'last': last,
        'related': related,
        'comments': comments,
        'most_popular': most_popular,
        'recent': recent,

    }
    return render(request,'news/post_detail.html', context)


def AllPost(request):
    post = Post.published_objects.all().order_by('-posted')
    most_popular = Post.published_objects.all().order_by('-views')[:4]
    recent = Post.published_objects.filter().order_by('-posted')[0:4]
    paginator = Paginator(post, 5)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 8 if index >= 8 else 0
    end_index = index + 8 if index <= max_index else max_index
    page_range = paginator.page_range[start_index:end_index]
    context = {
        'post':post,
        'items': items,
        'page_range': page_range,
        'most_popular': most_popular,
        'recent': recent,
    }
    return render(request,'news/all_post.html', context)


def PostCategory(request, name):
    topic = get_object_or_404(Category, name=name)
    post = Post.published_objects.filter(category=topic.id)[12:]
    post1 = Post.published_objects.filter(category=topic.id)[0]
    post2 = Post.published_objects.filter(category=topic.id)[1:4]
    post3 = Post.published_objects.filter(category=topic.id)[4:12]
    most_popular = Post.published_objects.filter(category=topic.id).order_by('-views')[:5]  ## SHOW MOST POULAR NEWS
    recent = Post.published_objects.filter(category=topic.id).order_by('-posted')[0:5]
    paginator = Paginator(post, 12)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 4 if index >= 4 else 0
    end_index = index + 4 if index <= max_index else max_index
    page_range = paginator.page_range[start_index:end_index]
    context = {
        'post': post,
        'topic': topic,
        'items': items,
        'page_range': page_range,
        'most_popular': most_popular,
        'recent': recent,
        'post1': post1,
        'post2': post2,
        'post3': post3,

    }

    return render(request,'news/category.html', context)

def signup(request):
    form =registerUser(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit = False)
            instance.is_active = False
            instance.save()
            site = get_current_site(request)
            mail_subject = "confirmation message for blog"
            message = render_to_string('registration/confirmation_email.html',{
                'user': instance,
                'domain': site.domain,
                'uid' : instance.id,
                'token': activation_token.make_token(instance)
            })
            to_email = form.cleaned_data.get('email')
            to_list = [to_email]
            from_email = settings.EMAIL_HOST_USER
            send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
            return HttpResponse("<h1>Thanks for your registration. A confirmation link was sent to your mail</h1>")
    else:
        form = registerUser()
    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html', context)

def activate(request, uid, token):
    try:
        user = get_object_or_404(User, pk=uid)
    except:
        raise Http404("No user found")
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("<h1>Account is activated. Now you can <a href='/articles/login'>login</a></h1>")
    else:
        return HttpResponse("<h3>Invalid activation</h3>")



# def signup(request):
#     kategorie = Category.objects.filter(parent=None).order_by('name')
#     breaking = Post.published_objects.all().order_by('-posted')[:6]
#     if request.method == 'POST':
#         form = registerUser(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('news:index')
#     else:
#         form = registerUser()
#     context = {
#         'form' : form,
#         'breaking': breaking,
#         'kategorie': kategorie,
#     }
#     return render(request, 'registration/signup.html', context)

def LogIn(request):
    if request.user.is_authenticated:
        return redirect('news:index')
    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('news:index')
            else:
                messages.add_message(request, messages.ERROR, 'username or password not match')
                return render(request, 'registration/login.html')
    return render(request,'registration/login.html')

def LogOut(request):
    logout(request)
    return redirect('news:index')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('news:index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


def CreateProfile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id= request.user.id)
        author_profile = author.objects.filter(auth_name = user.id)
        if author_profile:
            authorUser = get_object_or_404(author, auth_name = request.user.id)
            post = Post.published_objects.filter(author = authorUser.id)
            return render(request, 'news/author_posts_list.html', {"post":post}, {"user":authorUser})
        else:
            form = createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit = False)
                instance.auth_name = user
                instance.save()
                return redirect('news:CreateProfile')
            return render(request, 'news/create_author_profile.html', {"form":form})
    else:
        return redirect('news:login')


def getAuthor(request, name):
    p_author = get_object_or_404(User, username=name)
    auth = get_object_or_404(author, auth_name=p_author.id)
    post = Post.published_objects.filter(author=auth.id)
    cat = Category.objects.all()
    paginator = Paginator(post, 3)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 4 if index >= 4 else 0
    end_index = index + 4 if index <= max_index else max_index
    page_range = paginator.page_range[start_index:end_index]
    context = {
        'auth':auth,
        'cat':cat,
        'post':post,
        'items': items,
        'page_range': page_range
    }
    return render(request,'news/author_profile.html', context)




def search_posts(request):
    all_post = Post.published_objects.all().order_by('-posted')
    query = request.GET.get("q")
    if query:
        all_post = all_post.filter(
        Q(title__icontains=query) |
        Q(body__icontains=query) |
        Q(slug__icontains=query)
        ).distinct()
    context = {
        'all_post' : all_post,
    }
    return render(request, 'news/search_posts.html', context)



'''
#from django.db.models import Count

#popular_events = Events.objects.annotate(attendee_count=Count('attendee')).filter(attendee_count__gt=50)
#https://stackoverflow.com/questions/11127448/get-most-popular-list-in-django
'''
