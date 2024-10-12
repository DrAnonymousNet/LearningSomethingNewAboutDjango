from django_elasticsearch_dsl import Document, Index
from django_elasticsearch_dsl.registries import registry
from .models import Post

# Define the index for Posts
posts = Index('posts')

# Index settings
posts.settings(
    number_of_shards=1,
    number_of_replicas=1
)

@posts.document
class PostDocument(Document):
    class Django:
        model = Post  # The model associated with this Document
        fields = [
            'title',
            'content',
            'published_date'
        ]