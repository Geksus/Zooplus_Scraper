import csv
from six.moves import urllib
import json

response = urllib.request.urlopen(
    'https://www.zooplus.de/tierarzt/api/v2/token?debug=authReduxMiddleware-tokenIsExpired').read()
token_json = json.loads(response)

req = urllib.request.Request('https://www.zooplus.de/tierarzt/api/v2/results?animal_99=true&page=1&from=0&size=100')
req.add_header('authority', 'www.zooplus.de')
req.add_header('accept', 'application/json')
req.add_header('authorization', 'Bearer ' + token_json['token'])
req.add_header('x-api-authorization', token_json['token'])


response = urllib.request.urlopen(req).read()
result_json = json.loads(response)

result = []

for item in result_json['results']:
    subtitle = ""
    try:
        subtitle = item['subtitle']
    except KeyError:
        pass

    result.append(
        [item['name'].strip(),
         subtitle.strip(),
         item['open_time'],
         item['city'].strip(),
         item['address'].strip(),
         item['count_reviews'],
         item['avg_review_score']]
    )

with open('tieraertze.csv', 'a', encoding='utf8') as file:
    writer = csv.writer(file)

    writer.writerow(
        (
            'Name',
            'Subtitle',
            'Open time',
            'City',
            'Address',
            'Reviews',
            'Score'
        )
    )

    writer.writerows(result)

