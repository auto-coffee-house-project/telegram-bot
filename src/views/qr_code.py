from views import PhotoView

__all__ = ('QRCodeView',)


class QRCodeView(PhotoView):
    caption = 'Покажите этот QR-код баристе, чтобы получить бонус 🎉'

    def __init__(self, qr_code_url: str) -> None:
        self.__qr_code_url = qr_code_url

    def get_photo(self) -> str:
        return self.__qr_code_url
