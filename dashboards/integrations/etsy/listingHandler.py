from . import etsyAPI
from . import etsyHandler

from dashboards.models import Integrations_Etsy_Listing, Integrations_Etsy_Listing_Image_Variation, Integrations_Etsy_Listing_Product_Offering, \
                              Integrations_Etsy_Listing_Sku, Integrations_Etsy_Listing_Tag, Integrations_Etsy_Listing_Image, \
                              Integrations_Etsy_Listing_Product, Integrations_Etsy_Listing_Product_Property, Integrations_Etsy_Listing_Product_Property_Value, \
                              Integrations_Etsy_Listing_Product_Offering, Integrations_Etsy_Listing_Image_Variation, Integrations_Etsy_Shop, \
                              Integrations_Etsy_Listing_Material

from django.db import transaction


class ListingHandler(etsyHandler.EtsyHandler):

    def __init__(self, data, integration_id, user_iden, shop_id, request):
        self.listings = []
        self.images = []
        self.skus = {}
        self.tags = {}
        self.materials = {}
        self.variants = []
        self.offerings = []
        self.products = []
        self.props = []
        self.propValues = []
        self.shop_id = shop_id
        self.request = request
        super(ListingHandler, self).__init__(data, integration_id, user_iden, shop_id, "listing")

    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_listings()

    def _Handler__save_dependent_objects(self):
        def save_dep_1():
            with transaction.atomic():
                self.save_skus()
                self.save_tags()
                self.save_materials()
                self.save_images()
                self.save_products()
        def save_dep_2():
            with transaction.atomic():
                self.save_offerings()
                self.save_property()
        def save_dep_3():
            with transaction.atomic():
                self.save_property_values()
                self.save_variations()
        save_dep_1()
        save_dep_2()
        save_dep_3()

    def _Handler__parse_data(self):
        for obj in self.data:
            ls_id = obj.get("listing_id", None)
            listing = Integrations_Etsy_Listing(
                integration_id = self.integration_id,
                user_iden = self.user_iden,
                shop_id = self.shop_id,
                listing_id = ls_id,
                state = obj.get("state", None),
                user_id = obj.get("user_id", None),
                category_id = obj.get("category_id", None),
                title = obj.get("title", None),
                description = obj.get("description", None),
                creation_tsz = etsyAPI.unix2UTC(obj.get("creation_tsz", None)),
                ending_tsz = etsyAPI.unix2UTC(obj.get("ending_tsz", None)),
                original_creation_tsz = etsyAPI.unix2UTC(obj.get("original_creation_tsz", None)),
                last_modified_tsz = etsyAPI.unix2UTC(obj.get("last_modified_tsz", None)),
                price = obj.get("price", None),
                currency_code = obj.get("currency_code", None),
                quantity = obj.get("quantity", None),
                taxonomy_path = obj.get("taxonomy_path", None),
                taxonomy_id = obj.get("taxonomy_id", None),
                suggested_taxonomy_id = obj.get("suggested_taxonomy_id", None),
                shop_section_id = obj.get("shop_section_id", None),
                featured_rank = obj.get("featured_rank", None),
                state_tsz = etsyAPI.unix2UTC(obj.get("state_tsz", None)),
                views = obj.get("views", None),
                num_favorers = obj.get("num_favorers", None),
                shipping_template_id = obj.get("shipping_template_id", None),
                processing_min = obj.get("processing_min", None),
                processing_max = obj.get("processing_max", None),
                who_made = obj.get("who_made", None),
                is_supply = etsyAPI.etsyBool(obj.get("is_supply", None)),
                when_made = obj.get("when_made", None),
                item_weight = obj.get("item_weight", None),
                item_weight_unit = obj.get("item_weight_unit", None),
                item_length = obj.get("item_length", None),
                item_width = obj.get("item_width", None),
                item_height = obj.get("item_height", None),
                item_dimensions_unit = obj.get("item_dimensions_unit", None),
                is_private = etsyAPI.etsyBool(obj.get("is_private", None)),
                recipient = obj.get("recipient", None),
                occasion = obj.get("occasion", None),
                style = obj.get("style", None),
                non_taxable = etsyAPI.etsyBool(obj.get("non_taxable", None)),
                is_customizable = etsyAPI.etsyBool(obj.get("is_customizable", None)),
                is_digital = etsyAPI.etsyBool(obj.get("is_digital", None)),
                file_data = obj.get("file_data", None),
                can_write_inventory = etsyAPI.etsyBool(obj.get("can_write_inventory", None)),
                has_variations = etsyAPI.etsyBool(obj.get("has_variations", None)),
                should_auto_renew = etsyAPI.etsyBool(obj.get("should_auto_renew", None)),
                language = obj.get("language", None)
            )
            
            self.listings.append(listing)

            skus = obj.get("sku", None)
            tags = obj.get("tags", None)
            mats = obj.get("materials", None)

            self.grab_skus(listing.listing_id, skus)
            self.grab_tags(listing.listing_id, tags)
            self.grab_materials(listing.listing_id, mats)

            images = etsyAPI.getListingImage(self.request, ls_id)
            products = etsyAPI.getListingProducts(self.request, ls_id)
            variations = etsyAPI.getListingImageVariants(self.request, ls_id)
            
            self.grab_images(images)
            self.grab_products(products, ls_id)
            self.grab_variations(variations, ls_id)

    def save_listings(self):
        for listing_ins in self.listings:
            shop = self.get_instances_if_exists(
                Integrations_Etsy_Shop,
                Integrations_Etsy_Shop(shop_id=listing_ins.shop_id),
                "shop_id"
            )
            listing_ins.shop_ref = None if not shop else shop[0]
            self.update_or_save_instance(Integrations_Etsy_Listing, listing_ins, unique_attr="listing_id")    

    def grab_skus(self, listing_id, skus):
        self.skus[listing_id] = []
        for sku in skus:
            self.skus[listing_id].append(Integrations_Etsy_Listing_Sku(sku=sku))

    def grab_tags(self, listing_id, tags):
        self.tags[listing_id] = []
        for tag in tags:
            self.tags[listing_id].append(Integrations_Etsy_Listing_Tag(tag=tag))

    def grab_materials(self, listing_id, materials):
        self.materials[listing_id] = []
        for material in materials:
            self.materials[listing_id].append(Integrations_Etsy_Listing_Material(material=material))

    def grab_images(self, images):
        for obj in images:
                image = Integrations_Etsy_Listing_Image(
                    listing_image_id = obj.get("listing_image_id", None),
                    listing_id = obj.get("listing_id", None),
                    hex_code = obj.get("hex_code", None),
                    red = obj.get("red", None),
                    green = obj.get("green", None),
                    blue = obj.get("blue", None),
                    hue = obj.get("hue", None),
                    saturation = obj.get("saturation", None),
                    brightness = obj.get("brightness", None),
                    is_black_and_white = etsyAPI.etsyBool(obj.get("is_black_and_white", None)),
                    creation_tsz = etsyAPI.unix2UTC(obj.get("creation_tsz", None)),
                    rank = obj.get("rank", None),
                    url_75x75 = obj.get("url_75x75", None),
                    url_170x135 = obj.get("url_170x135", None),
                    url_570xN = obj.get("url_570xN", None),
                    url_fullxfull = obj.get("url_fullxfull", None),
                    full_height = obj.get("full_height", None),
                    full_width = obj.get("full_width", None)
                )
                self.images.append(image)

    def grab_products(self, products, listing_id):
        for obj in products:
            product = Integrations_Etsy_Listing_Product(
                product_id  = obj.get("product_id", None),
                is_deleted = obj.get("is_deleted", None), 
                sku = obj.get("sku", None),
                listing_id = listing_id
            )
            self.products.append(product)
            
            offerings = obj.get("offerings", None)
            props = obj.get("property_values", None)
            
            self.grab_offerings(offerings, product.product_id)
            self.grab_property(props, product.product_id)

    def grab_offerings(self, offerings, product_id):
        for obj in offerings:
            offering = Integrations_Etsy_Listing_Product_Offering(
                offering_id = obj.get("offering_id", None),
                product_id  = product_id,
                price = obj.get("price", None).get("currency_formatted_long", None),
                quantity = obj.get("quantity", None),
                is_enabled = obj.get("is_deleted", None),
                is_deleted = obj.get("is_deleted", None)
            )
            self.offerings.append(offering)
    
    def grab_property(self, props, product_id):
        for obj in props:
            prop = Integrations_Etsy_Listing_Product_Property(
                property_id = obj.get("property_id", None),
                product_id  = product_id,
                property_name = obj.get("property_name", None),
                scale_id = obj.get("scale_id", None),
                scale_name = obj.get("scale_name", None)
            )
            self.props.append(prop)

            values = obj.get("values", None)
            ids = obj.get("value_ids", None)

            self.grab_property_values(values, ids, product_id, prop.property_id)

    def grab_property_values(self, values, ids, product_id, property_id):      
        i = 0
        for value in values:
            propValue = Integrations_Etsy_Listing_Product_Property_Value(
                property_id  = property_id,
                product_id = product_id,
                value_id = ids[i],
                value_name = value
            )
            i+=1
            self.propValues.append(propValue)

    def grab_variations(self, vars, listing_id):
        for obj in vars:
            var = Integrations_Etsy_Listing_Image_Variation(
                listing_id = listing_id,
                property_id = obj.get("property_id", None),
                image_id = obj.get("image_id", None),
                value_id = obj.get("value_id", None)
            )

            self.variants.append(var)

    def save_skus(self):
        for l_id, skus in self.skus.items():
            listing = self.get_instances_if_exists(
                Integrations_Etsy_Listing,
                Integrations_Etsy_Listing(listing_id=l_id),
                "listing_id"
            )
            for sku in skus:
                sku.listing_ref = None if not listing else listing[0]
                self.update_or_save_instance(Integrations_Etsy_Listing_Sku, sku, unique_attr=None)

    def save_tags(self):
        for l_id, tags in self.tags.items():
            listing = self.get_instances_if_exists(
                Integrations_Etsy_Listing,
                Integrations_Etsy_Listing(listing_id=l_id),
                "listing_id"
            )
            for tag in tags:
                tag.listing_ref = None if not listing else listing[0]
                self.update_or_save_instance(Integrations_Etsy_Listing_Tag, tag, unique_attr=None)

    def save_materials(self):
        for l_id, materials in self.materials.items():
            listing = self.get_instances_if_exists(
                Integrations_Etsy_Listing,
                Integrations_Etsy_Listing(listing_id=l_id),
                "listing_id"
            )
            for material in materials:
                material.listing_ref = None if not listing else listing[0]
                self.update_or_save_instance(Integrations_Etsy_Listing_Material, material, unique_attr=None)

    def save_images(self):
        for image in self.images:
            listing = self.get_instances_if_exists(
                Integrations_Etsy_Listing,
                Integrations_Etsy_Listing(listing_id=image.listing_id),
                "listing_id"
            )
            image.listing_ref = None if not listing else listing[0]
            self.update_or_save_instance(Integrations_Etsy_Listing_Image, image, unique_attr="listing_image_id")    

    def save_products(self):
        for product in self.products:
            listing = self.get_instances_if_exists(
                Integrations_Etsy_Listing,
                Integrations_Etsy_Listing(listing_id=product.listing_id),
                "listing_id"
            )
            product.listing_ref = None if not listing else listing[0]
            self.update_or_save_instance(Integrations_Etsy_Listing_Product, product, unique_attr="product_id")    

    def save_offerings(self):
        for offering in self.offerings:
            product = self.get_instances_if_exists(
                Integrations_Etsy_Listing_Product,
                Integrations_Etsy_Listing_Product(product_id=offering.product_id),
                "product_id"
            )
            offering.product_ref = None if not product else product[0]
            self.update_or_save_instance(Integrations_Etsy_Listing_Product_Offering, offering, unique_attr="offering_id") 

    def save_property(self):
        for prop in self.props:
            product = self.get_instances_if_exists(
                Integrations_Etsy_Listing_Product,
                Integrations_Etsy_Listing_Product(product_id=prop.product_id),
                "product_id"
            )
            prop.product_ref = None if not product else product[0]
            self.update_or_save_instance(Integrations_Etsy_Listing_Product_Property, prop, unique_attr="product_id") 

    def save_property_values(self):
        for value in self.propValues:
            prop = self.get_instances_if_exists(
                Integrations_Etsy_Listing_Product_Property,
                Integrations_Etsy_Listing_Product_Property(product_id=value.product_id, property_id=value.property_id),
                ["product_id", "property_id"]
            )
            value.property_ref = None if not prop else prop[0]
            self.update_or_save_instance(Integrations_Etsy_Listing_Product_Property_Value, value, unique_attr=["product_id", "property_id"]) 

    def save_variations(self):
        for var in self.variants:
            listing = self.get_instances_if_exists(
                Integrations_Etsy_Listing,
                Integrations_Etsy_Listing(listing_id=var.listing_id),
                "listing_id"
            )
            image = self.get_instances_if_exists(
                Integrations_Etsy_Listing_Image,
                Integrations_Etsy_Listing_Image(listing_image_id=var.image_id),
                "listing_image_id"
            )
            var.listing_ref = None if not listing else listing[0]
            var.image_ref = None if not image else image[0]
            self.update_or_save_instance(Integrations_Etsy_Listing_Image_Variation, var, unique_attr=["listing_id", "image_id"])
