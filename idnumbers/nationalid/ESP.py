import re
from types import SimpleNamespace
from .util import validate_regexp


class NationalID:
    """
    Spain National ID number
    Documento Nacional de Identidad (DNI)
    https://en.wikipedia.org/wiki/National_identification_number#Spain
    https://es.wikipedia.org/wiki/C%C3%B3digo_de_identificaci%C3%B3n_fiscal
    https://gist.github.com/afgomez/5691823
    """
    METADATA = SimpleNamespace(**{
        'iso3166_alpha2': 'ES',
        # length without insignificant chars
        'min_length': 9,
        'max_length': 9,
        'parsable': False,
        'checksum': True,
        'regexp': re.compile(r'^(\d{8})([A-Z])$')
    })

    @staticmethod
    def validate(id_number: str) -> bool:
        """
        Validate the Spain national id number
        """
        if not validate_regexp(id_number, NationalID.METADATA.regexp):
            return False
        return NationalID.checksum(id_number)

    MAGIC_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"

    @staticmethod
    def checksum(id_number: str) -> bool:
        idx = int(id_number[:-1]) % 23
        return NationalID.MAGIC_LETTERS[idx] == id_number[-1]
