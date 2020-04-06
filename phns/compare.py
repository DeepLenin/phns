import editdistance

def compare(phns1, phns2):
    distance = editdistance.eval(phns1, phns2)
    return {
        "distance": distance,
        "cer": distance/len(phns1)
    }
