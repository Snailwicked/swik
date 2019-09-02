from test.tasks import add
result = add.delay(4,5)
print(result.ready())
print(result.backend)