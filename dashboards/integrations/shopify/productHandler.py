from . import shopifyHandler

from dashboards.models import Integrations_Shopify_Product, Integrations_Shopify_Product_Tag, \
    Integrations_Shopify_Product_Image, Integrations_Shopify_Product_Option, \
    Integrations_Shopify_Product_Option_Value, Integrations_Shopify_Product_Variant, Integrations_Shopify_Shop

from django.db import transaction


class ProductHandler(shopifyHandler.ShopifyHandler):

    def __init__(self, data, integration_id, user_iden,shop_id):
        self.products=[]
        self.tags = {}
        self.options = {}
        self.option_values = {}
        self.variants = {}
        self.images = {}
        super(ProductHandler, self).__init__(data, integration_id, user_iden,shop_id,"product")


    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_products()

    def _Handler__save_dependent_objects(self):
        def save_dep_1():
            with transaction.atomic():
                self.save_tags()
                self.save_options()
                self.save_images()

        def save_dep_2():
            with transaction.atomic():
                self.save_variants()
                self.save_option_values()
        save_dep_1()
        save_dep_2()

    def _Handler__parse_data(self):
        for obj in self.data:
            product = Integrations_Shopify_Product(
                integration_id=self.integration_id,
                user_iden=self.user_iden,
                product_id=getattr(obj, "id", None),
                created_at=getattr(obj, "created_at", None),
                product_type=getattr(obj, "product_type", None),
                published_at=getattr(obj, "published_at", None),
                published_scope=getattr(obj, "published_scope", None),
                title=getattr(obj, "title", None),
                updated_at=getattr(obj, "updated_at", None),
                vendor=getattr(obj, "vendor", None)
            )

            self.products.append(product)
            tags = getattr(obj, "tags", "").split(", ")
            self.grab_tags(product.product_id, tags)

            options = getattr(obj, "options", [])
            self.grab_options(product.product_id, options)



            images = getattr(obj, "images", [])
            self.grab_images(product.product_id, images)



            variants = getattr(obj, "variants", [])

            self.grab_variants(product.product_id, variants, images)




    def save_products(self):
        shop = Integrations_Shopify_Shop.objects.get(shop_id=self.shop_id)
        for product in self.products:
            product.shop = shop
            self.update_or_save_instance(Integrations_Shopify_Product, product, "product_id")

    def save_tags(self):
        for p_id, tag in self.tags.items():
            product = self.get_instances_if_exists(
                Integrations_Shopify_Product,
                Integrations_Shopify_Product(product_id=p_id),
                "product_id"
            )
            tag.product = None if not product else product[0]
            self.update_or_save_instance(Integrations_Shopify_Product_Tag, tag, unique_attr=None)

    def save_options(self):
        for p_id, options in self.options.items():
            product = self.get_instances_if_exists(
                Integrations_Shopify_Product,
                Integrations_Shopify_Product(product_id=p_id),
                "product_id"
            )
            if product:
                for option in options:
                    option.product = product[0]
                    self.update_or_save_instance(Integrations_Shopify_Product_Option, option, unique_attr="option_id")

    def save_option_values(self):
        for o_id, value in self.option_values.items():
            option = self.get_instances_if_exists(
                Integrations_Shopify_Product_Option,
                Integrations_Shopify_Product_Option(option_id=o_id),
                "option_id"
            )
            if option:
                value.option = option[0]
                self.update_or_save_instance(Integrations_Shopify_Product_Option_Value, value, unique_attr=None)

    def save_variants(self):
        for p_id, variants in self.variants.items():
            product = self.get_instances_if_exists(
                Integrations_Shopify_Product,
                Integrations_Shopify_Product(product_id=p_id),
                "product_id"
            )

            if product:
                for variant in variants:
                    variant.product = product[0]
                    image_id = variant.image_id
                    variant.image_id = None
                    imgs = self.get_instances_if_exists(
                        Integrations_Shopify_Product_Image,
                        Integrations_Shopify_Product_Image(product_image_id=image_id),
                        "product_image_id"
                    )
                    if imgs:
                        variant.image = imgs[0]

                    self.update_or_save_instance(Integrations_Shopify_Product_Variant, variant, unique_attr="variant_id")

    def save_images(self):
        for p_id, images in self.images.items():
            product = self.get_instances_if_exists(
                Integrations_Shopify_Product,
                Integrations_Shopify_Product(product_id=p_id),
                "product_id"
            )
            if product:
                for image in images:
                    image.product = product[0]
                    self.update_or_save_instance(Integrations_Shopify_Product_Image, image, unique_attr=None)

    def grab_tags(self, product_id, tags):
        for tag in tags:
            if tag != "":
                self.tags[product_id] = Integrations_Shopify_Product_Tag(tag=tag)

    def grab_options(self, product_id, options):
        for option in options:
            p_opt = Integrations_Shopify_Product_Option(
                option_id = getattr(option, "id", None),
                name = getattr(option, "name", None),
                position = getattr(option, "position", None),
            )
            if product_id not in self.options:
                self.options[product_id] = [p_opt]
            else:
                self.options[product_id].append(p_opt)
            self.grab_option_values(p_opt.option_id, getattr(option, "values", []))



    def grab_option_values(self, option_id, values):
        for value in values:
            self.option_values[option_id] = Integrations_Shopify_Product_Option_Value(
                value=value
            )


    def grab_variants(self, product_id, variants, images):

        variant_images = {}
        for variant in variants:
            variant_id = getattr(variant, "id", None)
            for img in images:
                if variant_id in getattr(img, "variant_ids", []):
                    variant_images[variant_id] = getattr(img, "id", None)


        for variant in variants:
            variant_id = getattr(variant, "id", None)
            try:
                image_id = variant_images[variant_id]
            except KeyError as e:
                image_id = None
            p_variant = Integrations_Shopify_Product_Variant(
                variant_id = variant_id,
                barcode=getattr(variant, "barcode", None),
                compare_at_price=getattr(variant, "compare_at_price", None),
                created_at=getattr(variant, "created_at", None),
                fulfillment_service=getattr(variant, "barcode", None),
                grams=getattr(variant, "grams", None),
                inventory_item_id=getattr(variant, "inventory_item_id", None),
                inventory_management=getattr(variant, "inventory_management", None),
                inventory_policy=getattr(variant, "inventory_policy", None),
                inventory_quantity=getattr(variant, "inventory_quantity", None),
                option1=getattr(variant, "option1", None),
                option2=getattr(variant, "option2", None),
                option3=getattr(variant, "option3", None),
                position=getattr(variant, "position", None),
                price=getattr(variant, "price", None),
                sku=getattr(variant, "sku", None),
                taxable=getattr(variant, "taxable", None),
                tax_code=getattr(variant, "tax_code", None),
                title=getattr(variant, "title", None),
                updated_at=getattr(variant, "updated_at", None),
                weight=getattr(variant, "weight", None),
                weight_unit=getattr(variant, "weight_unit", None),
                image_id = image_id
            )



            if product_id not in self.variants:
                self.variants[product_id] = [p_variant]
            else:
                self.variants[product_id].append(p_variant)

    def grab_images(self, product_id, images):
        for img in images:
            image = Integrations_Shopify_Product_Image(
                product_image_id=getattr(img, "id", None),
                src=getattr(img, "src", None),
                width=getattr(img, "width", None),
                height=getattr(img, "height", None),
                position=getattr(img, "position", None),
                updated_at=getattr(img, "updated_at", None),
                created_at=getattr(img, "created_at", None)
                )
            if product_id not in self.images:
                self.images[product_id] = [image]
            else:
                self.images[product_id].append(image)
