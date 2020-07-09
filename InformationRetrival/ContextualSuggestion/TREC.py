import json
import os
import re
from InformationRetrival.ContextualSuggestion.POITagBased import WordEmbeddingBased, SeasonTripTypeRelevance
from TextAnalysislib import TextEmbedding
from InformationRetrival.Measures import TREC
import unidecode

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
            self.user_info[user_id]["season"] = req_json["body"]["season"]
            self.user_info[user_id]["group"] = req_json["body"]["group"]

            for cand in req_json["candidates"]:
                self.user_info[user_id]["candidate"][cand['documentId']] = cand['tags']
        self.qrel_qid = qrelQid()
        self.qrel_qid = list(self.qrel_qid.intersection(self.user_info.keys()))
        self.profile_folder = profile_folder
        self.params_list = ["ndcg_cut_5", "ndcg_cut_10", "ndcg_cut_15", "ndcg_cut_20", "ndcg_cut_30", "ndcg", "P_5", "P_10",
                       "P_15", "P_20", "P_30", "map", "recip_rank", "map_cut_5", "map_cut_10", "map_cut_15",
                       "map_cut_20",
                       "map_cut_30", "Rprec", "bpref", "recall_5", "recall_10", "recall_15", "recall_20", "recall_30"]
        self.mp = None

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
        if user_id not in self.user_info:
            return None
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
        if self.mp is None:
            self.mp = self.find_all_param()
        return self.mp


    def storeOptimizationInfo(self, user_id, param_score):
        file_name = os.path.join(self.profile_folder, "opt_" + str(user_id) + ".json")
        fp = open(file_name, "w")
        json.dump(param_score, fp)
        return

    def find_all_param(self):
        params_list = ["ndcg_cut_5", "ndcg_cut_10", "ndcg_cut_15", "ndcg_cut_20", "ndcg_cut_30", "ndcg", "P_5", "P_10",
                       "P_15", "P_20", "P_30", "map", "recip_rank", "map_cut_5", "map_cut_10", "map_cut_15", "map_cut_20",
                       "map_cut_30", "Rprec", "bpref", "recall_5", "recall_10", "recall_15", "recall_20", "recall_30"]
        qid_parm_map = {}
        print(self.qrel_qid)
        print(self.user_info.keys())
        user_id_list = set(self.qrel_qid).intersection(self.user_info.keys())
        print("total user ids to be consider ", len(user_id_list))
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
        tg = unidecode.unidecode(tg)
        st = tg.encode('ascii', 'ignore').lower()
        st = st.decode()

        st = st.replace("'s", "").replace(" ", "")
        if st != "didn'tload" and st != "noneapply":
            if st == "cafs":
                print(tags)
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
    #param_map["doc_embedding"] = "centroid"
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
    lines = open("../../data/qrels_TREC2016_CS.txt").read().strip().split("\n")
    for line in lines:
        qid = line.split("\t")[0]
        #if "opt_" + qid + ".json" not in os.listdir("/Users/surajagrawal/suraj/MyProjects/informatinoretrival/data/2016EmbWeightedRocchioMultiLevelSumTag"):
        qid_list.append(qid)

    return set(qid_list)


def getContextData():
    queries = open("../../data/batch_requests.json").read().strip().split("\n")
    data_point_list = []
    for query in queries:
        data_point = {}
        mp = json.loads(query)['body']
        if 'season' not in mp or 'group' not in mp:
            continue
        data_point['season'] = mp['season']
        data_point['group'] = mp['group']
        data_point['candidates'] = mp['person']['preferences']
        data_point_list.append(data_point)
    return data_point_list

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
        print("adding 2015 tags")
        requests = open("../../data/batch_requests.json").read().strip().split("\n")
        for request in requests:
            req_json = json.loads(request)
            candidates = req_json["body"]["person"]["preferences"]
            for candidate in candidates:
                if "tags" in candidate and len(candidate["tags"])>0 :
                    sentence_list.append(candidate["tags"])
    if "2016_phase1" in consider_tag:
        print("adding 2016 phase1 tags")
        requests = open("../../data/Phase1_requests.json").read().strip().split("\n")
        for request in requests:
            req_json = json.loads(request)
            candidates = req_json["body"]["person"]["preferences"]
            for candidate in candidates:
                if "tags" in candidate and len(candidate["tags"]) > 0:
                    sentence_list.append(candidate["tags"])

    if "2016_phase2" in consider_tag:
        print("adding 2016 phase2 tags")
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
def process(grid_opt_param, all_params, parm_file_generate=False):

    datasource = TRECDataSource(all_params['request_file'], all_params['data_folder'])
    embedding = create_word_embedding(model_file=all_params['embedding'])
    poi_ranker = WordEmbeddingBased(datasource, embedding, profile_vector=all_params['profile'], profile_type="individual",
                                    ranking=all_params['ranking'], rating_shift=0, opt_name="grid_search",
                                    opt_param=grid_opt_param, poi_relevance=False)

    #context_relevence = SeasonTripTypeRelevance(datasource, embedding, True)
    #context_info = json.load(open("../../data/context_data.json"))
    #context_relevence.fit(getContextData())

    if parm_file_generate:
        poi_ranker.fit(user_ids=datasource.qrel_qid, param_type="all", score_file=None, store_profile=True, measure="ndcg_cut_5")
    else:
        whole_map = {}

        '''poi_ranker.fit(user_ids=datasource.qrel_qid, fit_type="learning", param_type="user_id", score_file="Given",
                       store_profile=True)
        user_recommendation = []

        for user_id in datasource.qrel_qid:
            output = poi_ranker.getArticles(user_id)
            # context_rel = context_relevence.getRelevance(season=datasource.user_info[user_id]["season"], group=datasource.user_info[user_id]["group"], user_id=user_id)
            # print(datasource.user_info[user_id]["season"], datasource.user_info[user_id]["group"])
            print("output_before", output)
            # print("context relevance", context_rel)
            # for key in output:
            #    output[key] += 2 * context_rel[key]
            # print("output_after", output)
            user_recommendation.append(output)
        TREC.create_output_file(user_recommendation, list(datasource.qrel_qid), "result.txt")
        score = TREC.get_score("../../data/qrels_TREC2016_CS.txt", "result.txt")["all"]
        print(score['ndcg_cut_5'], score['P_5'], score['P_10'], score["recip_rank"], score['ndcg'], score['map'],
              score["bpref"], score["Rprec"])
        whole_map['learning'] = [score['ndcg_cut_5'], score['P_5'], score['P_10'], score["recip_rank"], score['ndcg'],
                          score['map'],
                          score["bpref"], score["Rprec"]]
        '''
        #for par in datasource.params_list:
        for par in ['ndcg']:
            poi_ranker.fit(user_ids=datasource.qrel_qid, param_type="user_id", score_file="Given", store_profile=True, measure=par)
            #poi_ranker.fit(user_ids=datasource.qrel_qid, fit_type="search", param_type="all", score_file="Given", store_profile=True, measure=par)
            user_recommendation = []
            for user_id in datasource.qrel_qid:
                output = poi_ranker.getArticles(user_id)
                #context_rel = context_relevence.getRelevance(season=datasource.user_info[user_id]["season"], group=datasource.user_info[user_id]["group"], user_id=user_id)
                #print(datasource.user_info[user_id]["season"], datasource.user_info[user_id]["group"])
                print("output_before", output)
                #print("context relevance", context_rel)
                #for key in output:
                #    output[key] += 2 * context_rel[key]
                #print("output_after", output)
                user_recommendation.append(output)
            TREC.create_output_file(user_recommendation, list(datasource.qrel_qid), "result.txt")
            score = TREC.get_score("../../data/qrels_TREC2016_CS.txt", "result.txt")["all"]
            print(par)
            print(score['ndcg_cut_5'], score['P_5'], score['P_10'], score["recip_rank"], score['ndcg'], score['map'], score["bpref"], score["Rprec"])
            whole_map[par] = [score['ndcg_cut_5'], score['P_5'], score['P_10'], score["recip_rank"], score['ndcg'], score['map'],
                          score["bpref"], score["Rprec"]]
        #print(whole_map)
        return whole_map
    

    """
    mp = datasource.find_all_param()
    fp1= open("test.json","w")
    json.dump(mp, fp1)
    """
#tag_list = getTagData(["2016_phase1", "2016_phase2"])
#for tags in tag_list:
#    print(tags_preprocess(tags))
#tag_list = getTagData()
#print(len(tag_list), len(tag1))
#create_word_embedding(tag_list, model_file="../../data/embdding/embedding_correct_2016_1000_iter.bin")
#print(len(tag_list))
#print(tags_preprocess(["Didn't load"]))


#print(len(qrelQid()))
final_map = {}
'''
grid_opt_param = {}
grid_opt_param["param_min"] = [-4.0, -4.0]
grid_opt_param["param_max"] = [8.0, 8.0]
grid_opt_param["step_size"] = 0.2
all_params = {}
all_params['data_folder'] = "../../data/CorrectAllEmbWeightedRocchioMultiLevelSumTag1000Iter"
all_params['request_file'] = "../../data/Phase2_requests.json"
all_params['embedding'] = "../../data/embdding/embedding_correct_all_1000_iter.bin"
all_params['profile'] = "weighted"
all_params['ranking'] = "rocchio"
#all_params['ranking'] = "lambdaMART"
final_map["CorrectAllEmbWeightedRocchioMultiLevelSumTag1000Iter"] = process(grid_opt_param, all_params, parm_file_generate=False)
#print(getContextData())
'''
grid_opt_param = {}
grid_opt_param["param_min"] = [-4.0, -4.0]
grid_opt_param["param_max"] = [8.0, 8.0]
grid_opt_param["step_size"] = 0.2
all_params = {}
all_params['data_folder'] = "../../data/Correct2016EmbWeightedRocchioMultiLevelSumTag1000Iter"
all_params['request_file'] = "../../data/Phase2_requests.json"
all_params['embedding'] = "../../data/embdding/embedding_correct_2016_1000_iter.bin"
all_params['profile'] = "weighted"
all_params['ranking'] = "rocchio"
#all_params['ranking'] = "lambdaMART"
final_map["Correct2016EmbWeightedRocchioMultiLevelSumTag1000Iter"] = process(grid_opt_param, all_params, parm_file_generate=False)
'''
grid_opt_param = {}
grid_opt_param["param_min"] = [-4.0, -4.0]
grid_opt_param["param_max"] = [8.0, 8.0]
grid_opt_param["step_size"] = 0.2
all_params = {}
all_params['data_folder'] = "../../data/CorrectAllEmbWeightedRocchioMultiLevelSumTag500Iter"
all_params['request_file'] = "../../data/Phase2_requests.json"
all_params['embedding'] = "../../data/embdding/embedding_correct_all_500_iter.bin"
all_params['profile'] = "weighted"
#all_params['ranking'] = "rocchio"
all_params['ranking'] = "lambdaMART"
final_map["CorrectAllEmbWeightedRocchioMultiLevelSumTag500Iter"] = process(grid_opt_param, all_params, parm_file_generate=False)

grid_opt_param = {}
grid_opt_param["param_min"] = [-4.0, -4.0]
grid_opt_param["param_max"] = [8.0, 8.0]
grid_opt_param["step_size"] = 0.2
all_params = {}
all_params['data_folder'] = "../../data/Correct2016EmbWeightedRocchioMultiLevelSumTag500Iter"
all_params['request_file'] = "../../data/Phase2_requests.json"
all_params['embedding'] = "../../data/embdding/embedding_correct_2016_500_iter.bin"
all_params['profile'] = "weighted"
#all_params['ranking'] = "rocchio"
all_params['ranking'] = "lambdaMART"
final_map["Correct2016EmbWeightedRocchioMultiLevelSumTag500Iter"] = process(grid_opt_param, all_params, parm_file_generate=False)

grid_opt_param = {}
grid_opt_param["param_min"] = [-4.0, -8.0]
grid_opt_param["param_max"] = [8.0, 4.0]
grid_opt_param["step_size"] = 0.2
all_params = {}
all_params['data_folder'] = "../../data/Correct2016EmbUnWeightedRocchioMultiLevelSumTag1000Iter"
all_params['request_file'] = "../../data/Phase2_requests.json"
all_params['embedding'] = "../../data/embdding/embedding_correct_2016_1000_iter.bin"
all_params['profile'] = "unweighted"
all_params['ranking'] = "rocchio"
#all_params['ranking'] = "lambdaMART"
final_map["Correct2016EmbUnWeightedRocchioMultiLevelSumTag1000Iter"] = process(grid_opt_param, all_params, parm_file_generate=False)

grid_opt_param = {}
grid_opt_param["param_min"] = [-4.0, -8.0]
grid_opt_param["param_max"] = [8.0, 4.0]
grid_opt_param["step_size"] = 0.2
all_params = {}
all_params['data_folder'] = "../../data/CorrectAllEmbUnWeightedRocchioMultiLevelSumTag1000Iter"
all_params['request_file'] = "../../data/Phase2_requests.json"
all_params['embedding'] = "../../data/embdding/embedding_correct_all_1000_iter.bin"
all_params['profile'] = "unweighted"
all_params['ranking'] = "rocchio"
#all_params['ranking'] = "lambdaMART"
final_map["CorrectAllEmbUnWeightedRocchioMultiLevelSumTag1000Iter"] = process(grid_opt_param, all_params, parm_file_generate=False)


grid_opt_param = {}
grid_opt_param["param_min"] = [-4.0, -8.0]
grid_opt_param["param_max"] = [8.0, 4.0]
grid_opt_param["step_size"] = 0.2
all_params = {}
all_params['data_folder'] = "../../data/Correct2016EmbUnWeightedRocchioMultiLevelSumTag500Iter"
all_params['request_file'] = "../../data/Phase2_requests.json"
all_params['embedding'] = "../../data/embdding/embedding_correct_2016_500_iter.bin"
all_params['profile'] = "unweighted"
all_params['ranking'] = "rocchio"
#all_params['ranking'] = "lambdaMART"
final_map["Correct2016EmbUnWeightedRocchioMultiLevelSumTag500Iter"] = process(grid_opt_param, all_params, parm_file_generate=False)


grid_opt_param = {}
grid_opt_param["param_min"] = [-4.0, -8.0]
grid_opt_param["param_max"] = [8.0, 4.0]
grid_opt_param["step_size"] = 0.2
all_params = {}
all_params['data_folder'] = "../../data/CorrectAllEmbUnWeightedRocchioMultiLevelSumTag500Iter"
all_params['request_file'] = "../../data/Phase2_requests.json"
all_params['embedding'] = "../../data/embdding/embedding_correct_all_500_iter.bin"
all_params['profile'] = "unweighted"
#all_params['ranking'] = "rocchio"
all_params['ranking'] = "lambdaMART"
final_map["CorrectAllEmbUnWeightedRocchioMultiLevelSumTag500Iter"] = process(grid_opt_param, all_params, parm_file_generate=False)

print(final_map)
fp = open("learning_to_rank_user_id.json", "w")
json.dump(final_map, fp)
'''
