from uuid import uuid4


def create_id() -> str:
    """
    REMOVES DASHES FROM UUID AND RETURNS ID STRING
    example: a1d5b2a8-2dc1-428b-a6ec-b5ed8733bc4e == a1d5b2a82dc1428ba6ecb5ed8733bc4e
    """
    result = ''
    return result.join(str(uuid4()).split('-'))


def generate_id(number: int = 6) -> str:
    """
    CREATES RANDOM STRING CHARACTER WITH LENGTH OF NUMBER. DEFAULT = 6
    example: generate_id() == r54jY12 
            : generate_id(10) == r54jY12j80a
    """
    result = create_id()[:number]
    return result
