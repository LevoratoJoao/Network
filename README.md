# Network

This is a social network that allows users to make posts, follow other users and “like” posts.

## Installation

To use this project first you need python and django

To install django
```bash
pip3 install Django
```

To run the project
```bash
python3 manage.py runserver
```

If you change anything in ``àuctions/models.py``, you'll need to first run this commands to migrate those changes to your database
```bash
python3 manage.py makemigrations
```

```bash
python manage.py migrate
```

To create a superuser account that can access Django's admin interface
```bash
python3 manage.py createsuperuser
```

# Demo

Here it is a simple usage example on YouTube: [Demo](https://youtu.be/pcUBH0xVp_k).

## New Post

Users who are signed in can write a new text-based post by filling in text into a text area and then clicking a button to submit the post.

## All Posts

The “All Posts” link in the navigation bar should take the user to a page where they can see all posts from all users, with the most recent posts first.

* Each post includes the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has.

## Profile Page

Clicking on a username will load that user’s profile page.

* Displays the number of followers the user has, as well as the number of people that the user follows.
* Displays all of the posts for that user, in reverse chronological order.
* For any other user who is signed in, this page also displays a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user is not able to follow themselves.

## Following

The “Following” link in the navigation bar will take the user to a page where they see all posts made by users that the current user follows.

* This page is only available to users who are signed in.

## Pagination

On any page that displays posts, posts will only be displayed 10 on a page. If there are more than ten posts, a “Next” button will appear to take the user to the next page of posts (which will be older than the current page of posts). If not on the first page, a “Previous” button will appear to take the user to the previous page of posts as well.

## Edit Post

Users will be able to click an “Edit” button on any of their own posts to edit that post.
* When a user clicks “Edit” for one of their own posts a bootstrap modal will apear, the content of their post will be replaced with a textarea where the user can edit the content of their post.

## “Like” and “Unlike”

Users will be able to click a button or link on any post to toggle whether or not they “like” that post.

