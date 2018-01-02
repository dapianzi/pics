from django.db import models

# db manager
class ImgManager(models.Manager):
    '''
    custom img model manager
    '''
    def with_info(self):
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
            ''')
        result_list = []
        for row in cursor.fetchall():
            p = self.model(id=row[0], question=row[1], stars=row[3])
            p.num_responses = row[3]
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