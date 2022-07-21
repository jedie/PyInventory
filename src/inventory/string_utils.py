def ltruncatechars(text, max_length, truncate='…'):
    """
    >>> ltruncatechars('1234567890', max_length=10)
    '1234567890'
    >>> ltruncatechars('1234567890', max_length=5)
    '…7890'
    >>> ltruncatechars('1234567890', max_length=6)
    '…67890'
    >>> ltruncatechars('1234567890', max_length=6, truncate='...')
    '...890'
    """
    if len(text) > max_length:
        length = max_length - len(truncate)
        text = truncate + text[-length:]
    return text
