from collections import defaultdict
from tqdm import tqdm
def hyperlink_cleanup(str_link, language):
    link_prefix = f"https://{language}.wikipedia.org"
    if "/wiki/" in str_link:
        out = link_prefix + str_link
        if '#' in out:
            out = out.split('#')[0]
        if 'Wikipedia' in out:
            return False
        if 'Template' in out:
            return False
        return out
    else:
        return False

def get_category(input_list, EVENT_FILTER, PERSON_FILTER):
    event_score = 0
    person_score = 0
    for item in input_list:
        for E in EVENT_FILTER:
            if E in item.lower():
                event_score +=1
        for P in PERSON_FILTER:
            if P in item.lower():
                person_score +=1
    if not event_score and not person_score:
        return "none"
    return "event" if event_score > person_score else "person"

def df_get_url_list(df_wiki):
    return list(df_wiki.index)

def mask_list(base, to_mask):
    res = [o for o in to_mask if o in base]
    return res

def get_dict_reference_count(df_wiki):
    reference_count = defaultdict(lambda:0)

    url_list = df_get_url_list(df_wiki)
    for url in tqdm(url_list):
        references = df_wiki["LIST_REFERENCES"][url]
        references = mask_list(url_list, references)

        for url_ref in references:
            reference_count[(url, url_ref)] += 1

    return reference_count

def get_edge_list(df_wiki, directed=False):
    reference_count = get_dict_reference_count(df_wiki)

    edge_list = []
    url_list = df_get_url_list(df_wiki)
    for a in tqdm(url_list):
        for b in url_list:
            weight = reference_count[(a,b)]
            if not directed:
                weight += reference_count[(b,a)]
            if weight > 0:
                if directed:
                    edge_list.append((a, b, weight))
                elif not ((a, b, weight) in edge_list or (b, a, weight) in edge_list):
                    edge_list.append((a, b, weight))

    return edge_list

def generate_graph_with_node_attributes(graph, df_wiki):
    for node in graph.nodes:
        graph.nodes[node]['TYPE'] = df_wiki.TYPE[node]
        graph.nodes[node]['TOKENS'] = df_wiki.TOKENS[node]
        graph.nodes[node]['UNIQUE_TOKENS'] = df_wiki.UNIQUE_TOKENS[node]
    return graph

def get_subgraph(graph, attribute, values):
    nodes = (
        node for node, data in graph.nodes(data=True)
        if data.get(attribute) in values
    )
    return graph.subgraph(nodes)

def threshold_node_degree_undirected(graph, min=0, max=30):
    if graph.is_directed():
        raise Exception("Only use on undirected_graphs")
    nodes = (
        node for node, data in graph.nodes(data=True)
        if min <= graph.degree[node] <= max
    )
    return graph.subgraph(nodes)

def threshold_node_degree_directed(graph, min=[0, 0], max=[30,30]):
    if not graph.is_directed():
        raise Exception("Only use on directed graphs")
    if len(min) != 2:
        raise Exception("Min must be array of length 2")
    if len(max) != 2:
        raise Exception("Max must be array of length 2")
    nodes = (
        node for node, data in graph.nodes(data=True)
        if min[0] <= graph.in_degree[node] <= max[0]
        and min[1] <= graph.out_degree[node] <= max[1]
    )
    return graph.subgraph(nodes)

