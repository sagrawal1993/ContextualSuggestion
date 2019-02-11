import json
import os
from InformationRetrival.ContextualSuggestion.POITagBased import WordEmbeddingBased
from TextAnalysislib import TextEmbedding

class TRECDataSource:
    def __init__(self, file_name, profile_folder):
        req_list = open(file_name).read().strip().split("\n")
        self.user_info = {}
        for req in req_list:
            req_json = json.load(req)
            user_id = str(req_json["id"])
            self.user_info[user_id] = {}
            self.user_info[user_id]["preferences"] = req_json["body"]["person"]["preferences"]
            self.user_info[user_id]["candidate"] = {}
            for cand in req_json["candidate"]:
                self.user_info[user_id]["candidate"][cand['documentId']] = cand['tags']
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
        profile_path = os.path.join(self.profile_folder, user_id + ".json")
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
        profile_path = os.path.join(self.profile_folder, user_id + ".json")
        fp = open(profile_path, "w")
        json.dump(profile_json, fp)
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

    def getScoreGridMap(self, user_id):
        return {}

    def storeScoreGripMap(self, user_id, param_score):
        fp = open("score_file.json", "w")
        json.dump(param_score, fp)
        return

# create a sentence from the tags.
def tags_preprocess(tags):
    processed = []
    for tg in tags:
        st = tg.encode('ascii','ignore').lower()
        if st != "didn't load":
            st = st.replace("'s", "").replace(" ", "")
            processed.append(st)
    return processed


def create_word_embedding():
    param_map = {}
    param_map["min_count"] = 3
    param_map["size"] = 9
    param_map["iter"] = 1000
    param_map["window"] = 5
    param_map["analyser"] = tags_preprocess
    word_embedding = TextEmbedding.getTextEmbedder("word_embedding", param_map)
    return word_embedding


def process():
    datasource = TRECDataSource("../../data/Phase2_request.json", "../../data/")
    embedding = create_word_embedding()
    poi_ranker = WordEmbeddingBased(datasource, embedding)
    poi_ranker.fit([])
    poi_ranker.getArticles("123")
