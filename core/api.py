from rest_framework import generics
from rest_framework.response import Response
from .serializers import SymptomSerializer
from core.tasks import predict_disease


class DiseasePredictionAPI(generics.GenericAPIView):
    serializer_class = SymptomSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        symptoms = serializer.validated_data['symptoms'].split(',')
        symptoms = [symptom.strip() for symptom in symptoms]

        predicted_disease = predict_disease(symptoms)

        return Response({'likely_disease': predicted_disease})
