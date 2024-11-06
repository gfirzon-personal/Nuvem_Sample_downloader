import http.client
import os
import ssl
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import settings
import azureSettings

# Create an unverified SSL context
context = ssl._create_unverified_context()

# Azure Blob Storage connection string and container name
connection_string = azureSettings.azure_storage_connection_string
container_name = settings.azure_storage_container_name
blob_name = settings.blob_name

#conn = http.client.HTTPSConnection("340bopais.hrsa.gov")
conn = http.client.HTTPSConnection("340bopais.hrsa.gov", context=context)

payload = settings.payload
headers = settings.headers

conn.request("POST", "/reports?AspxAutoDetectCookieSupport=1", payload, headers)
res = conn.getresponse()

#save_directory = 'D:\\Test'
#save_directory = 'c:\\data'
#os.makedirs(save_directory, exist_ok=True)
#file_path = os.path.join(save_directory, 'output.xlsx')

# Check if the response is successful and content type is Excel
if res.status == 200 and res.getheader('Content-Type').startswith('application/vnd'):
    print("Starting file download...")

    # Read data from the response
    data = res.read()

    # Create a BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get a container client
    container_client = blob_service_client.get_container_client(container_name)

    # Upload the file to the container
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(data, overwrite=True)    
    print("File uploaded to Azure Blob Container successfully.")

    # Write the response data to an Excel file
    # with open(file_path, 'wb') as f:
    #     f.write(data)
    #print("file downloaded successfully.")

else:
    print(f"Failed to download file: {res.status} {res.reason}")

# Close the connection
conn.close()
