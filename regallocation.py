class Interval:
    """Represents a live range for a variable."""
    def __init__(self, name, start, end):
        self.name = name  # Variable name
        self.start = start  # Start of live range
        self.end = end  # End of live range
        self.register = None  # Assigned register, initially None

    def __repr__(self):
        return f"{self.name} [{self.start}, {self.end}] -> {self.register}"


class RegisterAllocator:
    """Linear scan register allocator."""
    def __init__(self, num_registers):
        self.num_registers = num_registers  # Total physical registers
        self.active = []  # List of active intervals
        self.registers = [f"R{i}" for i in range(num_registers)]  # Register names

    def expire_old_intervals(self, current):
        """Remove intervals that are no longer active."""
        self.active = [interval for interval in self.active if interval.end >= current]

    def allocate_register(self, interval):
        """Assign a register to the current interval or spill."""
        if len(self.active) < self.num_registers:
            # Allocate a register
            for reg in self.registers:
                if reg not in [i.register for i in self.active]:
                    interval.register = reg
                    self.active.append(interval)
                    self.active.sort(key=lambda x: x.end)  # Sort by end time
                    return
        else:
            # Spill the interval with the farthest end
            spill = max(self.active, key=lambda x: x.end)
            if spill.end > interval.end:
                interval.register = spill.register  # Reassign register
                spill.register = None  # Spill to memory
                self.active.remove(spill)
                self.active.append(interval)
                self.active.sort(key=lambda x: x.end)
            else:
                interval.register = None  # Spill current interval

    def allocate(self, intervals):
        """Main allocation function."""
        intervals.sort(key=lambda x: x.start)  # Sort intervals by start time
        for interval in intervals:
            self.expire_old_intervals(interval.start)
            self.allocate_register(interval)

        return intervals


# Example usage
if __name__ == "__main__":
    # Example intervals: [Variable Name, Start, End]
    intervals = [
        Interval("a", 0, 5),
        Interval("b", 2, 7),
        Interval("c", 4, 9),
        Interval("d", 6, 10),
        Interval("e", 8, 11)
    ]

    # Instantiate allocator with 3 physical registers
    allocator = RegisterAllocator(num_registers=3)
    result = allocator.allocate(intervals)

    # Print allocation results
    for interval in result:
        print(interval)
