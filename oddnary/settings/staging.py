from oddnary.default_settings import *
import dj_database_url

DEBUG = True

ALLOWED_HOSTS = ['*',]

# static and media storage setting

AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
STATIC_URL = "https://{}/{}/".format(AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
MEDIA_URL = "https://{}/{}/".format(AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=2592000',
}

# database
DATABASES = {
    'default': dj_database_url.config(
                default='postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'.format(
                	USER=os.getenv("SQL_USER"), 
                	PASSWORD=os.getenv("SQL_PASSWORD"),
                	HOST=os.getenv("SQL_HOST"),
                	PORT=os.getenv("PG_SQL_PORT"),
                	DB_NAME=os.getenv("SQL_DB_NAME")
                	)
            )
}
