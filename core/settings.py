"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import environ
import os


env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", default=False)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # PIP INSTALL
    'crispy_forms',
    'crispy_bootstrap4',
    'colorfield',
    'captcha',
    'tinymce',
    'six',

    # APLICATIONS
    'courses',
    'users'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/El_Salvador'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


# FOR CRISPY
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# FOR CUSTOM USER
AUTH_USER_MODEL = "users.CustomUser"
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


# RECAPTCHA
RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# TINYMCE
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
TINYMCE_DEFAULT_CONFIG = {
    "skin": 'oxide-dark',
    "custom_undo_redo_levels": 100,
    "selector": "textarea",
    "menubar": "file edit view insert format tools table help",
    "plugins": "link image preview codesample contextmenu table code lists fullscreen textcolor",
    "toolbar1": "undo redo | backcolor forecolor casechange permanentpen formatpainter removeformat formatselect fontselect fontsizeselect",
    "toolbar2": "bold italic underline blockquote | alignleft aligncenter alignright alignjustify "
    "| bullist numlist | outdent indent | table | link image | codesample | preview code | tiny_mce_wiris_formulaEditor tiny_mce_wiris_formulaEditorChemistry",
    "contextmenu": "formats | link image",
    "block_formats": "Paragraph=p; Header 1=h1; Header 2=h2",
    "fontsize_formats": "8pt 10pt 12pt 14pt 16pt 18pt",
    "file_picker_types": 'image',
    "image_class_list": [{"title": "Fluid", "value": "img-fluid", "style": {}}],
    "width": "auto",
    "height": "600px",
    "image_caption": True,
    "content_css": '//www.tiny.cloud/css/codepen.min.css',
    "file_picker_callback": """
        function (cb, value, meta) {
            var input = document.createElement('input');
            input.setAttribute('type', 'file');
            input.setAttribute('accept', 'image/*');

            input.onchange = function () {
                var file = this.files[0];

                var reader = new FileReader();
                reader.onload = function () {
                    var id = 'blobid' + (new Date()).getTime();
                    var blobCache = tinymce.activeEditor.editorUpload.blobCache;
                    var base64 = reader.result.split(',')[1];
                    var blobInfo = blobCache.create(id, file, base64);
                    blobCache.add(blobInfo);

                    cb(blobInfo.blobUri(), { title: file.name });
                };
                reader.readAsDataURL(file);
            };
            input.click();
        }
    """,
    "content_style": "body { font-family: Arial; background: rgb(32, 45, 83); color: white; font-size: 12pt}",
    "codesample_languages": [
        {"text": "HTML/XML", "value": "markup"},
        {"text": "JavaScript", "value": "javascript"},
        {"text": "CSS", "value": "css"},
        {"text": "PHP", "value": "php"},
        {"text": "Ruby", "value": "ruby"},
        {"text": "Python", "value": "python"},
        {"text": "Java", "value": "java"},
        {"text": "C", "value": "c"},
        {"text": "C#", "value": "csharp"},
        {"text": "C++", "value": "cpp"},
        {"text": "Bash/Shell", "value": "bash"},
        {"text": "CoffeeScript", "value": "coffeescript"},
        {"text": "Diff", "value": "diff"},
        {"text": "Erlang", "value": "erlang"},
        {"text": "Groovy", "value": "groovy"},
        {"text": "JSON", "value": "json"},
        {"text": "Less", "value": "less"},
        {"text": "Makefile", "value": "makefile"},
        {"text": "Markdown", "value": "markdown"},
        {"text": "Objective-C", "value": "objectivec"},
        {"text": "R", "value": "r"},
        {"text": "Sass", "value": "sass"},
        {"text": "SCSS", "value": "scss"},
        {"text": "SQL", "value": "sql"},
        {"text": "TypeScript", "value": "typescript"},
        {"text": "YAML", "value": "yaml"}
    ],

}


# FOR EMAIL TOKEN AND SETTINGS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

PASSWORD_RESET_TIMEOUT = 14400
