
import networkx as nx
import matplotlib.pyplot as plt

def build_and_save_graph_labeled(edges, edge_labels=None, output_file='graph.png'):
    """
    Builds a network graph with optional edge labels and saves it as a PNG image.

    Args:
        edges (list of tuple): List of tuples representing edges (e.g., [('A', 'B'), ('B', 'C')]).
        edge_labels (dict, optional): Dictionary of edge labels {(u, v): label}.
        output_file (str): Path to the output PNG file.
    """
    # plt.figure(figsize=(30, 30))
    G = nx.DiGraph()
    # pos = nx.kamada_kawai_layout(G) 
    G.add_edges_from(edges)

    # pos = nx.spring_layout(G)
    pos = nx.kamada_kawai_layout(G) 

    plt.figure(figsize=(15, 15))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', 
            edge_color='gray',
            node_size=2000, font_size=12, font_weight='bold')

    if edge_labels:
        nx.draw_networkx_edge_labels(G, pos,
                edge_labels=edge_labels, font_color='red')

    plt.savefig(output_file)
    plt.close()
    print(f"Graph with edge labels saved to {output_file}")

def build_and_save_graph(edges, output_file='graph.png'):
    """
    Builds a network graph from a list of edges and saves it as a PNG image.

    Args:
        edges (list of tuple): List of tuples representing edges (e.g., [('A', 'B'), ('B', 'C')]).
        output_file (str): Path to the output PNG file.
    """
    # Create a graph
    G = nx.DiGraph()

    # Add edges to the graph
    G.add_edges_from(edges)

    # Create a layout for the graph
    pos = nx.spring_layout(G)

    # Draw the graph
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray',
            node_size=2000, font_size=12, font_weight='bold')

    # Save to PNG
    plt.savefig(output_file)
    plt.close()
    print(f"Graph saved to {output_file}")

def make_edges():
    """
    SYN:
     *	sNO -> sSS	Initialize a new connection
     *	sSS -> sSS	Retransmitted SYN
     *	sS2 -> sS2	Late retransmitted SYN
     *	sSR -> sIG
     *	sES -> sIG	Error: SYNs in window outside the SYN_SENT state
     *			are errors. Receiver will reply with RST
     *			and close the connection.
     *			Or we are not in sync and hold a dead connection.
     *	sFW -> sIG
     *	sCW -> sIG
     *	sLA -> sIG
     *	sTW -> sSS	Reopened connection (RFC 1122).
     *	sCL -> sSS


    SYN/ACK
     *	sNO -> sIV	Too late and no reason to do anything
     *	sSS -> sIV	Client can't send SYN and then SYN/ACK
     *	sS2 -> sSR	SYN/ACK sent to SYN2 in simultaneous open
     *	sSR -> sSR	Late retransmitted SYN/ACK in simultaneous open
     *	sES -> sIV	Invalid SYN/ACK packets sent by the client
     *	sFW -> sIV
     *	sCW -> sIV
     *	sLA -> sIV
     *	sTW -> sIV
     *	sCL -> sIV
    FIN

    ACK

     *	sNO -> sES	Assumed.
     *	sSS -> sIV	ACK is invalid: we haven't seen a SYN/ACK yet.
     *	sS2 -> sIV
     *	sSR -> sES	Established state is reached.
     *	sES -> sES	:-)
     *	sFW -> sCW	Normal close request answered by ACK.
     *	sCW -> sCW
     *	sLA -> sTW	Last ACK detected (RFC5961 challenged)
     *	sTW -> sTW	Retransmitted last ACK. Remain in the same state.
     *	sCL -> sCL

     RST
     *  sNO, sSS, sSR, sES, sFW, sCW, sLA, sTW, sCL, sS2	*/
        { sIV, sCL, sCL, sCL, sCL, sCL, sCL, sCL, sCL, sCL },

    REPLY Direction:

    SYN:
     *	sNO -> sIV	Never reached.
     *	sSS -> sS2	Simultaneous open
     *	sS2 -> sS2	Retransmitted simultaneous SYN
     *	sSR -> sIV	Invalid SYN packets sent by the server
     *	sES -> sIV
     *	sFW -> sIV
     *	sCW -> sIV
     *	sLA -> sIV
     *	sTW -> sSS	Reopened connection, but server may have switched role
     *	sCL -> sIV

     SYN/ACK

     *	sSS -> sSR	Standard open.
     *	sS2 -> sSR	Simultaneous open
     *	sSR -> sIG	Retransmitted SYN/ACK, ignore it.
     *	sES -> sIG	Late retransmitted SYN/ACK?
     *	sFW -> sIG	Might be SYN/ACK answering ignored SYN
     *	sCW -> sIG
     *	sLA -> sIG
     *	sTW -> sIG
     *	sCL -> sIG

     ACK

     *	sSS -> sIG	Might be a half-open connection.
     *	sS2 -> sIG
     *	sSR -> sSR	Might answer late resent SYN.
     *	sES -> sES	:-)
     *	sFW -> sCW	Normal close request answered by ACK.
     *	sCW -> sCW
     *	sLA -> sTW	Last ACK detected (RFC5961 challenged)
     *	sTW -> sTW	Retransmitted last ACK.
     *	sCL -> sCL


    """

    orig_syn_edges = [('sNO','sSS'), ('sSS','sSS'), 
            ('sS2','sS2'),('sSR','sIG'),
            ('sES','sIG'),('sFW','sIG'),
            ('sCW','sIG'),('sLA','sIG'),
            ('sTW','sSS'),('sCL','sSS')]
    orig_syn_edges_labels = { e : 'syn_o' for e in orig_syn_edges}
    orig_synack_edges = [('sNO','sIV'),('sSS','sIV'),
            ('sS2','sSR'),('sSR','sSR'),
            ('sES','sIV'),('sFW','sIV'),
            ('sCW','sIV'),('sLA','sIV'),
            ('sTW','sIV'),('sCL','sIV')]
    orig_synack_edges_labels = { e : 'syn/ack_o'
            for e in orig_synack_edges}
    orig_ack_edges =[('sNO','sES'),('sSS','sIV'),
            ('sS2','sIV'),('sSR','sES'),
            ('sES','sES'),('sFW','sCW'),
            ('sCW','sCW'),('sLA','sTW'),
            ('sTW','sTW'),('sCL','sCL')]
    orig_ack_edges_labels = { e : 'ack_o' for e in orig_ack_edges}
    reply_syn_edges = [('sNO','sIV'),('sSS','sS2'),
            ('sS2','sS2'),('sSR','sIV'),
            ('sES','sIV'),('sFW','sIV'),
            ('sCW','sIV'),('sLA','sIV'),
            ('sTW','sSS'),('sCL','sIV')]
    reply_syn_edges_labels = { e : 'syn_r'
            for e in reply_syn_edges}
    reply_synack_edges = [('sSS','sSR'),('sS2','sSR'),
            ('sSR','sIG'),('sES','sIG'),
            ('sFW','sIG'),('sCW','sIG'),
            ('sLA','sIG'),('sTW','sIG'),
            ('sCL','sIG')]
    reply_synack_edges_labels = { e : 'syn/ack_r' 
            for e in reply_synack_edges}
    reply_ack_edges = [('sSS','sIG'),('sS2','sIG'),('sSR','sSR'),
            ('sES','sES'),('sFW','sCW'),
            ('sCW','sCW'),('sLA','sTW'),
            ('sTW','sTW'),('sCL','sCL')]
    reply_ack_edges_labels = { e : 'ack_r' 
            for e in reply_ack_edges}

    edges = orig_syn_edges+orig_synack_edges+orig_ack_edges +\
            reply_syn_edges+reply_synack_edges+reply_ack_edges

    labels = {**orig_syn_edges_labels,**orig_synack_edges_labels,\
            **orig_ack_edges_labels,**reply_syn_edges_labels,\
            **reply_synack_edges_labels,**reply_ack_edges_labels}
    return edges, labels


def main():
    edges, labels = make_edges()
    build_and_save_graph_labeled(
        edges, edge_labels=labels, output_file='my_network.png')

if __name__ == '__main__':
    main()
