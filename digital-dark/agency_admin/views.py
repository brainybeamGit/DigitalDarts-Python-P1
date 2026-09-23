import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from public.models import Lead, BlogPost, CaseStudy, Guide, Service, Category, SiteSetting, LegalPage

# Role Check Decorators
def is_staff_user(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name='Service Provider').exists())

def is_super_user(user):
    return user.is_authenticated and user.is_superuser

# ==========================================
# STAFF PORTAL VIEWS (/staff/)
# ==========================================

def staff_login(request):
    if request.user.is_authenticated and is_staff_user(request.user):
        return redirect('agency_admin:staff_dashboard')
    
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None and is_staff_user(user):
            login(request, user)
            return redirect('agency_admin:staff_dashboard')
        else:
            messages.error(request, "Invalid staff credentials or access denied.")

    return render(request, 'agency_admin/staff_login.html')

@login_required(login_url='agency_admin:staff_login')
@user_passes_test(is_staff_user, login_url='agency_admin:staff_login')
def staff_logout(request):
    logout(request)
    messages.info(request, "Logged out of staff portal.")
    return redirect('agency_admin:staff_login')

@login_required(login_url='agency_admin:staff_login')
@user_passes_test(is_staff_user, login_url='agency_admin:staff_login')
def staff_dashboard(request):
    new_leads_count = Lead.objects.filter(status='new').count()
    pending_drafts_count = BlogPost.objects.filter(status__in=['draft', 'review']).count()
    recent_leads = Lead.objects.all()[:5]
    my_drafts = BlogPost.objects.filter(author=request.user)

    return render(request, 'agency_admin/staff_dashboard.html', {
        'new_leads_count': new_leads_count,
        'pending_drafts_count': pending_drafts_count,
        'recent_leads': recent_leads,
        'my_drafts': my_drafts,
    })

@login_required(login_url='agency_admin:staff_login')
@user_passes_test(is_staff_user, login_url='agency_admin:staff_login')
def staff_leads_list(request):
    status_filter = request.GET.get('status')
    source_filter = request.GET.get('source')

    leads = Lead.objects.all()
    if status_filter:
        leads = leads.filter(status=status_filter)
    if source_filter:
        leads = leads.filter(source=source_filter)

    return render(request, 'agency_admin/staff_leads.html', {
        'leads': leads,
        'selected_status': status_filter,
        'selected_source': source_filter,
    })

@login_required(login_url='agency_admin:staff_login')
@user_passes_test(is_staff_user, login_url='agency_admin:staff_login')
def staff_lead_detail(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        lead.status = request.POST.get('status', lead.status)
        new_note = request.POST.get('note', '').strip()
        if new_note:
            timestamp = timezone.now().strftime("%Y-%m-%d %H:%M")
            lead.notes = f"{lead.notes}\n[{timestamp} by {request.user.username}]: {new_note}".strip()
        lead.save()
        messages.success(request, f"Lead #{lead.id} updated successfully.")
        return redirect('agency_admin:staff_lead_detail', lead_id=lead.id)

    return render(request, 'agency_admin/staff_lead_detail.html', {'lead': lead})

@login_required(login_url='agency_admin:staff_login')
@user_passes_test(is_staff_user, login_url='agency_admin:staff_login')
def staff_posts_list(request):
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'agency_admin/staff_posts.html', {'posts': posts})

@login_required(login_url='agency_admin:staff_login')
@user_passes_test(is_staff_user, login_url='agency_admin:staff_login')
def staff_post_create(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        excerpt = request.POST.get('excerpt', '')
        body = request.POST.get('body')
        category_id = request.POST.get('category_id')
        status = request.POST.get('status', 'review')
        if status not in ['draft', 'review']:
            status = 'review' # Staff cannot publish directly

        cat = Category.objects.filter(id=category_id).first() if category_id else None
        post = BlogPost.objects.create(
            title=title,
            excerpt=excerpt,
            body=body,
            category=cat,
            author=request.user,
            status=status
        )
        messages.success(request, f"Post '{post.title}' submitted for review!")
        return redirect('agency_admin:staff_posts_list')

    return render(request, 'agency_admin/staff_post_form.html', {'categories': categories})

@login_required(login_url='agency_admin:staff_login')
@user_passes_test(is_staff_user, login_url='agency_admin:staff_login')
def staff_post_edit(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.excerpt = request.POST.get('excerpt', '')
        post.body = request.POST.get('body')
        category_id = request.POST.get('category_id')
        status = request.POST.get('status', 'review')
        if status not in ['draft', 'review']:
            status = 'review' # Staff cannot publish directly

        post.category = Category.objects.filter(id=category_id).first() if category_id else None
        post.status = status
        post.save()
        messages.success(request, f"Post '{post.title}' updated.")
        return redirect('agency_admin:staff_posts_list')

    return render(request, 'agency_admin/staff_post_form.html', {'post': post, 'categories': categories})

@login_required(login_url='agency_admin:staff_login')
@user_passes_test(is_staff_user, login_url='agency_admin:staff_login')
def staff_case_study_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        client_name = request.POST.get('client_name')
        summary = request.POST.get('summary')
        result = request.POST.get('result')
        story = request.POST.get('story')
        status = request.POST.get('status', 'review')
        if status not in ['draft', 'review']:
            status = 'review'

        cs = CaseStudy.objects.create(
            title=title,
            client_name=client_name,
            summary=summary,
            result=result,
            story=story,
            status=status
        )
        messages.success(request, f"Case study '{cs.title}' created.")
        return redirect('agency_admin:staff_dashboard')

    return render(request, 'agency_admin/staff_case_study_form.html')

@login_required(login_url='agency_admin:staff_login')
@user_passes_test(is_staff_user, login_url='agency_admin:staff_login')
def staff_case_study_edit(request, cs_id):
    cs = get_object_or_404(CaseStudy, id=cs_id)
    if request.method == 'POST':
        cs.title = request.POST.get('title')
        cs.client_name = request.POST.get('client_name')
        cs.summary = request.POST.get('summary')
        cs.result = request.POST.get('result')
        cs.story = request.POST.get('story')
        status = request.POST.get('status', 'review')
        if status not in ['draft', 'review']:
            status = 'review'
        cs.status = status
        cs.save()
        messages.success(request, f"Case study '{cs.title}' updated.")
        return redirect('agency_admin:staff_dashboard')

    return render(request, 'agency_admin/staff_case_study_form.html', {'case_study': cs})

@login_required(login_url='agency_admin:staff_login')
@user_passes_test(is_staff_user, login_url='agency_admin:staff_login')
def staff_guide_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        pdf_file = request.FILES.get('pdf_file')
        pdf_url = request.POST.get('pdf_url', '')

        g = Guide.objects.create(
            title=title,
            description=description,
            pdf_file=pdf_file,
            pdf_url=pdf_url
        )
        messages.success(request, f"Guide '{g.title}' uploaded.")
        return redirect('agency_admin:staff_dashboard')

    return render(request, 'agency_admin/staff_guide_form.html')


# ==========================================
# CUSTOM SUPERUSER ADMIN PORTAL VIEWS (/control/)
# ==========================================

def admin_login(request):
    if request.user.is_authenticated and is_super_user(request.user):
        return redirect('agency_admin:admin_dashboard')

    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None and is_super_user(user):
            login(request, user)
            return redirect('agency_admin:admin_dashboard')
        else:
            messages.error(request, "Superuser authorization failed.")

    return render(request, 'agency_admin/admin_login.html')

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_logout(request):
    logout(request)
    messages.info(request, "Logged out of admin control center.")
    return redirect('agency_admin:admin_login')

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_dashboard(request):
    total_leads = Lead.objects.count()
    new_leads = Lead.objects.filter(status='new').count()
    drafts_for_review = BlogPost.objects.filter(status='review').count()
    total_published_posts = BlogPost.objects.filter(status='published').count()
    recent_leads = Lead.objects.all()[:5]
    recent_drafts = BlogPost.objects.filter(status='review')[:5]

    return render(request, 'agency_admin/admin_dashboard.html', {
        'total_leads': total_leads,
        'new_leads': new_leads,
        'drafts_for_review': drafts_for_review,
        'total_published_posts': total_published_posts,
        'recent_leads': recent_leads,
        'recent_drafts': recent_drafts,
    })

# User Management (Superuser Full CRUD)
@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_users_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'agency_admin/admin_users.html', {'users_list': users})

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_user_create(request):
    groups = Group.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        is_staff = request.POST.get('is_staff') == 'on'
        group_id = request.POST.get('group_id')

        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' already exists.")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.is_staff = is_staff
            user.save()

            if group_id:
                grp = Group.objects.filter(id=group_id).first()
                if grp:
                    user.groups.add(grp)

            messages.success(request, f"User '{user.username}' created successfully.")
            return redirect('agency_admin:admin_users_list')

    return render(request, 'agency_admin/admin_user_form.html', {'groups': groups})

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_user_edit(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    groups = Group.objects.all()

    if request.method == 'POST':
        user_obj.email = request.POST.get('email', user_obj.email)
        user_obj.first_name = request.POST.get('first_name', user_obj.first_name)
        user_obj.last_name = request.POST.get('last_name', user_obj.last_name)
        user_obj.is_staff = request.POST.get('is_staff') == 'on'
        
        new_password = request.POST.get('password', '').strip()
        if new_password:
            user_obj.set_password(new_password)

        user_obj.save()

        group_id = request.POST.get('group_id')
        user_obj.groups.clear()
        if group_id:
            grp = Group.objects.filter(id=group_id).first()
            if grp:
                user_obj.groups.add(grp)

        messages.success(request, f"User '{user_obj.username}' updated.")
        return redirect('agency_admin:admin_users_list')

    return render(request, 'agency_admin/admin_user_form.html', {'user_obj': user_obj, 'groups': groups})

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_user_toggle_active(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if user_obj == request.user:
        messages.error(request, "Cannot deactivate your own active superuser session.")
    else:
        user_obj.is_active = not user_obj.is_active
        user_obj.save()
        status_str = "activated" if user_obj.is_active else "deactivated"
        messages.success(request, f"User '{user_obj.username}' {status_str}.")
    return redirect('agency_admin:admin_users_list')

# Leads Management & CSV Export
@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_leads_list(request):
    status_filter = request.GET.get('status')
    source_filter = request.GET.get('source')

    leads = Lead.objects.all()
    if status_filter:
        leads = leads.filter(status=status_filter)
    if source_filter:
        leads = leads.filter(source=source_filter)

    return render(request, 'agency_admin/admin_leads.html', {
        'leads': leads,
        'selected_status': status_filter,
        'selected_source': source_filter,
    })

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_lead_detail(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        lead.name = request.POST.get('name', lead.name)
        lead.email = request.POST.get('email', lead.email)
        lead.status = request.POST.get('status', lead.status)
        lead.source = request.POST.get('source', lead.source)
        lead.notes = request.POST.get('notes', lead.notes)
        lead.save()
        messages.success(request, f"Lead #{lead.id} saved.")
        return redirect('agency_admin:admin_leads_list')

    return render(request, 'agency_admin/admin_lead_detail.html', {'lead': lead})

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_lead_delete(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    lead.delete()
    messages.success(request, f"Lead #{lead_id} deleted.")
    return redirect('agency_admin:admin_leads_list')

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_leads_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="digital_dark_leads.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Email', 'Source', 'Status', 'Message', 'Notes', 'Created At'])

    for lead in Lead.objects.all():
        writer.writerow([
            lead.id,
            lead.name,
            lead.email,
            lead.get_source_display(),
            lead.get_status_display(),
            lead.message,
            lead.notes,
            lead.created_at.strftime("%Y-%m-%d %H:%M")
        ])

    return response

# Posts Approval & Publishing
@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_posts_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'agency_admin/admin_posts.html', {'posts': posts})

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_post_toggle_publish(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if post.status == 'published':
        post.status = 'draft'
        messages.info(request, f"Post '{post.title}' unpublished.")
    else:
        post.status = 'published'
        post.published_at = timezone.now()
        messages.success(request, f"Post '{post.title}' is NOW LIVE on public site (/blog/{post.slug}/)!")
    post.save()
    return redirect('agency_admin:admin_posts_list')

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_post_edit(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.excerpt = request.POST.get('excerpt', '')
        post.body = request.POST.get('body')
        category_id = request.POST.get('category_id')
        post.status = request.POST.get('status', post.status)

        post.category = Category.objects.filter(id=category_id).first() if category_id else None
        if post.status == 'published' and not post.published_at:
            post.published_at = timezone.now()

        post.save()
        messages.success(request, f"Post '{post.title}' saved.")
        return redirect('agency_admin:admin_posts_list')

    return render(request, 'agency_admin/admin_post_form.html', {'post': post, 'categories': categories})

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_post_delete(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('agency_admin:admin_posts_list')

# Case Studies Full CRUD
@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_case_studies_list(request):
    case_studies = CaseStudy.objects.all()
    return render(request, 'agency_admin/admin_case_studies.html', {'case_studies': case_studies})

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_case_study_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        client_name = request.POST.get('client_name')
        summary = request.POST.get('summary')
        result = request.POST.get('result')
        story = request.POST.get('story')
        status = request.POST.get('status', 'published')

        cs = CaseStudy.objects.create(
            title=title,
            client_name=client_name,
            summary=summary,
            result=result,
            story=story,
            status=status
        )
        messages.success(request, f"Case Study '{cs.title}' created.")
        return redirect('agency_admin:admin_case_studies_list')

    return render(request, 'agency_admin/admin_case_study_form.html')

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_case_study_edit(request, cs_id):
    cs = get_object_or_404(CaseStudy, id=cs_id)
    if request.method == 'POST':
        cs.title = request.POST.get('title')
        cs.client_name = request.POST.get('client_name')
        cs.summary = request.POST.get('summary')
        cs.result = request.POST.get('result')
        cs.story = request.POST.get('story')
        cs.status = request.POST.get('status', cs.status)
        cs.save()
        messages.success(request, f"Case Study '{cs.title}' updated.")
        return redirect('agency_admin:admin_case_studies_list')

    return render(request, 'agency_admin/admin_case_study_form.html', {'case_study': cs})

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_case_study_delete(request, cs_id):
    cs = get_object_or_404(CaseStudy, id=cs_id)
    cs.delete()
    messages.success(request, "Case study deleted.")
    return redirect('agency_admin:admin_case_studies_list')

# Services Full CRUD
@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_services_list(request):
    services = Service.objects.all()
    return render(request, 'agency_admin/admin_services.html', {'services': services})

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_service_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        short_description = request.POST.get('short_description')
        full_description = request.POST.get('full_description')
        icon = request.POST.get('icon', 'fa-rocket')
        order = request.POST.get('order', 0)

        s = Service.objects.create(
            title=title,
            short_description=short_description,
            full_description=full_description,
            icon=icon,
            order=order
        )
        messages.success(request, f"Service '{s.title}' created.")
        return redirect('agency_admin:admin_services_list')

    return render(request, 'agency_admin/admin_service_form.html')

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_service_edit(request, service_id):
    s = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        s.title = request.POST.get('title')
        s.short_description = request.POST.get('short_description')
        s.full_description = request.POST.get('full_description')
        s.icon = request.POST.get('icon', s.icon)
        s.order = request.POST.get('order', s.order)
        s.save()
        messages.success(request, f"Service '{s.title}' updated.")
        return redirect('agency_admin:admin_services_list')

    return render(request, 'agency_admin/admin_service_form.html', {'service': s})

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_service_delete(request, service_id):
    s = get_object_or_404(Service, id=service_id)
    s.delete()
    messages.success(request, "Service deleted.")
    return redirect('agency_admin:admin_services_list')

# Guides Full CRUD
@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_guides_list(request):
    guides = Guide.objects.all()
    return render(request, 'agency_admin/admin_guides.html', {'guides': guides})

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_guide_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        pdf_file = request.FILES.get('pdf_file')
        pdf_url = request.POST.get('pdf_url', '')

        g = Guide.objects.create(
            title=title,
            description=description,
            pdf_file=pdf_file,
            pdf_url=pdf_url
        )
        messages.success(request, f"Guide '{g.title}' created.")
        return redirect('agency_admin:admin_guides_list')

    return render(request, 'agency_admin/admin_guide_form.html')

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_guide_delete(request, guide_id):
    g = get_object_or_404(Guide, id=guide_id)
    g.delete()
    messages.success(request, "Guide deleted.")
    return redirect('agency_admin:admin_guides_list')

# Settings & Legal Pages
@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_settings(request):
    if request.method == 'POST':
        for key, val in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                setting_obj, created = SiteSetting.objects.get_or_create(key=key)
                setting_obj.value = val
                setting_obj.save()
        messages.success(request, "Site settings updated.")

    settings_dict = {s.key: s.value for s in SiteSetting.objects.all()}
    return render(request, 'agency_admin/admin_settings.html', {'settings_dict': settings_dict})

@login_required(login_url='agency_admin:admin_login')
@user_passes_test(is_super_user, login_url='agency_admin:admin_login')
def admin_pages(request):
    privacy_page, _ = LegalPage.objects.get_or_create(slug='privacy', defaults={'title': 'Privacy Policy', 'content': 'Default Privacy Policy.'})
    terms_page, _ = LegalPage.objects.get_or_create(slug='terms', defaults={'title': 'Terms of Service', 'content': 'Default Terms of Service.'})

    if request.method == 'POST':
        privacy_content = request.POST.get('privacy_content')
        terms_content = request.POST.get('terms_content')

        if privacy_content:
            privacy_page.content = privacy_content
            privacy_page.save()
        if terms_content:
            terms_page.content = terms_content
            terms_page.save()

        messages.success(request, "Legal pages content updated successfully.")

    return render(request, 'agency_admin/admin_pages.html', {
        'privacy_page': privacy_page,
        'terms_page': terms_page,
    })
