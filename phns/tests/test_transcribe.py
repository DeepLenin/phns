from phns import Phn
from phns.utils import transcribe


def test_transcribe_simple_word():
    transcriptions = transcribe.word("that^is")
    assert transcriptions == {
        (Phn("dh"), Phn("ae1"), Phn("t"), Phn("ih1"), Phn("z")),
        (Phn("dh"), Phn("ah"), Phn("t"), Phn("ih1"), Phn("z")),
        (Phn("dh"), Phn("ae1"), Phn("t"), Phn("s")),
    }
