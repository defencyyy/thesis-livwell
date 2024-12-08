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
from rest_framework.parsers import MultiPartParser, FormParser
import traceback
from django.core.exceptions import ValidationError

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

        # Log incoming data to see what is being received
        print("Received data:", data)
        print("Received files:", request.FILES)

        data['company'] = company.id
        serializer = UnitTemplateSerializer(data=data)

        if serializer.is_valid():
            template = serializer.save()

            # Handle image creation if images are included
            images_data = request.FILES.getlist('images')
            if images_data:
                for image in images_data:
                    UnitImage.objects.create(unit_template=template, image=image)

            return Response({"success": True, "data": UnitTemplateSerializer(template).data}, status=status.HTTP_201_CREATED)

        # If serializer is not valid, log the errors
        print("Serializer errors:", serializer.errors)
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

        # Deserialize the data
        serializer = UnitTemplateSerializer(template, data=request.data, partial=True)
        
        if serializer.is_valid():
            template = serializer.save()

            # Handle image updates (if images are included in the request)
            images_data = request.FILES.getlist('images')
            if images_data:
                # Delete existing images before creating new ones (optional)
                template.images.all().delete()
                for image in images_data:
                    UnitImage.objects.create(unit_template=template, image=image)

            return Response({"success": True, "data": UnitTemplateSerializer(template).data}, status=status.HTTP_200_OK)

        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = request.user.company
        try:
            template = UnitTemplate.objects.get(pk=pk, company=company)
        except UnitTemplate.DoesNotExist:
            return Response({"error": "UnitTemplate not found"}, status=status.HTTP_404_NOT_FOUND)

        # Instead of deleting, archive the template by setting is_archived to True
        template.is_archived = True
        template.save()

        # Optional: You can delete associated images, but that's not necessary for archiving
        # template.images.all().delete()

        return Response({"success": True, "message": "Template archived successfully."}, status=status.HTTP_200_OK)

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
        try:
            unit = Unit.objects.get(pk=pk, company=company)
        except Unit.DoesNotExist:
            return Response({"success": False, "message": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch images related to the unit
        unit_images = unit.images.all()  # This uses the related_name 'images'

        # Serialize unit data and unit images
        unit_serializer = UnitSerializer(unit)
        unit_images_serializer = UnitImageSerializer(unit_images, many=True)

        # Include the serialized images data in the response
        return Response(
            {
                "success": True,
                "data": unit_serializer.data,
                "images": unit_images_serializer.data,  # Include the image data here
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        company = request.user.company
        try:
            unit = Unit.objects.get(pk=pk, company=company)
        except Unit.DoesNotExist:
            return Response({"success": False, "message": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)

        # Process the incoming request data
        data = request.data
        print(f"Request data for updating unit {unit.id}: {data}")

        # Validate and update fields for the unit
        unit.unit_title = data.get("unit_title", unit.unit_title)
        unit.unit_type = data.get("unit_type", unit.unit_type)
        unit.status = data.get("status", unit.status)
        unit.price = data.get("price", unit.price)
        unit.lot_area = data.get("lot_area", unit.lot_area)
        unit.floor_area = data.get("floor_area", unit.floor_area)
        unit.commission = data.get("commission", unit.commission)
        unit.balcony = data.get("balcony", unit.balcony)
        unit.view = data.get("view", unit.view)

        # Handle updating floor IDs if provided
        floor_ids = data.getlist("floor_ids[]", [])
        if floor_ids:
            unit.floors.clear()  # Clear the existing floors before adding new ones
            for floor_id in floor_ids:
                try:
                    floor = Floor.objects.get(id=floor_id)
                    unit.floors.add(floor)
                except Floor.DoesNotExist:
                    return Response({"error": f"Invalid floor ID: {floor_id}"}, status=status.HTTP_400_BAD_REQUEST)

        # Handle image updates
        image_files = request.FILES.getlist("images[]")
        if image_files:
            print(f"Found {len(image_files)} image(s) to update.")
            # You can add more logic here for handling image updates if needed
            for image in image_files:
                # Save the new image for the unit
                try:
                    # You can create new UnitImage instances or associate new images to the unit
                    unit_image = UnitImage.objects.create(
                        unit=unit,
                        image=image,
                        image_type="Unit",  # Set a default or extract from request data
                        primary=False,  # Set primary as per the request or default
                    )
                    print(f"Image {image.name} updated successfully.")
                except Exception as e:
                    return Response({"error": f"Error updating image: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save the updated unit
        try:
            unit.save()
            print(f"Unit {unit.id} updated successfully.")
            return Response({"success": True, "data": UnitSerializer(unit).data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error saving updated unit: {str(e)}")
            return Response({"error": f"Error saving unit: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        company = request.user.company
        unit = Unit.objects.get(pk=pk, company=company)
        unit.delete()
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
            print(f"Request data: {request.data}")


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
                    print(f"Request FILES: {request.FILES}")


                    # Check if images are present in the request files
                    images = []
                    for key in request.FILES.keys():
                        if key.startswith("images"):  # Checks if the key is related to images
                            images.extend(request.FILES.getlist(key))  # Add all images under that key

                    if images:
                        print(f"Found {len(images)} image(s).")



                        # Extract image types and primaries from request data
                        image_types = request.data.getlist("image_types")  # Extract image_types
                        primaries = request.data.getlist("primaries")  # Extract primaries
                        unit_template_id = request.data.get("unit_template")  # Get the unit_template ID from the request

                        # Debug: Log the length of the lists
                        print(f"Received {len(images)} image(s), {len(image_types)} image type(s), and {len(primaries)} primary flags")

                        # Check if unit_template_id is provided and retrieve the UnitTemplate instance
                        unit_template = None
                        if unit_template_id:
                            try:
                                unit_template = UnitTemplate.objects.get(id=unit_template_id)
                                print(f"Unit template {unit_template_id} found: {unit_template.name}")
                            except UnitTemplate.DoesNotExist:
                                print(f"UnitTemplate with ID {unit_template_id} does not exist.")
                                return Response({"error": f"Invalid unit template ID: {unit_template_id}"}, status=status.HTTP_400_BAD_REQUEST)

                        # Iterate through each image to process it
                        for i, image in enumerate(images):
                            # Debug: Log image data being processed
                            print(f"Processing image {i + 1}: {image.name}")
                            
                            image_type = image_types[i] if i < len(image_types) else 'Unit'  # Default to 'Unit' if not available
                            primary = primaries[i] if i < len(primaries) else False  # Default to False if not available

                            # Debug: Log the metadata being appended
                            print(f"Image {i + 1} metadata: type={image_type}, primary={primary}")

                            # Create UnitImage instance and save
                            try:
                                existing_images_count = UnitImage.objects.filter(unit=unit).count()
                                print(f"Unit: {unit}, Unit Template: {unit_template}, Primary: {primary}, Image Type: {image_type}")
                                print(f"Already {existing_images_count} images for this unit.")
                                
                                # Create UnitImage instance and save
                                unit_image = UnitImage.objects.create(
                                    unit=unit,  # assuming 'unit' is the correct Unit instance
                                    unit_template=unit_template,  # Associate the unit_template if provided
                                    image=image,
                                    image_type=image_type,
                                    primary=primary
                                )
                                print(f"Image {image.name} saved successfully for unit {unit.id}")
                            except ValidationError as e:
                                # Catch any validation errors
                                print(f"Validation error while saving image: {str(e)}")
                                print(f"Full traceback:\n{traceback.format_exc()}")
                                return Response({"error": f"Image validation error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
                            except Exception as e:
                                # General error handling
                                print(f"Error while saving image: {str(e)}")
                                print(f"Full traceback:\n{traceback.format_exc()}")
                                return Response({"error": f"Error saving image: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    else:
                        print("No images found in the request.")



            # After all units are created, return the response
            return Response({"message": f"{len(created_units)} units successfully added."}, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            print("Full traceback:")
            print(traceback.format_exc())  # Log full traceback in case of unexpected error
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, unit_id):
        try:
            # Get the unit by unit_id
            unit = Unit.objects.get(id=unit_id)

            # Make sure the image file is included in the request
            image_file = request.FILES.get('image')
            if not image_file:
                return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new UnitImage object and associate it with the unit
            image = UnitImage(unit=unit, image=image_file, image_type='unit')  # Adjust image_type if needed
            image.save()

            # Return the serialized image data
            image_serializer = UnitImageSerializer(image)
            return Response(image_serializer.data, status=status.HTTP_201_CREATED)

        except Unit.DoesNotExist:
            return Response({'error': 'Unit not found'}, status=status.HTTP_404_NOT_FOUND)

class ImageManagementView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, unit_id, image_id):
        try:
            # Retrieve unit and the specific image by ID
            unit = Unit.objects.get(id=unit_id)
            image = UnitImage.objects.get(id=image_id, unit=unit)
        except Unit.DoesNotExist:
            return Response({"detail": "Unit not found."}, status=404)
        except UnitImage.DoesNotExist:
            return Response({"detail": "Image not found."}, status=404)

        image_file = request.FILES.get('image')
        if image_file:
            image.image = image_file  # Replace the old image with the new one
            image.save()  # Save the changes to the database
            return Response(UnitImageSerializer(image).data, status=200)
        
        return Response({"detail": "No image provided."}, status=400)

    def delete(self, request, unit_id, image_id):
        """Handle image deletion."""
        try:
            unit = Unit.objects.get(id=unit_id)
            image = UnitImage.objects.get(id=image_id, unit=unit)
        except Unit.DoesNotExist:
            return Response({"detail": "Unit not found."}, status=404)
        except UnitImage.DoesNotExist:
            return Response({"detail": "Image not found."}, status=404)

        # Optionally delete the actual image file from the filesystem
        if image.image:
            image.image.delete()

        image.delete()  # Delete the image record
        return Response({"detail": "Image deleted successfully."}, status=200)


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
