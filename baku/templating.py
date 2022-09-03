class Template:
    def __init__(self, file):
        self.text = open(file, 'r').read()
        self.segments = []
        at = 0

        # Split template into segments of raw text and code
        while (block := self.text.find('{{', at)) > -1:
            self.segments.append((at, block))
            at = self.text.find('}}', block) + 2
            self.segments.append((block, at))

        self.segments.append((at, len(self.text)))


    def render(self, context):
        result, i, segments = '', 0, self.segments[:]

        # Traverse all segments
        while i < len(segments):
            b, e = segments[i]
            
            # If even, this is a raw segment
            if not i & 1:
                # Append to result and continue
                result += self.text[b:e]
            else:
                # If not, replace with value from context
                token = self.text[b + 2:e - 2].strip()
                result += context[token]

            i += 1

        return result
