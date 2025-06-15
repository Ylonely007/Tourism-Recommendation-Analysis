import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
user_ratings = {
    "User1": {"地点A": 5, "地点B": 4, "地点C": 0},
    "User2": {"地点A": 0, "地点B": 2, "地点C": 4, "地点D": 5},
    "User3": {"地点A": 4, "地点B": 0, "地点C": 3, "地点D": 0},
}
def user_based_collaborative_filtering(user_id, user_ratings, top_n=3):
    # 获取目标用户的评分数据
    target_user_ratings = user_ratings[user_id]

    # 初始化一个字典，用于保存其他用户与目标用户的相似度得分
    user_similarity_scores = {}

    # 将目标用户的评分转换为numpy数组
    target_user_ratings_list = np.array([rating for _, rating in target_user_ratings.items()])

    # 计算目标用户与其他用户之间的相似度得分
    for user, ratings in user_ratings.items():
        if user == user_id:
            continue

        # 将其他用户的评分转换为numpy数组
        user_ratings_list = np.array([ratings.get(item, 0) for item in target_user_ratings])

        # 计算余弦相似度
        similarity_score = cosine_similarity([user_ratings_list], [target_user_ratings_list])[0][0]
        user_similarity_scores[user] = similarity_score

    # 对用户相似度得分进行降序排列
    sorted_similar_users = sorted(user_similarity_scores.items(), key=lambda x: x[1], reverse=True)

    # 选择Top N个相似用户喜欢的地点作为推荐结果
    recommended_items = set()
    for similar_user, _ in sorted_similar_users[:top_n]:
        recommended_items.update(user_ratings[similar_user].keys())

    # 过滤掉目标用户已经评分过的地点
    recommended_items = [item for item in recommended_items if item not in target_user_ratings]

    return recommended_items

# 示例调用
user_id = "User1"  # 假设目标用户ID为"User1"
recommended_items = user_based_collaborative_filtering(user_id, user_ratings)
print("为用户推荐的旅游地点：", recommended_items)