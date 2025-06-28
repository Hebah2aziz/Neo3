from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    Represents a celestial object that comes close to Earth,
    encapsulating its primary orbital and physical characteristics.

    Attributes:
        designation (str): The unique identifier for the NEO.
        name (str or None): An optional human-friendly name.
        diameter (float or None): The diameter in kilometers.
        hazardous (bool): Whether the NEO is potentially hazardous.
        approaches (list): List of CloseApproach instances.
    """

    def __init__(self, designation, name=None, diameter=None, hazardous=False):
        self.designation = designation
        self.name = name
        self.diameter = diameter
        self.hazardous = hazardous
        self.approaches = []  # Will be filled by NEODatabase

    @property
    def fullname(self):
        """Return a complete name for this NEO."""
        if self.name:
            return f"{self.designation} ({self.name})"
        return self.designation

    def __str__(self):
        """Return a human-readable string representation of this object."""
        hazardous_status = "is" if self.hazardous else "is not"
        return (
            f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km "
            f"and {hazardous_status} potentially hazardous."
        )

    def __repr__(self):
        """Return a computer-readable string representation of this object."""
        return (
            f"NearEarthObject(designation={self.designation!r}, "
            f"name={self.name!r}, diameter={self.diameter:.3f}, "
            f"hazardous={self.hazardous!r})"
        )


class CloseApproach:
    """A close approach to Earth by an NEO.

    Represents a single approach event with timing, distance, and
    relative velocity, along with a reference to the associated NEO.

    Attributes:
        designation (str): The NEO's designation.
        time (datetime): Time of closest approach (converted).
        distance (float): Approach distance in astronomical units.
        velocity (float): Approach speed in kilometers per second.
        neo (NearEarthObject): The associated NEO (set later).
    """

    def __init__(self, designation, time, distance, velocity):
        self.designation = designation
        self.time = cd_to_datetime(time)
        self.distance = distance
        self.velocity = velocity
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this CloseApproach's approach time."""
        return datetime_to_str(self.time)

    def __str__(self):
        """Return a human-readable string representation of this object."""
        name = self.neo.fullname if self.neo else self.designation
        return (
            f"On {self.time_str}, '{name}' approaches Earth at a distance of "
            f"{self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."
        )

    def __repr__(self):
        """Return a computer-readable string representation of this object."""
        return (
            f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
        )
