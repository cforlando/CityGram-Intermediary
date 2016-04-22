# CityGram-Intermediary
Intermediary API between CityGram and Orlando data sources

# Usage
API is currently hosted on Azure at [http://orlando-citygram-api.azurewebsites.net](http://orlando-citygram-api.azurewebsites.net)

# Making a New Service
In order to add a new service, you'll need to make a new class that extends service and implements makeTitle and makeGeoJSON. Then create a new entry in optionDict where the key string is the name of the service endpoint you want.

After the intermediary endpoint works and formats the message data correctly, we'll need to make a Ruby file to create our new Publisher. This will be used by the Citygram application itself. Use an existing .rb file in orlando-dev/services as a template. The pub.icon must be an icon found in the CityGram repository at app/assets/img/publishers/icons. If the one you want isn't there, design a new one and make a pull request. Once the .rb is ready, paste the code as an issue in CityGram for one of the admins to add it to the production database.

# Updating
If anyone wants to push changes to the server, go ahead and fork the repo, message me on CfO Slack (@mdupont), or email me at [michael@mdupont.com](mailto:michael@mdupont.com)
