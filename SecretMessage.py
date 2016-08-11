def find_secret_message(paragraph):
    paragraph = paragraph.translate(None, ',.:!?')
    paragraph = [x.lower() for x in paragraph.split(' ')]

    final_string = []
    secret = set()

    for e in paragraph:
        if e not in secret:
            secret.add(e)
        elif e not in final_string:
            final_string.append(e)
        
    return ' '.join(final_string)