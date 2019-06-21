# Dealer Catalog Generator

MVP dealer catalog generator

Using the provided API here http://vautointerview.azurewebsites.net/swagger/ui/index(Now Expired), this program retrieves a datasetID, retrieves all vehicles and dealers for that dataset, and successfully posts to the answer endpoint. Each vehicle and dealer is requested only once. A response structure when you post to the answer endpoint that describes status and total ellapsed time will be returned; the program will output this response.

The server has a built in delay that varies between 1 and 4 seconds for each request for a vehicle or for a dealer. 
