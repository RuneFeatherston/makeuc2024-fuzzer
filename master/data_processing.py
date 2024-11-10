import logging
import random
from scapy.all import IP, TCP, send
from scapy.layers.inet import RandInt, RandShort
import socket
import sys

# Function to check each flag type and increment the corresponding count in the dictionary
def checkFlag(flagType):
    """
    Checks the flags in the TCP header and increments the count for each flag type.
    """
    # Dictionary to store counts for each flag type
    countFlags = {
        "SYN": 0,  # Synchronize flag
        "ACK": 0,  # Acknowledgment flag
        "FIN": 0,  # Finish flag
        "RST": 0,  # Reset flag
        "PSH": 0,  # Push flag
        "URG": 0,  # Urgent flag
        "ECE": 0,  # ECN Echo flag
        "CWR": 0   # Congestion Window Reduced flag
    }

    # Check the flag type and increment the dictionary value accordingly
    if "S" in flagType:  # If "SYN" flag is set
        countFlags["SYN"] += 1
    if "A" in flagType:  # If "ACK" flag is set
        countFlags["ACK"] += 1
    if "F" in flagType:  # If "FIN" flag is set
        countFlags["FIN"] += 1
    if "R" in flagType:  # If "RST" flag is set
        countFlags["RST"] += 1
    if "P" in flagType:  # If "PSH" flag is set
        countFlags["PSH"] += 1
    if "U" in flagType:  # If "URG" flag is set
        countFlags["URG"] += 1
    if "E" in flagType:  # If "ECE" flag is set
        countFlags["ECE"] += 1
    if "C" in flagType:  # If "CWR" flag is set
        countFlags["CWR"] += 1

    # Return the dictionary with the updated flag counts
    return countFlags


# Function to check and categorize sequence size (sequence number)
def checkSequenceSize(sequenceNum):
    """
    Categorizes the sequence number into small, medium, or large size based on its value.
    """
    # Dictionary to track sequence size ranges
    countSequenceSizes = {'small': 0, 'medium': 0, 'large': 0}
    
    # Define size ranges for sequence numbers (these can be adjusted as needed)
    if sequenceNum < 1000:  # Small sequence number (arbitrary threshold)
        countSequenceSizes['small'] += 1
    elif 1000 <= sequenceNum < 10000:  # Medium sequence number
        countSequenceSizes['medium'] += 1
    else:  # Large sequence number
        countSequenceSizes['large'] += 1

    # Return the categorized sequence size counts
    return countSequenceSizes


# Function to check and categorize payload size into small, medium, or large
def checkPayloadSize(payloadSize):
    """
    Categorizes the payload size into small, medium, or large based on its size.
    """
    # Dictionary to track how many packets fall into each payload size category
    countPayloads = {'small': 0, 'medium': 0, 'large': 0}
    
    # Define size ranges for payload (you can adjust these thresholds as needed)
    if payloadSize < 100:  # Small payload
        countPayloads['small'] += 1
    elif 100 <= payloadSize < 1000:  # Medium payload
        countPayloads['medium'] += 1
    else:  # Large payload
        countPayloads['large'] += 1

    # Return the categorized payload size counts
    return countPayloads


# Function to check and categorize TTL (Time-To-Live) values
def checkTTL(ttlValue):
    """
    Categorizes the TTL value into low, medium, or high based on its value.
    """
    # Dictionary to track TTL value ranges
    countTTL = {'low': 0, 'medium': 0, 'high': 0}
    
    # Define TTL ranges (these can be adjusted as needed based on your observations)
    if ttlValue < 32:  # Low TTL
        countTTL['low'] += 1
    elif 32 <= ttlValue < 64:  # Medium TTL
        countTTL['medium'] += 1
    else:  # High TTL
        countTTL['high'] += 1

    # Return the categorized TTL counts
    return countTTL


# Function to analyze each crash event by checking all attributes
def AnalyzeEvent(CrashEvent):
    """
    Analyzes each crash event by checking its flags, sequence size, payload size, and TTL.
    """
    # Check flags for the current crash event
    flagCounts = checkFlag(CrashEvent.flag)

    # Check sequence size for the current crash event
    sequenceSizeCounts = checkSequenceSize(CrashEvent.sequenceNum)

    # Check payload size for the current crash event
    payloadSizeCounts = checkPayloadSize(CrashEvent.payloadSize)

    # Check TTL value for the current crash event
    ttlCounts = checkTTL(CrashEvent.ttl)

    # Log the results of each attribute's analysis
    logging.info(f"Flags: {flagCounts}")
    logging.info(f"Sequence Size: {sequenceSizeCounts}")
    logging.info(f"Payload Size: {payloadSizeCounts}")
    logging.info(f"TTL: {ttlCounts}")

    # Return all the counts for further processing if needed
    return flagCounts, sequenceSizeCounts, payloadSizeCounts, ttlCounts


# Function to analyze all the crash data by looping through each event
def AnalyzeData(CrashData):
    """
    Analyzes the entire crash data by looping through all crash events and aggregating the counts for each attribute.
    """
    # Dictionaries to store the aggregated counts for each attribute
    allFlagCounts = {}
    allSequenceSizeCounts = {}
    allPayloadSizeCounts = {}
    allTTLCounts = {}

    # Loop through each crash event in the CrashData
    for crashEvent in CrashData:
        # Analyze the event and get the counts for each attribute
        flagCounts, sequenceSizeCounts, payloadSizeCounts, ttlCounts = AnalyzeEvent(crashEvent)

        # Aggregate the flag counts for all events
        for flag, count in flagCounts.items():
            if flag not in allFlagCounts:
                allFlagCounts[flag] = count
            else:
                allFlagCounts[flag] += count

        # Aggregate the sequence size counts for all events
        for size, count in sequenceSizeCounts.items():
            if size not in allSequenceSizeCounts:
                allSequenceSizeCounts[size] = count
            else:
                allSequenceSizeCounts[size] += count

        # Aggregate the payload size counts for all events
        for size, count in payloadSizeCounts.items():
            if size not in allPayloadSizeCounts:
                allPayloadSizeCounts[size] = count
            else:
                allPayloadSizeCounts[size] += count

        # Aggregate the TTL counts for all events
        for ttl, count in ttlCounts.items():
            if ttl not in allTTLCounts:
                allTTLCounts[ttl] = count
            else:
                allTTLCounts[ttl] += count

    # Log the aggregated counts for all attributes
    logging.info(f"Aggregated Flag Counts: {allFlagCounts}")
    logging.info(f"Aggregated Sequence Size Counts: {allSequenceSizeCounts}")
    logging.info(f"Aggregated Payload Size Counts: {allPayloadSizeCounts}")
    logging.info(f"Aggregated TTL Counts: {allTTLCounts}")
