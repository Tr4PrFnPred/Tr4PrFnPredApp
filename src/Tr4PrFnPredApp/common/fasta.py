
class FastaRule():

    @staticmethod
    def check_rule(fasta: str) -> bool:
        pass


class CheckEmpty(FastaRule):

    @staticmethod
    def check_rule(fasta: str) -> bool:
        return not fasta


class CheckTags(FastaRule):

    @staticmethod
    def check_rule(fasta: str) -> bool:

        return fasta.startswith(">")


class CheckInvalidCharacters(FastaRule):

    @staticmethod
    def get_sequences(fasta: str) -> list:
        split_by = fasta.split(">")

        return list(map(lambda sequence: "".join(sequence.split("\n")[1:]), split_by))

    def check_rule(self, fasta: str) -> bool:
        sequences = self.get_sequences(fasta)
        for sequence in sequences:
            if not sequence.isalpha():
                return False
        return True

