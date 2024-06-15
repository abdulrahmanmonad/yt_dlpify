from peewee import CompositeKey, Model, TextField


class DownloadTrackingModel(Model):
    video_url = TextField(null=False)
    video_resolution = TextField(null=False)
    video_title = TextField(null=False)
    destination_path = TextField(null=False)
    downloading_status = TextField(null=False)

    class Meta:
        table_name = "downloads_tracking"
        primary_key = CompositeKey(
            "video_url", "video_resolution", "video_title", "destination_path"
        )
