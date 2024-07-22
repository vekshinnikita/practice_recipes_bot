
def replace_by_dict(str: str, dict: dict[str,str]):
    for key, value in dict.items():
        str = str.replace(f'{{{key}}}', value)
        
    return str
        
def get_pagination_direction(start:int, end:int, current:int):
    if current > start and current < end:
        return 'both'
    elif current == start and current < end:
        return 'only_next'
    elif current == end and current > start:
        return 'only_prev'
    else:
        return 'none'