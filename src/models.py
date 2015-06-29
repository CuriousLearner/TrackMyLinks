from src import db

class Tags(db.EmbeddedDocument):
    tag_name = db.StringField()
    
    def __unicode__(self):
        return str(self.tag_name)
    
    def get_dict(self):
        return { 'tag_name' : self.tag_name}
    
    def __repr__(self):
        return 'tag_name ' + str(self.tag_name)

class Resource(db.Document):
    rid = db.IntField(unique=True)
    title = db.StringField()
    link = db.StringField()
    tags = db.ListField(db.EmbeddedDocumentField('Tags'))
    description = db.StringField()

    def __unicode__(self):
        return str(self.rid)

    def get_dict(self):
        return { 'rid': self.rid,
                 'title': self.title,
                 'link': self.link,
                 'tags': self.tags, 
                 'description': self.description}

    def __repr__(self):
        return 'rid ' + str(self.rid)


    def save(self, *args, **kwargs):
        if self.rid == None:
            try:
                self.rid = self.__class__.objects.order_by('-rid')[0].rid + 1
            except IndexError:
                self.rid = Resource.objects.count() + 1

        super(Resource, self).save(*args, **kwargs)