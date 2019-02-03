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
    kategorie = Category.objects.filter(parent=None).order_by('name')                       ## SHOW CATEGORY AND SUB-CATEGORY IN DROPDOWN LIST
    post = Post.published_objects.all().order_by('-posted')[0]                              ## SHOW POST FOR FIRST GRID
    post1 = Post.published_objects.all().order_by('-posted')[1:3]                           ## SHOW POST FOR SECOND GRID
    post2 = Post.published_objects.all().order_by('-posted')[3:8]                           ## SHOW POST FOR THIRD GRID
    breaking = Post.published_objects.all().order_by('-posted')[:6]                         ## SHOW BREAKING NEWS
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
    cricket = Post.published_objects.all().filter(category=topic_cricket).order_by('-posted')[:2]
    cricket1 = Post.published_objects.all().filter(category=topic_cricket).order_by('-posted')[0]
    topic_tech = get_object_or_404(Category, name='Tech')
    tech = Post.published_objects.all().filter(category=topic_tech).order_by('-posted')[:5]
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
    topic_finance = get_object_or_404(Category, name='Finance')
    finance = Post.published_objects.all().filter(category=topic_finance).order_by('-posted')[:4]
    finance1 = Post.published_objects.all().filter(category=topic_finance).order_by('-posted')[0]

    context = {
        'post':post,
        'post1':post1,
        'post2':post2,
        'all_post' : all_post,
        'breaking' : breaking,
        'most_popular':most_popular,
        'tech':tech,
        'tech1':tech1,
        'kategorie':kategorie,
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
        'finance' : finance,
        'finance1' : finance1,


    }
    return render(request,'news/index.html', context)


@login_required
def post_create(request):
    if request.user.is_authenticated:
        u = get_object_or_404(author, auth_name=request.user.id)
        form = CreateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = u
            instance.save()
            return redirect('news:index')
        return render(request, 'news/post_create.html', {"form": form, })
    else:
        return redirect('news:index')

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
    breaking = Post.published_objects.all().order_by('-posted')[:6]
    kategorie = Category.objects.filter(parent=None).order_by('name')
    most_popular = Post.published_objects.all().order_by('-views')[:4]  ## SHOW MOST POULAR NEWS
    recent = Post.published_objects.filter().order_by('-posted')[0:4]
    first = Post.published_objects.first()
    last = Post.published_objects.last()
    related = Post.published_objects.filter(category=post.category).exclude(id=id)[:2]
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
        'breaking': breaking,
        'tag' : tag,
        'first':first,
        'last': last,
        'kategorie': kategorie,
        'related': related,
        'comments': comments,
        'most_popular': most_popular,
        'recent': recent,

    }
    return render(request,'news/post_detail.html', context)


def AllPost(request):
    post = Post.published_objects.all().order_by('-posted')
    breaking = Post.published_objects.all().order_by('-posted')[:6]
    most_popular = Post.published_objects.all().order_by('-views')[:4]
    recent = Post.published_objects.filter().order_by('-posted')[0:4]
    kategorie = Category.objects.filter(parent=None).order_by('name')
    search = request.GET.get('q')
    if search:
        post = post.filter(
            Q(title__icontains = search)|
            Q(body__icontains = search)
        )
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
        'breaking':breaking,
        'kategorie':kategorie,
        'items': items,
        'page_range': page_range,
        'most_popular': most_popular,
        'recent': recent,
    }
    return render(request,'news/all_post.html', context)


def PostCategory(request, name):
    topic = get_object_or_404(Category, name=name)
    post = Post.published_objects.filter(category=topic.id)
    kategorie = Category.objects.filter(parent=None).order_by('name')
    breaking = Post.published_objects.all().order_by('-posted')[:6]
    most_popular = Post.published_objects.filter(category=topic.id).order_by('-views')[:4]  ## SHOW MOST POULAR NEWS
    recent = Post.published_objects.filter(category=topic.id).order_by('-posted')[0:4]
    paginator = Paginator(post, 2)
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
        'breaking': breaking,
        'kategorie': kategorie,
        'items': items,
        'page_range': page_range,
        'most_popular': most_popular,
        'recent': recent,

    }

    return render(request,'news/category.html', context)


def signup(request):
    kategorie = Category.objects.filter(parent=None).order_by('name')
    breaking = Post.published_objects.all().order_by('-posted')[:6]
    if request.method == 'POST':
        form = registerUser(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('news:index')
    else:
        form = registerUser()
    context = {
        'form' : form,
        'breaking': breaking,
        'kategorie': kategorie,
    }
    return render(request, 'registration/signup.html', context)

def LogIn(request):
    kategorie = Category.objects.filter(parent=None).order_by('name')
    breaking = Post.published_objects.all().order_by('-posted')[:6]
    context = {

        'breaking': breaking,
        'kategorie': kategorie,
    }
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
    return render(request,'registration/login.html', context)

def LogOut(request):
    logout(request)
    return redirect('news:index')

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








'''
#from django.db.models import Count

#popular_events = Events.objects.annotate(attendee_count=Count('attendee')).filter(attendee_count__gt=50)
#https://stackoverflow.com/questions/11127448/get-most-popular-list-in-django
'''
