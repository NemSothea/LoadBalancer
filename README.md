# 🚀 Load Balancer Setup with Nginx on AlmaLinux

## 📌 Project Overview

This document describes the step‑by‑step process to configure two virtual machines (VMs) to serve as a **high‑availability web infrastructure**:

- **VM1** → Hosts two independent websites (Site A on port 8081, Site B on port 8082)  
- **VM2** → Runs an **Nginx load balancer** that distributes incoming traffic between the two websites on VM1  

Additionally, a **health dashboard** is installed on VM1 (port 8080) to monitor both sites in real time.

---

## 🎯 Why Use a Load Balancer?

| Reason | Explanation |
|--------|-------------|
| **High availability** | If one website instance fails, traffic is redirected to the other. |
| **Scalability** | Add more backend servers without changing the public endpoint. |
| **Traffic distribution** | Prevents overload on a single server (round‑robin, least connections, etc.). |
| **Maintenance without downtime** | Take one backend offline while the other continues serving. |
| **Simplified SSL/TLS** | Terminate certificates on the load balancer only. |

---

## 🧱 Architecture & Process Flow

```
Client Request
       │
       ▼
┌──────────────────┐
│  VM2 (LB)        │
│  Nginx :80       │
│  upstream:       │
│  - 10.0.2.15:8081│
│  - 10.0.2.15:8082│
└────────┬─────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│ VM1    │ │ VM1    │
│ Site A │ │ Site B │
│ :8081  │ │ :8082  │
└────────┘ └────────┘
         │
         ▼
   Dashboard :8080
   (health checks)
```

**Flow:**
1. User accesses `http://<VM2_IP>`.
2. Nginx on VM2 selects a backend (round‑robin by default).
3. Request is proxied to VM1 on port 8081 or 8082.
4. The website responds; Nginx returns the response to the client.
5. The dashboard (port 8080) periodically checks both backends and displays status.

---

## 🛠️ Environment Details

| Component | Specification |
|-----------|---------------|
| OS | AlmaLinux 10 (or RHEL/CentOS 8+) |
| Web Server | Nginx 1.26 |
| Dynamic Content | PHP‑FPM (for dashboard & uptime) |
| Firewall | firewalld (optional) |
| SELinux | Enforcing (with custom booleans/ports) |
| VM1 IP | `192.168.1.8` (example) |
| VM2 IP | `192.168.1.20` (example) |

---

## 📖 Step‑by‑Step Implementation

### Phase 1: VM1 – Two Websites + Dashboard

#### 1.1 Install Nginx and PHP‑FPM
```bash
sudo dnf install -y nginx php php-fpm
sudo systemctl enable --now nginx php-fpm
```

#### 1.2 Create Website Directories
```bash
sudo mkdir -p /var/www/site_a/html /var/www/site_b/html /var/www/dashboard/html
```

#### 1.3 Create Sample Pages with Uptime Feature
**Site A (port 8081):**
```bash
echo "<h1>Welcome to Site A (Port 8081)</h1>" | sudo tee /var/www/site_a/html/index.html
sudo tee /var/www/site_a/html/uptime.php << 'EOF'
<?php echo shell_exec("uptime -p | sed 's/up //'"); ?>
EOF
```

**Site B (port 8082):** (similar, change port number)

#### 1.4 Configure Nginx for Both Sites (PHP support)
Create `/etc/nginx/conf.d/site_a.conf`:
```nginx
server {
    listen 8081;
    root /var/www/site_a/html;
    index index.html index.php;
    location ~ \.php$ {
        fastcgi_pass unix:/run/php-fpm/www.sock;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }
}
```
Repeat for `site_b.conf` (port 8082).

#### 1.5 Install Health Dashboard (port 8080)
Create `/etc/nginx/conf.d/dashboard.conf` with PHP support (port 8080).  
Place `index.html` (with auto‑refresh and cards) and `status.php` (checks both sites via fsockopen).  
*(Full code provided in previous answers.)*

#### 1.6 SELinux Configuration
```bash
# Allow Nginx to listen on custom ports
sudo semanage port -a -t http_port_t -p tcp 8081
sudo semanage port -a -t http_port_t -p tcp 8082
sudo semanage port -a -t http_port_t -p tcp 8080

# Allow PHP‑FPM to make network connections (for health checks)
sudo setsebool -P httpd_can_network_connect 1
```

#### 1.7 Firewall (if active)
```bash
sudo firewall-cmd --permanent --add-port={8081,8082,8080}/tcp
sudo firewall-cmd --reload
```

#### 1.8 Restart Services
```bash
sudo nginx -t && sudo systemctl restart nginx php-fpm
```

---

### Phase 2: VM2 – Nginx Load Balancer

#### 2.1 Install Nginx
```bash
sudo dnf install -y nginx
```

#### 2.2 Create Load Balancer Configuration
File: `/etc/nginx/conf.d/load_balancer.conf`
```nginx
upstream backend_servers {
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
}
```

#### 2.3 SELinux on VM2
```bash
sudo setsebool -P httpd_can_network_connect 1
```

#### 2.4 Firewall
```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
```

#### 2.5 Start Nginx
```bash
sudo systemctl enable --now nginx
```

---

## ✅ Verification & Testing

| Test | Command / Action | Expected Result |
|------|------------------|------------------|
| Site A directly | `curl http://192.168.1.8:8081` | Welcome message or styled page |
| Site B directly | `curl http://192.168.1.8:8082` | Same as above |
| Dashboard | `curl http://192.168.1.8:8080` | JSON health or HTML dashboard |
| Load balancer | `curl http://192.168.1.20` (multiple times) | Alternating responses from Site A and Site B |
| Health via LB | `curl http://192.168.1.20/dashboard` | Dashboard HTML |
| Backend failure test | Stop Nginx on VM1: `sudo systemctl stop nginx` | VM2 stops sending traffic to failed backend (after fail_timeout) |

---

## 🧠 Challenges Encountered & Solutions

| Challenge | Solution |
|-----------|----------|
| **SELinux blocking ports** | Used `semanage port -a -t http_port_t -p tcp 8081` |
| **PHP‑FPM unable to connect to local ports** | Enabled `httpd_can_network_connect` boolean |
| **Port 80 already used by HAProxy** | Stopped and removed HAProxy with `systemctl stop haproxy` |
| **Nginx configuration syntax errors** | Replaced with clean `nginx.conf` and validated with `nginx -t` |
| **Emojis not displaying** | Added `<meta charset="UTF-8">` to HTML files |
| **FirewallD not running** | Either start it or ignore (no firewall active) |
| **Permission denied in PHP socket** | Fixed by SELinux boolean and ensuring PHP‑FPM socket permissions |

---

## 📈 Performance & Health Monitoring

- **Passive health checks** (default): Nginx marks a backend as down after `max_fails=1` failure within `fail_timeout=10s`.  
- **Active health checks** require Nginx Plus or third‑party module.  
- **Custom dashboard** uses `fsockopen` with 2‑second timeout to test each backend every 10 seconds.  
- **Response time** is measured and displayed in milliseconds.

---

## 🔄 Extending the Infrastructure

- **Add more backends** – just add new `server` lines in the `upstream` block.  
- **Use different load balancing algorithms** – `least_conn;`, `ip_hash;`, or `random;`.  
- **Enable SSL** – obtain a certificate and add `listen 443 ssl;` on VM2.  
- **Implement session persistence** – use `sticky cookie` (Nginx Plus) or `ip_hash`.  
- **Set up logging** – access logs show which upstream handled the request.

---

## 📝 Full Command Summary (Cheat Sheet)

### On VM1
```bash
# Install
sudo dnf install -y nginx php php-fpm

# Create sites and dashboard
sudo mkdir -p /var/www/{site_a,site_b,dashboard}/html

# Configure SELinux
sudo semanage port -a -t http_port_t -p tcp 8081 8082 8080
sudo setsebool -P httpd_can_network_connect 1

# Start services
sudo systemctl enable --now nginx php-fpm
```

### On VM2
```bash
# Install
sudo dnf install -y nginx

# SELinux
sudo setsebool -P httpd_can_network_connect 1

# Create config (replace IP with VM1's IP)
cat > /etc/nginx/conf.d/lb.conf << 'EOF'
upstream backend { server 192.168.1.8:8081; server 192.168.1.8:8082; }
server { listen 80; location / { proxy_pass http://backend; } }
EOF

# Start
sudo systemctl enable --now nginx
```

---

## 🎓 Conclusion

This setup provides a **production‑ready, scalable, and monitored** web infrastructure using only open‑source tools. The load balancer ensures high availability, while the dashboard gives real‑time visibility into backend health. All common challenges (SELinux, PHP integration, port conflicts) have been addressed with practical solutions.

---

**Prepared by:** 
Group-2:
1. Suon Pisey
2. Nem Sothea
3. Sourn Savourn
4. Oun Sreynich
5. Moeun Nithvaraman
**Date:** April 2026  
**Environment:** AlmaLinux 10, Nginx 1.26, PHP-FPM 8.x

> *For any issues, refer to the troubleshooting section or check logs: `/var/log/nginx/error.log` and `/var/log/php-fpm/error.log`.*



