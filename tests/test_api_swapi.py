
#-------------Endpoint people test------------------------------
def test_get_all_people(api_request_context):
    """Test para verificar que la lista general de personas responde correctamente"""
    # 1. Realizamos la petición GET al endpoint de personas
    response = api_request_context.get("people/")

    # 2. Verificamos que el código de estado sea 200 (OK)
    assert response.status == 200

    # 3. Validamos que el JSON contenga resultados
    data = response.json()
    print(data)
    assert data["count"] > 0
    assert isinstance(data["results"], list)


def test_get_specific_character(api_request_context):
    """Test para validar los datos exactos de Luke Skywalker (ID 1)"""
    response = api_request_context.get("people/1/")
    assert response.ok

    character = response.json()

    # Validaciones de datos según la documentación de SWAPI
    assert character["name"] == "Luke Skywalker"
    assert character["gender"] == "male"
    assert "tatooine" in character["homeworld"]  # La URL del planeta suele contener el nombre o ID


def test_api_pepole_not_found(api_request_context):
    """Test negativo: ¿Qué pasa si pedimos un recurso que no existe?"""
    # Pedimos el personaje 9999 (que no existe)
    response = api_request_context.get("people/9999/")

    # Verificamos que la API responda con un 404 (Not Found)
    assert response.status == 404
    assert response.json()["detail"] == "Not found"


#-------------Endpoint people test------------------------------
def test_get_all_films(api_request_context):
    """Test para verificar que la lista general de personas responde correctamente"""
    # 1. Realizamos la petición GET al endpoint de personas
    response = api_request_context.get("films/")

    # 2. Verificamos que el código de estado sea 200 (OK)
    assert response.status == 200

    # 3. Validamos que el JSON contenga resultados
    data = response.json()
    print(data)
    assert data["count"] > 0
    assert isinstance(data["results"], list)


def test_get_specific_film(api_request_context):
    """Test para validar los datos exactos de Luke Skywalker (ID 1)"""
    response = api_request_context.get("films/1/")
    assert response.ok

    film = response.json()

    # Validaciones de datos según la documentación de SWAPI
    assert film["title"] == "A New Hope"
    assert film["director"] == "George Lucas"



def test_api_film_not_found(api_request_context):
    """Test negativo: ¿Qué pasa si pedimos un recurso que no existe?"""
    # Pedimos el personaje 9999 (que no existe)
    response = api_request_context.get("films/9999/")

    # Verificamos que la API responda con un 404 (Not Found)
    assert response.status == 404
    assert response.json()["detail"] == "Not found"