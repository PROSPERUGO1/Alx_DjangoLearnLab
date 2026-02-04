This project demostrates the use of permission handling with django. It takes 4 simple CRUD permissions

can_create
can_edit
can_view
can_delete
To assign permissions, you can create a user either through the admin site, or through the interactive shell. There are 3 groups for user classes.

Admins
Viewers
Editors
Conversely, you can assign permissions to the user directly(either programmatically or through the django shell)

Security updates implemented

HSTS & SSL Redirect - Eliminates "Man-in-the-Middle" attacks by ensuring the connection never drops to insecure HTTP.
Secure Cookies - Prevents session hijacking; even if a script tries to steal a cookie, the browser won't send it unless the connection is encrypted.
X-Frame-Options - Stops "Clickjacking" where an attacker overlays your site with an invisible layer to steal clicks.
Content-Type Nosniff - Forces the browser to stick to the Content-Type header, preventing "MIME-sniffing" exploits.