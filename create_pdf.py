#!/usr/bin/env python3
"""
Generate a polished PDF slide deck:
  Load Balancer Setup with Nginx on AlmaLinux

Reads the same content as the .pptx generator but renders directly to PDF
using fpdf2, producing a pixel-perfect dark-themed presentation.
"""

from fpdf import FPDF
import os, math

IMG_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Page geometry  (widescreen 16:9)
# ---------------------------------------------------------------------------
W = 338.667  # mm  (13.333 in)
H = 190.5    # mm  (7.5 in)

# ---------------------------------------------------------------------------
# Colour palette  (r, g, b)
# ---------------------------------------------------------------------------
BG_DARK       = (15, 23, 42)
BG_CARD       = (22, 33, 62)
ACCENT_BLUE   = (56, 189, 248)
ACCENT_GREEN  = (74, 222, 128)
ACCENT_PURPLE = (167, 139, 250)
ACCENT_ORANGE = (251, 146, 60)
ACCENT_PINK   = (244, 114, 182)
WHITE         = (255, 255, 255)
LIGHT_GRAY    = (203, 213, 225)
MID_GRAY      = (148, 163, 184)
CODE_BG       = (30, 41, 59)
DARK_ACCENT   = (20, 40, 80)

# ---------------------------------------------------------------------------
# PDF subclass
# ---------------------------------------------------------------------------
class SlidePDF(FPDF):
    def __init__(self):
        super().__init__(orientation="L", unit="mm", format=(H, W))
        self.set_auto_page_break(auto=False)
        self.set_margins(0, 0, 0)
        self.slide_num = 0
        self.total_slides = 16

    # -- helpers ----------------------------------------------------------
    def new_slide(self):
        self.add_page()
        self.slide_num += 1
        self.set_fill_color(*BG_DARK)
        self.rect(0, 0, W, H, "F")

    def slide_number(self):
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MID_GRAY)
        self.set_xy(W - 30, H - 8)
        self.cell(25, 5, f"{self.slide_num} / {self.total_slides}", align="R")

    def filled_rect(self, x, y, w, h, color, r=0):
        self.set_fill_color(*color)
        if r > 0:
            self.round_rect(x, y, w, h, r, style="F")
        else:
            self.rect(x, y, w, h, "F")

    def round_rect(self, x, y, w, h, r, style="F"):
        """Draw a rounded rectangle."""
        r = min(r, w/2, h/2)
        self.set_fill_color(*self._current_fill)
        # Use basic rect for simplicity (fpdf2 doesn't have native round_rect in all versions)
        self.rect(x, y, w, h, style)

    def _set_fill(self, color):
        self._current_fill = color
        self.set_fill_color(*color)

    def card(self, x, y, w, h, color=BG_CARD, accent_color=None):
        self.set_fill_color(*color)
        self.rect(x, y, w, h, "F")
        if accent_color:
            self.set_fill_color(*accent_color)
            self.rect(x, y, w, 1.2, "F")

    def accent_line(self, x, y, w, color=ACCENT_BLUE):
        self.set_fill_color(*color)
        self.rect(x, y, w, 0.8, "F")

    def text_at(self, x, y, w, text, size=10, color=WHITE, bold=False,
                align="L", font="Helvetica"):
        style = "B" if bold else ""
        self.set_font(font, style, size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.cell(w, size * 0.5, text, align=align)

    def mtext_at(self, x, y, w, h, text, size=10, color=WHITE, bold=False,
                 align="L", font="Helvetica", line_h=None):
        style = "B" if bold else ""
        self.set_font(font, style, size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        lh = line_h if line_h else size * 0.55
        self.multi_cell(w, lh, text, align=align)

    def badge(self, text, color=ACCENT_BLUE):
        self.set_fill_color(*color)
        tw = len(text) * 1.8 + 6
        self.rect(12, 8, tw, 7, "F")
        self.set_font("Helvetica", "B", 6.5)
        self.set_text_color(*BG_DARK)
        self.set_xy(12, 8.5)
        self.cell(tw, 6, text, align="C")

    def slide_title(self, text, y=20, color=WHITE):
        self.text_at(15, y, W - 30, text, size=22, color=color, bold=True)

    def subtitle_line(self, y=28, color=ACCENT_BLUE):
        self.accent_line(15, y, 50, color)

    def place_image(self, path, x, y, w, h):
        if os.path.exists(path):
            self.image(path, x, y, w, h)


# ---------------------------------------------------------------------------
# BUILD SLIDES
# ---------------------------------------------------------------------------
pdf = SlidePDF()

# ===================================================================
# SLIDE 1 — TITLE
# ===================================================================
pdf.new_slide()
# Decorative circles
pdf.set_fill_color(*DARK_ACCENT)
pdf.ellipse(-15, -15, 100, 100, "F")
pdf.ellipse(W - 70, H - 80, 110, 110, "F")

pdf.accent_line(30, 42, 60, ACCENT_BLUE)

pdf.text_at(30, 47, W - 60, "Load Balancer Setup", size=30, color=WHITE, bold=True)
pdf.text_at(30, 62, W - 60, "with Nginx on AlmaLinux", size=22, color=ACCENT_BLUE)

pdf.accent_line(30, 77, 100, ACCENT_PURPLE)

pdf.text_at(30, 82, W - 60, "High-Availability Web Infrastructure  |  Step-by-Step Guide",
            size=11, color=LIGHT_GRAY)
pdf.text_at(30, 92, W - 60, "April 2026  |  AlmaLinux 10  |  Nginx 1.26  |  PHP-FPM",
            size=9, color=MID_GRAY)

# Group-2 members card
pdf.card(W - 130, 40, 115, 68, accent_color=ACCENT_PURPLE)
pdf.text_at(W - 125, 44, 105, "Group-2", size=14, color=ACCENT_PURPLE, bold=True, align="C")
pdf.accent_line(W - 110, 53, 60, ACCENT_PURPLE)
members = [
    ("1.", "Suon Pisey", ACCENT_BLUE),
    ("2.", "Nem Sothea", ACCENT_GREEN),
    ("3.", "Sourn Savourn", ACCENT_PURPLE),
    ("4.", "Oun Sreynich", ACCENT_ORANGE),
    ("5.", "Moeun Nithvaraman", ACCENT_PINK),
]
for j, (num, name, mcolor) in enumerate(members):
    my = 57 + j * 9
    pdf.set_fill_color(*mcolor)
    pdf.ellipse(W - 122, my + 1.5, 2.5, 2.5, "F")
    pdf.text_at(W - 118, my, 100, f"{num}  {name}", size=8.5, color=LIGHT_GRAY)

pdf.slide_number()

# ===================================================================
# SLIDE 2 — TABLE OF CONTENTS
# ===================================================================
pdf.new_slide()
pdf.badge("OVERVIEW")
pdf.slide_title("Table of Contents")
pdf.subtitle_line()

toc = [
    ("01", "Project Overview", ACCENT_BLUE),
    ("02", "Why Use a Load Balancer?", ACCENT_GREEN),
    ("03", "Architecture & Process Flow", ACCENT_PURPLE),
    ("04", "Environment Details", ACCENT_ORANGE),
    ("05", "Phase 1 : VM1 - Websites + Dashboard", ACCENT_BLUE),
    ("06", "Phase 1 : Configuration & SELinux", ACCENT_GREEN),
    ("07", "Phase 2 : VM2 - Load Balancer Setup", ACCENT_PURPLE),
    ("08", "Demo : Site A & Site B", ACCENT_ORANGE),
    ("09", "Demo : Health Dashboard", ACCENT_PINK),
    ("10", "Demo : Nginx Load Balancer in Action", ACCENT_BLUE),
    ("11", "Verification & Testing", ACCENT_GREEN),
    ("12", "Challenges & Solutions", ACCENT_PURPLE),
    ("13", "Extending the Infrastructure", ACCENT_ORANGE),
    ("14", "Conclusion", ACCENT_PINK),
]

col1 = toc[:7]
col2 = toc[7:]

for i, (num, title, color) in enumerate(col1):
    y = 36 + i * 10
    pdf.set_fill_color(*color)
    pdf.rect(15, y, 10, 7, "F")
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*BG_DARK)
    pdf.set_xy(15, y + 0.5)
    pdf.cell(10, 6, num, align="C")
    pdf.text_at(28, y + 1, 120, title, size=9.5, color=LIGHT_GRAY)

for i, (num, title, color) in enumerate(col2):
    y = 36 + i * 10
    pdf.set_fill_color(*color)
    pdf.rect(170, y, 10, 7, "F")
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*BG_DARK)
    pdf.set_xy(170, y + 0.5)
    pdf.cell(10, 6, num, align="C")
    pdf.text_at(183, y + 1, 120, title, size=9.5, color=LIGHT_GRAY)

pdf.slide_number()

# ===================================================================
# SLIDE 3 — PROJECT OVERVIEW
# ===================================================================
pdf.new_slide()
pdf.badge("01  PROJECT OVERVIEW")
pdf.slide_title("Project Overview")
pdf.subtitle_line()

pdf.text_at(15, 33, W - 30,
            "Two virtual machines working together as a high-availability web infrastructure",
            size=11, color=LIGHT_GRAY)

# VM1 Card
pdf.card(15, 42, 150, 62, accent_color=ACCENT_BLUE)
pdf.text_at(20, 46, 140, "VM1  -  Web Server  (192.168.1.8)", size=12, color=ACCENT_BLUE, bold=True)
pdf.accent_line(20, 55, 40, ACCENT_BLUE)
vm1_lines = [
    "Site A on port 8081 (Primary Web App)",
    "Site B on port 8082 (Secondary Web App)",
    "Health Dashboard on port 8080",
    "PHP-FPM for dynamic content",
    "Real-time uptime monitoring",
]
for j, line in enumerate(vm1_lines):
    pdf.text_at(24, 59 + j * 8, 130, f"   {line}", size=9, color=LIGHT_GRAY)

# VM2 Card
pdf.card(175, 42, 150, 62, accent_color=ACCENT_PURPLE)
pdf.text_at(180, 46, 140, "VM2  -  Load Balancer  (192.168.1.20)", size=12, color=ACCENT_PURPLE, bold=True)
pdf.accent_line(180, 55, 40, ACCENT_PURPLE)
vm2_lines = [
    "Nginx reverse proxy on port 80",
    "Round-robin traffic distribution",
    "Proxies to VM1:8081 and VM1:8082",
    "Automatic failover on backend failure",
    "Single public entry point for users",
]
for j, line in enumerate(vm2_lines):
    pdf.text_at(184, 59 + j * 8, 130, f"   {line}", size=9, color=LIGHT_GRAY)

pdf.slide_number()

# ===================================================================
# SLIDE 4 — WHY LOAD BALANCER?
# ===================================================================
pdf.new_slide()
pdf.badge("02  WHY LOAD BALANCER?", ACCENT_GREEN)
pdf.slide_title("Why Use a Load Balancer?")
pdf.subtitle_line(color=ACCENT_GREEN)

reasons = [
    ("High Availability", "If one backend fails, traffic is\nautomatically redirected to\nthe healthy one.", ACCENT_BLUE),
    ("Scalability", "Add more backend servers without\nchanging the public endpoint.", ACCENT_GREEN),
    ("Traffic Distribution", "Prevents overload on a single\nserver using round-robin,\nleast connections, etc.", ACCENT_PURPLE),
    ("Zero-Downtime Maintenance", "Take one backend offline while\nthe other continues serving\nrequests.", ACCENT_ORANGE),
    ("Simplified SSL/TLS", "Terminate certificates on the\nload balancer only - backends\nstay simple.", ACCENT_PINK),
]

for i, (title, desc, color) in enumerate(reasons):
    col = i % 3
    row = i // 3
    x = 15 + col * 106
    y = 35 + row * 48
    cw = 98
    ch = 43

    pdf.card(x, y, cw, ch, accent_color=color)
    pdf.text_at(x + 5, y + 5, cw - 10, title, size=11, color=color, bold=True)
    pdf.mtext_at(x + 5, y + 16, cw - 10, 25, desc, size=8.5, color=LIGHT_GRAY, line_h=5)

pdf.slide_number()

# ===================================================================
# SLIDE 5 — ARCHITECTURE
# ===================================================================
pdf.new_slide()
pdf.badge("03  ARCHITECTURE", ACCENT_PURPLE)
pdf.slide_title("Architecture & Process Flow")
pdf.subtitle_line(color=ACCENT_PURPLE)

# Client box
pdf.set_fill_color(*ACCENT_BLUE)
pdf.rect(135, 34, 68, 12, "F")
pdf.text_at(135, 36, 68, "Client Request", size=10, color=BG_DARK, bold=True, align="C")

# Arrow
pdf.set_fill_color(*ACCENT_BLUE)
pdf.rect(168, 46, 1.2, 8, "F")

# VM2 LB box
pdf.card(95, 55, 148, 28, accent_color=ACCENT_PURPLE)
pdf.text_at(100, 58, 138, "VM2  -  Nginx Load Balancer  (port 80)",
            size=11, color=ACCENT_PURPLE, bold=True, align="C")
pdf.text_at(100, 68, 138, "upstream: 192.168.1.8:8081  |  192.168.1.8:8082",
            size=8, color=LIGHT_GRAY, align="C")
pdf.text_at(100, 74, 138, "Algorithm: Round-Robin  |  Failover: Automatic",
            size=8, color=LIGHT_GRAY, align="C")

# Arrows down
pdf.set_fill_color(*ACCENT_BLUE)
pdf.rect(140, 83, 1.2, 8, "F")
pdf.set_fill_color(*ACCENT_GREEN)
pdf.rect(198, 83, 1.2, 8, "F")

# Site A
pdf.card(100, 92, 78, 24, accent_color=ACCENT_BLUE)
pdf.text_at(105, 96, 68, "Site A  (port 8081)", size=10, color=ACCENT_BLUE, bold=True, align="C")
pdf.text_at(105, 105, 68, "Primary Web Application", size=7.5, color=LIGHT_GRAY, align="C")
pdf.text_at(105, 110, 68, "VM1: 192.168.1.8", size=7, color=MID_GRAY, align="C")

# Site B
pdf.card(162, 92, 78, 24, accent_color=ACCENT_GREEN)
pdf.text_at(167, 96, 68, "Site B  (port 8082)", size=10, color=ACCENT_GREEN, bold=True, align="C")
pdf.text_at(167, 105, 68, "Secondary Web Application", size=7.5, color=LIGHT_GRAY, align="C")
pdf.text_at(167, 110, 68, "VM1: 192.168.1.8", size=7, color=MID_GRAY, align="C")

# Dashboard box (left)
pdf.card(10, 60, 72, 36, accent_color=ACCENT_ORANGE)
pdf.text_at(15, 64, 62, "Health Dashboard", size=10, color=ACCENT_ORANGE, bold=True, align="C")
pdf.mtext_at(15, 73, 62, 20,
             "Port 8080\nAuto-refresh every 10s\nMonitors both backends\nResponse time in ms",
             size=7.5, color=LIGHT_GRAY, align="C", line_h=5)

# Flow steps (right)
pdf.card(255, 36, 72, 80, accent_color=ACCENT_PINK)
pdf.text_at(259, 40, 64, "Request Flow", size=10, color=ACCENT_PINK, bold=True)
flow = [
    "1. User accesses VM2 IP",
    "2. Nginx selects backend",
    "3. Proxied to :8081/:8082",
    "4. Backend responds",
    "5. Dashboard health check",
]
for j, f in enumerate(flow):
    pdf.text_at(259, 52 + j * 12, 64, f, size=7.5, color=LIGHT_GRAY)

pdf.slide_number()

# ===================================================================
# SLIDE 6 — ENVIRONMENT DETAILS
# ===================================================================
pdf.new_slide()
pdf.badge("04  ENVIRONMENT", ACCENT_ORANGE)
pdf.slide_title("Environment Details")
pdf.subtitle_line(color=ACCENT_ORANGE)

env_items = [
    ("Operating System", "AlmaLinux 10\n(RHEL-compatible)", ACCENT_BLUE),
    ("Web Server", "Nginx 1.26", ACCENT_GREEN),
    ("Dynamic Content", "PHP-FPM 8.x", ACCENT_PURPLE),
    ("Firewall", "firewalld\n(optional)", ACCENT_ORANGE),
    ("SELinux", "Enforcing\n(custom booleans)", ACCENT_PINK),
    ("VM1 IP Address", "192.168.1.8", ACCENT_BLUE),
    ("VM2 IP Address", "192.168.1.20", ACCENT_GREEN),
    ("Dashboard Port", "8080\n(health monitoring)", ACCENT_PURPLE),
]

for i, (label, value, color) in enumerate(env_items):
    col = i % 4
    row = i // 4
    x = 15 + col * 80
    y = 36 + row * 42
    cw = 73
    ch = 36

    pdf.card(x, y, cw, ch, accent_color=color)
    pdf.text_at(x + 5, y + 6, cw - 10, label, size=8.5, color=MID_GRAY)
    pdf.mtext_at(x + 5, y + 16, cw - 10, 18, value, size=11, color=color, bold=True, line_h=6)

pdf.slide_number()

# ===================================================================
# SLIDE 7 — PHASE 1: VM1 SETUP
# ===================================================================
pdf.new_slide()
pdf.badge("05  PHASE 1: VM1")
pdf.slide_title("Phase 1: VM1 - Two Websites + Dashboard")
pdf.subtitle_line()

steps = [
    ("Step 1: Install Nginx & PHP-FPM", [
        "sudo dnf install -y nginx php php-fpm",
        "sudo systemctl enable --now nginx php-fpm",
        "Provides web serving + dynamic PHP content",
    ], ACCENT_BLUE),
    ("Step 2: Create Website Directories", [
        "/var/www/site_a/html   (Site A)",
        "/var/www/site_b/html   (Site B)",
        "/var/www/dashboard/html (Dashboard)",
    ], ACCENT_GREEN),
    ("Step 3: Create Sample Pages", [
        "index.html with welcome message",
        "uptime.php for live server uptime",
        "Each site has unique styling & identity",
    ], ACCENT_PURPLE),
    ("Step 4: Configure Nginx Virtual Hosts", [
        "site_a.conf  -  listen 8081",
        "site_b.conf  -  listen 8082",
        "dashboard.conf  -  listen 8080 (PHP)",
    ], ACCENT_ORANGE),
]

for i, (title, bullets, color) in enumerate(steps):
    col = i % 2
    row = i // 2
    x = 15 + col * 162
    y = 35 + row * 44
    cw = 152
    ch = 40

    pdf.card(x, y, cw, ch, accent_color=color)
    pdf.text_at(x + 5, y + 5, cw - 10, title, size=11, color=color, bold=True)
    pdf.accent_line(x + 5, y + 13, 35, color)
    for j, b in enumerate(bullets):
        pdf.text_at(x + 8, y + 17 + j * 7, cw - 16, f"   {b}", size=8.5, color=LIGHT_GRAY)

pdf.slide_number()

# ===================================================================
# SLIDE 8 — CONFIG & SELINUX
# ===================================================================
pdf.new_slide()
pdf.badge("06  CONFIG & SELINUX", ACCENT_GREEN)
pdf.slide_title("Phase 1: Configuration & SELinux")
pdf.subtitle_line(color=ACCENT_GREEN)

# Nginx Config
pdf.text_at(15, 34, 150, "Nginx Virtual Host Configuration (site_a.conf)",
            size=9.5, color=ACCENT_BLUE, bold=True)
pdf.set_fill_color(*CODE_BG)
pdf.rect(15, 39, 150, 58, "F")

nginx_code = """server {
    listen 8081;
    root /var/www/site_a/html;
    index index.html index.php;

    location ~ \\.php$ {
        fastcgi_pass unix:/run/php-fpm/www.sock;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME
            $document_root$fastcgi_script_name;
    }
}"""
pdf.set_font("Courier", "", 7.5)
pdf.set_text_color(*ACCENT_GREEN)
pdf.set_xy(19, 42)
pdf.multi_cell(142, 4.5, nginx_code)

# SELinux config
pdf.text_at(175, 34, 150, "SELinux Configuration", size=9.5, color=ACCENT_ORANGE, bold=True)
pdf.set_fill_color(*CODE_BG)
pdf.rect(175, 39, 150, 58, "F")

selinux_code = """# Allow custom ports
sudo semanage port -a -t http_port_t -p tcp 8081
sudo semanage port -a -t http_port_t -p tcp 8082
sudo semanage port -a -t http_port_t -p tcp 8080

# Allow network connections
sudo setsebool -P httpd_can_network_connect 1"""
pdf.set_font("Courier", "", 7.5)
pdf.set_text_color(*ACCENT_GREEN)
pdf.set_xy(179, 42)
pdf.multi_cell(142, 4.5, selinux_code)

# Firewall
pdf.text_at(15, 102, 150, "Firewall Rules", size=9.5, color=ACCENT_PINK, bold=True)
pdf.set_fill_color(*CODE_BG)
pdf.rect(15, 107, 150, 16, "F")
pdf.set_font("Courier", "", 7.5)
pdf.set_text_color(*ACCENT_GREEN)
pdf.set_xy(19, 109)
pdf.multi_cell(142, 4.5, "sudo firewall-cmd --permanent --add-port={8081,8082,8080}/tcp\nsudo firewall-cmd --reload")

# Restart
pdf.text_at(175, 102, 150, "Validate & Restart", size=9.5, color=ACCENT_GREEN, bold=True)
pdf.set_fill_color(*CODE_BG)
pdf.rect(175, 107, 150, 16, "F")
pdf.set_font("Courier", "", 7.5)
pdf.set_text_color(*ACCENT_GREEN)
pdf.set_xy(179, 109)
pdf.multi_cell(142, 4.5, "sudo nginx -t && sudo systemctl restart nginx php-fpm")

pdf.slide_number()

# ===================================================================
# SLIDE 9 — PHASE 2: VM2 LOAD BALANCER
# ===================================================================
pdf.new_slide()
pdf.badge("07  PHASE 2: VM2", ACCENT_PURPLE)
pdf.slide_title("Phase 2: VM2 - Nginx Load Balancer")
pdf.subtitle_line(color=ACCENT_PURPLE)

# LB Config
pdf.text_at(15, 34, 160, "Load Balancer Config  (/etc/nginx/conf.d/load_balancer.conf)",
            size=9.5, color=ACCENT_PURPLE, bold=True)
pdf.set_fill_color(*CODE_BG)
pdf.rect(15, 39, 160, 78, "F")

lb_code = """upstream backend_servers {
    server 192.168.1.8:8081;
    server 192.168.1.8:8082;
}

server {
    listen 80;

    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /dashboard {
        proxy_pass http://192.168.1.8:8080;
    }
}"""
pdf.set_font("Courier", "", 7.5)
pdf.set_text_color(*ACCENT_GREEN)
pdf.set_xy(19, 42)
pdf.multi_cell(152, 4.3, lb_code)

# Steps on right
steps_data = [
    ("Step 1: Install Nginx", "sudo dnf install -y nginx", ACCENT_BLUE),
    ("Step 2: SELinux Boolean", "sudo setsebool -P httpd_can_network_connect 1", ACCENT_GREEN),
    ("Step 3: Open Firewall", "sudo firewall-cmd --permanent --add-service=http\nsudo firewall-cmd --reload", ACCENT_ORANGE),
    ("Step 4: Start Nginx", "sudo systemctl enable --now nginx", ACCENT_PINK),
]

for i, (title, cmd, color) in enumerate(steps_data):
    y = 36 + i * 23
    pdf.card(185, y, 140, 20, accent_color=color)
    pdf.text_at(190, y + 3, 130, title, size=9.5, color=color, bold=True)
    pdf.set_font("Courier", "", 7)
    pdf.set_text_color(*ACCENT_GREEN)
    pdf.set_xy(190, y + 11)
    pdf.multi_cell(130, 4, cmd)

pdf.slide_number()

# ===================================================================
# SLIDE 10 — DEMO: SITE A & SITE B
# ===================================================================
pdf.new_slide()
pdf.badge("08  DEMO: WEBSITES", ACCENT_ORANGE)
pdf.slide_title("Demo: Site A & Site B")
pdf.subtitle_line(color=ACCENT_ORANGE)

img_a = os.path.join(IMG_DIR, "resized", "Websites-b.png")
img_b = os.path.join(IMG_DIR, "resized", "Websites-a.png")

# Site A
pdf.card(10, 35, 158, 88, BG_CARD)
pdf.place_image(img_a, 12, 37, 154, 84)
pdf.text_at(12, 124, 154, "Site A  -  Primary Web Application  (port 8081)",
            size=9, color=ACCENT_BLUE, bold=True, align="C")
pdf.text_at(12, 130, 154, "Server IP: 192.168.1.8  |  Healthy & Running  |  Uptime: 49 min",
            size=7, color=MID_GRAY, align="C")

# Site B
pdf.card(172, 35, 158, 88, BG_CARD)
pdf.place_image(img_b, 174, 37, 154, 84)
pdf.text_at(174, 124, 154, "Site B  -  Secondary Web Application  (port 8082)",
            size=9, color=ACCENT_PINK, bold=True, align="C")
pdf.text_at(174, 130, 154, "Server IP: 192.168.1.8  |  Healthy & Running  |  Uptime: 49 min",
            size=7, color=MID_GRAY, align="C")

pdf.slide_number()

# ===================================================================
# SLIDE 11 — DEMO: HEALTH DASHBOARD
# ===================================================================
pdf.new_slide()
pdf.badge("09  HEALTH DASHBOARD", ACCENT_PINK)
pdf.slide_title("Demo: Health Dashboard")
pdf.subtitle_line(color=ACCENT_PINK)

img_dash = os.path.join(IMG_DIR, "resized", "HealthDashboard.png")
pdf.card(10, 35, 218, 93, BG_CARD)
pdf.place_image(img_dash, 12, 37, 214, 89)

# Info cards
info_cards = [
    ("Auto-Refresh", "Updates every 10\nseconds automatically", ACCENT_BLUE),
    ("Response Time", "Measures latency in\nmilliseconds per backend", ACCENT_GREEN),
    ("Status Monitor", "Green = UP, Red = DOWN\nReal-time health check", ACCENT_ORANGE),
    ("Dual Backend", "Monitors Site A (:8081)\nand Site B (:8082)", ACCENT_PINK),
]

for i, (title, desc, color) in enumerate(info_cards):
    y = 35 + i * 23.5
    pdf.card(234, y, 95, 21, accent_color=color)
    pdf.text_at(238, y + 3, 87, title, size=9, color=color, bold=True)
    pdf.mtext_at(238, y + 11, 87, 10, desc, size=7, color=LIGHT_GRAY, line_h=4)

pdf.slide_number()

# ===================================================================
# SLIDE 12 — DEMO: NGINX LB IN ACTION
# ===================================================================
pdf.new_slide()
pdf.badge("10  LB IN ACTION")
pdf.slide_title("Demo: Nginx Load Balancer in Action")
pdf.subtitle_line()

img_nginx = os.path.join(IMG_DIR, "resized", "Nginxstatus.png")
pdf.card(10, 35, 218, 93, BG_CARD)
pdf.place_image(img_nginx, 12, 37, 214, 89)

highlights = [
    ("Round-Robin Proof", "curl shows alternating\nSite A / Site B responses", ACCENT_BLUE),
    ("Access Logs", "tail -f shows distributed\nrequests across backends", ACCENT_GREEN),
    ("Service Status", "systemctl shows nginx\nactive (running) on VM2", ACCENT_PURPLE),
    ("HTTP 200 OK", "All responses return\n200 - backends healthy", ACCENT_ORANGE),
]

for i, (title, desc, color) in enumerate(highlights):
    y = 35 + i * 23.5
    pdf.card(234, y, 95, 21, accent_color=color)
    pdf.text_at(238, y + 3, 87, title, size=9, color=color, bold=True)
    pdf.mtext_at(238, y + 11, 87, 10, desc, size=7, color=LIGHT_GRAY, line_h=4)

pdf.slide_number()

# ===================================================================
# SLIDE 13 — VERIFICATION & TESTING
# ===================================================================
pdf.new_slide()
pdf.badge("11  TESTING", ACCENT_GREEN)
pdf.slide_title("Verification & Testing")
pdf.subtitle_line(color=ACCENT_GREEN)

tests = [
    ("Site A Direct", "curl http://192.168.1.8:8081", "Welcome message or styled page", ACCENT_BLUE),
    ("Site B Direct", "curl http://192.168.1.8:8082", "Welcome message or styled page", ACCENT_GREEN),
    ("Dashboard", "curl http://192.168.1.8:8080", "Health status JSON or HTML", ACCENT_PURPLE),
    ("Load Balancer", "curl http://192.168.1.20 (x3)", "Alternating: Site A, B, A...", ACCENT_ORANGE),
    ("Dashboard via LB", "curl http://192.168.1.20/dashboard", "Dashboard HTML page", ACCENT_PINK),
    ("Failure Test", "sudo systemctl stop nginx (VM1)", "VM2 stops routing to failed backend", (239, 68, 68)),
]

for i, (name, cmd, expected, color) in enumerate(tests):
    col = i % 2
    row = i // 2
    x = 15 + col * 162
    y = 35 + row * 30
    cw = 152
    ch = 26

    pdf.card(x, y, cw, ch, accent_color=color)
    pdf.text_at(x + 5, y + 4, cw - 10, name, size=10, color=color, bold=True)
    pdf.set_font("Courier", "", 7.5)
    pdf.set_text_color(*ACCENT_GREEN)
    pdf.set_xy(x + 5, y + 12)
    pdf.cell(cw - 10, 4, cmd)
    pdf.text_at(x + 5, y + 18, cw - 10, f"Expected: {expected}", size=7.5, color=LIGHT_GRAY)

pdf.slide_number()

# ===================================================================
# SLIDE 14 — CHALLENGES & SOLUTIONS
# ===================================================================
pdf.new_slide()
pdf.badge("12  CHALLENGES", ACCENT_PURPLE)
pdf.slide_title("Challenges & Solutions")
pdf.subtitle_line(color=ACCENT_PURPLE)

challenges = [
    ("SELinux Blocking Ports", "Used semanage port -a to add\ncustom HTTP ports", ACCENT_BLUE),
    ("PHP-FPM Network Error", "Enabled httpd_can_network_connect\nSELinux boolean", ACCENT_GREEN),
    ("Port 80 Conflict", "Stopped & removed HAProxy that\nwas occupying the port", ACCENT_PURPLE),
    ("Nginx Syntax Errors", "Replaced config & validated with\nnginx -t before restart", ACCENT_ORANGE),
    ("Emoji Display Issues", "Added <meta charset=\"UTF-8\">\nto all HTML pages", ACCENT_PINK),
    ("PHP Socket Permission", "Fixed via SELinux boolean +\nPHP-FPM socket permissions", ACCENT_BLUE),
]

for i, (challenge, solution, color) in enumerate(challenges):
    col = i % 3
    row = i // 3
    x = 15 + col * 106
    y = 35 + row * 48
    cw = 98
    ch = 43

    pdf.card(x, y, cw, ch, accent_color=color)
    pdf.text_at(x + 5, y + 5, cw - 10, "CHALLENGE", size=6.5, color=MID_GRAY, bold=True)
    pdf.text_at(x + 5, y + 12, cw - 10, challenge, size=10, color=color, bold=True)
    pdf.text_at(x + 5, y + 22, cw - 10, "SOLUTION", size=6.5, color=MID_GRAY, bold=True)
    pdf.mtext_at(x + 5, y + 29, cw - 10, 14, solution, size=8, color=LIGHT_GRAY, line_h=4.5)

pdf.slide_number()

# ===================================================================
# SLIDE 15 — EXTENDING THE INFRASTRUCTURE
# ===================================================================
pdf.new_slide()
pdf.badge("13  EXTENDING", ACCENT_ORANGE)
pdf.slide_title("Extending the Infrastructure")
pdf.subtitle_line(color=ACCENT_ORANGE)

extensions = [
    ("Add More Backends", "Add new server lines in upstream block.\nNo client-side changes needed -\ninstant horizontal scaling.", ACCENT_BLUE),
    ("LB Algorithms", "Switch from round-robin to:\nleast_conn; ip_hash; random;\nfor different traffic patterns.", ACCENT_GREEN),
    ("Enable SSL/TLS", "Obtain certificate (Let's Encrypt)\nand add listen 443 ssl; on VM2.\nBackends use plain HTTP.", ACCENT_PURPLE),
    ("Session Persistence", "Use sticky cookie (Nginx Plus)\nor ip_hash for session affinity.\nKeeps user on same backend.", ACCENT_ORANGE),
    ("Logging & Monitoring", "Access logs show which upstream\nhandled each request. Integrate\nGrafana or Prometheus.", ACCENT_PINK),
]

for i, (title, desc, color) in enumerate(extensions):
    col = i % 3
    row = i // 3
    x = 15 + col * 106
    y = 35 + row * 48
    cw = 98
    ch = 43

    pdf.card(x, y, cw, ch, accent_color=color)
    pdf.text_at(x + 5, y + 6, cw - 10, title, size=11, color=color, bold=True)
    pdf.accent_line(x + 5, y + 14, 30, color)
    pdf.mtext_at(x + 5, y + 18, cw - 10, 22, desc, size=8, color=LIGHT_GRAY, line_h=4.5)

pdf.slide_number()

# ===================================================================
# SLIDE 16 — CONCLUSION
# ===================================================================
pdf.new_slide()
# Decorative
pdf.set_fill_color(*DARK_ACCENT)
pdf.ellipse(-15, -15, 100, 100, "F")
pdf.ellipse(W - 70, H - 80, 110, 110, "F")

pdf.badge("14  CONCLUSION", ACCENT_PINK)
pdf.text_at(30, 24, W - 60, "Conclusion", size=26, color=WHITE, bold=True)
pdf.accent_line(30, 36, 60, ACCENT_PINK)

points = [
    ("Production-ready, scalable, and monitored web infrastructure", ACCENT_BLUE),
    ("Built entirely with open-source tools (Nginx + PHP-FPM)", ACCENT_GREEN),
    ("Load balancer ensures high availability with automatic failover", ACCENT_PURPLE),
    ("Health dashboard provides real-time visibility into backend status", ACCENT_ORANGE),
    ("SELinux enforcing mode maintained for enterprise-grade security", ACCENT_PINK),
    ("All common challenges addressed with practical solutions", ACCENT_BLUE),
]

for i, (point, color) in enumerate(points):
    y = 44 + i * 12
    pdf.set_fill_color(*color)
    pdf.ellipse(34, y + 1.5, 3, 3, "F")
    pdf.text_at(42, y, W - 80, point, size=11, color=LIGHT_GRAY)

# Group-2 card on right
pdf.card(W - 120, 44, 105, 68, accent_color=ACCENT_PURPLE)
pdf.text_at(W - 115, 48, 95, "Group-2", size=13, color=ACCENT_PURPLE, bold=True, align="C")
pdf.accent_line(W - 100, 56, 55, ACCENT_PURPLE)
members_c = [
    ("1.", "Suon Pisey", ACCENT_BLUE),
    ("2.", "Nem Sothea", ACCENT_GREEN),
    ("3.", "Sourn Savourn", ACCENT_PURPLE),
    ("4.", "Oun Sreynich", ACCENT_ORANGE),
    ("5.", "Moeun Nithvaraman", ACCENT_PINK),
]
for j, (num, name, mcolor) in enumerate(members_c):
    my = 60 + j * 9
    pdf.set_fill_color(*mcolor)
    pdf.ellipse(W - 112, my + 1.5, 2.5, 2.5, "F")
    pdf.text_at(W - 108, my, 90, f"{num}  {name}", size=8.5, color=LIGHT_GRAY)

# Footer
pdf.accent_line(30, 125, 280, MID_GRAY)
pdf.text_at(30, 129, 280, "AlmaLinux 10  |  Nginx 1.26  |  PHP-FPM 8.x  |  April 2026",
            size=9, color=MID_GRAY, align="C")
pdf.text_at(50, 140, 140, "Thank You!", size=22, color=ACCENT_BLUE, bold=True, align="C")

pdf.slide_number()

# ===================================================================
# SAVE
# ===================================================================
output = os.path.join(IMG_DIR, "LoadBalancer_Presentation.pdf")
pdf.output(output)
print(f"PDF saved to: {output}")
print(f"Total pages: {pdf.slide_num}")
