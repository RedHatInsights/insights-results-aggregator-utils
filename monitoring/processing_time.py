"""Processing time computation."""

l1 = int(input("Lag 1 hour ago: "))
l2 = int(input("Lag now: "))

incoming_rate = 2  # messages per second
lag_increase = l2 - l1

processing_speed = abs(lag_increase - incoming_rate*60*60)
print(f"Processing speed: {processing_speed} messages per hour")

processing_time = l2 / processing_speed

print(f"Processing time: {processing_time}")
