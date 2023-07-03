from rest_framework import serializers

from .models import Talent
from .models import Region
from apps.rmsManager.models import RecruitmentWay
from apps.rmsauth.models import User
from apps.rmsauth.models import Group


class GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["title"]


class UserSerializers(serializers.ModelSerializer):
    group = GroupSerializers()

    class Meta:
        model = User
        fields = ('username', 'group')


class RegionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['name']


class RecruitmentWaySerializers(serializers.ModelSerializer):
    class Meta:
        model = RecruitmentWay
        fields = ['name']


class TalentSerializers(serializers.ModelSerializer):
    channel = RecruitmentWaySerializers()
    user = UserSerializers()
    region = RegionSerializers()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Talent
        fields = ('id', 'name', 'gender', 'user', 'region', 'channel', 'status')

    def get_status(self, obj):
        return obj.get_status_display()
