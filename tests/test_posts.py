from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts")
    assert len(res.json()["data"]) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts")
    print(res.json())
    assert res.status_code == 401
    assert res.json()["detail"] == 'Not authenticated'

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    assert res.status_code == 401
    assert res.json()["detail"] == 'Not authenticated'

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    print(res.json())
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostWithVotes(**res.json())
    assert res.status_code == 200
    assert post.post.id == test_posts[0].id
    assert post.post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published",[
    ("awesome new title", "awesome new content", True),
    ("nice title", "nice content", False),
    ("worst title ever", "worst content ever", True)
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts", json={"title":title, "content":content, "published":published})
    created_post = schemas.PostCreateResponse(**res.json())
    assert res.status_code == 201
    assert created_post.data.title == title


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post("/posts", json={"title":"arbitirary title", "content":"arbitirary content"})
    created_post = schemas.PostCreateResponse(**res.json())
    assert res.status_code == 201
    assert created_post.data.published == True

def test_unauthorized_user_create_post(client, test_user):
    res = client.post("/posts", json={"title":"arbitirary title", "content":"arbitirary content"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/888")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    print(res.json())
    assert res.status_code == 403

def test_update_post(authorized_client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": True
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostCreateResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.data.title == data["title"]

def test_update_other_user_post(authorized_client, test_posts, test_user, test_user2):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": True
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_posts, test_user, test_user2):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": True
    }
    res = client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_posts, test_user, test_user2):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": True
    }
    res = authorized_client.put(f"/posts/8888", json=data)
    assert res.status_code == 404