import string
from ckan.common import _, config
from ckan.lib.navl.dictization_functions import Missing, Invalid
from paste.deploy.converters import asbool

MIN_PASSWORD_LENGTH = config.get('ckan.fortify.password_policy.min_length', 12)
MIN_LEN_ERROR = (
    'Your password must be {} characters or longer and contain at least 1 character '
    'from each of the following character sets: uppercase characters, lowercase '
    'characters, digits, punctuation/special characters (e.g. !"#$%&()*+,-./:;<=>?@[\]^_`~).'
)
REPEATING_CHAR_ERROR = 'Passwords must not contain repeating values.'


def user_password_validator(key, data, errors, context):
    value = data[key]

    if isinstance(value, Missing):
        pass  # Already handeled in core
    elif not isinstance(value, basestring):
        raise Invalid(_('Passwords must be strings.'))
    elif value == '':
        pass  # Already handled in core
    else:
        allow_repeated_chars = asbool(config.get('ckan.fortify.password_policy.allow_repeated_chars', True))
        if allow_repeated_chars:
            for c in value:
                if c * 2 in value:
                    raise Invalid(_(REPEATING_CHAR_ERROR))
        # NZISM compliant password rules
        rules = [
            any(x.isupper() for x in value),
            any(x.islower() for x in value),
            any(x.isdigit() for x in value),
            any(x in string.punctuation for x in value)
        ]
        if len(value) < MIN_PASSWORD_LENGTH or sum(rules) < 4:
            raise Invalid(_(MIN_LEN_ERROR.format(MIN_PASSWORD_LENGTH)))

