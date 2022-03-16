import tests.db_setup as db_config


def test_create_message(db_init, client):
    response = client.post(f'/recipients/{db_config.recipient}/messages',json={
        "sender": "test@test.com",
        "subject": "Test1",
        "content": "hello, this is a test"
    })
    assert response.status_code == 201
    message = response.get_json()
    assert len(message) == 7, "Invalid number of keys returned"
    assert "id" in message, "Id not present in the response"
    assert "sender" in message, "Sender not present in the response"
    assert "subject" in message, "Subject not present in the response"
    assert "content" in message, "Content not present in the response"


def test_create_message_with_invalid_content_typ(db_init, client):
    response = client.post(f'/recipients/{db_config.recipient}/messages', data={
        "sender": "test@test.com",
        "subject": "Test1",
        "content": "hello, this is a test"
    })
    assert response.status_code == 400
    assert response.get_json().get("error") == "400 Bad Request: Invalid content-type"
    


def test_create_message_with_invalid_sender(db_init, client): 
    response = client.post(f'/recipients/{db_config.recipient}/messages',json={
        "subject": "Test1",
        "content": "hello, this is a test"
    })
    assert response.status_code == 400
    assert response.get_json().get("error") == "400 Bad Request: Email invalid"



def test_create_message_with_invalid_subject(db_init, client): 

    response = client.post(f'/recipients/{db_config.recipient}/messages',json={
        "sender": "test@test.com",
        "content": "hello, this is a test"
    })
    assert response.status_code == 400
    assert response.get_json().get("error") == "400 Bad Request: Subject missing"
    


def test_create_message_with_invalid_content(db_init, client): 
    response = client.post(f'/recipients/{db_config.recipient}/messages',json={
        "sender": "test@test.com",
        "subject": "Test1",
    })
    assert response.status_code == 400
    assert response.get_json().get("error") == "400 Bad Request: Content missing"



def test_get_new_messages(db_init_with_data, client):
    response = client.get(f'/recipients/{db_config.recipient}/messages')
    assert response.status_code == 200
    messages = response.get_json()
    
    assert messages[0]["id"] == db_config.id1
    assert messages[1]["id"] == db_config.id2
    assert messages[2]["id"] == db_config.id3

    assert messages[0]["new"]
    assert messages[1]["new"]
    assert messages[2]["new"]
    
    response = client.get(f'/recipients/{db_config.recipient}/messages')
    assert response.status_code == 200
    messages = response.get_json()
    assert len(messages) == 0



def test_get_all_messages_including_old_ones(db_init_with_data, client):
    response = client.get(f'/recipients/{db_config.recipient}/messages')
    assert response.status_code == 200
    messages = response.get_json()
    assert len(messages) == 3

    response = client.get(f'/recipients/{db_config.recipient}/messages?all=true')
    assert response.status_code == 200
    messages = response.get_json()
    assert len(messages) == 3



def test_get_all_messages_with_invalid_pagination(db_init_with_data, client):
    response = client.get(f'/recipients/{db_config.recipient}/messages?all=true&page=')
    assert response.status_code == 400
    assert response.get_json().get("error") == "400 Bad Request: Page and page size must be an int"



def test_get_all_messages_for_page_0(db_init_with_data, client):
    response = client.get(f'/recipients/{db_config.recipient}/messages?all=true&page=0&page_size=2')
    assert response.status_code == 200
    messages = response.get_json()
    assert len(messages) == 2
    assert messages[0]["id"] == db_config.id1
    assert messages[1]["id"] == db_config.id2



def test_get_all_messages_for_page_1(db_init_with_data, client):
    response = client.get(f'/recipients/{db_config.recipient}/messages?all=true&page=1&page_size=2')
    assert response.status_code == 200
    message = response.get_json()
    assert len(message) == 1
    assert message[0]["id"] == db_config.id3



def test_get_messages_by_id(db_init_with_data, client):
    response = client.get(f'/recipients/{db_config.recipient}/messages/{db_config.id1}')
    assert response.status_code == 200
    message = response.get_json()
    assert len(message) == 7, "Invalid number of keys returned"



def test_get_messages_by_id_with_non_existent_id(db_init_with_data, client):
    response = client.get(f'/recipients/{db_config.recipient}/messages/34567NonExistingId')
    assert response.status_code == 404
    message = response.get_json()
    assert response.get_json().get("error") == "404 Not Found: No message found for that id"



def test_delete_single_message(db_init_with_data, client):
    response = client.delete(f'/recipients/{db_config.recipient}/messages/{db_config.id1}')
    assert response.status_code == 200
    delete_stats = response.get_json()
    assert delete_stats["count_deleted"] == 1



def test_delete_multiple_messages(db_init_with_data, client):
    response = client.delete(f'/recipients/{db_config.recipient}/messages', json={
        "ids": [db_config.id1, db_config.id2, "34567NonExistingId"]
    })
    assert response.status_code == 200
    delete_stats = response.get_json()
    assert delete_stats["count_deleted"] == 2



def test_delete_multiple_messages_with_invalid_ids(db_init_with_data, client):
    response = client.delete(f'/recipients/{db_config.recipient}/messages', json={
        "ids": [True, 4, "34567NonExistingId"]
    })
    assert response.status_code == 400
    assert response.get_json().get("error") == "400 Bad Request: The list of ids must contain only string"
    
    
