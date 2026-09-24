import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#5C4235"))
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Digital Dark Platform - Technical Documentation & Progress Report")
            self.setStrokeColor(colors.HexColor("#DFC2A8"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer (all pages)
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, footer_text)
        self.drawString(54, 36, "CONFIDENTIAL - Digital Dark Project Architecture Document")
        self.setStrokeColor(colors.HexColor("#DFC2A8"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        
        self.restoreState()

def create_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette matching Digital Dark
    c_espresso = colors.HexColor("#4E220F")
    c_copper = colors.HexColor("#9D6638")
    c_sage = colors.HexColor("#7A8564")
    c_cream = colors.HexColor("#F7F1DE")
    c_cream_alt = colors.HexColor("#FFFDF8")
    c_dark_bg = colors.HexColor("#1F0D05")
    c_text_dark = colors.HexColor("#2F1307")
    c_border = colors.HexColor("#E0D6C3")

    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_espresso,
        alignment=0,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_copper,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_espresso,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_copper,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_text_dark,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=4
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10,
        textColor=colors.white,
        alignment=0
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=c_text_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold',
        textColor=c_espresso
    )

    story = []

    # Document Header / Banner
    story.append(Paragraph("Digital Dark Platform", title_style))
    story.append(Paragraph("Comprehensive Project Documentation, Progress Report & Database Architecture", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_copper, spaceBefore=0, spaceAfter=15))

    # Executive Summary Card Box
    summary_html = """<b>Project Overview:</b> Digital Dark is a high-performance, luxury Shopify Google Ads & SEO growth agency web platform built with Django 6.1. It features a public client-facing portal, lead generation engine, staff management portal, superuser admin control panel, and dynamic content management system."""
    summary_table = Table([[Paragraph(summary_html, body_style)]], colWidths=[504])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_cream),
        ('BOX', (0,0), (-1,-1), 1, c_copper),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # SECTION 1: IMPLEMENTATION & PROGRESS REPORT
    # ---------------------------------------------------------
    story.append(Paragraph("1. Implementation & Progress Report", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_sage, spaceBefore=0, spaceAfter=10))

    progress_p1 = """This section details the start-to-finish process of technical enhancements and design implementations executed on the Digital Dark codebase:"""
    story.append(Paragraph(progress_p1, body_style))

    impl_items = [
        "<b>Route Bug Resolution (/case-studies/):</b> Resolved a <i>NoReverseMatch</i> server crash on <code>/case-studies/</code> by updating template URL reverse tags to properly supply <code>slug</code> arguments for dynamic case studies.",
        "<b>Superuser & Staff Login Redesign:</b> Implemented 60fps HTML5 Canvas real-time background particle and ambient bubble animations for <code>/control/login/</code> and <code>/control/staff/login/</code>. Fixed text contrast issues for input labels, headings, and focus states.",
        "<b>Sticky Top Navbar Enhancements:</b> Upgraded header navigation styling in <code>styles.css</code> with <code>rgba(247, 241, 222, 0.96)</code> glassmorphism blur, copper gradient active pills, and high-contrast button styling.",
        "<b>Free Course Form Redesign (/free-course/):</b> Lightened the dark form container into a luxury cream bubble card (<code>#FFFDF8</code>, <code>border-radius: 36px</code>), integrated floating ambient CSS bubbles, and formatted required headline and subhead texts.",
        "<b>Database Seeding & Test Verification:</b> Executed initial data seeding via <code>seed_initial_data.py</code> and verified 200 OK status codes across all public and admin endpoints."
    ]
    for item in impl_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # SECTION 2: USER ROLES & ACCESS CONTROL MATRIX
    # ---------------------------------------------------------
    story.append(Paragraph("2. User Roles & Access Control Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_sage, spaceBefore=0, spaceAfter=10))

    roles_data = [
        [
            Paragraph("Role Name", table_header_style),
            Paragraph("Access Level & Portal", table_header_style),
            Paragraph("System Permissions & Detailed Capabilities", table_header_style)
        ],
        [
            Paragraph("Customer / Public Visitor", table_cell_bold),
            Paragraph("Public Site<br/>(Unauthenticated)", table_cell_style),
            Paragraph("• Browse agency growth services and detailed service pages.<br/>• Read Shopify case studies and organic growth metrics.<br/>• Filter blog articles by categories and perform search queries.<br/>• Download PDF growth playbooks (triggers lead creation).<br/>• Submit free growth course enrollment form.<br/>• Submit general contact and store audit request forms.", table_cell_style)
        ],
        [
            Paragraph("Staff Member", table_cell_bold),
            Paragraph("Staff Portal<br/>(<code>/control/staff/</code>)", table_cell_style),
            Paragraph("• Restricted staff authentication portal (<code>is_staff=True</code>).<br/>• View incoming client leads and detailed lead notes.<br/>• Draft new blog articles (status forced to 'draft' or 'review').<br/>• Edit own blog drafts and submit for admin review.<br/>• Submit draft case studies and downloadable guides.", table_cell_style)
        ],
        [
            Paragraph("Superuser Admin", table_cell_bold),
            Paragraph("Control Panel<br/>(<code>/control/</code>)", table_cell_style),
            Paragraph("• Master superuser portal (<code>is_superuser=True</code>).<br/>• Complete lead pipeline management & CSV export.<br/>• Full user management (create, edit, activate/deactivate staff).<br/>• Blog moderation: publish, edit, or delete any post.<br/>• Case study & service CRUD management.<br/>• Global site settings & legal pages configuration.", table_cell_style)
        ]
    ]

    roles_table = Table(roles_data, colWidths=[110, 110, 284])
    roles_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_espresso),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,1), (-1,1), c_cream_alt),
        ('BACKGROUND', (0,2), (-1,2), colors.white),
        ('BACKGROUND', (0,3), (-1,3), c_cream_alt),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(roles_table)

    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # SECTION 3: COMPLETE DATABASE ARCHITECTURE SCHEMA
    # ---------------------------------------------------------
    story.append(PageBreak()) # Clean page break for schema
    story.append(Paragraph("3. Database Architecture & Model Schemas", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_sage, spaceBefore=0, spaceAfter=10))

    schema_intro = """The Digital Dark platform utilizes SQLite (relational database engine) managed via Django ORM. Below is the full attribute specification for every model entity:"""
    story.append(Paragraph(schema_intro, body_style))

    def make_model_table(model_name, description, field_rows):
        table_data = [
            [Paragraph("Field Name", table_header_style), Paragraph("Data Type", table_header_style), Paragraph("Key / Constraint", table_header_style), Paragraph("Description", table_header_style)]
        ]
        for row in field_rows:
            table_data.append([
                Paragraph(row[0], table_cell_bold),
                Paragraph(row[1], table_cell_style),
                Paragraph(row[2], table_cell_style),
                Paragraph(row[3], table_cell_style)
            ])
        
        t = Table(table_data, colWidths=[100, 110, 100, 194])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), c_copper),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_cream_alt]),
            ('PADDING', (0,0), (-1,-1), 4.5),
        ]))

        elements = [
            Paragraph(f"<b>Model Entity: <code>{model_name}</code></b>", h2_style),
            Paragraph(f"<i>Description:</i> {description}", body_style),
            t,
            Spacer(1, 10)
        ]
        return KeepTogether(elements)

    # 1. Lead Model
    story.append(make_model_table(
        "Lead (public.Lead)",
        "Captures customer lead inquiries, free course signups, PDF playbook downloads, and newsletter subscriptions.",
        [
            ["id", "BigAutoField", "PK, Auto", "Primary Key unique identifier."],
            ["name", "CharField(150)", "Optional, Default=''", "Full name of prospect user."],
            ["email", "EmailField", "Required", "Email address of lead."],
            ["message", "TextField", "Optional, Default=''", "Customer inquiry text message."],
            ["source", "CharField(20)", "Choices, Default='contact'", "Inquiry origin ('newsletter', 'guide', 'course', 'contact')."],
            ["status", "CharField(20)", "Choices, Default='new'", "Lead pipeline state ('new', 'contacted', 'qualified', 'closed')."],
            ["notes", "TextField", "Optional, Default=''", "Internal staff / admin follow-up notes."],
            ["created_at", "DateTimeField", "Auto Now Add", "Timestamp when record created."],
            ["updated_at", "DateTimeField", "Auto Now", "Timestamp of last modification."]
        ]
    ))

    # 2. Category Model
    story.append(make_model_table(
        "Category (public.Category)",
        "Taxonomy categories for organizing blog posts and educational content.",
        [
            ["id", "BigAutoField", "PK, Auto", "Primary Key unique identifier."],
            ["name", "CharField(100)", "Required", "Display name of category."],
            ["slug", "SlugField", "Unique, Auto Slug", "URL-friendly slug generated from name."]
        ]
    ))

    # 3. BlogPost Model
    story.append(make_model_table(
        "BlogPost (public.BlogPost)",
        "Stores editorial blog posts, growth case articles, and CRO insights.",
        [
            ["id", "BigAutoField", "PK, Auto", "Primary Key unique identifier."],
            ["title", "CharField(255)", "Required", "Article title."],
            ["slug", "SlugField", "Unique, Auto Slug", "URL slug identifier."],
            ["author", "ForeignKey(User)", "FK (auth_user.id)", "Author relation (Cascade delete)."],
            ["category", "ForeignKey(Category)", "FK (Category.id), Null", "Category relation (Set Null on delete)."],
            ["excerpt", "TextField", "Optional", "Brief preview text summary."],
            ["body", "TextField", "Required", "Full content text of post."],
            ["featured_image", "CharField(500)", "Optional", "Image URL / path."],
            ["status", "CharField(20)", "Choices, Default='draft'", "Publish state ('draft', 'review', 'published')."],
            ["published_at", "DateTimeField", "Null, Optional", "Timestamp when post published."],
            ["created_at", "DateTimeField", "Auto Now Add", "Creation timestamp."],
            ["updated_at", "DateTimeField", "Auto Now", "Last modification timestamp."]
        ]
    ))

    # 4. CaseStudy Model
    story.append(make_model_table(
        "CaseStudy (public.CaseStudy)",
        "Stores Shopify merchant growth proof, metrics, and strategy breakdowns.",
        [
            ["id", "BigAutoField", "PK, Auto", "Primary Key unique identifier."],
            ["title", "CharField(255)", "Required", "Case study headline."],
            ["slug", "SlugField", "Unique, Auto Slug", "Unique URL slug."],
            ["client_name", "CharField(150)", "Required", "Name of Shopify merchant / brand."],
            ["summary", "TextField", "Required", "Executive overview summary."],
            ["result", "CharField(255)", "Required", "Key metric highlight (e.g. '+340% ROAS')."],
            ["story", "TextField", "Required", "Detailed strategy and execution text."],
            ["image", "CharField(500)", "Optional", "Banner image URL / path."],
            ["status", "CharField(20)", "Choices, Default='draft'", "Publication status ('draft', 'review', 'published')."],
            ["created_at", "DateTimeField", "Auto Now Add", "Creation timestamp."]
        ]
    ))

    # 5. Guide Model
    story.append(make_model_table(
        "Guide (public.Guide)",
        "Downloadable PDF growth playbooks and lead magnets.",
        [
            ["id", "BigAutoField", "PK, Auto", "Primary Key unique identifier."],
            ["title", "CharField(255)", "Required", "Guide title."],
            ["slug", "SlugField", "Unique, Auto Slug", "URL slug."],
            ["description", "TextField", "Required", "Summary of guide content."],
            ["pdf_file", "FileField", "Upload to 'guides/'", "Uploaded PDF file asset."],
            ["pdf_url", "CharField(500)", "Optional", "Direct static URL to PDF."],
            ["created_at", "DateTimeField", "Auto Now Add", "Creation timestamp."]
        ]
    ))

    # 6. Service Model
    story.append(make_model_table(
        "Service (public.Service)",
        "Core agency growth services rendered on public pages.",
        [
            ["id", "BigAutoField", "PK, Auto", "Primary Key unique identifier."],
            ["title", "CharField(200)", "Required", "Service title."],
            ["slug", "SlugField", "Unique, Auto Slug", "URL slug."],
            ["short_description", "TextField", "Required", "Card summary text."],
            ["full_description", "TextField", "Required", "Comprehensive methodology text."],
            ["icon", "CharField(100)", "Default='fa-rocket'", "FontAwesome icon class name."],
            ["order", "IntegerField", "Default=0", "Display ordering integer."]
        ]
    ))

    # 7. SiteSetting & LegalPage Models
    story.append(make_model_table(
        "SiteSetting & LegalPage (public)",
        "Global configuration key-values and legal terms pages.",
        [
            ["key (SiteSetting)", "CharField(100)", "Unique", "Global setting key name."],
            ["value (SiteSetting)", "TextField", "Optional", "Setting value."],
            ["slug (LegalPage)", "SlugField", "Unique", "Legal page key ('privacy', 'terms')."],
            ["content (LegalPage)", "TextField", "Required", "Legal page terms content."]
        ]
    ))

    # ---------------------------------------------------------
    # SECTION 4: PROJECT WORKFLOW & SYSTEM DATA PIPELINE
    # ---------------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Project End-to-End Execution Flow", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_sage, spaceBefore=0, spaceAfter=10))

    flow_p1 = """The application follows a clean 3-tier architecture separating Public Prospecting, Staff Pipeline Management, and Superuser Administration:"""
    story.append(Paragraph(flow_p1, body_style))

    flow_steps = [
        "<b>Phase A (Lead Acquisition Flow):</b> Public visitor accesses site → submits Free Course or Guide Download form → Django view validates CSRF token → creates <code>Lead</code> object with <code>source='course'</code> and <code>status='new'</code> → renders success message.",
        "<b>Phase B (Staff Review Flow):</b> Staff member logs in at <code>/control/staff/login/</code> → authenticated session validated → accesses Staff Dashboard → views new lead inquiries and adds follow-up notes → drafts blog post or case study (status set to 'review').",
        "<b>Phase C (Superuser Approval & Export Flow):</b> Admin logs in at <code>/control/login/</code> → reviews pending drafts → publishes articles to public site → filters lead pipeline and exports CSV report via <code>/control/leads/export-csv/</code>."
    ]
    for step in flow_steps:
        story.append(Paragraph(f"• {step}", bullet_style))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=c_copper, spaceBefore=10, spaceAfter=10))
    story.append(Paragraph("End of Technical Documentation & Progress Report - Digital Dark Platform", ParagraphStyle('EndDoc', parent=body_style, fontName='Helvetica-Bold', alignment=1, textColor=c_copper)))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF report: {filename}")

if __name__ == '__main__':
    target_path = sys.argv[1] if len(sys.argv) > 1 else 'Digital_Dark_Project_Documentation.pdf'
    create_pdf(target_path)
