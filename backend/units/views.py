import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from .models import Unit, UnitImage, UnitTemplate, UnitType
from sites.models import Floor
from .serializers import UnitSerializer, UnitImageSerializer, UnitTemplateSerializer, UnitTypeSerializer

def get_company(request):
    company = request.user.company
    if not company:
        raise ValueError("Company not found for this developer.")
    return company

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

class BulkAddUnitsView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            floor_ids = data.get("floor_ids", [])
            quantity = data.get("quantity", 1)
            unit_type_id = data.get("unit_type_id")

            if not floor_ids:
                return Response({"error": "No floors selected."}, status=status.HTTP_400_BAD_REQUEST)
            if not quantity:
                return Response({"error": "Quantity must be specified."}, status=status.HTTP_400_BAD_REQUEST)
            if not unit_type_id:
                return Response({"error": "Unit type must be specified."}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the company ID
            company = get_company(request)

            # Fetch the UnitType instance based on the unit_type_id
            try:
                unit_type = UnitType.objects.get(id=unit_type_id)
            except UnitType.DoesNotExist:
                return Response({"error": f"Invalid unit type ID: {unit_type_id}"}, status=status.HTTP_400_BAD_REQUEST)

            # Validate floors and create units
            for floor_id in floor_ids:
                try:
                    floor = Floor.objects.get(id=floor_id)
                except Floor.DoesNotExist:
                    return Response({"error": f"Invalid floor ID: {floor_id}"}, status=status.HTTP_400_BAD_REQUEST)

                for _ in range(quantity):
                    unit = Unit(
                        floor=floor,
                        site=floor.site,
                        unit_type=unit_type,
                        company=company,  # Ensure the company is passed to the unit
                        status="Available",  # Default status
                        unit_title=data.get("unit_title"),
                        bedroom=data.get("bedroom"),
                        bathroom=data.get("bathroom"),
                        lot_area=data.get("lot_area"),
                        floor_area=data.get("floor_area"),
                        price=data.get("price"),
                        view=data.get("view"),
                        balcony=data.get("balcony"),
                        commission=data.get("commission"),
                        spot_discount_percentage=data.get("spot_discount_percentage"),
                        spot_discount_flat=data.get("spot_discount_flat"),
                        reservation_fee=data.get("reservation_fee"),
                        other_charges=data.get("other_charges"),
                        vat_percentage=data.get("vat_percentage")
                    )
                    unit.save()

            return Response({"message": "Units successfully added."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)