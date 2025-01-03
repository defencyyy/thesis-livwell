import logging
import traceback
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import Unit, UnitImage, UnitTemplate, UnitType
from sites.models import Section
from .serializers import UnitSerializer, UnitImageSerializer, UnitTemplateSerializer, UnitTypeSerializer
logger = logging.getLogger(__name__)

# Utility to retrieve the company associated with the request user
def get_company(request):
    company = request.user.company
    if not company:
        raise ValueError("Company not found for this developer.")
    return company

class UnitTemplateListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company = get_company(request)
        templates = UnitTemplate.objects.filter(company=company)
        serializer = UnitTemplateSerializer(templates, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            company = get_company(request)
            # Process non-file data
            data = {key: value for key, value in request.data.items() if key != 'images'}
            data['company'] = company.id  # Add company ID to the form data

            # Validate that required fields are present
            if not data.get('unit_type'):
                return Response({"error": "Unit type must be specified."}, status=status.HTTP_400_BAD_REQUEST)
            if not data.get('name'):
                return Response({"error": "Name must be specified."}, status=status.HTTP_400_BAD_REQUEST)

            # Serialize form data
            serializer = UnitTemplateSerializer(data=data)

            if serializer.is_valid():
                template = serializer.save()

                # Handle images if present
                self._handle_images(request, template)

                return Response({"success": True, "data": UnitTemplateSerializer(template).data}, status=status.HTTP_201_CREATED)

            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error creating template: {str(e)}\n{traceback.format_exc()}")
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _handle_images(self, request, template):
        # Get the list of images from the request
        images = request.FILES.getlist("images")  # Use getlist() to receive an array of images
        
        if images:
            image_types = request.data.getlist("image_types", [])
            primaries = request.data.getlist("primaries", [])
            
            for i, image in enumerate(images):
                try:
                    image_type = image_types[i] if i < len(image_types) else 'unit'
                    primary = primaries[i] if i < len(primaries) else False

                    # Ensure that the value is a boolean
                    primary = True if str(primary).lower() == "true" else False

                    # Then create the image
                    unit_image = UnitImage.objects.create(
                        unit_template=template,
                        image=image,
                        image_type=image_type,
                        primary=primary  # Now it will always be a boolean
                    )

                    logger.info(f"Image successfully added: {unit_image}")

                except Exception as e:
                    logger.error(f"Error saving image: {e}\n{traceback.format_exc()}")
                    return Response({"error": f"Error saving image: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UnitTemplateDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        company = get_company(request)
        print(f"Company: {company}")
        print(f"Template ID: {pk}")
        template = UnitTemplate.objects.filter(pk=pk, company=company).first()
        
        if not template:
            print("Template not found")
            return Response({"error": "UnitTemplate not found"}, status=status.HTTP_404_NOT_FOUND)
        
        print("Template found:", template)
        serializer = UnitTemplateSerializer(template)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        company = get_company(request)
        template = UnitTemplate.objects.filter(pk=pk, company=company).first()
        if not template:
            return Response({"error": "UnitTemplate not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UnitTemplateSerializer(template, data=request.data, partial=True)
        if serializer.is_valid():
            template = serializer.save()
            images_data = request.FILES.getlist('images')
            if images_data:
                template.images.all().delete()
                for image in images_data:
                    UnitImage.objects.create(unit_template=template, image=image)
            
            return Response({"success": True, "data": UnitTemplateSerializer(template).data}, status=status.HTTP_200_OK)

        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = get_company(request)
        template = UnitTemplate.objects.filter(pk=pk, company=company).first()
        if not template:
            return Response({"error": "UnitTemplate not found"}, status=status.HTTP_404_NOT_FOUND)

        template.is_archived = True
        template.save()
        return Response({"success": True, "message": "Template archived successfully."}, status=status.HTTP_200_OK)


class UnitListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company = get_company(request)

        unit_number = request.query_params.get('unitNumber', None)
        unit_type = request.query_params.get('unitType', None)
        site_id = request.query_params.get('siteId', None)
        section_id = request.query_params.get('sectionId', None)
        status_param = request.query_params.get('status', None)

        # Using Q object to build query dynamically
        query = Q(company=company)
        if unit_number:
            query &= Q(unit_number__icontains=unit_number)
        if unit_type:
            query &= Q(unit_type__id=unit_type)
        if site_id:
            query &= Q(section__site__id=site_id)
        if section_id:
            query &= Q(section__id=section_id)
        if status_param:
            query &= Q(status=status_param)

        # Execute the query
        units = Unit.objects.filter(query)

        serializer = UnitSerializer(units, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        company = get_company(request)
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
        company = get_company(request)
        unit = Unit.objects.filter(pk=pk, company=company).first()
        if not unit:
            return Response({"success": False, "message": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if unit.unit_template:
            # Fetch images from the unit template
            unit_images = unit.unit_template.images.all()
        else:
            # Fetch images from the unit itself
            unit_images = unit.get_unit_images_model()

        unit_serializer = UnitSerializer(unit)
        unit_images_serializer = UnitImageSerializer(unit_images, many=True)

        return Response(
            {"success": True, "data": unit_serializer.data, "images": unit_images_serializer.data},
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        company = get_company(request)
        unit = Unit.objects.filter(pk=pk, company=company).first()
        if not unit:
            return Response({"success": False, "message": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        unit.unit_title = data.get("unit_title", unit.unit_title)
        unit.unit_type = data.get("unit_type", unit.unit_type)
        unit.status = data.get("status", unit.status)
        unit.price = data.get("price", unit.price)
        unit.lot_area = data.get("lot_area", unit.lot_area)
        unit.floor_area = data.get("floor_area", unit.floor_area)
        unit.commission = data.get("commission", unit.commission)
        unit.balcony = data.get("balcony", unit.balcony)
        unit.view = data.get("view", unit.view)

        section_ids = data.getlist("section_ids[]", [])
        if section_ids:
            unit.sections.clear()
            for section_id in section_ids:
                try:
                    section = Section.objects.get(id=section_id)  # Updated to Section
                    unit.sections.add(section)
                except Section.DoesNotExist:
                    return Response({"error": f"Invalid section ID: {section_id}"}, status=status.HTTP_400_BAD_REQUEST)

        image_files = request.FILES.getlist("images[]")
        if image_files:
            for image in image_files:
                try:
                    unit_image = UnitImage.objects.create(
                        unit=unit,
                        image=image,
                        image_type="Unit",
                        primary=False, 
                    )
                except Exception as e:
                    return Response({"error": f"Error updating image: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        unit.save()
        return Response({"success": True, "data": UnitSerializer(unit).data}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        company = get_company(request)
        unit = Unit.objects.filter(pk=pk, company=company).first()
        if not unit:
            return Response({"success": False, "message": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)

        unit.delete()
        return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)

class UnitTypeListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company = get_company(request)  # Reuse the company logic
        # Get all unit types where is_custom is False (default types)
        unit_types = UnitType.objects.filter(is_custom=False)
        
        # Include company-specific custom unit types if the user belongs to a company
        if company:
            unit_types = unit_types | UnitType.objects.filter(company=company, is_custom=True)
        
        serializer = UnitTypeSerializer(unit_types.distinct(), many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        
    def post(self, request):
        company = get_company(request)  # Reuse the company logic
        data = request.data.copy()
        data['company'] = company.id  # Ensure the company is associated when creating the unit type
        
        serializer = UnitTypeSerializer(data=data)
        if serializer.is_valid():
            unit_type = serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UnitTypeDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        company = get_company(request)  # Reuse the company logic
        unit_type = UnitType.objects.filter(pk=pk, company=company).first()  # Filter by company
        if not unit_type:
            return Response({"error": "UnitType not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UnitTypeSerializer(unit_type)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        company = get_company(request)  # Reuse the company logic
        unit_type = UnitType.objects.filter(pk=pk, company=company).first()  # Filter by company
        if not unit_type:
            return Response({"error": "UnitType not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UnitTypeSerializer(unit_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = get_company(request)  # Reuse the company logic
        unit_type = UnitType.objects.filter(pk=pk, company=company).first()  # Filter by company
        if not unit_type:
            return Response({"error": "UnitType not found"}, status=status.HTTP_404_NOT_FOUND)

        unit_type.delete()
        return Response({"success": True, "message": "UnitType deleted successfully"}, status=status.HTTP_200_OK)

class BulkAddUnitsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            quantity = int(data.get("quantity", 1))
            unit_type_id = data.get("unit_type_id")
            section_ids = data.getlist("section_ids[]", [])
            unit_template_id = data.get("unit_template_id")  # Retrieve unit_template_id from request data

            # Validate required fields
            if not section_ids:
                return Response({"error": "No sections selected."}, status=status.HTTP_400_BAD_REQUEST)
            if not quantity:
                return Response({"error": "Quantity must be specified."}, status=status.HTTP_400_BAD_REQUEST)
            if not unit_type_id:
                return Response({"error": "Unit type must be specified."}, status=status.HTTP_400_BAD_REQUEST)

            company = get_company(request)

            # Fetch UnitType
            try:
                unit_type = UnitType.objects.get(id=unit_type_id)
            except UnitType.DoesNotExist:
                return Response({"error": f"Invalid unit type ID: {unit_type_id}"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Fetch UnitTemplate (if unit_template_id is provided)
            unit_template = None
            if unit_template_id:
                try:
                    unit_template = UnitTemplate.objects.get(id=unit_template_id)
                except UnitTemplate.DoesNotExist:
                    return Response({"error": f"Invalid unit template ID: {unit_template_id}"}, status=status.HTTP_400_BAD_REQUEST)

            created_units = []
            for section_id in section_ids:
                try:
                    section = Section.objects.get(id=section_id)
                except Section.DoesNotExist:
                    return Response({"error": f"Invalid section ID: {section_id}"}, status=status.HTTP_400_BAD_REQUEST)

                # Get unit fields, default to values if not provided
                unit_fields = {
                    'bedroom': int(data.get("bedroom", 1)),
                    'bathroom': int(data.get("bathroom", 1)),
                    'lot_area': Decimal(data.get("lot_area", 5)),
                    'floor_area': Decimal(data.get("floor_area", 5)),
                    'price': Decimal(data.get("price", 5)),
                    'view': data.get("view"),
                    'balcony': data.get("balcony"),
                    'unit_title': data.get("unit_title"),
                    'commission': data.get("commission"),
                    'spot_discount_percentage': data.get("spot_discount_percentage"),
                    'spot_discount_flat': data.get("spot_discount_flat"),
                    'reservation_fee': data.get("reservation_fee"),
                    'other_charges': data.get("other_charges"),
                    'vat_percentage': data.get("vat_percentage"),
                }

                for i in range(quantity):
                    unit = Unit(
                        section=section,
                        site=section.site,
                        unit_type=unit_type,
                        company=company,
                        status="Available",
                        unit_template=unit_template, 
                        **unit_fields
                    )
                    unit.save()
                    created_units.append(unit)

                    # Handle images if present
                    self._handle_images(request, unit)

            return Response({"message": f"{len(created_units)} units successfully added."}, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            print("Full traceback:", traceback.format_exc())
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _handle_images(self, request, unit):
        images = [image for key, image in request.FILES.items() if key.startswith("images")]
        if images:
            image_types = request.data.getlist("image_types")
            primaries = request.data.getlist("primaries")
            unit_template_id = request.data.get("unit_template")

            unit_template = None
            if unit_template_id:
                try:
                    unit_template = UnitTemplate.objects.get(id=unit_template_id)
                except UnitTemplate.DoesNotExist:
                    logger.error(f"Invalid unit template ID: {unit_template_id}")
                    return Response({"error": f"Invalid unit template ID: {unit_template_id}"}, status=status.HTTP_400_BAD_REQUEST)

            for i, image in enumerate(images):
                try:
                    image_type = image_types[i] if i < len(image_types) else 'unit'
                    primary = primaries[i] if i < len(primaries) else False

                    unit_image = UnitImage.objects.create(
                        unit=unit,
                        unit_template=unit_template,
                        image=image,
                        image_type=image_type,
                        primary=primary
                    )
                    logger.info(f"Image successfully added: {unit_image}")
                except Exception as e:
                    logger.error(f"Error saving image: {e}")
                    return Response({"error": f"Error saving image: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, unit_id):
        try:
            unit = Unit.objects.get(id=unit_id)
            image_file = request.FILES.get('image')
            if not image_file:
                return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

            image = UnitImage(unit=unit, image=image_file, image_type='unit')
            image.save()

            image_serializer = UnitImageSerializer(image)
            return Response(image_serializer.data, status=status.HTTP_201_CREATED)

        except Unit.DoesNotExist:
            return Response({'error': 'Unit not found'}, status=status.HTTP_404_NOT_FOUND)

class ImageManagementView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, unit_id, image_id):
        try:
            unit = Unit.objects.get(id=unit_id)
            image = UnitImage.objects.get(id=image_id, unit=unit)
        except Unit.DoesNotExist:
            return Response({"detail": "Unit not found."}, status=404)
        except UnitImage.DoesNotExist:
            return Response({"detail": "Image not found."}, status=404)

        image_file = request.FILES.get('image')
        if image_file:
            image.image = image_file
            image.save()
            return Response(UnitImageSerializer(image).data, status=200)
        
        return Response({"detail": "No image provided."}, status=400)

    def delete(self, request, unit_id, image_id):
        try:
            unit = Unit.objects.get(id=unit_id)
            image = UnitImage.objects.get(id=image_id, unit=unit)
        except Unit.DoesNotExist:
            return Response({"detail": "Unit not found."}, status=404)
        except UnitImage.DoesNotExist:
            return Response({"detail": "Image not found."}, status=404)

        # Optionally delete the image file from the filesystem
        if image.image:
            image.image.delete()

        image.delete()
        return Response({"detail": "Image deleted successfully."}, status=200)

class TemplateImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, template_id):
        try:
            unit_template = UnitTemplate.objects.get(id=template_id)
            image_file = request.FILES.get('image')
            if not image_file:
                return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

            image = UnitImage(unit_template=unit_template, image=image_file, image_type='template')
            image.save()

            image_serializer = UnitImageSerializer(image)
            return Response(image_serializer.data, status=status.HTTP_201_CREATED)

        except UnitTemplate.DoesNotExist:
            return Response({'error': 'Unit Template not found'}, status=status.HTTP_404_NOT_FOUND)

class TemplateImageManagementView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, template_id, image_id):
        try:
            unit_template = UnitTemplate.objects.get(id=template_id)
            image = UnitImage.objects.get(id=image_id, unit_template=unit_template)
        except UnitTemplate.DoesNotExist:
            return Response({"detail": "Unit Template not found."}, status=404)
        except UnitImage.DoesNotExist:
            return Response({"detail": "Image not found."}, status=404)

        image_file = request.FILES.get('image')
        if image_file:
            image.image = image_file
            image.save()
            return Response(UnitImageSerializer(image).data, status=200)
        
        return Response({"detail": "No image provided."}, status=400)

    def delete(self, request, template_id, image_id):
        try:
            unit_template = UnitTemplate.objects.get(id=template_id)
            image = UnitImage.objects.get(id=image_id, unit_template=unit_template)
        except UnitTemplate.DoesNotExist:
            return Response({"detail": "Unit Template not found."}, status=404)
        except UnitImage.DoesNotExist:
            return Response({"detail": "Image not found."}, status=404)

        # Optionally delete the image file from the filesystem
        if image.image:
            image.image.delete()

        image.delete()
        return Response({"detail": "Image deleted successfully."}, status=200)

class UnitsBySectionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, site_id, section_id):
        company = request.user.company
        if not company:
            return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

        section = get_object_or_404(Section, id=section_id, site_id=site_id, site__company=company)

        # Using Q to filter and allow more flexible queries if necessary
        units = Unit.objects.filter(Q(section=section) & Q(company=company))
        

        serializer = UnitSerializer(units, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
    