from django.db.models import Model, CharField, GenericIPAddressField, IntegerField, TextField, DateTimeField, \
    ManyToManyField, ForeignKey, DO_NOTHING, BooleanField, SmallIntegerField


# Create your models here.
class UserInfo(Model):
    name = CharField(max_length=255, blank=True, null=False)
    total = IntegerField(default=0)
    taskId = CharField(max_length=255, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'user_info'

    def __str__(self):
        """
        to string
        :return: name
        """
        return self.name


class TaskInfo(Model):
    url = CharField(max_length=255, blank=True, null=True)
    xmlPath = CharField(max_length=255, blank=True, null=True)
    title = CharField(max_length=255, blank=True, null=True)
    taskId = CharField(max_length=255, blank=True, null=True)
    status = BooleanField(default=1)
    fetch_datetime = DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'task_info'

    def __str__(self):
        """
        to string
        :return: taskId
        """
        return self.taskId


class VideoInfo(Model):
    article_url = CharField(max_length=255, blank=True, null=True)
    taskId = CharField(max_length=255, blank=True, null=True)
    vid = CharField(max_length=255, blank=True, null=True)
    video_file_name = CharField(max_length=255, blank=True, null=True)
    src_video_url = CharField(max_length=255, blank=True, null=True)
    src_video_image = CharField(max_length=255, blank=True, null=True)
    uuid = CharField(max_length=255, blank=True, null=True)
    status = IntegerField(default=0)
    width = IntegerField(default=0)
    height = IntegerField(default=0)
    src_width = IntegerField(default=0)
    src_height = IntegerField(default=0)
    file_length = IntegerField(default=0)
    file_size = IntegerField(default=0)

    class Meta:
        db_table = 'video_info'

    def __str__(self):
        """
        to string
        :return: title
        """
        return (self.taskId, self.article_url)


class XinhuaWeb(Model):
    url = CharField(unique=True, max_length=255, blank=True, null=True)
    title = CharField(max_length=255, blank=True, null=True)
    publish_date = DateTimeField(blank=True, null=True)
    source = CharField(max_length=255, blank=True, null=True)
    author = CharField(max_length=255, blank=True, null=True)
    xml_file = CharField(max_length=255, blank=True, null=True)
    content = TextField(blank=True, null=True)
    images = TextField(blank=True, null=True)
    video_url = TextField(blank=True, null=True)
    video_image_url = TextField(blank=True, null=True)
    article_type = CharField(max_length=255, blank=True, null=True)
    fetch_date = DateTimeField(blank=True, null=True)
    xml_content = TextField(blank=True, null=True)

    class Meta:
        db_table = 'xinhua_web'

    def __str__(self):
        """
        to string
        :return: title
        """
        return self.title
