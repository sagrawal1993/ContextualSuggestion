import json
import os
import re
from InformationRetrival.ContextualSuggestion.POITagBased import WordEmbeddingBased
from TextAnalysislib import TextEmbedding
from InformationRetrival.Measures import TREC

class TRECDataSource:
    def __init__(self, file_name, profile_folder):
        req_list = open(file_name).read().strip().split("\n")
        self.user_info = {}
        for req in req_list:
            req_json = json.loads(req)
            user_id = str(req_json["id"])
            self.user_info[user_id] = {}
            self.user_info[user_id]["preferences"] = req_json["body"]["person"]["preferences"]
            self.user_info[user_id]["candidate"] = {}
            for cand in req_json["candidates"]:
                self.user_info[user_id]["candidate"][cand['documentId']] = cand['tags']
        self.qrel_qid = qrelQid()
        self.profile_folder = profile_folder

    def getCandidateArticles(self, user_id):
        return self.user_info[user_id]["candidate"].keys()

    def getStoreUserProfile(self, user_id):
        """
        Get the user profile from storage.
        :param user_id:
        :type user_id:
        :return:
        :rtype:
        """
        profile_path = os.path.join(self.profile_folder, "profile_" + user_id + ".json")
        fp = open(profile_path)
        return json.load(fp)

    def storeUserProfile(self, user_id, profile_json):
        """
        Will store the user's created profile in storage, means store all of its parameters as well.
        :param user_id:
        :type user_id:
        :param profile_json:
        :type profile_json:
        :return:
        :rtype:
        """
        profile_path = os.path.join(self.profile_folder, "profile_" + user_id + ".json")
        fp = open(profile_path, "w")
        json.dump(profile_json["final_param"], fp)
        return

    def getUserPreferences(self, user_id):
        """
        Provide the documents user rated.
        :param user_id: user's unique id.
        :type user_id: int
        :return: the list of json contains documentId, rating and tags.
        :rtype: list of dict.
        """
        return self.user_info[user_id]["preferences"]

    def getArticleTags(self, user_id, article_id):
        """
        Returns the tags corresponding to article_id.
        :param article_id:
        :type article_id:
        :return:
        :rtype:
        """
        return self.user_info[user_id]["candidate"][article_id]

    """
    @TODO:
    load information from the previous stored parameters to check the results.
    """
    def getOptimizationInfo(self, user_id):
        print("Getting optimization info")
        if user_id != 'all':
            file_name = os.path.join(self.profile_folder, "opt_" + str(user_id) + ".json")
            fp = open(file_name)
            return json.load(fp)
        mp = self.find_all_param()
        return mp


    def storeOptimizationInfo(self, user_id, param_score):
        file_name = os.path.join(self.profile_folder, "opt_" + str(user_id) + ".json")
        fp = open(file_name, "w")
        json.dump(param_score, fp)
        return

    def find_all_param(self):
        params_list = ["ndcg_cut_5", "ndcg_cut_10", "ndcg_cut_15", "ndcg_cut_20"]
        qid_parm_map = {}
        for user_id in self.qrel_qid:
            file_name = os.path.join(self.profile_folder, "opt_" + str(user_id) + ".json")
            if "opt_" + str(user_id) + ".json" not in os.listdir(self.profile_folder):
                print(file_name + " not there.")
                continue
            print(file_name)
            par_map = json.load(open(file_name))
            for a in par_map:
                if a not in qid_parm_map:
                    qid_parm_map[a] = {}
                for b in par_map[a]:
                    if b not in qid_parm_map[a]:
                        qid_parm_map[a][b] = {}
                        qid_parm_map[a][b]['all'] = {}
                    for param in params_list:
                        if param not in qid_parm_map[a][b]['all']:
                            qid_parm_map[a][b]['all'][param] = 0.0
                        qid_parm_map[a][b]['all'][param] += float(par_map[a][b][user_id][param])
        return qid_parm_map

# create a sentence from the tags.
def tags_preprocess(tags):
    processed = []
    for tg in tags:
        st = tg.encode('ascii','ignore').lower()
        if st != "didn't load":
            st = st.decode()
            st = st.replace("'s", "").replace(" ", "")
            processed.append(st)
    return processed


"""
@TODO:
load the previous trained model to verify the result.
"""
def create_word_embedding(sentence_list=None, model_file="embedding.bin"):
    param_map = {}
    param_map["min_count"] = 3
    param_map["size"] = 9
    param_map["iter"] = 1000
    param_map["window"] = 5
    param_map["doc_embedding"] = "vectorSum"
    param_map["analyzer"] = tags_preprocess
    word_embedding = TextEmbedding.getTextEmbedder("word_embedding", param_map)
    if sentence_list is None and model_file is not None:
        word_embedding.fit(model_file=model_file)
    elif sentence_list is not None:
        word_embedding.fit(sentence_list=sentence_list)
        word_embedding.save_model(model_file)
    return word_embedding

def qrelQid():
    qid_list = []
    lines = open("/Users/surajagrawal/suraj/MyProjects/informatinoretrival/data/qrels_TREC2016_CS.txt").read().strip().split("\n")
    for line in lines:
        qid = line.split("\t")[0]
        qid_list.append(qid)
    return list(set(qid_list))


def getTagData(consider_tag=["2015", "2016_phase1", "2016_phase2"]):
    """
    It will give the tag list for generating the tag embedding from the request file.
    :param consider_tag:
    :type consider_tag:
    :return:
    :rtype:
    """
    sentence_list = []
    if "2015" in consider_tag:
        requests = open("../../data/batch_requests.json").read().strip().split("\n")
        for request in requests:
            req_json = json.loads(request)
            candidates = req_json["body"]["person"]["preferences"]
            for candidate in candidates:
                if "tags" in candidate and len(candidate["tags"])>0 :
                    sentence_list.append(candidate["tags"])
    if "2016_phase1" in consider_tag:
        requests = open("../../data/Phase1_requests.json").read().strip().split("\n")
        for request in requests:
            req_json = json.loads(request)
            candidates = req_json["body"]["person"]["preferences"]
            for candidate in candidates:
                if "tags" in candidate and len(candidate["tags"]) > 0:
                    sentence_list.append(candidate["tags"])

    if "2016_phase2" in consider_tag:
        requests = open("../../data/Phase2_requests.json").read().strip().split("\n")
        for request in requests:
            req_json = json.loads(request)
            candidates = req_json["candidates"] + req_json["body"]["person"]["preferences"]
            for candidate in candidates:
                if "tags" in candidate and len(candidate["tags"]) > 0:
                    sentence_list.append(candidate["tags"])
    return sentence_list

"""
@TODO:
Generate output file with the given parameters to get the score.
"""
def process():
    grid_opt_param = {}
    grid_opt_param["param_min"] = [-2.0, -2.0]
    grid_opt_param["param_max"] = [8.0, 8.0]
    grid_opt_param["step_size"] = 0.3
    datasource = TRECDataSource("../../data/Phase2_requests.json",
                                "/Users/surajagrawal/suraj/MyProjects/informatinoretrival/data/2016EmbWeigtedRocchioMultiLevel")
    embedding = create_word_embedding(model_file="../../data/embdding/embedding_2016.bin")
    poi_ranker = WordEmbeddingBased(datasource, embedding, profile_vector="weighted", profile_type="individual",
                                    ranking="rocchio", rating_shift=0, opt_name="grid_search",
                                    opt_param=grid_opt_param)
    poi_ranker.fit(user_ids=datasource.user_info.keys(), param_type="all", score_file="given", store_profile=True)
    user_recommendation = []
    for user_id in datasource.user_info.keys():
        output = poi_ranker.getArticles(user_id)
        user_recommendation.append(output)
    TREC.create_output_file(user_recommendation, list(datasource.user_info.keys()), "result.txt")

#tag_list = getTagData(["2016_phase1", "2016_phase2"])
#tag1 = getTagData()
#print(len(tag_list), len(tag1))
#create_word_embedding(tag_list, model_file="embedding_2016.bin")
#print(len(tag_list))

process()
#print(qrelQid())