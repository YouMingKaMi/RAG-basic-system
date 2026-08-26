class DocumentNotFoundError(Exception):
    pass

class InvalidUploadError(Exception):
    pass

class UploadProcessError(Exception):
    pass

class ChunkProcessError(Exception):
    pass

class IndexProcessError(Exception):
    pass