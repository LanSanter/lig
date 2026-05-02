# Island Light Generator 網站部署流程

## 1) 伺服器前置
- OS：Ubuntu 22.04+
- 套件：`python3.11`, `nginx`, `nodejs 20+`, `npm`

## 2) 取得程式碼
```bash
git clone <your-repo-url> /opt/island-light-generator
cd /opt/island-light-generator
```

## 3) 部署 Backend（systemd）
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

建立 `/etc/systemd/system/island-light-api.service`：
```ini
[Unit]
Description=Island Light API
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/island-light-generator
EnvironmentFile=/opt/island-light-generator/.env
ExecStart=/opt/island-light-generator/.venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

啟用：
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now island-light-api
sudo systemctl status island-light-api
```

## 4) 部署 Frontend（靜態檔）
```bash
cd frontend
npm install
npm run build
sudo mkdir -p /var/www/island-light
sudo cp -r dist/* /var/www/island-light/
```

## 5) Nginx 反向代理
建立 `/etc/nginx/sites-available/island-light`：
```nginx
server {
  listen 80;
  server_name your-domain.com;

  root /var/www/island-light;
  index index.html;

  location / {
    try_files $uri $uri/ /index.html;
  }

  location /api/ {
    proxy_pass http://127.0.0.1:8000/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/island-light /etc/nginx/sites-enabled/island-light
sudo nginx -t
sudo systemctl reload nginx
```

## 6) HTTPS（Let’s Encrypt）
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 7) 維運檢查
```bash
curl http://127.0.0.1:8000/api/health
journalctl -u island-light-api -n 100 --no-pager
```
