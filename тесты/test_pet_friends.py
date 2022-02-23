import os

from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result


def test_get_all_pets_with_valid_key(filter=""):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0


def test_add_new_pet_with_valid_data(name="Рута", animal_type="дворняжка", age="0,5", pet_photo="images/Рута..JPG"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result["name"] == name


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "Рута", "дворняжка", "0,5", "images/Рута..JPG")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets["pets"][0]["id"]
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name="Гера", animal_type="борзая", age=4):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets["pets"][0]["id"], name, animal_type, age)
        assert status == 200
        assert result["name"] == name
    else:
        raise Exception("Нет моих питомцев")


# Тест 1 - без фото
def test_add_new_pet_simple_with_valid_data_without_photo(name='ЯйценКлацКлац', animal_type='Собака'def test_add_new_pet_simple(name="Пацан", animal_type="кот", age=1):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result["name"] == name
    assert result["pet_photo"] == ""


# Тест 2 - добавить фото
def test_add_photo_of_pet(pet_photo='images/Рута 3 мес.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
    assert status == 200
    assert result['pet_photo'] != ''


# Тест 3 - отрицательный возраст
def test_add_pet_with_negative_age(name='Семён', animal_type='кот', age='-8', pet_photo='images/Сёма.JPG'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


# Тест 4 - возраст 1000 лет
def test_unreal_age(name="Рута", animal_type="дворняжка", age="2000", pet_photo="images/Рута 3 мес.jpg"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


# Тест 5 - недопустимое имя
def test_add_new_pet_with_invalid_name(name="2!5@1#?№$^%*", animal_type="утконос", age="6", pet_photo='images/Сёма.JPG'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


# Тест 6 - кривое фото
def test_add_pet_with_invalid_photo(name="Рута", animal_type="дворняжка", age="0,5", pet_photo=""):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except PermissionError:
        print("Укажите путь к файлу")


# Тест 7 - неверный пароль
def test_invalid_password(email=valid_email, password=""):
    status, result = pf.get_api_key(email, password)
    assert status == 403


# Тест 8 - неверный логин
def test_invalid_login(email="", password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403


# Тест 9 - фото без данных
def test_add_photo_pet_without_data(name="", animal_type="", age="", pet_photo="images/Сёма.JPG"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


# Тест 10 - обновление с неверным ID
def test_update_pet_info_with_invalid_id(name='Рута', animal_type='дворняжка', age=0,5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][100]['id'], name, animal_type, age)
        assert status == 400
    else:
        raise Exception("Нет таких питомцев")                                                  
