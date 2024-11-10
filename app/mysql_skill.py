from mindsdb_sdk import connect
import mysql.connector
from typing import Dict
from mindsdb_sdk.skills import BaseSkill

class MySQLSkill(BaseSkill):
    # Define the required arguments for the skill
    ARGUMENTS = {
        'host': {'type': str, 'description': 'MySQL host address'},
        'user': {'type': str, 'description': 'MySQL username'},
        'password': {'type': str, 'description': 'MySQL password'},
        'database': {'type': str, 'description': 'MySQL database name'},
        'query': {'type': str, 'description': 'SQL query to execute'}
    }

    def connect_to_mysql(self, params: Dict) -> mysql.connector.connection.MySQLConnection:
        """Establish connection to MySQL database"""
        try:
            connection = mysql.connector.connect(
                host=params['host'],
                user=params['user'],
                password=params['password'],
                database=params['database']
            )
            return connection
        except mysql.connector.Error as err:
            raise Exception(f"Failed to connect to MySQL: {err}")

    def execute_query(self, connection: mysql.connector.connection.MySQLConnection, query: str) -> list:
        """Execute SQL query and return results"""
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            raise Exception(f"Error executing query: {err}")

    def run(self, params: Dict) -> Dict:
        """Main method to execute the skill"""
        try:
            # Connect to MySQL
            connection = self.connect_to_mysql(params)
            
            # Execute the query
            results = self.execute_query(connection, params['query'])
            
            # Close connection
            connection.close()
            
            return {'status': 'success', 'results': results}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

# Initialize MindsDB connection
server = connect()

# Register the skill
server.skills.create(
    name='mysql_skill',
    skill_class=MySQLSkill,
    description='A skill to connect to MySQL and execute queries'
)

# Example usage
params = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database',
    'query': 'SELECT * FROM your_table LIMIT 5'
}

# Execute the skill
result = server.skills.mysql_skill.run(params)
print(result)