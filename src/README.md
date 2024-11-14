
- Cross Site Request Forgery protection
> https://docs.djangoproject.com/en/5.1/ref/csrf/

```py
CSRF_COOKIE_DOMAIN = '.example.com'
CSRF_TRUSTED_ORIGINS = ["https://your_CSRF_TRUSTED_ORIGINS/"]
# https://docs.djangoproject.com/en/5.1/ref/csrf/
# https://docs.djangoproject.com/en/5.1/ref/settings/#std-setting-CSRF_TRUSTED_ORIGINS

CSRF_COOKIE_AGE
CSRF_COOKIE_DOMAIN
CSRF_COOKIE_HTTPONLY
CSRF_COOKIE_NAME
CSRF_COOKIE_PATH
CSRF_COOKIE_SAMESITE
CSRF_COOKIE_SECURE
CSRF_FAILURE_VIEW
CSRF_HEADER_NAME
CSRF_TRUSTED_ORIGINS
CSRF_USE_SESSIONS
```
