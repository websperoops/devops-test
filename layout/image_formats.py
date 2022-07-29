from wagtail.images.formats import Format, register_image_format


register_image_format(Format('center', 'Center', 'centered-wagtail-image', 'original' ))