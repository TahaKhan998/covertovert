Covert Storage Channel that Exploits Packet Bursting using DNS [Code: CSC-PB-DNS]

Approach and Concept:

For this covert channel, we used Packet Bursting to encode and decode messages. The number of packets sent in each burst represents the encoded bits:

- 2 packets in a burst represent a binary 1.
- 3 packets in a burst represent a binary 0.

Additionally, a burst time interval separates consecutive bursts. This idle time between bursts lets us know that the receiver can process and tell each burst apart, even in environments with network delays or jitter. At the end of the transmission, a final packet is sent to show the conclusion of the message.

The design makes use of the fact that the receiver is aware of the encoding rules and the burst timing. This synchronization allows for decoding the message based on the number of packets received in each burst.

Implementation Highlights:

1. Encoding the Message:

- A binary message is generated using generate_random_binary_message_with_logging().
- Each bit is encoded as either 2 packets (for 1) or 3 packets (for 0).
- After each burst, the program waits for the specified burst_time before sending the next burst.

2. Decoding the Message:

- The receiver receives packets using sniff() on UDP port 53.

- It counts the number of packets received within a time window and decodes them based on the already defined encoding rules.

3. Challenges and Solutions:

- Challenge: Smaller burst times (e.g., 1 second) caused decoding errors due to insufficient idle time between bursts, as network jitter made it difficult to distinguish packet boundaries.

- Solution: We used a burst time of 2 seconds to ensure reliable decoding, even in normal network conditions.

Key Decisions and Testing:

1. Burst Time Selection:

We initially tested with a burst time of 1 second, which achieved a total transmission time of approximately 790 seconds for 128 bits.
However, the error rate with a burst time of 1 was higher due to insufficient time for the receiver to process packets properly.
With a burst time of 2 seconds, the transmission took slightly longer (895 seconds for 128 bits) but provided significantly more reliable results, with zero errors observed during testing.
While a shorter burst time increases the channel capacity (bits per second), reliability was prioritized for this implementation.

2. Channel Capacity:

With a burst time of 2 seconds, the average covert channel capacity was calculated as:
Capacity= Message Length (128 bits) / Total Time (895.55 seconds) = 0.14 bits/second.

Although the capacity is low, the reliability ensures the transmitted message is decoded correctly without errors.

3. Protocol Selection:

- We used DNS over UDP packets for their lightweight nature and ease of crafting using the scapy library.

Conclusion:

The assignment was both challenging and enlightening, as it required balancing transmission speed and reliability. We found that using a burst time of 2 seconds provided the best trade-off between these factors in our network environment. While the covert channel capacity is low compared to other methods, the technique demonstrates a robust encoding mechanism that ensures reliable communication in a covert manner.
