# General-Django-CMS-Template

A Follower-Following Content Management System (Based on Twitter CMS).
This Project serves just as backend API. Host this as a server and connect it with your FrontEnd.

The Project DB is SQLITE-3, would recommend using a proper DB service such as PostGreSQL or MariaDB.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Django and Other Dependecies.

```bash
pip install -r requirements.txt
```

```bash
cd src
python manage.py runserver
```

## Alternative Installation (with Docker)

```bash
 docker build -t cms-api .
 docker run --name cms-api -d -p 8000:8000 cms-api:latest
```

> Create a super-user and then login to admin
```
python manage.py createsuperuser 
```

> Note: `Would reccomend using a Virtual Environment(venv)`

## Official API Documentation

https://documenter.getpostman.com/view/18719663/UVsPP51N

| URLS | Action | Work-Description |
| ------ | ------ | ------ |
| /api-token-auth | post | Login to recieve a Auth-token(Use that auth token in header as `Authorisation: Token "Your token without double-commas"`)
| /admin | get | Use Admin
| /api | get | Gets Profile Info depending upon the presence of "id" variable. If "id" is not present, it will return logged in user's profile.
| /api | post |  Updates Profile Info
| /api/signUp | post | Signs-Up an User
| /api/search | get | Searches a user with variable 'username'
| /api/follow | get | Gets Follower and Followed List of the logged-in User or if "id" is provided and logged-in User follows it, the Follow/Followed List of that user
| /api/follow | post | Follow/Unfollow by "id" variable provided 
| /api/Feed | get | Gets daily feed unless an "id" is provided,in that case it gets the post with that id
| /api/Feed | post | Upload a new Post by "content" variable or edit by providing "id" of an existing post long with new content to update that post
| /api/Feed | delete | Deletes the post with given "id" as query param
| /api/Feed/like | post | Likes/Unlikes a post with given "id"
| /api/Feed/comment | get | Gets Comment if "id" is provided a, Gets comments in post by provided "post_id" 
| /api/Feed/comment | post | Posts comment on post by providing "post_id" and "comment" (content of the comment)
| /api/feed/comment | delete | Delete a comment on a post providing "post_id" and "id" (Comment id) as query params.
