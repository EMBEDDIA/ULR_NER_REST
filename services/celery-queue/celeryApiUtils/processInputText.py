

def readText(input, format):
    if format == "plain":
        data_set = [{'tokens': x.split()} for x in input.split("\n") if len(x) > 0]
    elif format == "sentences":
        data_set = [{"tokens": sentence.split()} for sentence in input]
    else:
        data_set = [{"tokens": sentence} for sentence in input]
    return data_set

