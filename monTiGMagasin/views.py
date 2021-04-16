from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from monTiGMagasin.config import baseUrl
from monTiGMagasin.models import InfoProduct
from monTiGMagasin.serializers import InfoProductSerializer

# Create your views here.
class InfoProductList(APIView):
    def get(self, request, format=None):
        products = InfoProduct.objects.all()
        serializer = InfoProductSerializer(products, many=True)
        return Response(serializer.data)
        
class InfoProductDetail(APIView):
    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404
    def get(self, request, tig_id, format=None):
        product = self.get_object(tig_id=tig_id)
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)
        
class ProductIncrementStock(APIView):
    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, tig_id, number, format=None):
        productBefore = InfoProduct.objects.get(tig_id=tig_id)
        productBefore.quantityInStock = productBefore.quantityInStock + number
        productBefore.save()
        
        product = self.get_object(tig_id=tig_id)
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)
        
class ProductDecrementStock(APIView):
    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, tig_id, number, format=None):
        productBefore = InfoProduct.objects.get(tig_id=tig_id)
        if productBefore.quantityInStock - number >= 0 :
            productBefore.quantityInStock = productBefore.quantityInStock - number
            productBefore.save()
        
        product = self.get_object(tig_id=tig_id)
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)


class ProductModifyDiscount(APIView):
    def get_object(self, tig_id):
        try:
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, tig_id, number, format=None):
        productBefore = InfoProduct.objects.get(tig_id=tig_id)
        if number == 0:
            productBefore.sale = False
            productBefore.discount = 0
        else :
            if number <= 100:
                if productBefore.sale == False:
                    productBefore.sale = True
                productBefore.discount = number
        productBefore.save()

        product = self.get_object(tig_id=tig_id)
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)


class IncrementMultiple(APIView):
    def get_object(self, tig_id):
        try:
            tig_id = self.request.query_params.getlist('id', '')
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        ids = self.request.query_params.getlist('id', '')
        numbers = self.request.query_params.getlist('number', '')
        for i in range(len(ids)):
            productBefore = InfoProduct.objects.get(tig_id=ids[i])
            productBefore.quantityInStock = productBefore.quantityInStock + int(numbers[i])
            productBefore.save()

        products = InfoProduct.objects.all()
        serializer = InfoProductSerializer(products, many=True)
        return Response(serializer.data)

class DecrementMultiple(APIView):
    def get_object(self, tig_id):
        try:
            tig_id = self.request.query_params.getlist('id', '')
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        ids = self.request.query_params.getlist('id', '')
        numbers = self.request.query_params.getlist('number', '')
        for i in range(len(ids)):
            productBefore = InfoProduct.objects.get(tig_id=ids[i])
            if productBefore.quantityInStock - int(numbers[i]) >= 0 :
                productBefore.quantityInStock = productBefore.quantityInStock - int(numbers[i])
                productBefore.save()

        products = InfoProduct.objects.all()
        serializer = InfoProductSerializer(products, many=True)
        return Response(serializer.data)


class ModifyDiscountMultiple(APIView):
    def get_object(self, tig_id):
        try:
            tig_id = self.request.query_params.getlist('id', '')
            return InfoProduct.objects.get(tig_id=tig_id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        ids = self.request.query_params.getlist('id', '')
        numbers = self.request.query_params.getlist('number', '')
        for i in range(len(ids)):
            productBefore = InfoProduct.objects.get(tig_id=ids[i])
            if int(numbers[i]) == 0:
                productBefore.sale = False
                productBefore.discount = 0
            else:
                if int(numbers[i]) <= 100:
                    if productBefore.sale == False:
                        productBefore.sale = True
                    productBefore.discount = int(numbers[i])
            productBefore.save()

        products = InfoProduct.objects.all()
        serializer = InfoProductSerializer(products, many=True)
        return Response(serializer.data)
