# explorer

Talk to your data. Send in your data in PDF or JSON format.

### How to run
Create a virtualenv for convenience.
Install packages in requirements.txt using 
`pip install -r requirements.txt`

Run server using
`uvicorn main:app --reload`

### How to use
Use a Testing service like [Postman](https://www.postman.com/).

Send in your questions as a JSON file.
Send the context as a JSON or PDF file.

Sample [`questions.json`](./sample/questions.json)
```
[
  "What were the results of the Company's latest pen test, and what remediation was done?",
  "Does Company have an Incident Response Program?",
  "Does Company encrypt data in transit and at rest?",
  "Does company have career managers for engineers?",
  "What do you even do?"
]
```

Sample [context can be seen here](./sample/zaina.json)

Sample Postman request for reference

![image](https://github.com/sprajosh/explorer/assets/16593348/e463ad3b-f8eb-424a-9b9d-b7580bed458d)
