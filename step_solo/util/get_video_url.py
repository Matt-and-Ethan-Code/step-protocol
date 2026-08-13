from typing import Literal
import boto3
from django.conf import settings

s3 = boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
def get_video_url_impl(object_key: str) -> str:
    """
    object_key: the path to the object in the bucket
    """
    global s3
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": object_key},
        ExpiresIn=settings.AWS_QUERYSTRING_EXPIRE,
    )

type VideoName = Literal[
    "4_elements_with_music",
    "4_elements_without_music",
    "bilateral_tapping",
    "container_video",
    "solo_introduction",
    "solo_1",
    "solo_2",
    "solo_3",
    "solo_4",
    "solo_5",
    "solo_6",
    "solo_7",
    "solo_8p1",
    "solo_8p2",
    "solo_9",
    "solo_10",
    "solo_11",
    "solo_12",
    "drawing_guide",
]

# the path to the resource in the Tigris bucket
object_key_from_video_name: dict[VideoName, str] = {
    '4_elements_with_music': 'solo/4_elements_with_music.mp4',
    '4_elements_without_music': 'solo/4_elements_without_music.mp4',
    'bilateral_tapping': 'solo/bilateral_tapping_video.mp4',
    'container_video': 'solo/container_video.mp4',
    'solo_introduction': 'solo/solo_introduction.mp4',
    'solo_1': 'solo/solo_01.mp4',
    'solo_2': 'solo/solo_02.mp4',
    'solo_3': 'solo/solo_03.mp4',
    'solo_4': 'solo/solo_04.mp4',
    'solo_5': 'solo/solo_05.mp4',
    'solo_6': 'solo/solo_06.mp4',
    'solo_7': 'solo/solo_07.mp4',
    'solo_8p1': 'solo/solo_08p1.mp4',
    'solo_8p2': 'solo/solo_08p2.mp4',
    'solo_9': 'solo/solo_09.mp4',
    'solo_10': 'solo/solo_10.mp4',
    'solo_11': 'solo/solo_11.mp4',
    'solo_12': 'solo/solo_12.mp4',
    'drawing_guide': 'solo/drawing_guide.mp4',
}


def get_video_url(video_name: VideoName) -> str:
    return get_video_url_impl(object_key_from_video_name[video_name])
