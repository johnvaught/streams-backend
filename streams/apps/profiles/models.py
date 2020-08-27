import uuid
from django.db import models
from django.db.models import F, Q
from streams.apps.core.models import TimestampedModel
from streams.settings import AUTH_USER_MODEL

from streams.apps.streams.models import Stream
from streams.apps.follows.models import ProfileFollow, StreamFollow


class ProfileManager(models.Manager):
    """
    Inactivating an account also `deletes` the associated profile by
    removing them from all queries.
    """
    # TODO: Research .select_related() because I'm pretty sure I could be using it better.
    def get_queryset(self):
        return super(ProfileManager, self).get_queryset()\
            .select_related('account').filter(account__is_active=True)


class Profile(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=50, blank=True)
    image = models.CharField(max_length=36, blank=True, default="")
    bio = models.TextField(max_length=1000, blank=True, default="")
    is_private = models.BooleanField(default=False)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    followed_streams = models.ManyToManyField('streams.Stream', through='follows.StreamFollow',
                                              related_name='following_profiles')

    @property
    def handle(self):
        return self.account.handle

    @property
    def is_active(self):
        return self.account.is_active

    objects = ProfileManager()

    def cond_add_to_follower_count(self, owner_or_sub_of_following_stream, following_stream, recursive=True):

        # check if this profile is following me from any of their streams, or if any of
        # the streams they are subscribed to are following me
        streams_by_owner_or_sub_of_following_stream = Stream.objects.exclude(pk=following_stream.id).filter(
            owner=owner_or_sub_of_following_stream)
        stream_ids_owner_of_following_stream_is_sub_to = StreamFollow.objects.filter(
            profile=owner_or_sub_of_following_stream).values('stream')
        streams_owner_of_following_stream_is_sub_to = Stream.objects.exclude(pk=following_stream.id).filter(
            pk__in=stream_ids_owner_of_following_stream_is_sub_to)

        following_me = ProfileFollow.objects.filter(
            Q(profile=self),
            Q(stream__in=streams_by_owner_or_sub_of_following_stream) |
            Q(stream__in=streams_owner_of_following_stream_is_sub_to))

        if not following_me:
            self.follower_count = F('follower_count') + 1
            self.save()

        # and perform this same function for the profiles who subscribe to this stream
        if recursive:
            profiles_ids_sub_to_following_stream = StreamFollow.objects.filter(
                stream=following_stream.id).values('profile')
            profiles_sub_to_following_stream = Profile.objects.filter(
                pk__in=profiles_ids_sub_to_following_stream)

            for sub_profile in profiles_sub_to_following_stream:
                self.cond_add_to_follower_count(sub_profile, following_stream, recursive=False)

        # check if this profile is already following me from any of their other streams.
        # or streams they are following.
        # and perform this check for all followers of the stream

        # streams = Stream.objects.filter(owner=profile)
        # follower = ProfileFollow.objects.filter(stream__in=streams, profile=self)
        #
        # stream_follows = StreamFollow.objects.filter(profile=profile).values('stream')
        # followed_streams = Stream.objects.filter(pk__in=stream_follows)
        # profile_follows = ProfileFollow.objects\
        #     .filter(stream__in=followed_streams, profile=self).values('profile')
        #
        # if count:
        #     stream_follows = StreamFollow.objects.filter(stream=stream).values('profile')
        #     profiles_following_stream = Profile.objects.filter(pk__in=stream_follows)
        #
        #     for profile_following in profiles_following_stream:
        #         self.cond_add_to_follower_count(profile_following, stream, 0)
        #
        # if not follower and not profile_follows:
        #     self.follower_count = F('follower_count') + 1
        #     # self.update(follower_count=F('follower_count') + 1)
        #     self.save()

    def cond_remove_from_follower_count(self, owner_or_sub_of_following_stream, following_stream, recursive=True):
        # check if this profile is following me from any of their streams, or if any of
        # the streams they are subscribed to are following me
        streams_by_owner_of_following_stream = Stream.objects.exclude(pk=following_stream.id).filter(
            owner=owner_or_sub_of_following_stream)
        stream_ids_owner_of_following_stream_is_sub_to = StreamFollow.objects.filter(
            profile=owner_or_sub_of_following_stream).values('stream')
        streams_owner_of_following_stream_is_sub_to = Stream.objects.exclude(pk=following_stream.id).filter(
            pk__in=stream_ids_owner_of_following_stream_is_sub_to)

        following_me = ProfileFollow.objects.filter(
            Q(profile=self),
            Q(stream__in=streams_by_owner_of_following_stream) |
            Q(stream__in=streams_owner_of_following_stream_is_sub_to))

        if not following_me:
            self.follower_count = F('follower_count') - 1
            self.save()

        # and perform this same function for the profiles subscribed to this stream
        if recursive:
            profiles_ids_sub_to_following_stream = StreamFollow.objects.filter(
                stream=following_stream.id).values('profile')
            profiles_sub_to_following_stream = Profile.objects.filter(
                pk__in=profiles_ids_sub_to_following_stream)

            for sub_profile in profiles_sub_to_following_stream:
                self.cond_remove_from_follower_count(sub_profile, following_stream, recursive=False)

        # check if the owner of this stream is following me from any of their other streams.
        # or streams they are following.
        # and perform this check for all followers of the stream

        # streams = Stream.objects.filter(owner=profile).exclude(pk=stream_to_exclude.id)
        # follower = ProfileFollow.objects.filter(stream__in=streams, profile=self)
        #
        # stream_follows = StreamFollow.objects.filter(profile=profile).values('stream')
        # followed_streams = Stream.objects.filter(pk__in=stream_follows).exclude(pk=stream_to_exclude.id)
        # profile_follows = ProfileFollow.objects\
        #     .filter(stream__in=followed_streams, profile=profile).values('profile')
        #
        # if count:
        #     stream_follows = StreamFollow.objects.filter(stream=stream_to_exclude).values('profile')
        #     profiles_following_stream = Profile.objects.filter(pk__in=stream_follows).exclude(pk=profile.id)
        #
        #     for profile_following in profiles_following_stream:
        #         self.cond_remove_from_follower_count(profile_following, stream_to_exclude, 0)
        #
        # if not follower and not profile_follows:
        #     self.follower_count = F('follower_count') - 1
        #     self.save()

    def cond_add_to_following_count(self, profile_stream_follows, following_stream, recursive=True):
        # check if i am following following this profile from any of my streams, or if any of
        # the streams i am subscribed to are following this profile
        my_streams = Stream.objects.exclude(pk=following_stream.id).filter(owner=self)
        my_subscribed_to_stream_ids = StreamFollow.objects.filter(profile=self).values('stream')
        my_subscribed_to_streams = Stream.objects.exclude(pk=following_stream.id).filter(pk__in=my_subscribed_to_stream_ids)

        is_following = ProfileFollow.objects.filter(
            Q(profile=profile_stream_follows),
            Q(stream__in=my_streams) | Q(stream__in=my_subscribed_to_streams))

        if not is_following:
            self.following_count = F('following_count') + 1
            self.save()

        # and perform this same function for the profiles subscribed to this stream
        # wait a minute... this shouldn't be necessary
        # i think so for a profile follow, but not so for a stream follow...
        if recursive:
            profiles_ids_sub_to_following_stream = StreamFollow.objects.filter(
                stream=following_stream.id).values('profile')
            profiles_sub_to_following_stream = Profile.objects.filter(
                pk__in=profiles_ids_sub_to_following_stream)

            for sub_profile in profiles_sub_to_following_stream:
                sub_profile.cond_add_to_following_count(profile_stream_follows, following_stream, recursive=False)


        # check if i am already following this profile from any of my streams
        # or streams i'm following.
        # and perform this check for all followers of this stream
        # streams = Stream.objects.filter(owner=self)
        # following = ProfileFollow.objects.filter(stream__in=streams, profile=profile)
        #
        # stream_follows = StreamFollow.objects.filter(profile=self).values('stream')
        # followed_streams = Stream.objects.filter(pk__in=stream_follows)
        # profile_follows = ProfileFollow.objects\
        #     .filter(stream__in=followed_streams, profile=profile).values('profile')
        #
        # if count:
        #     stream_follows = StreamFollow.objects.filter(stream=stream).values('profile')
        #     profiles_following_stream = Profile.objects.filter(pk__in=stream_follows)
        #
        #     for profile_following in profiles_following_stream:
        #         profile_following.cond_add_to_following_count(profile, stream, 0)
        #
        # if not following and not profile_follows:
        #     self.following_count = F('following_count') + 1
        #     self.save()

    def cond_remove_from_following_count(self, profile_stream_follows, following_stream, recursive=True):
        # check if i am following following this profile from any of my streams, or if any of
        # the streams i am subscribed to are following this profile
        my_streams = Stream.objects.exclude(pk=following_stream.id).filter(owner=self)
        my_subscribed_to_stream_ids = StreamFollow.objects.filter(profile=self).values('stream')
        my_subscribed_to_streams = Stream.objects.exclude(pk=following_stream.id).filter(pk__in=my_subscribed_to_stream_ids)

        is_following = ProfileFollow.objects.filter(
            Q(profile=profile_stream_follows),
            Q(stream__in=my_streams) | Q(stream__in=my_subscribed_to_streams))

        if not is_following:
            self.following_count = F('following_count') - 1
            self.save()

        # and perform this same function for the profiles subscribed to this stream
        # is this needed?????
        # i think so for a profile follow, but not so for a stream follow...
        if recursive:
            profiles_ids_sub_to_following_stream = StreamFollow.objects.filter(
                stream=following_stream.id).values('profile')
            profiles_sub_to_following_stream = Profile.objects.filter(
                pk__in=profiles_ids_sub_to_following_stream)

            for sub_profile in profiles_sub_to_following_stream:
                sub_profile.cond_remove_from_following_count(profile_stream_follows, following_stream, recursive=False)

        # check if i am still following this profile from any of my streams
        # or streams i'm following.
        # and perform this check for all followers of this stream
        # streams = Stream.objects.filter(owner=self).exclude(pk=stream_to_exclude.id)
        # following = ProfileFollow.objects.filter(stream__in=streams, profile=profile)
        #
        # # check if i am following this profile from any of the streams i follow
        # stream_ids = StreamFollow.objects.filter(profile=self).values('stream')
        # followed_streams = Stream.objects.filter(pk__in=stream_ids).exclude(pk=stream_to_exclude.id)
        # profiles_following = ProfileFollow.objects\
        #     .filter(stream__in=followed_streams, profile=profile)
        #
        # if count:
        #     stream_follows = StreamFollow.objects.filter(stream=stream_to_exclude).values('profile')
        #     profiles_following_stream = Profile.objects.filter(pk__in=stream_follows).exclude(pk=self.id)
        #
        #     for profile_following in profiles_following_stream:
        #         profile_following.cond_remove_from_following_count(profile, stream_to_exclude, 0)
        #
        # if not following and not profiles_following:
        #     self.following_count = F('following_count') - 1
        #     self.save()

    def cond_add_to_follower_count_for_stream_follow(self, stream_follow):
        profile_ids = ProfileFollow.objects.filter(stream=stream_follow.stream).values('profile')
        profiles = Profile.objects.filter(pk__in=profile_ids)

        for profile in profiles:
            profile.cond_add_to_follower_count(stream_follow.profile, stream_follow.stream, recursive=False)

    def cond_remove_from_follower_count_for_stream_follow(self, stream_follow):
        profile_ids = ProfileFollow.objects.filter(stream=stream_follow.stream).values('profile')
        profiles = Profile.objects.filter(pk__in=profile_ids)

        for profile in profiles:
            profile.cond_remove_from_follower_count(stream_follow.profile, stream_follow.stream, recursive=False)

    def cond_add_to_following_count_for_stream_follow(self, stream_follow):
        profile_ids = ProfileFollow.objects.filter(stream=stream_follow.stream).values('profile')
        profiles = Profile.objects.filter(pk__in=profile_ids)

        for profile in profiles:
            stream_follow.profile.cond_add_to_following_count(profile, stream_follow.stream, recursive=False)

    def cond_remove_from_following_count_for_stream_follow(self, stream_follow):
        profile_ids = ProfileFollow.objects.filter(stream=stream_follow.stream).values('profile')
        profiles = Profile.objects.filter(pk__in=profile_ids)

        for profile in profiles:
            stream_follow.profile.cond_remove_from_following_count(profile, stream_follow.stream, recursive=False)

    def __str__(self):
        return self.account.handle


# class ProfileFollows(TimestampedModel):
#     account = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

