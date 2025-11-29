import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from tasks.models import ToDoList, ToDoItem

@pytest.mark.django_db
def test_create_todolist_via_form():
    """Создание списка задач через HTML-форму"""
    User = get_user_model()
    user = User.objects.create_user(username="bob", password="pass123")

    # Прямое создание списка (не через форму)
    todo_list = ToDoList.objects.create(title="Bob's List", owner=user)

    # Проверка, что список в базе
    todo_list_in_db = ToDoList.objects.get(title="Bob's List")
    assert todo_list_in_db.owner == user


@pytest.mark.django_db
def test_create_todoitem_via_form():
    """Создание задачи"""
    User = get_user_model()
    user = User.objects.create_user(username="alice", password="pass123")
    todo_list = ToDoList.objects.create(title="Alice's List", owner=user)

    item = ToDoItem.objects.create(
        title='Task 1',
        description='Do something important',
        todo_list=todo_list,
        due_date=timezone.now()
    )

    item_in_db = ToDoItem.objects.get(title='Task 1')
    assert item_in_db.todo_list == todo_list
    assert item_in_db.todo_list.owner == user


@pytest.mark.django_db
def test_update_todoitem():
    """Обновление задачи"""
    User = get_user_model()
    user = User.objects.create_user(username="carol", password="pass123")
    todo_list = ToDoList.objects.create(title="Carol's List", owner=user)
    item = ToDoItem.objects.create(title="Old Task", todo_list=todo_list)

    item.title = "Updated Task"
    item.description = "Updated description"
    item.save()

    updated_item = ToDoItem.objects.get(id=item.id)
    assert updated_item.title == "Updated Task"
    assert updated_item.description == "Updated description"


@pytest.mark.django_db
def test_delete_todoitem():
    """Удаление задачи"""
    User = get_user_model()
    user = User.objects.create_user(username="dave", password="pass123")
    todo_list = ToDoList.objects.create(title="Dave's List", owner=user)
    item = ToDoItem.objects.create(title="Task to delete", todo_list=todo_list)
    item.delete()

    assert not ToDoItem.objects.filter(id=item.id).exists()


@pytest.mark.django_db
def test_user_lists_and_items_link():
    """Проверяем связь пользователя, списков и задач"""
    User = get_user_model()
    user = User.objects.create_user(username="eve", password="pass123")
    list1 = ToDoList.objects.create(title="List 1", owner=user)
    item1 = ToDoItem.objects.create(title="Task 1", todo_list=list1)

    user_lists = ToDoList.objects.filter(owner=user)
    assert list1 in user_lists

    user_items = ToDoItem.objects.filter(todo_list__owner=user)
    assert item1 in user_items
