import random 

# Table hardcoded from:
# https://www.washingtonpost.com/news/the-fix/wp/2014/10/21/lets-rank-the-media-from-liberal-to-conservative-based-on-their-audiences/?utm_term=.0df4726d156b
BIAS_TABLE = {
  'new yorker': 11,
  'slate': 11,
  'daily show': 10,
  'the guardian': 10,
  'al jazeera america': 10,
  'npr': 10,
  'colbert report': 10,
  'new york times': 10,
  'nytimes.com': 10,
  'buzzfeed': 9,
  'pbs': 9,
  'bbc': 9,
  'huffington post': 9,
  'washington post': 9,
  'the economist': 9,
  'politico': 9,
  'msnbc': 8,
  'cnn': 7,
  'nbc news': 6,
  'cbs news': 5,
  'google news': 5,
  'bloomberg': 5,
  'abc news': 5,
  'usa today': 5,
  'yahoo news': 4,
  'wall street journal': 4,
  'fox news': 3,
  'drudge report': 2,
  'breitbart': 1,
  'rush limbaugh show': 1,
  'the blaze': 1,
  'sean hannity show': 1,
  'glenn beck program': 1
}

class PewExtractor():
    def __init__(self):
      self.num_suggestions = 3

    def get_ordering(self, source, suggestions):

      def sanitizeSrc(s):
        return s.lower().strip()

      def biasValue(elem):
        matches = [x for x in BIAS_TABLE.keys() if elem.find(x) != -1]
        if len(matches) >= 1:
          return BIAS_TABLE[matches[0]]
        return -1

      # Get the bias of the article you are currently on
      bias_source = biasValue(sanitizeSrc(source))

      def diffBias(entry):
        sugg_src = entry["providers"][0] # TODO: run through all the providers when querying

        bias_sugg_src = biasValue(sanitizeSrc(sugg_src))
        if bias_source >= 0:
          if bias_sugg_src >= 0:
            return abs(bias_source - bias_sugg_src)
          else:
            return -1

        # If the original source is not in BIAS_TABLE, we check that the suggested is not a duplicate
        if source.find(sugg_src) != -1 or sugg_src.find(source) != -1:
          return -1

        return random.randint(0, len(suggestions))


      sorted_suggestions = sorted(suggestions, key=lambda x: diffBias(x), reverse=True)
      return sorted_suggestions[:self.num_suggestions] 

      

