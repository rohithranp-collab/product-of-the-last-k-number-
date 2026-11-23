class ProductOfNumbers(object):

    def __init__(self):
        self.stream = []
        self.prefix = []
        self.zeros = []  # indices in self.stream where num == 0

    def add(self, num):
        """
        :type num: int
        :rtype: None
        """
        idx = len(self.stream)
        self.stream.append(num)

        if num == 0:
            self.zeros.append(idx)
            # Keep prefix non-zero so future divisions never divide by 0
            prev = self.prefix[-1] if self.prefix else 1
            self.prefix.append(prev)
        else:
            prev = self.prefix[-1] if self.prefix else 1
            self.prefix.append(prev * num)

    def getProduct(self, k):
        """
        :type k: int
        :rtype: int
        """
        n = len(self.stream)
        start = n - k

        # Check if the most recent zero falls at or after `start`
        if self.zeros and self.zeros[-1] >= start:
            return 0

        if start == 0:
            return self.prefix[-1]
        return self.prefix[-1] // self.prefix[start - 1]