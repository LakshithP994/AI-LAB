class VacuumCleaner:
    def __init__(self):
        # Initial state: both rooms dirty
        self.environment = {"A": "Dirty", "B": "Dirty"}
        self.current_position = "A"  # Start at A

    def clean(self):
        if self.environment[self.current_position] == "Dirty":
            print(f"Cleaning location {self.current_position}")
            self.environment[self.current_position] = "Clean"
        else:
            print(f"Location {self.current_position} already clean")

    def left(self):
        print("Moving to Left (A)")
        self.current_position = "A"

    def right(self):
        print("Moving to Right (B)")
        self.current_position = "B"

    def run(self):
        print(f"Initial State: {self.environment}, Position: {self.current_position}")
        
        # Clean current position
        self.clean()

        # Move right and clean
        self.right()
        self.clean()

        # Move left back (optional, if you want agent to return home)
        self.left()

        print(f"Final State: {self.environment}, Position: {self.current_position}")


# Run the simulation
vacuum = VacuumCleaner()
vacuum.run()
