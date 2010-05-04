
from django.contrib.gis.db import models
from django.contrib.auth.models import User




#class OsmFile(models.Model):
#    user = models.ForeignKey(User)
#    geom = models.PolygonField(srid=4326) # bounding box of the osm file


# maybe these should go in a seperate db to decouple it from an OSM database?
# ForeignKeys are currently not mapped and they need to be 
# some of the fields may be off also
# most important for now is to pull in partial version and store it in the db 


### CustomFields 

class NoTzDateTimeField(models.DateTimeField):
    def db_type(self, connection):
        return 'timestamp without timezone'


# will need to do some more customization later... 
# this will not map exactly to OSMs database format 
# for now the only customization is for the timezone field 
# most important databases to support or Postgres (which is native to OSM)
# and spatialite later to allow for disconnected databases that can be 
# placed on a usb stick


# django creates default values for character fields at the application layer 

#class DefCharField(models.CharField):
#    import code; code.inteart(local=locals())
#    return 'varying(255)' 

# need custom managers to deal with some type of queries, because there can be multiple columns 
# that make up a key 


### Changesets ###

class ChangeSetTag(models.Model):
    id = models.BigIntegerField(primary_key=True)
    k = models.CharField(max_length=255,default="") # mismatch
    v = models.CharField(max_length=255,default="") # mismatch
    objects = models.GeoManager()
    class Meta:
        db_table = 'changeset_tags'

class ChangeSet(models.Model):
    id = models.BigIntegerField(primary_key=True) 
    user_id = models.ForeignKey(User)  # BigIntegerField
    created_at = NoTzDateTimeField()
    min_lat = models.IntegerField(null=True)
    max_lat = models.IntegerField(null=True)
    min_lon = models.IntegerField(null=True)
    max_lon = models.IntegerField(null=True)
    closed_at = NoTzDateTimeField()
    num_changes = models.IntegerField(default=0)  # mismatch
    objects = models.GeoManager()
    class Meta:
        db_table = 'changesets'


class CurrentNodeTag(models.Model):
    id = models.BigIntegerField(primary_key=True) #  -- primary key part 1/2; references current_nodes(id)
    k = models.CharField(max_length=255,default="") # mismatch -- primary key part 2/2
    v = models.CharField(max_length=255,default="") # mismatch    
    objects = models.GeoManager()
    class Meta:
        db_table = 'current_node_tags'

 
class CurrentNode(models.Model):
    id = models.BigIntegerField(primary_key=True) 
    latitude = models.IntegerField() 
    longitude = models.IntegerField() 
    changeset_id = models.ForeignKey(ChangeSet)
    visible = models.BooleanField() 
    timestamp = NoTzDateTimeField()
    tile = models.BigIntegerField() 
    version = models.BigIntegerField()
    objects = models.GeoManager()
    class Meta:
        db_table = 'current_nodes' 

## this shouldn't have a incrementing key? 
## need to do something custom to drop the sequence after database creation?
class NodeTag(models.Model):
    id = models.BigIntegerField(primary_key=True) # -- primary key part 1/3; references nodes(id,version) part 1/2
    version = models.BigIntegerField() # primary key part 2/3; references nodes(id,version) part 2/2
    k = models.CharField(max_length=255) # -- primary key part 3/3
    v = models.CharField(max_length=255) 
    objects = models.GeoManager()
    class Meta:
        db_table = 'node_tags'
 

class Node(models.Model):
    id = models.BigIntegerField(primary_key=True)
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    changeset_id = models.ForeignKey(ChangeSet) # BigIntegerField 
    visible = models.BooleanField()
    timestamp = NoTzDateTimeField()
    tile = models.BigIntegerField()
    version = models.BigIntegerField()
    objects = models.GeoManager()
    class Meta:
        db_table = 'nodes'


### ways


# should not have a sequence ? 
class CurrentWayNode(models.Model):
    id = models.BigIntegerField(primary_key=True) # -- primary key part 1/2; references current_ways(id)

    node_id = models.BigIntegerField()
    sequence_id = models.BigIntegerField() # -- primary key part 2/2
    objects = models.GeoManager()
    class Meta:
        db_table = 'current_way_nodes'


class CurrentWayTag(models.Model):
    id = models.BigIntegerField(primary_key=True)
    k = models.CharField(max_length=255)
    v = models.CharField(max_length=255)
    objects = models.GeoManager()
    class Meta:
        db_table = 'current_way_tags'


class CurrentWay(models.Model):
    id = models.BigIntegerField(primary_key=True)
    changeset_id = models.ForeignKey(ChangeSet)
    timestamp = NoTzDateTimeField() 
    visible = models.BooleanField() 
    version = models.BigIntegerField()
    objects = models.GeoManager()
    class Meta:
        db_table = 'current_ways'

class WayNode(models.Model):
    id = models.BigIntegerField(primary_key=True)
    node_id = models.BigIntegerField()
    version = models.BigIntegerField() 
    sequence_id = models.BigIntegerField() 
    objects = models.GeoManager()
    class Meta:
        db_table = 'way_nodes'


class WayTag(models.Model):
    id = models.BigIntegerField(primary_key=True)
    k = models.CharField(max_length=255)
    v = models.CharField(max_length=255)
    version = models.BigIntegerField()
    objects = models.GeoManager()
    class Meta:
        db_table = 'way_tags'
 
class Way(models.Model):
    id = models.BigIntegerField(primary_key=True)
    changeset_id = models.BigIntegerField()
    timestamp = NoTzDateTimeField()
    version = models.BigIntegerField()
    visible = models.BooleanField()
    objects = models.GeoManager()
    class Meta:
        db_table = 'ways'


###  Relations

### need a custom way to deal with enums 
class CurrentRelationMember(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ### member_type nwr_enum NOT NULL, -- primary key part 2/5
    member_id = models.BigIntegerField()
    member_role = models.CharField(max_length=255)
    sequence_id = models.IntegerField(default=0)
    objects = models.GeoManager()


class CurrentRelationTag(models.Model):
    id = models.BigIntegerField(primary_key=True)
    k = models.CharField(max_length=255)
    v = models.CharField(max_length=255)
    objects = models.GeoManager()
    class Meta:
        db_table = 'current_relation_tags'


class Meta: 
    db_table = 'current_relations'

class CurrentRelation(models.Model):
    id = models.BigIntegerField(primary_key=True)
    changeset_id = models.BigIntegerField()
    timestamp = NoTzDateTimeField()
    visible = models.BooleanField()
    version = models.BigIntegerField()
    objects = models.GeoManager()
    class Meta: 
        db_table = 'current_relations'


### need something custom to deal with the enum 

class RelationMember(models.Model):


    id = models.BigIntegerField(primary_key=True)
    ### member_type nwr_enum NOT NULL, -- primary key part 3/6 
    member_id = models.BigIntegerField()
    member_role = models.CharField(max_length=255)
    version = models.BigIntegerField()
    sequence_id = models.IntegerField(default=0)


class RelationTag(models.Model):
    id = models.BigIntegerField(primary_key=True)
    k = models.CharField(max_length=255)
    v = models.CharField(max_length=255)
    version = models.BigIntegerField()
    objects = models.GeoManager()


class Relation(models.Model):
    id = models.BigIntegerField(primary_key=True)
    changeset_id = models.BigIntegerField()
    timestamp = NoTzDateTimeField()
    version = models.BigIntegerField()
    visible = models.BooleanField()
    objects = models.GeoManager()
    

class Country(models.Model):
    id = models.BigIntegerField(primary_key=True)
    code = models.CharField(max_length=2)
    min_lat = models.FloatField()
    max_lat = models.FloatField()
    min_lon = models.FloatField()
    max_lon = models.FloatField()
    class Meta:
        db_table = 'countries'

class GpsPoint(models.Model):
    altitude = models.FloatField(null=True)
    trackid = models.IntegerField()
    latitude =  models.IntegerField()
    longitude =  models.IntegerField()
    gpx_id = models.BigIntegerField()
    timestamp = NoTzDateTimeField()
    tile = models.BigIntegerField()
    objects = models.GeoManager()
    class Meta:
        db_table = 'gps_points'

class GpxFileTag(models.Model):
     gpx_id =  models.BigIntegerField()
     tag = models.CharField(max_length=255)
     id = models.BigIntegerField(primary_key=True)
     objects = models.GeoManager()
     class Meta:
         db_table = 'gpx_file_tags'


### need special case for enum
class GpxFile(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    visible  = models.BooleanField()
    name = models.CharField(max_length=255)
    size = models.BigIntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = NoTzDateTimeField()
    description = models.CharField(max_length=255)
    inserted = models.BooleanField()
    ### visibility gpx_visibility_enum DEFAULT 'public'::gpx_visibility_enum NOT NULL
    objects = models.GeoManager()
    class Meta:
        db_table = 'gpx_files'


### need special case for inet field 
class Acl(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ### address inet NOT NULL,
    ### netmask inet NOT NULL,
    k = models.CharField(max_length=255)
    v = models.CharField(max_length=255)
    objects = models.GeoManager()


class ClientApplication(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    url =  models.CharField(max_length=255)
    support_url =  models.CharField(max_length=255)
    callback_url =  models.CharField(max_length=255)
    KEY =  models.CharField(max_length=50)
    secret =  models.CharField(max_length=50)
    user_id = models.IntegerField()
    created_at = NoTzDateTimeField()
    updated_at = NoTzDateTimeField()
    allow_read_prefs = models.BooleanField(default=False)
    allow_write_prefs = models.BooleanField(default=False)
    allow_write_diary = models.BooleanField(default=False)
    allow_write_api = models.BooleanField(default=False)
    allow_read_gpx = models.BooleanField(default=False)
    allow_write_gpx =  models.BooleanField(default=False)
    objects = models.GeoManager()


class DiaryComment(models.Model):
    id = models.BigIntegerField(primary_key=True)
    diary_entry_id = models.BigIntegerField(primary_key=True)
    user_id = models.BigIntegerField(primary_key=True)
    body = models.TextField()
    created_at =  NoTzDateTimeField()
    updated_at =  NoTzDateTimeField()
    objects = models.GeoManager()


class DiaryEntry(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user_id =  models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at =  NoTzDateTimeField()
    updated_at =  NoTzDateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    language_code = models.CharField(max_length=255) 
    objects = models.GeoManager()


class Friend(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    friend_user_id =  models.BigIntegerField()
    objects = models.GeoManager()
    
class Language (models.Model):
    code = models.CharField(max_length=255)
    english_name = models.CharField(max_length=255)
    native_name = models.CharField(max_length=255)
    objects = models.GeoManager()


class Message(models.Model):
    id = models.BigIntegerField(primary_key=True)
    from_user_id =  models.BigIntegerField()
    title = models.CharField(max_length=255)
    body = models.TextField()
    sent_on = NoTzDateTimeField()
    message_read = models.BooleanField()
    message_read = models.BooleanField(default=False)
    to_user_id = models.BigIntegerField()
    to_user_visible = models.BooleanField()
    from_user_visible = models.BooleanField()
    objects = models.GeoManager()

class OauthNonce(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nonce = models.CharField(max_length=255)
    created_at = NoTzDateTimeField()
    updated_at =  NoTzDateTimeField(null=True)
    objects = models.GeoManager()

class OauthToken(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user_id =  models.BigIntegerField()
    _type = models.CharField(db_column="type", max_length=20)
    client_application_id = models.IntegerField()
    token = models.CharField(max_length=50)
    secret = models.CharField(max_length=50)
    authorized_at = NoTzDateTimeField(null=True)
    invalidated_at =  NoTzDateTimeField(null=True)
    created_at =  NoTzDateTimeField(null=True)
    updated_at =  NoTzDateTimeField(null=True)
    allow_read_prefs = models.BooleanField(default=False)
    allow_write_prefs = models.BooleanField(default=False)
    allow_write_diary = models.BooleanField(default=False)
    allow_write_api = models.BooleanField(default=False)
    allow_read_gpx = models.BooleanField(default=False)
    allow_write_gpx = models.BooleanField(default=False)

class SchemaMigration(models.Model):
    version = models.CharField(max_length=255)


class Session(models.Model):
    id = models.BigIntegerField(primary_key=True)
    session_id =  models.CharField(max_length=255)
    DATA = models.TextField(null=True)
    created_at = NoTzDateTimeField()
    updated_at =  NoTzDateTimeField(null=True)
    objects = models.GeoManager()
   

class UserBlock(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    creator_id = models.BigIntegerField()
    reason = models.TextField()
    ends_at =  NoTzDateTimeField()
    needs_view = models.BooleanField(default=False)
    revoker_id= models.BigIntegerField()
    created_at =  NoTzDateTimeField(null=True)
    updated_at = NoTzDateTimeField(null=True)
    objects = models.GeoManager()

class UserPreference(models.Model):
    user_id = models.BigIntegerField()
    k =  models.CharField(max_length=255)
    v =   models.CharField(max_length=255)
    objects = models.GeoManager()

### need custom enum field 
class UserRole(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    created_at = NoTzDateTimeField(null=True)
    updated_at = NoTzDateTimeField(null=True)
    ### role user_role_enum NOT NULone NOT NULL,
    referer =  models.TextField(null=True)
    objects = models.GeoManager()

 

class User(models.Model):
    email = models.CharField(max_length=255)
    id =  models.BigIntegerField(primary_key=True)
    active = models.IntegerField(default=0)
    pass_crypt = models.CharField(max_length=255)
    creation_time = NoTzDateTimeField()
    display_name = models.CharField(max_length=255,default="") 
    data_public = models.BooleanField(default=False)
    description = models.TextField(default="")
    home_lat = models.FloatField(null=True)
    home_lon = models.FloatField(null=True)
    home_zoom = models.SmallIntegerField(default=3)
    nearby = models.IntegerField(default=50)
    pass_salt = models.CharField(null=True,max_length=255)
    image = models.TextField(null=True)
    email_valid =  models.BooleanField(default=False)
    new_email = models.CharField(max_length=255)
    visible  = models.BooleanField(default=True)
    creation_ip = models.CharField(max_length=255)
    languages = models.CharField(max_length=255,null=True)
    objects = models.GeoManager()

# how do you use types in django?

# CREATE TYPE gpx_visibility_enum AS ENUM (
#    'private',
#     'public',
#    'trackable',
#    'identifiable'
#);
 
#CREATE TYPE nwr_enum AS ENUM (
#    'node',
#    'way',
#    'relation'
#);


    









