from django.http import JsonResponse
from .models import Drink
from .serializers import DrinkSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET','POST'])
def drink_list(request, format=None):
		#get all drinks, serialise them, return json
		if request.method == 'GET':
			drinks=Drink.objects.all()
			serializers=DrinkSerializer(drinks, many=True)
			return JsonResponse(serializers.data, safe=False)
			#or use this return JsonResponse({'drinks':serializers.data}) ~ safe =False not needed as we send as dictionary values
		if request.method == 'POST':
			serializer=DrinkSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def drink_detail(request,id,format=None):
		try:
			drink=Drink.objects.get(pk=id)
		except Drink.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)	
		
		if request.method == 'GET':
			serializers=DrinkSerializer(drink)
			return  Response(serializers.data)
			
		elif request.method == 'PUT':
			serializer=DrinkSerializer(drink, data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		elif request.method == 'DELETE':
			drink.delete()
			return Response( status=status.HTTP_204_NO_CONTENT)