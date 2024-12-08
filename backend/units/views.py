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
from decimal import Decimal
import traceback

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

        # Get filters from query parameters
        unit_number = request.query_params.get('unitNumber', None)
        unit_type = request.query_params.get('unitType', None)
        site_id = request.query_params.get('siteId', None)
        floor_id = request.query_params.get('floorId', None)

        # Apply filters if provided
        units = Unit.objects.filter(company=company)

        if unit_number:
            units = units.filter(unit_number__icontains=unit_number)
        if unit_type:
            units = units.filter(unit_type__id=unit_type)  # Assuming unit_type is an ID
        if site_id:
            units = units.filter(floor__site__id=site_id)
        if floor_id:
            units = units.filter(floor__id=floor_id)  # Filter by floor's ID

        # Serialize the data
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Debugging the incoming request data
            data = request.data

            # Convert numerical fields to appropriate types
            quantity = int(data.get("quantity", 1))  # Ensure quantity is an integer
            unit_type_id = data.get("unit_type_id")
            floor_ids = data.getlist("floor_ids[]", [])

            # Log the values for debugging
            print(f"Floor IDs: {floor_ids}")
            print(f"Quantity: {quantity}")
            print(f"Unit Type ID: {unit_type_id}")

            if not floor_ids:
                return Response({"error": "No floors selected."}, status=status.HTTP_400_BAD_REQUEST)
            if not quantity:
                return Response({"error": "Quantity must be specified."}, status=status.HTTP_400_BAD_REQUEST)
            if not unit_type_id:
                return Response({"error": "Unit type must be specified."}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the company ID
            company = get_company(request)
            print(f"Company ID: {company}")  # Debug company ID

            # Fetch the UnitType instance based on the unit_type_id
            try:
                unit_type = UnitType.objects.get(id=unit_type_id)
                print(f"Found Unit Type: {unit_type.name}")  # Log unit type found
            except UnitType.DoesNotExist:
                return Response({"error": f"Invalid unit type ID: {unit_type_id}"}, status=status.HTTP_400_BAD_REQUEST)

            # Validate floors and create units
            created_units = []
            for floor_id in floor_ids:
                try:
                    # Attempt to fetch the floor based on the ID
                    floor = Floor.objects.get(id=floor_id)
                    print(f"Found floor: {floor.floor_number} (ID: {floor.id})")  # Log the floor number
                except Floor.DoesNotExist:
                    print(f"Floor with ID {floor_id} not found")
                    return Response({"error": f"Invalid floor ID: {floor_id}"}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    print(f"Error fetching floor with ID {floor_id}: {str(e)}")
                    return Response({"error": f"Error fetching floor: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Ensure numerical fields are correctly converted
                print(f"Creating {quantity} units for floor: {floor.id}")
                quantity = int(data.get("quantity", 1))
                bedroom = int(data.get("bedroom", 1))  # Default to 0 if not provided
                bathroom = int(data.get("bathroom", 1))  # Default to 0 if not provided
                lot_area = Decimal(data.get("lot_area", 5))  # Convert to float, default to 0 if not provided
                floor_area = Decimal(data.get("floor_area", 5))  # Convert to float, default to 0 if not provided
                price = Decimal(data.get("price", 5))  # Convert to float, default to 0 if not provided
                view = data.get("view")
                balcony = data.get("balcony")

                for i in range(quantity):
                    print(f"Creating unit number {i + 1} of {quantity}")  # Debugging the loop
                    unit = Unit(
                        floor=floor,
                        site=floor.site,
                        unit_type=unit_type,
                        company=company,
                        status="Available",
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
                    print(f"Creating unit with the following data: {unit.__dict__}")
                    try:
                        unit.save()
                        print(f"Unit {unit.id} created successfully.")
                    except Exception as e:
                        print(f"Error saving unit: {str(e)}")  # Log the error
                        print("Full traceback:")
                        print(traceback.format_exc())  # Capture full error traceback and log it
                        return Response({"error": f"Error saving unit: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    created_units.append(unit)

                    # Handle images if provided
                    if "images" in request.FILES:
                        images = request.FILES.getlist("images")
                        print(f"Images received for unit: {len(images)} image(s)")
                        for image in images:
                            try:
                                UnitImage.objects.create(
                                    unit=unit,
                                    image=image,
                                    image_type="Unit"
                                )
                                print(f"Image {image.name} saved for unit {unit.id}")
                            except ValidationError as e:
                                return Response({"error": f"Image validation error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            # After all units are created, return the response
            return Response({"message": f"{len(created_units)} units successfully added."}, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            print("Full traceback:")
            print(traceback.format_exc())  # Log full traceback in case of unexpected error
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UnitsByFloorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, site_id, floor_id):
        # Get the company from the authenticated user
        company = request.user.company
        if not company:
            return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the floor object, ensuring the company matches the site's company
        floor = get_object_or_404(Floor, id=floor_id, site_id=site_id, site__company=company)

        # Get all units for this floor
        units = Unit.objects.filter(floor=floor)

        # Serialize the unit data
        serializer = UnitSerializer(units, many=True)

        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
