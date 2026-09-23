from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from public.models import Lead, BlogPost, Category, CaseStudy, Guide

class DigitalDarkPlatformTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_group = Group.objects.create(name="Service Provider")
        
        # Staff user
        self.staff_user = User.objects.create_user("staff_member", "staff@test.com", "pass123")
        self.staff_user.is_staff = True
        self.staff_user.groups.add(self.staff_group)
        self.staff_user.save()

        # Superuser
        self.admin_user = User.objects.create_superuser("admin_member", "admin@test.com", "admin123")

        # Category
        self.category = Category.objects.create(name="SEO Growth")

    def test_public_lead_creation_newsletter(self):
        response = self.client.post(reverse('public:index'), {'email': 'newsletter@test.com'})
        self.assertEqual(response.status_code, 302)
        lead = Lead.objects.filter(email='newsletter@test.com').first()
        self.assertIsNotNone(lead)
        self.assertEqual(lead.source, 'newsletter')
        self.assertEqual(lead.status, 'new')

    def test_public_lead_creation_contact(self):
        response = self.client.post(reverse('public:contact'), {
            'name': 'John Doe',
            'email': 'john@test.com',
            'message': 'Growth inquiry'
        })
        self.assertEqual(response.status_code, 302)
        lead = Lead.objects.filter(email='john@test.com').first()
        self.assertIsNotNone(lead)
        self.assertEqual(lead.source, 'contact')

    def test_staff_login_and_access(self):
        login_success = self.client.login(username='staff_member', password='pass123')
        self.assertTrue(login_success)

        # Access staff dashboard
        res = self.client.get(reverse('agency_admin:staff_dashboard'))
        self.assertEqual(res.status_code, 200)

        # Access superuser control panel (should redirect/deny)
        res_admin = self.client.get(reverse('agency_admin:admin_dashboard'))
        self.assertIn(res_admin.status_code, [302, 403])

    def test_post_creation_and_superuser_publish_workflow(self):
        # 1. Staff logs in & creates draft post
        self.client.login(username='staff_member', password='pass123')
        post_data = {
            'title': 'High ROAS Scaling 2026',
            'category_id': self.category.id,
            'excerpt': 'Brief summary',
            'body': 'Full post content for testing',
            'status': 'review'
        }
        res_post = self.client.post(reverse('agency_admin:staff_post_create'), post_data)
        self.assertEqual(res_post.status_code, 302)

        post = BlogPost.objects.get(title='High ROAS Scaling 2026')
        self.assertEqual(post.status, 'review')

        # Visitor cannot see draft post on public blog page
        res_blog = self.client.get(reverse('public:blog'))
        self.assertNotIn('High ROAS Scaling 2026', res_blog.content.decode('utf-8'))

        # 2. Superuser logs in & publishes post
        self.client.login(username='admin_member', password='admin123')
        res_pub = self.client.get(reverse('agency_admin:admin_post_toggle_publish', args=[post.id]))
        self.assertEqual(res_pub.status_code, 302)

        post.refresh_from_db()
        self.assertEqual(post.status, 'published')

        # Visitor now sees published post live on public blog page
        res_blog_after = self.client.get(reverse('public:blog'))
        self.assertIn('High ROAS Scaling 2026', res_blog_after.content.decode('utf-8'))

    def test_admin_leads_csv_export(self):
        Lead.objects.create(email="export@test.com", source="course", status="new")
        self.client.login(username='admin_member', password='admin123')
        res = self.client.get(reverse('agency_admin:admin_leads_export_csv'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res['Content-Type'], 'text/csv')
        self.assertIn('export@test.com', res.content.decode('utf-8'))
