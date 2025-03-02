
class CommonUtils:

    @staticmethod
    def to_camel_case(snake_str: str) -> str:
        substrings = snake_str.split('_')
        return substrings[0] + ''.join(x.title() for x in substrings[1:])
