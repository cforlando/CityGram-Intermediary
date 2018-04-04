# CityGram-Intermediary
Intermediary API between CityGram and Orlando data sources  
CityGram - [GitHub - Code for America](https://github.com/codeforamerica/citygram)  
Orlando Intermediary - [Github - Code for Orlando](https://github.com/cforlando/CityGram-Intermediary)

# Services

## Voter Notifications

### Adding Election Data

Election info and dates live in a JSON file in cgorl/data/elections.json. Each election object is a dictionary which looks like the following:

```json
[
    {
        'title': 'Election Name',
        'date': '2018-01-01',
        'precints': 'all' | ['list', 'of', 'names'],
        'info': 'Other info about the election'
    },
    ...
]
```