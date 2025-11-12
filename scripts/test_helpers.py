"""Test script to verify helpers implementation."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.helpers import (
    ValidationError,
    validate_response_status,
    validate_required_fields,
    validate_field_types,
    DataGenerator,
    generate_cpf,
    generate_phone_number,
    generate_secure_password,
    generate_email,
    generate_user_data,
)


def test_validators():
    """Test validator functions."""
    print("Testing validators...")
    
    # Test validate_required_fields
    data = {'name': 'John', 'email': 'john@example.com'}
    try:
        validate_required_fields(data, ['name', 'email'])
        print("✓ validate_required_fields: PASS")
    except ValidationError as e:
        print(f"✗ validate_required_fields: FAIL - {e}")
    
    # Test missing field
    try:
        validate_required_fields(data, ['name', 'email', 'phone'])
        print("✗ validate_required_fields (missing): Should have raised error")
    except ValidationError:
        print("✓ validate_required_fields (missing): PASS")
    
    # Test validate_field_types
    try:
        validate_field_types(data, {'name': str, 'email': str})
        print("✓ validate_field_types: PASS")
    except ValidationError as e:
        print(f"✗ validate_field_types: FAIL - {e}")
    
    print()


def test_data_generator():
    """Test data generator functions."""
    print("Testing data generator...")
    
    generator = DataGenerator()
    
    # Test CPF generation
    cpf_formatted = generate_cpf(formatted=True)
    cpf_unformatted = generate_cpf(formatted=False)
    print(f"✓ CPF (formatted): {cpf_formatted}")
    print(f"✓ CPF (unformatted): {cpf_unformatted}")
    
    # Test phone number generation
    phone_mobile = generate_phone_number(mobile=True, formatted=True)
    phone_landline = generate_phone_number(mobile=False, formatted=True)
    print(f"✓ Phone (mobile): {phone_mobile}")
    print(f"✓ Phone (landline): {phone_landline}")
    
    # Test password generation
    password = generate_secure_password(length=12)
    print(f"✓ Secure password: {password} (length: {len(password)})")
    
    # Test email generation
    email = generate_email()
    print(f"✓ Email: {email}")
    
    # Test user data generation
    user_data = generate_user_data(include_password=True)
    print(f"✓ User data generated:")
    print(f"  - Username: {user_data['username']}")
    print(f"  - Email: {user_data['email']}")
    print(f"  - Full name: {user_data['full_name']}")
    print(f"  - CPF: {user_data['cpf']}")
    print(f"  - Phone: {user_data['phone']}")
    print(f"  - Password: {user_data['password']}")
    
    # Test address generation
    print(f"  - Address: {user_data['address']['street']}, {user_data['address']['number']}")
    print(f"    {user_data['address']['city']}/{user_data['address']['state']} - {user_data['address']['cep']}")
    
    # Test CEP generation
    cep = generator.generate_cep(formatted=True)
    print(f"✓ CEP: {cep}")
    
    # Test random string
    random_str = generator.generate_random_string(length=10)
    print(f"✓ Random string: {random_str}")
    
    # Test random number
    random_num = generator.generate_random_number(1, 100)
    print(f"✓ Random number: {random_num}")
    
    print()


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing Helpers Implementation")
    print("=" * 60)
    print()
    
    try:
        test_validators()
        test_data_generator()
        
        print("=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
