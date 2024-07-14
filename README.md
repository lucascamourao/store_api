# TDD Project

## What is TDD?
TDD stands for Test Driven Development. The idea of TDD is that you work in cycles.

### TDD Cycle
![C4](/docs/img/img-tdd.png)

### Advantages of TDD
- Deliver high-quality software;
- Test to find potential failures;
- Create integration tests and unit tests;
- Avoid writing complex or unnecessary code;

The purpose of TDD is to write tests before the actual code, ensuring higher quality in the project. Additionally, if you leave testing until the end, you might end up not doing it at all. This results in an application that is more prone to errors and of lower quality.

# Store API
## Project Summary
This document provides information on the development of an API using FastAPI and TDD.

## Objetive
The main goal of this application is to provide practical knowledge of TDD by developing an API with the Python framework FastAPI. It uses MongoDB as the database, Pydantic for validations, Pytest for testing, among other libraries.

## What is it?
An application that:
- Is for educational purposes;
- Allows practical learning about TDD with FastAPI and Pytest;

## What is it not?
An application that:
- Communicates with external apps;

## Proposed Solution
Development of a simple application using TDD to understand how to create tests with pytest. This includes building tests for Schemas, Usecases, and Controllers (integration tests).

### Architecture
|![C4](/docs/img/store.drawio.png)|
|:--:|
| C4 Diagram of the Store API | Diagrama de C4 da Store API |

### Database - MongoDB
|![C4](/docs/img/product.drawio.png)|
|:--:|
| Database - Store API |


## StoreAPI
### Sequence Diagrams for the Product Module
#### Product Creation Diagram

```mermaid
sequenceDiagram
    title Create Product
    Client->>+API: Request product creation
    Note right of Client: POST /products

    API->>API: Validate body

    alt Invalid body
        API->Client: Error Response
        Note right of Client: Status Code: 422 - Unprocessable Entity
    end

    API->>+Database: Request product creation
    alt Error on insertion
        API->Client: Error Response
        note right of Client: Status Code: 500 - Internal Server Error
        end
    Database->>-API: Successfully created

    API->>-Client: Successful Response
    Note right of Client: Status Code: 201 - Created

```
#### Product Listing Diagram

```mermaid
sequenceDiagram
    title List Products
    Client->>+API: Request products list
    Note right of Client: GET /products

    API->>+Database: Request products list

    Database->>-API: Successfully queried

    API->>-Client: Successful Response
    Note right of Client: Status Code: 200 - Ok
```

#### Product Detail Diagram

```mermaid
sequenceDiagram
    title Get Product
    Client->>+API: Request product
    Note right of Client: GET /products/{id}<br/> Path Params:<br/>    - id: <id>

    API->>+Database: Request product
    alt Error on query
        API->Client: Error Response
        Note right of Client: Status Code: 500 - Internal Server Error
    else Product not found
        API->Client: Error Response
        Note right of Client: Status Code: 404 - Not Found
        end

    Database->>-API: Successfully queried

    API->>-Client: Successful Response
    Note right of Client: Status Code: 200 - Ok
```
#### Product Update Diagram

```mermaid
sequenceDiagram
    title PUT Product
    Client->>+API: Request product update
    Note right of Client: PUT /products/{id}<br/> Path Params:<br/>    - id: <id>

    API->>API: Validate body

    alt Invalid body
        API->Client: Error Response
        Note right of Client: Status Code: 422 - Unprocessable Entity
    end

    API->>+Database: Request product
    alt Product not found
        API->Client: Error Response
        Note right of Client: Status Code: 404 - Not Found
        end

    Database->>-API: Successfully updated

    API->>-Client: Successful Response
    Note right of Client: Status Code: 200 - Ok
```

#### Product Deletion Diagram

```mermaid
sequenceDiagram
    title Delete Product
    Client->>+API: Request product delete
    Note right of Client: DELETE /products/{id}<br/> Path Params:<br/>    - id: <id>

    API->>+Database: Request product
    alt Product not found
        API->Client: Error Response
        Note right of Client: Status Code: 404 - Not Found
        end

    Database->>-API: Successfully deleted

    API->>-Client: Successful Response
    Note right of Client: Status Code: 204 - No content
```

## Final Challenge
- Create
    - Map an exception in case of an insertion error and capture it in the controller.
- Update
    - Modify the patch method to return a Not Found exception when the data is not found.
    - Handle the exception in the controller to return a user-friendly message.
    - When updating data, the updated_at field should correspond to the current time, and allow modification of updated_at.
- Filters:
    - Register products with different prices.
    - Apply a price filter like this: (price > 5000 and price < 8000).

## Prepare Environment

We will use Pyenv + Poetry, follow the link below for setting up the environment:

[poetry-documentation](https://github.com/nayannanara/poetry-documentation/blob/master/poetry-documentation.md)

## Useful Documentation Links
[mermaid](https://mermaid.js.org/)

[pydantic](https://docs.pydantic.dev/dev/)

[validatores-pydantic](https://docs.pydantic.dev/latest/concepts/validators/)

[model-serializer](https://docs.pydantic.dev/dev/api/functional_serializers/#pydantic.functional_serializers.model_serializer)

[mongo-motor](https://motor.readthedocs.io/en/stable/)

[pytest](https://docs.pytest.org/en/7.4.x/)

## Note
This is a fork from the [original DIO store_api project](https://github.com/digitalinnovationone/store_api). The project is from the Python AI Backend Developer Bootcamp [(DIO)](https://www.dio.me/). <br/>
The API was coded throughout the course and I only made the modifications needed for the challenge. 
