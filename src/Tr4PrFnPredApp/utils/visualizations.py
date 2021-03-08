from collections import deque


def create_d3_network_json_for_terms(terms, go_ont):
    """
        Create the json needed for d3.js network graphs based on GO terms.

        :param terms:
        :param go_ont:
        :return:
    """

    # list of all nodes to render in the graph
    nodes = []

    # list of node links
    links = []

    # create a set to ensure we do not have duplicate nodes
    go_set = set()

    # create a set to ensure we do not have duplicate links
    link_set = set()

    q = deque()

    for term in terms:
        # add the term we want to generate the network with
        # will create a network of all parent GO terms that lead to
        # this GO term
        q.append(term)

        while len(q) != 0:
            current = q.popleft()
            parents = go_ont.get_parents(current)
            for go in parents:
                if (go, current) not in link_set:
                    link_dict = {'source': go, 'target': current, 'stroke_width': 5}
                    links.append(link_dict)
                    link_set.add((go, current))

                q.append(go)

            if current not in go_set:
                go_dict = {'id': current, 'group': go_ont.get_namespace(current)}
                nodes.append(go_dict)
                go_set.add(current)

    return nodes, links


def create_d3_scatter_json_for_terms(all_terms_to_render):

    terms_score_dict_pairs = []

    for terms_to_render in all_terms_to_render:

        for name in list(terms_to_render.keys()):
            terms_score_dict = {'name': name, 'value': terms_to_render[name]}
            terms_score_dict_pairs.append(terms_score_dict)

    return terms_score_dict_pairs
