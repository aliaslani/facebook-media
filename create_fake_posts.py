# create_fake_posts.py

import os
import random
import django
from faker import Faker

# --------------------------------------------------
# Django Setup
# --------------------------------------------------

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook.settings')
django.setup()

# --------------------------------------------------
# Imports
# --------------------------------------------------

from core.models import Post, Comment
from accounts.models import CustomUser

# --------------------------------------------------
# Faker
# --------------------------------------------------

fake = Faker()

# --------------------------------------------------
# Config
# --------------------------------------------------

NUMBER_OF_POSTS = 50
MAX_COMMENTS_PER_POST = 8

# --------------------------------------------------
# Subjects
# --------------------------------------------------

subjects = [
    'SP',  # sport
    'MU',  # music
    'MO',  # movie
    'TE',  # tech
]

# --------------------------------------------------
# Users
# --------------------------------------------------

users = list(CustomUser.objects.all())

if not users:
    raise Exception('No users found. Create users first.')

# --------------------------------------------------
# Create Posts
# --------------------------------------------------

for _ in range(NUMBER_OF_POSTS):

    user = random.choice(users)

    post = Post.objects.create(
        title=fake.sentence(nb_words=6),
        content=fake.paragraph(nb_sentences=5),
        subject=random.choice(subjects),
        user=user,
    )

    print(f'Created Post: {post.title}')

    # ----------------------------------------------
    # Create Comments
    # ----------------------------------------------

    number_of_comments = random.randint(0, MAX_COMMENTS_PER_POST)

    for _ in range(number_of_comments):

        comment_user = random.choice(users)

        comment = Comment.objects.create(
            post=post,
            user=comment_user,
            body=fake.sentence(nb_words=20),
        )

        print(f'   ↳ Comment by {comment.user.username}')

print('\nFake data created successfully!')