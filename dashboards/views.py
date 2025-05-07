from django.shortcuts import get_object_or_404, redirect, render
from blogs.models import Blog, Category
from dashboards.forms import BlogPostForm, CategoryForm
from django.template.defaultfilters import slugify

# Create your views here.

################# CRUD Y VISTAS PARA = CATEGORIAS  #################

def categories(request):    
    return render(request, 'dashboards/categories.html')

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
        
    form = CategoryForm()
    context = {
        'form' : form,
    }
    return render(request, 'dashboards/add_category.html', context)

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    
    form = CategoryForm(instance=category)
    context = {
        'form' : form,
        'category' : category,
    }
    return render (request, 'dashboards/edit_category.html', context)

def delete_category(request,pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')

################# CRUD Y VISTAS PARA = POSTS  #################

def posts(request):
    posts = Blog.objects.all()
    context = {
        'posts':posts,
    }
    return render(request, 'dashboards/posts.html', context)

def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('posts')
        
    form = BlogPostForm()
    context = {
        'form' : form,
    }
    return render(request, 'dashboards/add_post.html', context)

def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('posts')
    
    form = BlogPostForm(instance=post)
    context = {
        'form' : form,
        'post' : post,
    }
    return render (request, 'dashboards/edit_post.html', context)

def delete_post(request,pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('posts')