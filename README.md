Py Tools is Simple Data Mutator and Analys created with flask

Please install flask first if not yet installed

    pip install flask

To run temporary :

    python3 app.py

To run with reverse proxy run following commands:

    pip install gunicorn
    npm install pm2 -g
    pm2 start 'gunicorn -w 4 -b 0.0.0.0:5000 app:app' --name py-tools

create nginx config

    server {
        listen 80;
        server_name py-tools.test;
    
        location / {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    
        location /static {
            alias /var/www/py-tools/templates;
        }
    
        location /favicon.ico {
            alias /var/www/py-tools/templates/favicon.ico;
        }
    
        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            root /usr/share/nginx/html;
        }
    }

and activate with

    sudo ln -s /etc/nginx/sites-available/py-tools.test /etc/nginx/sites-enabled


