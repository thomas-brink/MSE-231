import argparse
from array import array
import json
import ast
import sys
import numpy as np
import networkx
from treelib import Node, Tree


def eprint(*args, **kwargs):
    """Print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


def create_tweet_tree(tweet: json, cid_tree_dict: dict):
    ''' Set initial tweets as root notes of the trees
    '''
    tree = Tree()
    tweet_info = tweet['tweet_info']
    tweet_info['public_metrics']['has_dropped_node'] = 0
    tree.create_node(tweet_info['id'], tweet_info['id'],
                     data=tweet_info['public_metrics'])
    cid_tree_dict[tweet_info['conversation_id']] = tree


def create_tweet_graph(tweet: json, cid_graph_dict: dict):
    ''' Set initial tweets as initial node in the graph
    '''
    graph = networkx.DiGraph()
    tweet_info = tweet['tweet_info']
    graph.add_node(tweet_info['author_id'],
                   public_metrics=tweet['user_info']['public_metrics'])
    cid_graph_dict[tweet_info['conversation_id']] = graph


def create_tweet_tree_node(line: str, cid_tree_dict: dict):
    ''' Add nodes to existing tweet trees
    '''
    reply_tweet = json.loads(line)
    tweet_info = reply_tweet['tweet_info']
    cid = tweet_info['conversation_id']
    if cid not in cid_tree_dict.keys():
        eprint('Reply tweet with no matching tree encountered, cid: {}'.format(cid))
    else:
        nid = tweet_info['id']
        tree = cid_tree_dict[cid]
        try:
            tree.create_node(nid, nid, parent=tree.root)
        except:
            tree[tree.root].data['has_dropped_node'] += 1
            eprint('Tree with cid {} dropped node with nid {}, total dropped: {}'.format(
                cid, nid, tree[tree.root].data['has_dropped_node']
            ))


def create_tweet_graph_node(line: str, cid_graph_dict: dict):
    reply_tweet = json.loads(line)
    tweet_info = reply_tweet['tweet_info']
    cid = tweet_info['conversation_id']
    if cid not in cid_graph_dict.keys():
        eprint(
            'Node: Reply tweet with no matching graph encountered, cid: {}'.format(cid))
    else:
        author_id = tweet_info['author_id']
        graph = cid_graph_dict[cid]
        if author_id not in graph.nodes:
            graph.add_node(tweet_info['author_id'],
                           public_metrics=reply_tweet['user_info']['public_metrics'])


def create_tweet_graph_edge(line: str, cid_graph_dict: dict):
    reply_tweet = json.loads(line)
    tweet_info = reply_tweet['tweet_info']
    cid = tweet_info['conversation_id']
    if cid not in cid_graph_dict.keys():
        eprint(
            'Edge: Reply tweet with no matching graph encountered, cid: {}'.format(cid))
    else:
        author_id = tweet_info['author_id']
        in_reply_to = tweet_info['in_reply_to_user_id']
        graph = cid_graph_dict[cid]
        if (author_id, in_reply_to) not in graph.edges:
            graph.add_edge(author_id, in_reply_to)


def reorder_trees(cid_tree_dict: dict, reply_mappings: dict):
    for cid, tree in cid_tree_dict.items():
        for node in tree.all_nodes():
            if node.is_root():
                continue  # don't drop the root node
            nid = node.identifier
            try:
                parent_nid = reply_mappings.get(nid)
                tree.move_node(nid, parent_nid)
            except:
                eprint('Node with id {} is being removed from tree with cid {}'
                       .format(nid, cid))
                tree.remove_node(nid)


def create_reply_trees_and_graphs(flags):
    # extract cids that we got replies for
    reply_cids = set()
    for line in open(flags.reply_tweets, "r"):
        tweet = json.loads(line)
        reply_cids.add(tweet['tweet_info']['conversation_id'])

    # make roots of trees and graphs
    cid_tree_dict = {}
    cid_graph_dict = {}
    prob_sample = 0.3
    for line in open(flags.initial_tweets, "r"):
        reply_tweet = json.loads(line)
        cid = reply_tweet['tweet_info']['conversation_id']
        reply_count = reply_tweet['tweet_info']['public_metrics']['reply_count']
        if cid in reply_cids or (reply_count == 0 and np.random.uniform() < prob_sample):
            create_tweet_tree(reply_tweet, cid_tree_dict)
            create_tweet_graph(reply_tweet, cid_graph_dict)

    print(len(cid_tree_dict), len(cid_graph_dict))

    reply_mappings = {}
    for line in open(flags.reply_mappings, "r"):
        data = ast.literal_eval(line)
        reply_mappings[str(data['id'])] = str(data['replied_to_tweet_id'])

    for line in open(flags.reply_tweets, "r"):
        create_tweet_tree_node(line, cid_tree_dict)
        create_tweet_graph_node(line, cid_graph_dict)

    reorder_trees(cid_tree_dict, reply_mappings)

    for line in open(flags.reply_tweets, "r"):
        create_tweet_graph_edge(line, cid_graph_dict)

    return cid_tree_dict, cid_graph_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch data with Twitter Streaming API"
    )
    parser.add_argument(
        "--initial_tweets", help="file with initial tweets", required=True)
    parser.add_argument(
        "--reply_tweets", help="file with reply tweets", required=True)
    parser.add_argument(
        "--reply_mappings", help="file with reply tweets mappings", required=True)
    flags = parser.parse_args()

    cid_tree_dict, cid_graph_dict = create_reply_trees_and_graphs(flags)

    print('1587162493889044480')
    tree = cid_tree_dict['1587162493889044480']
    print(tree.show())
    graph = cid_graph_dict['1587162493889044480']
    print('nodes: ', graph.nodes)
    print('edges: ', graph.edges)

    # for key, value in cid_graph_dict.items():
    #   print(key, value)
