import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from .models import Unit, UnitImage, UnitTemplate, UnitType
from .serializers import UnitSerializer, UnitImageSerializer, UnitTemplateSerializer, UnitTypeSerializer

class UnitTemplateListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company = request.user.company
        templates = UnitTemplate.objects.filter(company=company)
        serializer = UnitTemplateSerializer(templates, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        company = request.user.company
        data = request.data.copy()
        data['company'] = company.id
        serializer = UnitTemplateSerializer(data=data)
        if serializer.is_valid():
            template = serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UnitTemplateDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        company = request.user.company
        try:
            template = UnitTemplate.objects.get(pk=pk, company=company)
        except UnitTemplate.DoesNotExist:
            return Response({"error": "UnitTemplate not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UnitTemplateSerializer(template)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        company = request.user.company
        try:
            template = UnitTemplate.objects.get(pk=pk, company=company)
        except UnitTemplate.DoesNotExist:
            return Response({"error": "UnitTemplate not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UnitTemplateSerializer(template, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = request.user.company
        try:
            template = UnitTemplate.objects.get(pk=pk, company=company)
        except UnitTemplate.DoesNotExist:
            return Response({"error": "UnitTemplate not found"}, status=status.HTTP_404_NOT_FOUND)
        
        template.delete()
        return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)

class UnitListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company = request.user.company
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )
        units = Unit.objects.filter(company=company)
        serializer = UnitSerializer(units, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        company = request.user.company
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data.copy()
        data['company'] = company.id

        serializer = UnitSerializer(data=data)
        if serializer.is_valid():
            unit = serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UnitDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        company = request.user.company
        unit = Unit.objects.get(pk=pk, company=company)
        serializer = UnitSerializer(unit)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        company = request.user.company
        unit = Unit.objects.get(pk=pk, company=company)
        serializer = UnitSerializer(unit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = request.user.company
        unit = Unit.objects.get(pk=pk, company=company)
        unit.delete()
        return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)


class UnitTemplateListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company = request.user.company
        templates = UnitTemplate.objects.filter(company=company)
        serializer = UnitTemplateSerializer(templates, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        company = request.user.company
        data = request.data.copy()
        data['company'] = company.id
        serializer = UnitTemplateSerializer(data=data)
        if serializer.is_valid():
            template = serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UnitTemplateDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        company = request.user.company
        template = UnitTemplate.objects.get(pk=pk, company=company)
        serializer = UnitTemplateSerializer(template)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        company = request.user.company
        template = UnitTemplate.objects.get(pk=pk, company=company)
        serializer = UnitTemplateSerializer(template, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = request.user.company
        template = UnitTemplate.objects.get(pk=pk, company=company)
        template.delete()
        return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)

class UnitTypeListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        unit_types = UnitType.objects.all()
        serializer = UnitTypeSerializer(unit_types, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UnitTypeSerializer(data=request.data)
        if serializer.is_valid():
            unit_type = serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class UnitTypeDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            unit_type = UnitType.objects.get(pk=pk)
        except UnitType.DoesNotExist:
            return Response({"error": "UnitType not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UnitTypeSerializer(unit_type)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            unit_type = UnitType.objects.get(pk=pk)
        except UnitType.DoesNotExist:
            return Response({"error": "UnitType not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UnitTypeSerializer(unit_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            unit_type = UnitType.objects.get(pk=pk)
        except UnitType.DoesNotExist:
            return Response({"error": "UnitType not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Archive the unit type instead of deleting it
        unit_type.is_archived = True
        unit_type.save()

        return Response({"success": True, "message": "Unit type archived successfully"}, status=status.HTTP_200_OK)
