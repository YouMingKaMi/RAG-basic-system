class DocumentNotFoundError(Exception):
    pass

class MessageNotFoundError(Exception):
    pass

class InvalidUploadError(Exception):
    pass

class DocumentProcessError(Exception):
    pass

class UploadProcessError(DocumentProcessError):
    pass

class ChunkProcessError(DocumentProcessError):
    pass

class IndexProcessError(DocumentProcessError):
    pass

