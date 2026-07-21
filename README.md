*** REQUIREMENTS ***
- Paramiko 2.12
- Python 3.12.7
- Directories for the inventory and generated reports
- An .env file with the credentials of the SSH conection like this:
    SSH_USER=user
    SSH_PASSWORD=password


NOTE: The folders must be specifically "Inventario" and "Reportes". Alternatively, you can modify the destination paths directly in the code. 


*** FUNCTIONALITY ***
This code executes a ping command and establishes an SSH connection with remote devices to verify their connectivity, retrieving the inventory from an .xlsx file; the user must specify ONLY the name of this inventory, THERE IS NO NEED TO WRITE THE TYPE OF FILE, IT ALREADY FILLS with .xlsx, if there´s another type of file used you must modify the file. At the end of the execution it automatically generates a report file where the state of each ping and connection is detailed individually.
