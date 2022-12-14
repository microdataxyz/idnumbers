import re
from types import SimpleNamespace
from .util import validate_regexp


def normalize(id_number: str) -> str:
    return re.sub(r'[.]', '', id_number)


class NationalID:
    """
    Netherlands National ID number
    Burgerservicenummer (BSN) (Citizen Service Number)
    https://en.wikipedia.org/wiki/National_identification_number#Netherlands
    https://nl.wikipedia.org/wiki/Burgerservicenummer
    """
    METADATA = SimpleNamespace(**{
        'iso3166_alpha2': 'NL',
        # length without insignificant chars
        'min_length': 9,
        'max_length': 9,
        'parsable': False,
        'checksum': True,
        'regexp': re.compile(r'(?!0000.00.000)^\d{4}[.]\d{2}[.]\d{3}$')

    })

    @staticmethod
    def validate(id_number: str) -> bool:
        """
        Validate the NLD id number
        """
        if not validate_regexp(id_number, NationalID.METADATA.regexp):
            return False
        return NationalID.checksum(id_number)

    MAGIC_MULTIPLIER = [9, 8, 7, 6, 5, 4, 3, 2]

    @staticmethod
    def checksum(id_number: str) -> bool:
        normalized = normalize(id_number)
        number_list = [int(char) for char in list(normalized[:-1])]
        total = sum([value * NationalID.MAGIC_MULTIPLIER[index] for (index, value) in enumerate(number_list)])
        checksum = total % 11
        return str(total % 11) == normalized[-1] if checksum != 10 else False
