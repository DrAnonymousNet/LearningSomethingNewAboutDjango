# settings.py

INSTALLED_APPS = [
    'django_elasticsearch_dsl',  # Add this for Elasticsearch integration
    'myapp',
    # other apps...
]

# Elasticsearch configuration
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'  # Your Elasticsearch host
    },
}