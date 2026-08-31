from app.chunkers.text_chunker import chunk_text

def test_chunk_text():
    str_for_test = "abcdefghijf"
    arrage = ["abcd","defg","ghij",'jf']
    actual = chunk_text(str_for_test, 4, 1)
    assert actual == arrage