

test = {
    "a":1,
    "b":2,
    "ac":3
}

a=[*test.values()]

{'$and': [{'facultyName': '国際高等教育院'}, {'accepted.0': {'$gt': 15}},{'$expr': {'$gt': ['accepted.0', {'$multiply': [0.8, '$accepted']}]}}]}