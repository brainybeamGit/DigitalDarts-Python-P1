from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Lead, Service, BlogPost, CaseStudy, Guide, Category, LegalPage

def index(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            Lead.objects.create(email=email, source='newsletter', status='new')
            messages.success(request, "Thank you for subscribing to our newsletter!")
        return redirect('public:index')

    services = Service.objects.all()[:6]
    blog_posts = BlogPost.objects.filter(status='published')[:3]
    case_studies = CaseStudy.objects.filter(status='published')[:2]
    return render(request, 'public/index.html', {
        'services': services,
        'blog_posts': blog_posts,
        'case_studies': case_studies,
    })

def services(request):
    services_list = Service.objects.all()
    return render(request, 'public/services.html', {'services': services_list})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    other_services = Service.objects.exclude(id=service.id)[:3]
    return render(request, 'public/service_detail.html', {
        'service': service,
        'other_services': other_services,
    })

def case_studies(request):
    cases = CaseStudy.objects.filter(status='published')
    return render(request, 'public/case_studies.html', {'case_studies': cases})

def case_study_detail(request, slug):
    case_study = get_object_or_404(CaseStudy, slug=slug, status='published')
    return render(request, 'public/case_study_detail.html', {'case_study': case_study})

def blog(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '').strip()

    posts = BlogPost.objects.filter(status='published')
    categories = Category.objects.all()

    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    if search_query:
        posts = posts.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query) | Q(excerpt__icontains=search_query))

    return render(request, 'public/blog.html', {
        'posts': posts,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query,
    })

def blog_single(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    recent_posts = BlogPost.objects.filter(status='published').exclude(id=post.id)[:3]
    return render(request, 'public/blog_single.html', {
        'post': post,
        'recent_posts': recent_posts,
    })

def guides(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        guide_id = request.POST.get('guide_id')
        if email:
            Lead.objects.create(name=name, email=email, source='guide', status='new', notes=f"Downloaded guide #{guide_id}" if guide_id else "")
            messages.success(request, "Guide download link has been sent to your email!")
            return redirect('public:guides')

    guides_list = Guide.objects.all()
    return render(request, 'public/guides.html', {'guides': guides_list})

def free_course(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        if email:
            Lead.objects.create(name=name, email=email, source='course', status='new')
            messages.success(request, "Welcome to the Free Growth Course! Check your inbox for Module 1.")
            return redirect('public:free_course')

    return render(request, 'public/free_course.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message_text = request.POST.get('message', '').strip()

        if email and message_text:
            Lead.objects.create(name=name, email=email, message=message_text, source='contact', status='new')
            messages.success(request, "Your message has been sent successfully. Our team will contact you shortly!")
            return redirect('public:contact')
        else:
            messages.error(request, "Please fill out all required fields.")

    return render(request, 'public/contact.html')

def about(request):
    return render(request, 'public/about.html')

def careers(request):
    return render(request, 'public/careers.html')

def partners(request):
    return render(request, 'public/partners.html')

def privacy(request):
    page = LegalPage.objects.filter(slug='privacy').first()
    return render(request, 'public/legal.html', {'page': page, 'title': 'Privacy Policy'})

def terms(request):
    page = LegalPage.objects.filter(slug='terms').first()
    return render(request, 'public/legal.html', {'page': page, 'title': 'Terms of Service'})
