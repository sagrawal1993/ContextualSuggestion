"""
This module will contains method to recomment
"""

#from InformationRetrival import AbstractIR
from analysislib import clustering
from sklearn.metrics.pairwise import cosine_similarity

class AbstractDataSource:
    def getArticles(self, param_map):
        pass

    def getStoreUserProfile(self, user_id):
        """
        Get the user profile from storage.
        :param user_id:
        :type user_id:
        :return:
        :rtype:
        """
        pass

    def storeUserProfile(self, user_id, profile_json):
        """
        Will store the user's created profile in storage.
        :param user_id:
        :type user_id:
        :param profile_json:
        :type profile_json:
        :return:
        :rtype:
        """
        pass

    def getUserPreferences(self, user_id):
        """
        Provide the documents user rated.
        :param user_id: user's unique id.
        :type user_id: int
        :return: the list of json contains documentId, rating and tags.
        :rtype: list of dict.
        """
        pass

    def getArticleTags(self, article_id):
        """
        Returns the tags corresponding to article_id.
        :param article_id:
        :type article_id:
        :return:
        :rtype:
        """
        pass

class WordEmbeddingBased():

    """
    query:: {"id":1, "body":
    {"group": "Family", "season":"Summer", "trip_type":"Holiday", "duration":"Weekend trip",
    "location":{"id":152,"name":"Chicago","state":"IL","lat":41.85003,"lng":-87.65005},
    "person": {"gender": "Male", "age": 23, "id": "A00126103VB6TFM3EITH9",
    "preferences":[
    {"documentId":"TRECCS-00247633-160","rating":3,"tags":["Museums"]},
    {"documentId":"TRECCS-00018097-160","rating":3,"tags":["Farmer's markets"]},
    {"documentId":"TRECCS-00086564-160","rating":3},
    {"documentId":"TRECCS-00086340-160","rating":1,"tags":["Bar-hopping"]},
    {"documentId":"TRECCS-00086298-160","rating":-1},
    {"documentId":"TRECCS-00018094-160","rating":3,"tags":["Theatre"]},
    {"documentId":"TRECCS-00247656-160","rating":3,"tags":["Bar-hopping"]},
    {"documentId":"TRECCS-00018110-160","rating":2,"tags":["Shopping for food","Markets","Organic Food"]},
    {"documentId":"TRECCS-00675013-160","rating":3,"tags":["Fine Dining"]},
    {"documentId":"TRECCS-00087026-160","rating":3,"tags":["Fine Dining"]},
    {"documentId":"TRECCS-00086310-160","rating":3},
    {"documentId":"TRECCS-00087258-160","rating":4,"tags":["Museums","Art Galleries"]}
    ]}}}

    """
    def __init__(self, datasource, tag_embedding, profile_vector="unweighted", profile_type="individual", rating_shift=0):
        super.__init__(datasource)
        self.tag_embedding = tag_embedding
        self.profile_vector = profile_vector
        self.rating_shift = rating_shift
        self.profile_type = profile_type
        if profile_vector == "weighted":
            self.doc_combiner = clustering.getClusterEmbeddingFromPoints("weightedCentroid")
        else:
            self.doc_combiner = clustering.getClusterEmbeddingFromPoints("centroid")
        print("This is instance for getting articles recommendation based on word embedding")

    def __getProfile(self, preferences):
        pos_rating_list = []
        neu_rating_list = []
        neg_rating_list = []
        pos_doc_embedding_list = []
        neg_doc_embedding_list = []
        neu_doc_embedding_list = []

        for doc in preferences:
            if 'rating' in doc and 'tags' in doc:
                rating = doc['rating'] - self.rating_shift
                doc_embedding = self.tag_embedding.get_doc_embedding(doc['tags'])
                if rating > 0:
                    pos_rating_list.append(rating)
                    pos_doc_embedding_list.append(doc_embedding)
                elif rating == 0:
                    neu_rating_list.append(rating)
                    neu_doc_embedding_list.append(doc_embedding)
                else:
                    neg_rating_list.append(rating)
                    neg_doc_embedding_list.append(doc_embedding)

        parm_map = {}
        if self.profile_type == "combined":
            parm_map["weights"] = pos_rating_list + neu_rating_list + neg_rating_list
            doc_embedding_list = pos_doc_embedding_list + neu_doc_embedding_list + neg_doc_embedding_list
            profile_vec = self.doc_combiner.getClusterRepresentation(doc_embedding_list, parm_map)
            return profile_vec

        parm_map["weights"] = pos_rating_list
        pos_profile_vec = self.doc_combiner.getClusterRepresentation(pos_doc_embedding_list, parm_map)
        parm_map["weights"] = neu_rating_list
        neu_profile_vec = self.doc_combiner.getClusterRepresentation(neu_doc_embedding_list, parm_map)
        parm_map["weights"] = neg_rating_list
        neg_profile_vec = self.doc_combiner.getClusterRepresentation(neg_doc_embedding_list, parm_map)
        return pos_profile_vec, neu_profile_vec, neg_profile_vec


    def fit(self, query_set, ground_truth):
        for query in query_set:
            print("xyz")
        return

    def rank_articles(self, profile_vec, candidate_articles):
        return

    def rocchio_ranker(self, user_profile, params, candidate_suggestion):
        profile_vec = params[0] * user_profile[0] + params[1] * user_profile[1] + params[2] * user_profile[2]
        doc_id_score_map = {}
        for doc in candidate_suggestion:
            doc_vec = self.poi.get_vec_tags(doc['tags'])
            doc_id_score_map[doc['documentId']] = cosine_similarity([profile_vec], [doc_vec])[0][0]
        return doc_id_score_map

    def similarity_ranker(self, user_profile, pos_par, neg_par, candidate_suggestion):
        doc_id_score_map = {}
        for doc in candidate_suggestion:
            doc_vec = self.poi.get_vec_tags(doc['tags'])
            temp = cosine_similarity([doc_vec], user_profile)
            doc_id_score_map[doc['documentId']] = cosine_similarity(temp, [[pos_par, 1, neg_par]])[0][0]
        return doc_id_score_map

    def __getArticles(self, paramters, query_dict):

        return []

    def getArticles(self, query_dict):
        id = query_dict["id"]
        return []