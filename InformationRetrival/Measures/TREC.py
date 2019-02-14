import numpy as np
import subprocess
import os

def create_qrel_from_preferences(pref_list, user_id_list, qrel_file, level="multi"):
    print("Create Qrel from Preferences")
    not_rated = 0
    total_poi = 0
    for i, pref in enumerate(pref_list):
        if level == "uni":
            not_rated += __get_qrel_file_single_level(pref, qrel_file + "temp", user_id_list[i])
        else:
            not_rated += __get_qrel_file_multi_level(pref, qrel_file + "temp", user_id_list[i])

    print("Total POI in the Preference", total_poi)
    print("Total POI not rated", not_rated)
    os.rename(qrel_file + "temp", qrel_file)
    print("qrel created.")

# create the qrel file given the user preferences.
# It consider relevency at the score of -2 to +2.{-2,-1,0,1,2}
# This will return the tuple contains the counts of poi rated by the user
# and heaving -1 rating( User Doesn't give the rating.)
def __get_qrel_file_multi_level(place_list, file_name, qid):
    print("Qrel with Rating on the scale -2 to +2")
    q_id = str(qid)
    out_file = ""
    not_rated = 0
    for place in place_list:
        if place["rating"] == -1:
            not_rated += 1
            continue
        out_file += q_id + "\t0\t" + place["documentId"] + "\t" + str(place["rating"] - 2) + "\n"
    fp = open(file_name, "a+")
    fp.write(out_file)
    fp.close()
    print("Total POI's Rated by user: " + str(qid), len(place_list) - not_rated)
    print("Total POI's Not Rated by user: " + str(qid), not_rated)

    return not_rated


# create the qrel file given the user preferences.
# create the qrel file with relevant or not relevent score.
def __get_qrel_file_single_level(place_list, file_name, qid):
    print("Qrel with Binary 0/1 relevance")
    q_id = str(qid)
    out_file = ""
    for place in place_list:
        if place["rating"] == -1:
            continue
        if place["rating"] - 2 > 0:
            rate = 1
        else:
            rate = 0
        out_file += q_id + "\t0\t" + place["documentId"] + "\t" + str(rate) + "\n"
    fp = open(file_name, "a")
    fp.write(out_file)
    fp.close()


def create_output_file(ranked_doc_list, qid_list, file_name):
    temp = open(file_name, "w")
    for i, qid in enumerate(qid_list):
        __get_output_file(ranked_doc_list[i], temp, qid)
    temp.close()

def __get_output_file(rank_list, temp, qid):
    """

    :param id_score_map:
    :type id_score_map:
    :param file_name:
    :type file_name:
    :param qid:
    :type qid:
    :return:
    :rtype:
    """
    result_file = ""
    query_id = str(qid)
    rank_list = [(rank_list[id], id) for id in rank_list]
    rank_list.sort(reverse=True)
    i = 1
    for doc in rank_list:
        result_file += query_id+" Q0 "+doc[1]+" "+str(i)+" "+str(doc[0])+" STANDARD\n"
        i += 1
    temp.write(result_file)

def get_score(qrel_file, output_file):
    """
    get the measures score calculated by trec_eval scripts.
    @arg1: qrel file
    @arg2: result file
    @arg3: query id for which result required./ "all" if avg score is required.

    """
    from InformationRetrival.Measures import TREC
    import os
    path = os.path.dirname(TREC.__file__)
    result = subprocess.check_output(['./../Measures/trec_eval/trec_eval', '-m', 'all_trec', '-q', qrel_file, output_file])
    query_score_map = {}
    result = result.decode()
    lines = result.strip().split('\n')
    print(len(lines))
    for line in result.strip().split('\n'):
        temp = line.split()
        if temp[1] not in query_score_map:
            query_score_map[str(temp[1])] = {}
        query_score_map[str(temp[1])][str(temp[0])]=str(temp[2])
    print("Score ndcg_cut_5 ", query_score_map['all']['ndcg_cut_5'])
    return query_score_map

#m = get_score("../../data/qrels_TREC2016_CS.txt","../../data/output.txt")
#print(m)

