# TODO: validation
# TODO: deserialization
from rest_framework import serializers

from poem.common import CATEGORIES, PARTS_OF_SPEECH, TAGS
from poem.models.words import Poem


class TokenSerializer(serializers.Serializer):
    category = serializers.ChoiceField(choices=CATEGORIES)
    content = serializers.CharField(
        trim_whitespace=False, allow_blank=True, required=False)
    original_word = serializers.CharField(
        required=False, trim_whitespace=False)
    tag = serializers.ChoiceField(choices=TAGS, required=False)

    def validate(self, data):
        is_pos = data['category'] in PARTS_OF_SPEECH 
        if is_pos and 'content' in data and 'original_word' not in data:
            raise serializers.ValidationError('Missing original_word.')

        if data['category'] == 'new_line' and '\n' not in data['content']:
            raise serializers.ValidationError('Inconsistent newline.')

        return data


class OptionsSerializer(serializers.Serializer):
    advance_by__noun = serializers.IntegerField(
            required=False, min_value=-10, max_value=10)
    advance_by__verb = serializers.IntegerField(
            required=False, min_value=-10, max_value=10)


class PoemModelSerializer(serializers.Serializer):
    title = serializers.CharField(
        trim_whitespace=False, allow_blank=True, max_length=200)
    raw_text = serializers.CharField(
        trim_whitespace=False, allow_blank=True, max_length=2000)
    options = OptionsSerializer()
    tokens = TokenSerializer(required=False, many=True)

    def create(self, validated_data):
        return Poem(**validated_data)
