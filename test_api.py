import allure

import config
from services import ApiService, UserService


class TestAPI:

    @allure.description("This test gets all posts")
    def test_get_all_posts(self):
        url = '/posts'

        response = ApiService.get(action_url=url)

        assert response.status_code == 200, \
            f'Response status code is not 200. Response status code is {response.status_code}'
        assert response.json(), "The list in response body is not json"
        prev_id = 0
        for item in response.json():
            id = item.get('id')
            assert id > prev_id, "Posts are not sorting ascending"
            prev_id = id

    @allure.description("This test gets post with id 99")
    def test_get_post_with_id(self):
        id = 99
        url = f'/posts/{id}'

        response = ApiService.get(action_url=url)

        assert response.status_code == 200, \
            f'Response status code is not 200. Response status code is {response.status_code}'
        assert response.json().get('id') == id, \
            f"Id is not correct. Expected {id}, actual {response.json().get('id')}"
        assert response.json().get('userId') == 10, \
            f"UserId is not correct. Expected {id}, actual {response.json().get('userId')}"
        assert response.json().get('title'), "Title is empty"
        assert response.json().get('body'), "Body is empty"

    @allure.description("This test gets post with id 404")
    def test_get_post_with_id_404(self):
        id = 150
        url = f'/posts/{id}'

        response = ApiService.get(action_url=url)

        assert response.status_code == 404, \
            f'Response status code is not 404. Response status code is {response.status_code}'
        assert not response.json(), "Response body is not empty"

    @allure.description("This test creates user")
    def test_create_user(self):
        url = f'/posts'
        body = config.body_for_create_user

        response = ApiService.post(action_url=url, body=body)

        assert response.status_code == 201, \
            f'Response status code is not 201. Response status code is {response.status_code}'
        assert response.json().get('id'), "There is no id in response"
        assert response.json().get('title') == body.get('title'), \
            f"Expected title is {body.get('title')}, but actual title is {response.json().get('title')}"
        assert response.json().get('body') == body.get('body'), \
            f"Expected body is {body.get('body')}, but actual body is {response.json().get('body')}"
        assert response.json().get('userId') == body.get('userId'), \
            f"Expected userId is {body.get('userId')}, but actual userId is {response.json().get('userId')}"

    @allure.description("This test gets user")
    def test_get_users(self):
        url = f'/users'

        assert_body = config.assert_body_with_id_5

        response = ApiService.get(action_url=url)

        assert response.status_code == 200, \
            f'Response status code is not 200. Response status code is {response.status_code}'
        assert response.json(), "The list in response body is not json"

        user = UserService.find_user(response.json(), 5)
        assert user == assert_body, "Users data is invalid"

    @allure.description("This test gets user")
    def test_get_user(self):
        url = f'/users/5'

        assert_body = config.assert_body_with_id_5

        response = ApiService.get(action_url=url)

        assert response.status_code == 200, \
            f'Response status code is not 200. Response status code is {response.status_code}'
        assert response.json() == assert_body, "Users data is invalid"
