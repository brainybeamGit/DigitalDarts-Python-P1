import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digital_dark.settings')
django.setup()

from django.contrib.auth.models import User, Group
from public.models import Category, BlogPost, CaseStudy, Guide, Service, SiteSetting, LegalPage, Lead

def seed():
    print("Seeding initial Digital Dark platform data...")

    # 1. Groups & Users
    staff_group, _ = Group.objects.get_or_create(name="Service Provider")
    
    # Superuser
    if not User.objects.filter(username="admin").exists():
        admin_user = User.objects.create_superuser("admin", "admin@digitaldark.com", "adminpass123")
        print("Created Superuser: admin / adminpass123")
    else:
        admin_user = User.objects.get(username="admin")

    # Staff User
    if not User.objects.filter(username="staff_user").exists():
        staff_user = User.objects.create_user("staff_user", "staff@digitaldark.com", "staffpass123")
        staff_user.is_staff = True
        staff_user.first_name = "Alex"
        staff_user.last_name = "Morgan"
        staff_user.save()
        staff_user.groups.add(staff_group)
        print("Created Staff User: staff_user / staffpass123")
    else:
        staff_user = User.objects.get(username="staff_user")

    # 2. Categories
    cat1, _ = Category.objects.get_or_create(name="Growth Marketing")
    cat2, _ = Category.objects.get_or_create(name="Conversion Rate Optimization")
    cat3, _ = Category.objects.get_or_create(name="Paid Search & Social")

    # 3. Services
    services_data = [
        {
            "title": "E-Commerce Growth Engineering",
            "short_description": "Data-driven scaling strategies for luxury and direct-to-consumer digital brands.",
            "full_description": "We engineer high-growth marketing funnels combining acquisition, retention, and custom analytics tracking.",
            "icon": "fa-chart-line",
            "order": 1
        },
        {
            "title": "Conversion Rate Optimization (CRO)",
            "short_description": "Turn visitors into buyers through rigorous A/B testing and behavioral psychology.",
            "full_description": "Our CRO framework optimizes UX friction points, page load performance, and checkout conversions.",
            "icon": "fa-bullseye",
            "order": 2
        },
        {
            "title": "Paid Media & Search Mastery",
            "short_description": "Precision ad campaigns across Meta, Google Search, YouTube, and TikTok.",
            "full_description": "Full-funnel campaign architecture designed to scale ROAS while maintaining brand authority.",
            "icon": "fa-ad",
            "order": 3
        }
    ]
    for s in services_data:
        Service.objects.get_or_create(title=s['title'], defaults=s)

    # 4. Blog Posts
    posts_data = [
        {
            "title": "Scaling DTC Brands in 2026: The New Rules of Customer Acquisition",
            "author": admin_user,
            "category": cat1,
            "excerpt": "Discover how leading luxury e-commerce brands maintain profitability while scaling paid ads in 2026.",
            "body": "In today's competitive landscape, customer acquisition costs require hyper-targeted creative testing and first-party data strategies...",
            "status": "published"
        },
        {
            "title": "5 High-Impact CRO Frameworks for High-Ticket E-commerce",
            "author": staff_user,
            "category": cat2,
            "excerpt": "A deep dive into checkout optimization techniques that increased revenue by 42%.",
            "body": "When selling premium products, visual hierarchy and micro-interactions dictate customer trust...",
            "status": "published"
        },
        {
            "title": "Draft Strategy: Retargeting Sequences for Q4 Launch",
            "author": staff_user,
            "category": cat3,
            "excerpt": "Draft framework for upcoming holiday campaign strategies.",
            "body": "Internal notes for seasonal retargeting ad sets and email flows...",
            "status": "review"
        }
    ]
    for p in posts_data:
        BlogPost.objects.get_or_create(title=p['title'], defaults=p)

    # 5. Case Studies
    case_data = [
        {
            "title": "340% ROAS Expansion for Luxury Apparel Brand",
            "client_name": "Aura Atelier",
            "summary": "Full digital overhaul and full-funnel media buy for premium fashion label.",
            "result": "+340% ROAS ($1.4M ARR)",
            "story": "Aura Atelier faced plateauing meta ad returns. We redesigned their mobile store landing pages and deployed high-converting video creative...",
            "status": "published"
        },
        {
            "title": "Scaling DTC Skincare Subscription Revenue by 210%",
            "client_name": "Botanica Glow",
            "summary": "Optimized subscriber retention and personalized quiz checkout flow.",
            "result": "+210% Monthly Recurring Revenue",
            "story": "By introducing personalized product match quizzes and automated multi-channel follow-ups, we increased LTV significantly...",
            "status": "published"
        }
    ]
    for c in case_data:
        CaseStudy.objects.get_or_create(title=c['title'], defaults=c)

    # 6. Guides
    Guide.objects.get_or_create(
        title="The Ultimate E-commerce CRO Checklist (2026 Edition)",
        defaults={
            "description": "A comprehensive 40-point checklist used by digital agencies to unlock 2x revenue growth.",
            "pdf_url": "/static/guides/cro-checklist-2026.pdf"
        }
    )

    # 7. Leads
    Leads_sample = [
        {"name": "Sarah Connor", "email": "sarah@cyberdyne.com", "source": "contact", "message": "Interested in scaling our store.", "status": "new"},
        {"name": "John Smith", "email": "john@example.com", "source": "newsletter", "status": "contacted"},
        {"name": "Emily Watson", "email": "emily@brand.co", "source": "guide", "status": "qualified"},
    ]
    for l in Leads_sample:
        Lead.objects.get_or_create(email=l['email'], defaults=l)

    # 8. Legal Pages & Settings
    LegalPage.objects.get_or_create(slug="privacy", defaults={"title": "Privacy Policy", "content": "Digital Dark respects your privacy. We store lead inquiries securely."})
    LegalPage.objects.get_or_create(slug="terms", defaults={"title": "Terms of Service", "content": "Terms of service and usage guidelines for Digital Dark services."})
    
    SiteSetting.objects.get_or_create(key="site_name", defaults={"value": "Digital Dark", "description": "Global website title"})
    SiteSetting.objects.get_or_create(key="contact_email", defaults={"value": "hello@digitaldark.agency", "description": "Support email"})

    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed()
