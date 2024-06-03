from rest_framework import serializers
from service.models import ServiceType,CourseType

class ServiceSerializer(serializers.ModelSerializer):
    course_type=serializers.SerializerMethodField()

    class Meta:
        model=ServiceType
        fields=(
            'id',
            'service',
            'course_type',
        )
    def get_course_type(self,instance):
        request = self.context.get('request')
        if (course_type := CourseType.objects.filter(service=instance, is_deleted=False)).exists():
           
           serialized_data = CourseTypeSerializer(
               course_type,
               context = {
                   "request" : request
               },
               many = True
           ).data

           return serialized_data
        else:
            return []
        

class AddServiceSerializer(serializers.Serializer):
    service=serializers.CharField()

class CourseTypeSerializer(serializers.ModelSerializer):
    service=serializers.SerializerMethodField()
    class Meta:
        model=CourseType
        fields=(
            'id',
            'course_type',
            'service',
        )
    def to_representation(self, obj):
      return {"id":obj.id,"value":obj.course_type}    
      
    def get_service(self,instance):
        if instance:
            s=list(instance.servicetype_set.filter(is_deleted=False).values('id','service'))
            return s
        else:
            return None
    

class ViewCourseTypeSerializer(serializers.ModelSerializer):
    service_name=serializers.SerializerMethodField()
    class Meta:
        model=CourseType
        fields=(
            'id',
            'course_type',
            'service',
            'service_name',
        )
    def get_service_name(self,instance):
        if instance:
            return instance.service.service     
        else:
            return None


class AddCourseTypeSerializer(serializers.Serializer):
    course_type=serializers.CharField()