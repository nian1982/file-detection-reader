class SFTPError(Exception):
    pass


class SFTPConnectionError(SFTPError):
    pass


class SFTPAuthenticationError(SFTPError):
    pass


class RemoteFileNotFoundError(SFTPError):
    pass


class RemoteDirectoryCreateError(SFTPError):
    pass
