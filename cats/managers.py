from django.db import models

# db manager
class ImgManager(models.Manager):
    '''
    custom img model manager
    '''
    def get_queryset(self):
        return super(ImgManager, self).get_queryset().filter(img_status=0)

    def with_info(self, offset=0, limit=30):
        from django.db import connection
        result_list = []
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT i.id,i.img_src,i.img_from,i.img_desc,IFNULL(l.likes,0)likes,
                IFNULL(s.comments,0)comments,IFNULL(s.stars,0)stars FROM cat_imgs i 
                LEFT JOIN 
                (SELECT img_id,COUNT(DISTINCT user_id) likes FROM cats_pic_likes WHERE is_like=1 GROUP BY img_id ) l
                ON i.id=l.img_id
                LEFT JOIN 
                (SELECT img_id,comments,stars FROM cats_pic_stars) s 
                ON i.id=s.img_id
                WHERE img_status=0 LIMIT 30
                ''' )
            for row in cursor.fetchall():
                p = self.model(id=row[0], img_src=row[1], img_from=row[2], img_desc=row[3])
                p.n_likes = row[4]
                p.n_comments = row[5]
                p.n_stars = row[6]
                p.n_star = 0 if row[5]==0 else row[6]//row[5]
                result_list.append(p)
        return result_list

    def only_likes(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('''
            SELECT i.id,i.img_src,i.img_from,i.img_desc,l.likes,s.comments,s.stars FROM cat_imgs i 
            LEFT JOIN 
            (SELECT img_id,COUNT(DISTINCT user_id) likes FROM cats_pic_lisks WHERE is_like=1 GROUP BY img_id ) l
            ON i.id=l.img_id
            LEFT JOIN 
            (SELECT img_id,comments,stars FROM cats_pic_stars) s ON i.id=s.img_id) s 
            ON i.id=s.img_id
            WHERE likes>0
            ''')