import os, arcpy

class CreateDatabaseConnection:
    def __init__(self, path):
        self.path = path
        self.connection_file = path + "connection.sde"
    
    def create_connection(self):
        print "Checking if connection file already exists"
        
        if os.path.exists(self.connection_file):
            print("Connection file already exists, delete it")
            os.remove(self.connection_file)
        
        print("continue with creating connection file")
        file_name = "connection.sde"
        database_platform = "POSTGRESQL"
        instance = "localhost"
        port = "5432"
        auth_type = "DATABASE_AUTH"
        user_name = "postgres"
        password = "12345"
        save_user_info = "SAVE_USERNAME"
        database_name = "AICM-WORK"
        # database_name = "postgres"
        # database_name = "AICM7_RU"
        version = "SDE.Default"
        save_version_info = "SAVE_VERSION"
        
        try:
            arcpy.CreateDatabaseConnection_management(self.path, file_name, database_platform, instance, auth_type, 
            user_name, password, save_user_info, database_name)#, version, save_version_info)
            print("Connection file created successfully")
            #self.log.trace('SDE Connection created successfully')
            return True
        except arcpy.ExecuteError, ex:
            print("An error occurred in creating Connection file: {}".format(ex[0]))
            #self.log.error('Error occurred while creating connection file: ' + ex[0])
            return False