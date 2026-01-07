from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):

        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status = status.HTTP_200_OK)
       
    def post(self, request):
        data = request.data

        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)

        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)
    
    # PUT: Reemplazo completo
    def put(self, request, item_id):
        item = next((x for x in data_list if x['id'] == item_id), None)
        if not item:
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        # Actualizamos todos los campos excepto el ID
        item['name'] = request.data.get('name')
        item['email'] = request.data.get('email')
        item['is_active'] = request.data.get('is_active')
        
        return Response({"message": "Usuario reemplazado con éxito", "data": item}, status=status.HTTP_200_OK)

    # PATCH: Actualización parcial
    def patch(self, request, item_id):
        item = next((x for x in data_list if x['id'] == item_id), None)
        if not item:
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        # Solo actualizamos lo que venga en la solicitud
        item['name'] = request.data.get('name', item['name'])
        item['email'] = request.data.get('email', item['email'])
        item['is_active'] = request.data.get('is_active', item['is_active'])
        
        return Response({"message": "Usuario actualizado parcialmente", "data": item}, status=status.HTTP_200_OK)

    # DELETE: Eliminación lógica
    def delete(self, request, item_id):
        item = next((x for x in data_list if x['id'] == item_id), None)
        if not item:
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        # Eliminación lógica: en lugar de remove(), cambiamos el estado
        item['is_active'] = False
        return Response({"message": f"Usuario {item_id} desactivado (eliminación lógica)"}, status=status.HTTP_200_OK)