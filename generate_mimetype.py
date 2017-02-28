import pymysql.cursors
import zipfile
import os
import zipfile
from mimetypes import MimeTypes

def __get_mime(path):
    mime = MimeTypes()
    return mime.guess_type(path)[0]

def __connect_database():
    connection = pymysql.connect(host=os.environ['DB_HOST'],
                                 user=os.environ['DB_USER'],
                                 password=os.environ['DB_PASS'],
                                 db='medialibrary',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def __close_database(conn):
    conn.close()
    print('SQL connection to %s closed' % os.environ['DB_HOST'])


def __clean_dir():
    print('Cleanup of /payload')
    if os.path.exists('/payload/mimetype.txt'):
        os.remove('/payload/mimetype.txt')
    if os.path.exists('/payload/mimetype_cache.zip'):
        os.remove('/payload/mimetype_cache.zip')


def __generate_string(row):
    return row['regno'] + '\n' + __get_mime(row['master_file']) + '\n'


def __generate_text_line(line):
    if not os.path.exists('/payload'):
        os.makedirs('/payload')
    if not os.path.exists('/payload/mimetype.txt'):
        with open("/payload/mimetype.txt", "w") as myfile:
            myfile.write(line)
    else:
        with open("/payload/mimetype.txt", "a") as myfile:
            myfile.write(line)


def __generate_zip():
    zf = zipfile.ZipFile('/payload/mimetype_cache.zip',
                     mode='w',
                     compression=zipfile.ZIP_DEFLATED,
                     )
    try:
        print('Generating zip file')
        zf.write('/payload/mimetype.txt','mimetype.txt')
    finally:
        zf.close()
        os.remove('/payload/mimetype.txt')


def generate_mimetype():
    conn = __connect_database()
    __clean_dir()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM media")
            count = cursor.fetchone()['count(*)']
            batch_size = 100000 # whatever
            print('Found %s records' % count)
            for offset in range(0, int(count), batch_size):
                cursor.execute(
                    "SELECT regno,master_file FROM media LIMIT %s OFFSET %s",
                    (batch_size, offset))
                print('Batch %s of %s' % (offset,count))
                lines = ''
                for row in cursor:
                    lines = lines + __generate_string(row)
                __generate_text_line(lines)
    except Exception as e:
        print('Error: Failed to generate mimetype. %s' % e)
        __close_database(conn)
    finally:
        __generate_zip()
        __close_database(conn)

generate_mimetype()
