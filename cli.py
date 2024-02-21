import fire
from datetime import datetime
import subprocess
import pymysql


class Backup(object):
    """ Comando para generar un respaldo de la base de datos.
        USO: py cli.py backup COMMAND
    """
    def run(self):
      # Generar el backup mysql+pymysql://huber:huber123@localhost/app_flujo_caja'
      name="app_flujo_caja"
      user="huber"
      password="huber123"
      host="localhost"

      date = datetime.now()
      filename = f"backup/backup-{date.strftime('%Y-%m-%d_%H-%M')}.sql"
      print("|Filename: ",filename)

      # Comando para hacer un respaldo con mysqldump (para MySQL)
      cmd = f"mysqldump -u {user} -p{password} -h {host} {name} > {filename}"
      print("|Comando: ",cmd)
      try:
          # Ejecutar el comando
          subprocess.run(cmd, shell=True, check=True)
          return f"Backup generado exitosamente en {filename}"
      except subprocess.CalledProcessError as e:
          return f"Error al generar el backup: {e}"


class Restore(object):

    def run(self, filename):
        """ filename = backup/backup-2024-02-19_17-09.sql """
        # datos
        name="app_flujo_caja"
        user="huber"
        password="huber123"
        host="localhost"
        
        print("|Filename: ",filename)
        print("|Creando base de datos: ",name)
        cmd = f"mysql -u {user} -p{password} -h {host} {name} -e 'CREATE DATABASE {name}' "
        try:
            # Conectar a MySQL (puedes ajustar la conexión según tus necesidades)
            connection = pymysql.connect(host=host, user=user, password=password)

            with connection.cursor() as cursor:

              # Comando SQL para crear la base de datos
              create_db_query = f"CREATE DATABASE {name}"
              cursor.execute(create_db_query)

              # Confirmar la transacción
              connection.commit()
            print(f"Base de datos '{name}' creada exitosamente.")
        except Exception as e:
            print (f"Error al restaurar la base de datos: {e}")
        
        print("|Restaurando base de datos con backup: ",filename)
        # Restaurando la base de datos desde el archivo SQL
        cmd = f"mysql -u {user} -p{password} -h {host} {name} < {filename}"
        print("|Comando: ",cmd)
        try:
            # Ejecutar el comando
            subprocess.run(cmd, shell=True, check=True)
            return f"Base de datos restaurada exitosamente desde {filename}"
        except subprocess.CalledProcessError as e:
            return f"Error al restaurar la base de datos: {e}"


class Pipeline(object):

  def __init__(self):
    self.backup = Backup()
    self.restore = Restore()

  def run(self,data):
    """ backup = self.backup.run()
    restore = self.restore.run()
    return [backup, restore] """
    return data

if __name__ == '__main__':
  fire.Fire(Pipeline)