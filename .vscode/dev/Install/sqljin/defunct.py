import logging

def translate_loglevel(input:str) -> int:
    if input[:1].lower() == 'd': return logging.DEBUG
    if input[:1].lower() == 'i': return logging.INFO
    if input[:1].lower() == 'w': return logging.WARNING
    if input[:1].lower() == 'e': return logging.ERROR
    # maybe raise exception / error?  for now:
    return None
