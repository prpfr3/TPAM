from decimal import Decimal
from django.conf import settings
from locos.models import Slide

class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the slides
        from the database.
        """
        slide_ids = self.cart.keys()
        # get the slide objects and add them to the cart
        slides = Slide.objects.filter(id__in=slide_ids)

        cart = self.cart.copy()
        for slide in slides:
            cart[str(slide.id)]['slide'] = slide

        for item in cart.values():
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['slide_order'] for item in self.cart.values())

    def add(self, slide, slide_order=1):
        """
        Add a slide to the cart or update its slide_order.
        Set the slide_id to a string as JSON is used for serialization of data in sessions
        """
        slide_id = str(slide.id)
        if slide_id not in self.cart:
            self.cart[slide_id] = {'slide_order': 0,}

        self.cart[slide_id]['slide_order'] = slide_order
        print(self.cart[slide_id]['slide_order'])
        for k, v in self.cart.items():
            print(k,v)
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, slide):
        """
        Remove a slide from the cart.
        """
        slide_id = str(slide.id)
        if slide_id in self.cart:
            del self.cart[slide_id]
            self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()