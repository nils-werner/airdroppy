class BoundaryStripper(object):
    def __init__(self):
        self.initialized = False

    def process(self, data):
        trimmed = data.splitlines()
        tmp = data.splitlines(True)

        if not self.initialized:
            self.boundary = trimmed[0].strip()
            tmp = tmp[1:]
            trimmed = trimmed[1:]
            self.initialized = True

            try:
                firstelem = trimmed[:5].index("")
                tmp = tmp[firstelem + 1:]
                trimmed = trimmed[firstelem + 1:]
            except ValueError:
                pass

        try:
            lastelem = trimmed.index(self.boundary + "--")
            self.initialized = False
            return "".join(tmp[:lastelem - 1])
        except ValueError:
            return "".join(tmp)
