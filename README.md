# CityGram-Intermediary
Intermediary API between CityGram and Orlando data sources  
CityGram - [GitHub - Code for America](https://github.com/codeforamerica/citygram)  
Orlando Intermediary - [Github - Code for Orlando](https://github.com/cforlando/CityGram-Intermediary)

# Usage
API is currently hosted on Azure at [http://orlando-citygram-api.azurewebsites.net]()  
You can run the code locally using `python3 app.py [service]`

# Making a New Service
In order to add a new service, you'll need to make a new class that extends service and implements makeTitle and makeGeoJSON. Then create a new entry in optionDict where the key string is the name of the service endpoint you want.

After the intermediary endpoint works and formats the message data correctly, we'll need to make a Ruby file to create our new Publisher. This will be used by the Citygram application itself. Use an existing .rb file in orlando-dev/services as a template. The pub.icon must be an icon found in the CityGram repository at app/assets/img/publishers/icons. If the one you want isn't there, design a new one and make a pull request. Once the .rb is ready, paste the code as an issue in CityGram for one of the admins to add it to the production database.

# Updating
The GitHub repository is set to automatically deploy changes to the Azure web application. Any commits pushed to the master branch will be automatically synced. We accept pull requests, so go ahead and fork the repo or request access. Message me on CfO Slack (@mdupont) or email me at [michael@mdupont.com](mailto:michael@mdupont.com) for more information.

# Services

## Police
Data source - [https://brigades.opendatanetwork.com/Transparency/Police-Dispatch-Calls/52xa-596i]()  
We filter police reports based on the reason. Many items aren't worth sending to people as a public notification. This includes reasons like patrol areas, shoplifting, and minor accidents. We also don't want to include reasons that have privacy implications or sensitive information like rape, domestic incidents, and downed officers.