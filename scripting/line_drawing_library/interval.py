class Interval:
    def __init__(self, lower, upper):
        self.min = min(lower, upper)
        self.max = max(lower, upper)
    
    @property
    def delta(self):
        return self.max - self.min

    def intersect(self, other):
        return self.max >= other.min and self.min <= other.max

    def force_merge(self, other):
        return Interval(min(self.min, other.min), max(self.max, other.max))
    
    def simple_repr(self):
        return "[{}, {}]".format(self.min, self.max)

    def as_tuple(self):
        return self.min, self.max

    def __mul__(self, other):
        d = self.delta*(other - 1.)
        return Interval(self.min - d, self.max + d)

    def __add__(self, other):
        if self.intersect(other):
            return self.force_merge(other)
        else:
            raise ValueError("these intervals {} and {} don't intersect".format(
                self.simple_repr(), other.simple_repr()
            ))

    def __eq__(self, other):
        return self.min == other.min and self.max == other.max

    def __lt__(self, other):
        return self.max <= other.min

    def __gt__(self, other):
        return self.min >= other.max

    def __repr__(self):
        return "Interval {}".format(self.simple_repr())

    @staticmethod
    def bounds(intervals):
        mins, maxs = zip(*[i.as_tuple() for i in intervals])

        return Interval(min(mins), max(maxs))

if __name__ == "__main__":
    an_int = Interval(0, 1)
    an_int_half = Interval(1.5, 2.5)
    an_int_2 = Interval(1, 2)
    an_int_3 = Interval(2, 3)

    print(an_int)
    print(an_int+an_int_2)
    print(an_int < an_int_half)
    print(an_int == an_int_2)
    print(Interval.bounds([an_int, an_int_2, an_int_half]))
    print(an_int_3 + an_int)
