# Helpers Module

This module provides reusable validators and data generators for test automation.

## Validators

The validators module provides functions to validate HTTP responses, JSON schemas, field types, and database data.

### HTTP Response Validators

```python
from core.helpers import validate_response_status, validate_response_time

# Validate status code
validate_response_status(response, 200)
validate_response_status(response, [200, 201, 204])

# Validate response time
validate_response_time(response, max_time_ms=1000)
```

### Data Validators

```python
from core.helpers import validate_required_fields, validate_field_types, validate_json_schema

# Validate required fields
data = {'name': 'John', 'email': 'john@example.com'}
validate_required_fields(data, ['name', 'email'])

# Validate field types
validate_field_types(data, {'name': str, 'email': str})

# Validate JSON schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"}
    },
    "required": ["name"]
}
validate_json_schema(data, schema)
```

### Database Validators

```python
from core.helpers import (
    validate_db_record_exists,
    validate_db_record_count,
    validate_db_field_value,
    validate_db_relationship
)

# Validate record exists
validate_db_record_exists(session, User, {'email': 'test@example.com'})

# Validate record count
validate_db_record_count(session, User, expected_count=5)

# Validate field value
validate_db_field_value(session, User, record_id=1, field_name='is_active', expected_value=True)

# Validate relationship
validate_db_relationship(session, user_record, 'profile', expected_count=1)
```

## Data Generator

The data generator module provides functions to generate test data using Faker with Brazilian localization.

### Brazilian Data

```python
from core.helpers import generate_cpf, generate_phone_number, DataGenerator

# Generate CPF
cpf = generate_cpf(formatted=True)  # 123.456.789-00
cpf_raw = generate_cpf(formatted=False)  # 12345678900

# Generate phone number
mobile = generate_phone_number(mobile=True, formatted=True)  # +55 (11) 99999-9999
landline = generate_phone_number(mobile=False, formatted=True)  # +55 (11) 3333-4444

# Generate CEP
generator = DataGenerator()
cep = generator.generate_cep(formatted=True)  # 12345-678
```

### User Data

```python
from core.helpers import generate_email, generate_secure_password, generate_user_data

# Generate email
email = generate_email()
email_custom = generate_email(domain='example.com')

# Generate secure password
password = generate_secure_password(length=12)

# Generate complete user data
user_data = generate_user_data(include_password=True)
# Returns:
# {
#     'username': 'johndoe',
#     'email': 'john@example.com',
#     'first_name': 'John',
#     'last_name': 'Doe',
#     'full_name': 'John Doe',
#     'phone': '+55 (11) 99999-9999',
#     'cpf': '123.456.789-00',
#     'date_of_birth': '1990-01-01',
#     'address': {...},
#     'password': 'SecurePass123!'
# }
```

### Advanced Usage

```python
from core.helpers import DataGenerator

generator = DataGenerator(locale='pt_BR')

# Generate address
address = generator.generate_address()
# Returns:
# {
#     'street': 'Rua das Flores',
#     'number': '123',
#     'complement': 'Apto 101',
#     'neighborhood': 'Centro',
#     'city': 'São Paulo',
#     'state': 'SP',
#     'cep': '01234-567',
#     'country': 'Brasil'
# }

# Generate random data
random_str = generator.generate_random_string(length=10)
random_num = generator.generate_random_number(1, 100)
random_bool = generator.generate_boolean()

# Pick random item
status = generator.pick_random(['active', 'inactive', 'pending'])
```

## Custom Validators

You can create custom field validators:

```python
from core.helpers import validate_field_values

def is_valid_email(value):
    return '@' in value and '.' in value

def is_positive(value):
    return value > 0

data = {'email': 'test@example.com', 'age': 25}
validate_field_values(data, {
    'email': is_valid_email,
    'age': is_positive
})
```

## Error Handling

All validators raise `ValidationError` when validation fails:

```python
from core.helpers import ValidationError, validate_required_fields

try:
    validate_required_fields(data, ['name', 'email'])
except ValidationError as e:
    print(f"Validation failed: {e}")
```

## Integration with Tests

Example usage in pytest tests:

```python
import pytest
from core.helpers import (
    validate_response_status,
    validate_required_fields,
    generate_user_data,
    ValidationError
)

def test_create_user(api_client):
    # Generate test data
    user_data = generate_user_data()
    
    # Make API request
    response = api_client.post('/users', json=user_data)
    
    # Validate response
    validate_response_status(response, 201)
    
    # Validate response data
    response_data = response.json()
    validate_required_fields(response_data, ['id', 'username', 'email'])
    
    assert response_data['username'] == user_data['username']
```

## Requirements

- `requests` - For HTTP response validation
- `jsonschema` - For JSON schema validation
- `faker` - For test data generation
- `sqlalchemy` (optional) - For database validators
