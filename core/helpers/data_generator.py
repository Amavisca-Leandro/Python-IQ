"""Data generator using Faker for test data creation."""

from typing import Optional, Dict, Any
from faker import Faker
import random
import string
import re


class DataGenerator:
    """Generate test data using Faker with Brazilian localization."""
    
    def __init__(self, locale: str = 'pt_BR'):
        """
        Initialize data generator with specified locale.
        
        Args:
            locale: Faker locale (default: pt_BR for Brazilian Portuguese)
        """
        self.faker = Faker(locale)
        Faker.seed(None)  # Use random seed for each instance
    
    # Brazilian-specific data generators
    
    def generate_cpf(self, formatted: bool = True) -> str:
        """
        Generate a valid Brazilian CPF number.
        
        Args:
            formatted: If True, returns formatted CPF (XXX.XXX.XXX-XX)
                      If False, returns only digits
        
        Returns:
            Valid CPF string
        """
        # Generate 9 random digits
        cpf_digits = [random.randint(0, 9) for _ in range(9)]
        
        # Calculate first verification digit
        sum_1 = sum((10 - i) * digit for i, digit in enumerate(cpf_digits))
        digit_1 = (sum_1 * 10) % 11
        digit_1 = 0 if digit_1 == 10 else digit_1
        cpf_digits.append(digit_1)
        
        # Calculate second verification digit
        sum_2 = sum((11 - i) * digit for i, digit in enumerate(cpf_digits))
        digit_2 = (sum_2 * 10) % 11
        digit_2 = 0 if digit_2 == 10 else digit_2
        cpf_digits.append(digit_2)
        
        cpf = ''.join(map(str, cpf_digits))
        
        if formatted:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf
    
    def generate_phone_number(self, mobile: bool = True, formatted: bool = True) -> str:
        """
        Generate a valid Brazilian phone number.
        
        Args:
            mobile: If True, generates mobile number (9 digits)
                   If False, generates landline (8 digits)
            formatted: If True, returns formatted number
        
        Returns:
            Brazilian phone number string
        """
        # Brazilian area codes (DDD)
        area_codes = ['11', '12', '13', '14', '15', '16', '17', '18', '19',  # SP
                     '21', '22', '24',  # RJ
                     '27', '28',  # ES
                     '31', '32', '33', '34', '35', '37', '38',  # MG
                     '41', '42', '43', '44', '45', '46',  # PR
                     '47', '48', '49',  # SC
                     '51', '53', '54', '55',  # RS
                     '61',  # DF
                     '62', '64',  # GO
                     '63',  # TO
                     '65', '66',  # MT
                     '67',  # MS
                     '68',  # AC
                     '69',  # RO
                     '71', '73', '74', '75', '77',  # BA
                     '79',  # SE
                     '81', '87',  # PE
                     '82',  # AL
                     '83',  # PB
                     '84',  # RN
                     '85', '88',  # CE
                     '86', '89',  # PI
                     '91', '93', '94',  # PA
                     '92', '97',  # AM
                     '95',  # RR
                     '96',  # AP
                     '98', '99']  # MA
        
        ddd = random.choice(area_codes)
        
        if mobile:
            # Mobile numbers start with 9
            number = f"9{random.randint(10000000, 99999999)}"
        else:
            # Landline numbers
            number = f"{random.randint(10000000, 99999999)}"
        
        if formatted:
            if mobile:
                return f"+55 ({ddd}) {number[:5]}-{number[5:]}"
            else:
                return f"+55 ({ddd}) {number[:4]}-{number[4:]}"
        
        return f"55{ddd}{number}"
    
    def generate_cep(self, formatted: bool = True) -> str:
        """
        Generate a Brazilian CEP (postal code).
        
        Args:
            formatted: If True, returns formatted CEP (XXXXX-XXX)
        
        Returns:
            CEP string
        """
        cep = f"{random.randint(10000, 99999)}{random.randint(100, 999)}"
        
        if formatted:
            return f"{cep[:5]}-{cep[5:]}"
        return cep
    
    # Password generation
    
    def generate_secure_password(
        self,
        length: int = 12,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_special: bool = True,
        special_chars: str = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    ) -> str:
        """
        Generate a secure password with specified criteria.
        
        Args:
            length: Password length (minimum 8)
            include_uppercase: Include uppercase letters
            include_lowercase: Include lowercase letters
            include_digits: Include digits
            include_special: Include special characters
            special_chars: String of special characters to use
        
        Returns:
            Secure password string
        
        Raises:
            ValueError: If length < 8 or no character types selected
        """
        if length < 8:
            raise ValueError("Password length must be at least 8 characters")
        
        char_sets = []
        password_chars = []
        
        if include_uppercase:
            char_sets.append(string.ascii_uppercase)
            password_chars.append(random.choice(string.ascii_uppercase))
        
        if include_lowercase:
            char_sets.append(string.ascii_lowercase)
            password_chars.append(random.choice(string.ascii_lowercase))
        
        if include_digits:
            char_sets.append(string.digits)
            password_chars.append(random.choice(string.digits))
        
        if include_special:
            char_sets.append(special_chars)
            password_chars.append(random.choice(special_chars))
        
        if not char_sets:
            raise ValueError("At least one character type must be selected")
        
        # Fill remaining length with random characters from all sets
        all_chars = ''.join(char_sets)
        remaining_length = length - len(password_chars)
        password_chars.extend(random.choice(all_chars) for _ in range(remaining_length))
        
        # Shuffle to avoid predictable patterns
        random.shuffle(password_chars)
        
        return ''.join(password_chars)
    
    # Common test data generators
    
    def generate_email(self, domain: Optional[str] = None) -> str:
        """
        Generate a random email address.
        
        Args:
            domain: Optional domain name (e.g., 'example.com')
        
        Returns:
            Email address string
        """
        if domain:
            username = self.faker.user_name()
            return f"{username}@{domain}"
        return self.faker.email()
    
    def generate_username(self, min_length: int = 3, max_length: int = 20) -> str:
        """
        Generate a random username.
        
        Args:
            min_length: Minimum username length
            max_length: Maximum username length
        
        Returns:
            Username string
        """
        username = self.faker.user_name()
        
        # Ensure length constraints
        if len(username) < min_length:
            username = username + ''.join(
                random.choices(string.ascii_lowercase + string.digits, 
                             k=min_length - len(username))
            )
        elif len(username) > max_length:
            username = username[:max_length]
        
        return username
    
    def generate_full_name(self) -> str:
        """Generate a random full name."""
        return self.faker.name()
    
    def generate_first_name(self) -> str:
        """Generate a random first name."""
        return self.faker.first_name()
    
    def generate_last_name(self) -> str:
        """Generate a random last name."""
        return self.faker.last_name()
    
    def generate_company_name(self) -> str:
        """Generate a random company name."""
        return self.faker.company()
    
    def generate_address(self) -> Dict[str, str]:
        """
        Generate a complete Brazilian address.
        
        Returns:
            Dictionary with address components
        """
        return {
            'street': self.faker.street_name(),
            'number': str(random.randint(1, 9999)),
            'complement': random.choice(['Apto 101', 'Casa', 'Bloco A', '']),
            'neighborhood': self.faker.bairro(),
            'city': self.faker.city(),
            'state': self.faker.estado_sigla(),
            'cep': self.generate_cep(formatted=True),
            'country': 'Brasil'
        }
    
    def generate_date_of_birth(self, min_age: int = 18, max_age: int = 80) -> str:
        """
        Generate a date of birth.
        
        Args:
            min_age: Minimum age in years
            max_age: Maximum age in years
        
        Returns:
            Date string in ISO format (YYYY-MM-DD)
        """
        date = self.faker.date_of_birth(minimum_age=min_age, maximum_age=max_age)
        return date.strftime('%Y-%m-%d')
    
    def generate_url(self, scheme: str = 'https') -> str:
        """
        Generate a random URL.
        
        Args:
            scheme: URL scheme (http or https)
        
        Returns:
            URL string
        """
        return self.faker.url(schemes=[scheme])
    
    def generate_text(self, max_sentences: int = 3) -> str:
        """
        Generate random text.
        
        Args:
            max_sentences: Maximum number of sentences
        
        Returns:
            Text string
        """
        return self.faker.text(max_nb_chars=200)
    
    def generate_uuid(self) -> str:
        """Generate a random UUID."""
        return self.faker.uuid4()
    
    # User data generation for testing
    
    def generate_user_data(
        self,
        include_password: bool = True,
        password_length: int = 12
    ) -> Dict[str, Any]:
        """
        Generate complete user data for testing.
        
        Args:
            include_password: Whether to include password field
            password_length: Length of generated password
        
        Returns:
            Dictionary with user data
        """
        data = {
            'username': self.generate_username(),
            'email': self.generate_email(),
            'first_name': self.generate_first_name(),
            'last_name': self.generate_last_name(),
            'full_name': self.generate_full_name(),
            'phone': self.generate_phone_number(mobile=True, formatted=True),
            'cpf': self.generate_cpf(formatted=True),
            'date_of_birth': self.generate_date_of_birth(),
            'address': self.generate_address()
        }
        
        if include_password:
            data['password'] = self.generate_secure_password(length=password_length)
        
        return data
    
    # Utility methods
    
    def generate_random_string(
        self,
        length: int = 10,
        chars: str = string.ascii_letters + string.digits
    ) -> str:
        """
        Generate a random string.
        
        Args:
            length: String length
            chars: Characters to use
        
        Returns:
            Random string
        """
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_random_number(self, min_value: int = 0, max_value: int = 100) -> int:
        """
        Generate a random number.
        
        Args:
            min_value: Minimum value
            max_value: Maximum value
        
        Returns:
            Random integer
        """
        return random.randint(min_value, max_value)
    
    def generate_boolean(self) -> bool:
        """Generate a random boolean value."""
        return random.choice([True, False])
    
    def pick_random(self, items: list) -> Any:
        """
        Pick a random item from a list.
        
        Args:
            items: List of items to choose from
        
        Returns:
            Random item from the list
        """
        return random.choice(items)


# Global instance for convenience
data_generator = DataGenerator()


# Convenience functions that use the global instance

def generate_cpf(formatted: bool = True) -> str:
    """Generate a valid Brazilian CPF number."""
    return data_generator.generate_cpf(formatted)


def generate_phone_number(mobile: bool = True, formatted: bool = True) -> str:
    """Generate a valid Brazilian phone number."""
    return data_generator.generate_phone_number(mobile, formatted)


def generate_secure_password(length: int = 12) -> str:
    """Generate a secure password."""
    return data_generator.generate_secure_password(length)


def generate_email(domain: Optional[str] = None) -> str:
    """Generate a random email address."""
    return data_generator.generate_email(domain)


def generate_user_data(include_password: bool = True) -> Dict[str, Any]:
    """Generate complete user data for testing."""
    return data_generator.generate_user_data(include_password)
