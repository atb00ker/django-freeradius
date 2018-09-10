from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class BaseTestNas(object):
    def test_string_representation(self):
        nas = self.nas_model(name='entry nasname')
        self.assertEqual(str(nas), nas.name)


class BaseTestRadiusAccounting(object):
    def test_string_representation(self):
        radiusaccounting = self.radius_accounting_model(unique_id='entry acctuniqueid')
        self.assertEqual(str(radiusaccounting), radiusaccounting.unique_id)


class BaseTestRadiusCheck(object):
    def test_string_representation(self):
        radiuscheck = self.radius_check_model(username='entry username')
        self.assertEqual(str(radiuscheck), radiuscheck.username)


class BaseTestRadiusReply(object):
    def test_string_representation(self):
        radiusreply = self.radius_reply_model(username='entry username')
        self.assertEqual(str(radiusreply), radiusreply.username)


class BaseTestRadiusGroupReply(object):
    def test_string_representation(self):
        radiusgroupreply = self.radius_groupreply_model(groupname='entry groupname')
        self.assertEqual(str(radiusgroupreply), radiusgroupreply.groupname)


class BaseTestRadiusGroupCheck(object):
    def test_string_representation(self):
        radiusgroupcheck = self.radius_groupcheck_model(groupname='entry groupname')
        self.assertEqual(str(radiusgroupcheck), radiusgroupcheck.groupname)


class BaseTestRadiusUserGroup(object):
    def test_string_representation(self):
        radiususergroup = self.radius_usergroup_model(username='entry username')
        self.assertEqual(str(radiususergroup), radiususergroup.username)


class BaseTestRadiusPostAuth(object):
    def test_string_representation(self):
        radiuspostauthentication = self.radius_postauth_model(username='entry username')
        self.assertEqual(str(radiuspostauthentication), radiuspostauthentication.username)


class BaseTestRadiusGroup(object):
    def test_string_representation(self):
        radiusgroup = self.radius_group_model(groupname='entry groupname')
        self.assertEqual(str(radiusgroup), radiusgroup.groupname)


class BaseTestRadiusBatch(object):
    def test_string_representation(self):
        radiusbatch = self.radius_batch_model(name='test')
        self.assertEqual(str(radiusbatch), 'test')

    def test_delete_method(self):
        options = dict(strategy='prefix', prefix='test', name='test')
        radiusbatch = self._create_radius_batch(**options)
        radiusbatch.prefix_add('test', 5)
        User = get_user_model()
        self.assertEqual(User.objects.all().count(), 5)
        radiusbatch.delete()
        self.assertEqual(self.radius_batch_model.objects.all().count(), 0)
        self.assertEqual(User.objects.all().count(), 0)

    def test_clean_method(self):
        radiusbatch = self._create_radius_batch()
        with self.assertRaises(ValidationError):
            radiusbatch.full_clean()
        options = dict(strategy='csv', prefix='test', name='test')
        radiusbatch = self._create_radius_batch(**options)
        with self.assertRaises(ValidationError):
            radiusbatch.full_clean()


class BaseTestRadiusProfile(object):
    def test_string_representation(self):
        RadiusProfile = self.radius_profile_model
        radiusprofile = RadiusProfile(name='test')
        self.assertEqual(str(radiusprofile), 'test')

    def test_save_method(self):
        RadiusProfile = self.radius_profile_model
        options = dict(name='test', default=True, daily_session_limit=10)
        self._create_radius_profile(**options)
        self.assertEqual(RadiusProfile.objects.all().count(), 3)
        self.assertEqual(RadiusProfile.objects.filter(default=True).count(), 1)
        options.update(dict(name='test1', daily_session_limit=20))
        self._create_radius_profile(**options)
        self.assertEqual(RadiusProfile.objects.all().count(), 4)
        self.assertEqual(RadiusProfile.objects.filter(default=True).count(), 1)


class BaseTestRadiusUserProfile(object):
    def test_string_representation(self):
        self._create_radius_profile(**dict(name='test'))
        user = get_user_model().objects.create(username="test")
        radiususerprofile = self.radius_userprofile_model.objects.get(user=user)
        self.assertEqual(str(radiususerprofile), 'test-test')

    def test_save_method(self):
        RadiusCheck = self.radius_check_model
        RadiusUserProfile = self.radius_userprofile_model
        options = dict(name='test', default=True, daily_session_limit=10)
        radiusprofile = self._create_radius_profile(**options)
        get_user_model().objects.create(username="test")
        self.assertEqual(RadiusUserProfile.objects.all().count(), 1)
        self.assertEqual(RadiusCheck.objects.all().count(), 1)
        radiususerprofile = RadiusUserProfile.objects.first()
        radiusprofile.daily_session_limit = 20
        radiusprofile.daily_bandwidth_limit = 10
        radiusprofile.save()
        radiususerprofile.profile = radiusprofile
        radiususerprofile.save()
        self.assertEqual(RadiusCheck.objects.all().count(), 2)
