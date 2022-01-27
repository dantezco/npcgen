class MarkovModel:
    def __init__(self, payload: dict):
        self.fields = payload.get("fields").split(",")
        self.payload = payload

    def parse_markov_payload(self) -> list[list[float]]:
        markov_mapping = []
        for from_field in self.fields:
            line = []
            for to_field in self.fields:
                line.append(float(self.payload.get(f"{from_field}_to_{to_field}")))
            markov_mapping.append(line)
        return markov_mapping

    @staticmethod
    def validate_line_weights(map_line: list):
        if sum(map_line) <= 1:
            highest_value = map_line.index(max(map_line))
            missing = 1 - sum(map_line)
            map_line[highest_value] += missing

    def fill_zeroed_weights(self, node: list[float]):
        zeros_index = []
        current_total = 0
        for i, weight in enumerate(node):
            if weight == 0.0:
                zeros_index.append(i)
            else:
                current_total += weight
        missing = 1.0 - current_total
        filling = missing / len(zeros_index) if zeros_index else missing
        for pos in zeros_index:
            node[pos] = filling

    def balance_mapping(self, mapping: list[list[float]]):
        for node in mapping:
            if sum(node) > 1:
                raise ValueError(f"Line {node} adds up to more than 1: {sum(node)}")
            self.fill_zeroed_weights(node=node)
            self.validate_line_weights(map_line=node)
        return mapping

    def process_form(self):
        markov_mapping_raw = self.parse_markov_payload()
        balanced_mapping = self.balance_mapping(markov_mapping_raw)
        return balanced_mapping
