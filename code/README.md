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

- Challenge:

--During testing, we experimented with shorter burst times of 1 second, 0.5 seconds, and 0.2 seconds. These worked perfectly in our controlled environment without causing any decoding errors or synchronization issues.

--However, in cases where testers encounter packet loss, network delays, or jitter in different environments, shorter burst times might lead to errors in decoding.

- Solution:

--While shorter burst times provide faster transmission, testers should consider increasing the burst time (e.g., to 1 or 2 seconds) if they experience any reliability issues during decoding.

--Adjusting the burst time allows the receiver to better process and separate bursts under challenging network conditions.

Key Decisions and Testing:

1. Burst Time Selection:

We initially tested with a burst time of 1 second, which worked without any issues.

Next, we tested with a shorter burst time of 0.5 seconds, which also worked perfectly in our controlled environment. This reduced the total transmission time to 91.8 seconds, achieving a significantly improved bit rate of 1.39 bits/second.

Finally, we tested with an even shorter burst time of 0.2 seconds, which again performed well without any decoding errors. This further reduced the transmission time to 53.4 seconds, yielding an impressive bit rate of 2.40 bits/second.

While these shorter burst times demonstrated faster transmission and worked reliably in our environment, testers experiencing network delays, jitter, or packet loss might encounter decoding issues. In such cases, we recommend increasing the burst time (e.g., to 1 or 2 seconds) to improve reliability under challenging network conditions.

2. Channel Capacity:

With a burst time of 0.2 seconds, the average covert channel capacity was calculated as:

Capacity = Message Length (128 bits)/Total Time (53.4 seconds) ≈ 2.40 bits/second.

This significantly higher capacity demonstrates the efficiency of using shorter burst times. Despite the faster transmission, the reliability of the channel was maintained in our controlled environment, with all bits decoded correctly without errors. However, in less stable network conditions, a longer burst time may be needed to ensure consistent decoding

3. Protocol Selection:

- We used DNS over UDP packets for their lightweight nature and ease of crafting using the scapy library.

Conclusion:

The assignment was both challenging and enlightening, as it required balancing transmission speed and reliability. Through testing, we found that shorter burst times, such as 0.5 seconds and 0.2 seconds, provided significantly faster transmission rates, with bit rates of 1.39 bits/second and 2.40 bits/second, respectively, while maintaining reliability in our controlled environment.

To calculate covert channel capacity and total transmission time, we initially implemented the necessary calculations in our code. However, these calculations have been commented out in the final implementation to streamline the code for the covert channel’s primary functionality. Testers can uncomment these sections if they wish to measure performance metrics during their own testing.

This demonstrates the efficiency of the approach when network conditions are favorable. However, for scenarios with potential network delays or jitter, increasing the burst time (e.g., to 1 or 2 seconds) ensures consistent and reliable decoding.

Overall, the technique showcases a robust and adaptable encoding mechanism for covert communication, balancing flexibility, speed, and reliability effectively.
