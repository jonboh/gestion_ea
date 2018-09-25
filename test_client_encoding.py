import client

new_client = client.Client(observations='Billy/#nHello Billy')


print(new_client.encode_observations())

print(new_client.decode_observations(new_client.observations))

print(new_client.observations)