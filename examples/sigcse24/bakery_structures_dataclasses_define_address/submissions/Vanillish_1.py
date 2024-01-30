from dataclasses import dataclass

@dataclass
class Address:
    number: int
    street: str
    city: str
    state: str
    
location = Address(18,'Amstel Ave', 'Newark','DE')
print(location.state)
