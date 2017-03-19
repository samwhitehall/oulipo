from rest_framework import serializers

from poem.common import CATEGORIES, PARTS_OF_SPEECH, TAGS
from poem.models.words import Poem


class TokenSerializer(serializers.Serializer):
    category = serializers.ChoiceField(choices=CATEGORIES)
    original_word = serializers.CharField(required=False, trim_whitespace=False)
    tag = serializers.ChoiceField(choices=TAGS, required=False)
    offsets = serializers.DictField(
        child=serializers.CharField(), required=False)


class PoemModelSerializer(serializers.Serializer):
    title = serializers.CharField(
        trim_whitespace=False, allow_blank=True, max_length=200)
    raw_text = serializers.CharField(
        trim_whitespace=False, allow_blank=True, max_length=2000)
    tokens = TokenSerializer(required=False, many=True)

    def create(self, validated_data):
        return Poem(**validated_data)
